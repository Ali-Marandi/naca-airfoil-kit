"""Restricted HTTP worker for isolated XFOIL polar calculations.

The worker accepts only a validated coordinate contour and an allowlisted polar
specification. It is intended for an internal, TLS-terminating ingress and does
not expose arbitrary commands, persistent run files, or interactive API docs.
"""

from __future__ import annotations

import asyncio
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from hashlib import sha256
import hmac
import os
from pathlib import Path
import time
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

from xfoil_adapter import XFoilAdapter, XFoilRunSpec, XFoilValidationError


class PolarRequest(BaseModel):
    """Strictly allowlisted request body for one XFOIL alpha-sweep run."""

    model_config = ConfigDict(extra="forbid")

    airfoil_name: str = Field(min_length=1, max_length=80)
    coordinates: list[tuple[float, float]] = Field(min_length=8, max_length=601)
    reynolds: float = Field(ge=1.0e4, le=5.0e7)
    alpha_start: float = Field(ge=-30.0, le=30.0)
    alpha_end: float = Field(ge=-30.0, le=30.0)
    alpha_step: float = Field(ge=0.05, le=5.0)
    mach: float = Field(default=0.0, ge=0.0, le=0.75)
    ncrit: float = Field(default=9.0, ge=0.1, le=20.0)
    xtr_top: float = Field(default=1.0, ge=0.0, le=1.0)
    xtr_bottom: float = Field(default=1.0, ge=0.0, le=1.0)
    iteration_limit: int = Field(default=100, ge=10, le=500)
    timeout_seconds: float = Field(default=30.0, ge=1.0, le=120.0)
    viscous: bool = True

    @field_validator("coordinates")
    @classmethod
    def coordinate_values_must_be_finite(cls, coordinates):
        for x_value, y_value in coordinates:
            if not (-2.0 <= x_value <= 3.0 and -2.0 <= y_value <= 2.0):
                raise ValueError("Coordinate values must lie within the worker safety envelope.")
        return coordinates

    @field_validator("alpha_end")
    @classmethod
    def alpha_range_must_increase(cls, alpha_end, info):
        alpha_start = info.data.get("alpha_start")
        if alpha_start is not None and alpha_end <= alpha_start:
            raise ValueError("alpha_end must be greater than alpha_start.")
        return alpha_end

    def to_run_spec(self) -> XFoilRunSpec:
        return XFoilRunSpec(
            airfoil_name=self.airfoil_name,
            coordinates=self.coordinates,
            reynolds=self.reynolds,
            alpha_start=self.alpha_start,
            alpha_end=self.alpha_end,
            alpha_step=self.alpha_step,
            mach=self.mach,
            ncrit=self.ncrit,
            xtr_top=self.xtr_top,
            xtr_bottom=self.xtr_bottom,
            iteration_limit=self.iteration_limit,
            timeout_seconds=self.timeout_seconds,
            viscous=self.viscous,
        )


class WorkerSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    api_key: str = ""
    allow_insecure_no_auth: bool = False
    xfoil_executable: str = "/usr/bin/xfoil"
    max_concurrency: int = Field(default=1, ge=1, le=4)
    request_body_limit_bytes: int = Field(default=262_144, ge=1_024, le=1_048_576)
    requests_per_minute: int = Field(default=30, ge=1, le=600)
    temp_root: Path = Path("/tmp/xfoil-runs")


def _read_secret_from_env() -> str:
    """Prefer a mounted secret file and fall back to environment for local development."""
    secret_path = os.getenv("XFOIL_WORKER_API_KEY_FILE", "").strip()
    if secret_path:
        try:
            return Path(secret_path).read_text(encoding="utf-8").strip()
        except OSError:
            return ""
    return os.getenv("XFOIL_WORKER_API_KEY", "").strip()


def read_settings() -> WorkerSettings:
    return WorkerSettings(
        api_key=_read_secret_from_env(),
        allow_insecure_no_auth=os.getenv("XFOIL_ALLOW_INSECURE_NO_AUTH", "false").lower() == "true",
        xfoil_executable=os.getenv("XFOIL_EXECUTABLE", "/usr/bin/xfoil"),
        max_concurrency=int(os.getenv("XFOIL_MAX_CONCURRENCY", "1")),
        request_body_limit_bytes=int(os.getenv("XFOIL_REQUEST_BODY_LIMIT_BYTES", "262144")),
        requests_per_minute=int(os.getenv("XFOIL_REQUESTS_PER_MINUTE", "30")),
        temp_root=Path(os.getenv("XFOIL_TEMP_ROOT", "/tmp/xfoil-runs")),
    )


def create_app(settings: WorkerSettings | None = None) -> FastAPI:
    settings = settings or read_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        settings.temp_root.mkdir(parents=True, exist_ok=True)
        app.state.settings = settings
        app.state.semaphore = asyncio.Semaphore(settings.max_concurrency)
        app.state.request_times = defaultdict(deque)
        yield

    app = FastAPI(
        title="NACA Airfoil Kit XFOIL Worker",
        version="0.2.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=lifespan,
    )

    @app.middleware("http")
    async def set_security_headers_and_check_body_size(request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and content_length.isdigit() and int(content_length) > request.app.state.settings.request_body_limit_bytes:
            return JSONResponse(status_code=413, content={"detail": "Request body exceeds worker limit."})
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    async def require_api_key(
        request: Request,
        x_api_key: Annotated[str | None, Header()] = None,
    ) -> None:
        active_settings: WorkerSettings = request.app.state.settings
        expected = active_settings.api_key
        if not expected and not active_settings.allow_insecure_no_auth:
            raise HTTPException(status_code=503, detail="Worker authentication is not configured.")
        if expected and (x_api_key is None or not hmac.compare_digest(x_api_key, expected)):
            raise HTTPException(status_code=401, detail="Invalid worker API key.")

        # Per-credential, in-memory quota. The deployment ingress must also
        # enforce rate/connection limits because this bucket is process-local.
        identity = sha256((x_api_key or "insecure-development").encode("utf-8")).hexdigest()
        now = time.monotonic()
        timestamps = request.app.state.request_times[identity]
        while timestamps and now - timestamps[0] >= 60.0:
            timestamps.popleft()
        if len(timestamps) >= active_settings.requests_per_minute:
            raise HTTPException(status_code=429, detail="Worker request rate limit exceeded.")
        timestamps.append(now)

    @app.get("/healthz")
    async def healthz(request: Request):
        active_settings: WorkerSettings = request.app.state.settings
        if not active_settings.api_key and not active_settings.allow_insecure_no_auth:
            status = "misconfigured"
        elif not Path(active_settings.xfoil_executable).is_file():
            status = "degraded"
        else:
            status = "ok"
        return {"status": status, "service": "naca-airfoil-kit-xfoil-worker"}

    @app.post("/v1/polar", dependencies=[Depends(require_api_key)])
    async def compute_polar(request: Request, body: PolarRequest):
        try:
            run_spec = body.to_run_spec()
            run_spec.validate()
        except XFoilValidationError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        active_settings: WorkerSettings = request.app.state.settings
        adapter = XFoilAdapter(active_settings.xfoil_executable, active_settings.temp_root)
        async with request.app.state.semaphore:
            result = await asyncio.to_thread(adapter.run, run_spec)
        return {
            "status": result.status,
            "message": result.message,
            "rows": result.rows,
            "return_code": result.return_code,
            "duration_ms": result.duration_ms,
            "solver": "xfoil",
            "manifest": result.manifest,
        }

    return app


app = create_app()
