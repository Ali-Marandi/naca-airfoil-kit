"""HTTP worker for isolated XFOIL polar calculations.

This service is deliberately narrow: it accepts a validated coordinate contour
and an allowlisted polar specification, delegates to ``XFoilAdapter``, and
returns structured numerical results. It is designed to run behind a TLS
terminating ingress; it does not expose arbitrary commands or persistent files.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
import os
from pathlib import Path
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, Header, HTTPException, Request
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
    xfoil_executable: str = "/usr/bin/xfoil"
    max_concurrency: int = Field(default=1, ge=1, le=4)
    temp_root: Path = Path("/tmp/xfoil-runs")


def read_settings() -> WorkerSettings:
    return WorkerSettings(
        api_key=os.getenv("XFOIL_WORKER_API_KEY", ""),
        xfoil_executable=os.getenv("XFOIL_EXECUTABLE", "/usr/bin/xfoil"),
        max_concurrency=int(os.getenv("XFOIL_MAX_CONCURRENCY", "1")),
        temp_root=Path(os.getenv("XFOIL_TEMP_ROOT", "/tmp/xfoil-runs")),
    )


def create_app(settings: WorkerSettings | None = None) -> FastAPI:
    settings = settings or read_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        settings.temp_root.mkdir(parents=True, exist_ok=True)
        app.state.settings = settings
        app.state.semaphore = asyncio.Semaphore(settings.max_concurrency)
        yield

    app = FastAPI(
        title="NACA Airfoil Kit XFOIL Worker",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )

    async def require_api_key(
        request: Request,
        x_api_key: Annotated[str | None, Header()] = None,
    ) -> None:
        expected = request.app.state.settings.api_key
        if expected and x_api_key != expected:
            raise HTTPException(status_code=401, detail="Invalid worker API key.")

    @app.get("/healthz")
    async def healthz(request: Request):
        active_settings: WorkerSettings = request.app.state.settings
        executable_available = Path(active_settings.xfoil_executable).is_file()
        return {
            "status": "ok" if executable_available else "degraded",
            "service": "naca-airfoil-kit-xfoil-worker",
            "xfoil_executable_available": executable_available,
            "max_concurrency": active_settings.max_concurrency,
        }

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
