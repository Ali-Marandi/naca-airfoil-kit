"""Safe, testable XFOIL batch adapter for preliminary viscous-polar studies.

The adapter exposes only an allowlisted analysis workflow. It never accepts a
free-form XFOIL command script from a UI user and executes the configured XFOIL
binary with ``shell=False`` in a newly-created temporary work directory.

XFOIL results are numerical predictions, not experimental measurements. Its
convergence and post-stall limitations must be surfaced by calling code.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import math
import os
import re
import shutil
import subprocess
import tempfile
import time
from typing import Iterable, Sequence


class XFoilValidationError(ValueError):
    """Raised when a solver request lies outside adapter guardrails."""


@dataclass(frozen=True)
class XFoilRunSpec:
    """Allowlisted numerical inputs for one XFOIL alpha-sweep run."""

    airfoil_name: str
    coordinates: Sequence[tuple[float, float]]
    reynolds: float
    alpha_start: float
    alpha_end: float
    alpha_step: float
    mach: float = 0.0
    ncrit: float = 9.0
    xtr_top: float = 1.0
    xtr_bottom: float = 1.0
    iteration_limit: int = 100
    timeout_seconds: float = 30.0
    viscous: bool = True

    MAX_ALPHA_POINTS = 241

    def validate(self) -> None:
        if not isinstance(self.airfoil_name, str) or not self.airfoil_name.strip():
            raise XFoilValidationError("An airfoil name is required.")
        coordinates = list(self.coordinates)
        if len(coordinates) < 8:
            raise XFoilValidationError("At least eight airfoil contour points are required.")
        for pair in coordinates:
            if not isinstance(pair, (tuple, list)) or len(pair) != 2:
                raise XFoilValidationError("Each coordinate must be an (x, y) pair.")
            if not all(math.isfinite(float(value)) for value in pair):
                raise XFoilValidationError("Coordinates must be finite numeric values.")
        if not 1.0e4 <= float(self.reynolds) <= 5.0e7:
            raise XFoilValidationError("Reynolds number must lie between 1e4 and 5e7.")
        if not 0.0 <= float(self.mach) <= 0.75:
            raise XFoilValidationError("Mach must lie between 0.0 and 0.75 for this adapter.")
        if not 0.1 <= float(self.ncrit) <= 20.0:
            raise XFoilValidationError("Ncrit must lie between 0.1 and 20.0.")
        if not 0.0 <= float(self.xtr_top) <= 1.0 or not 0.0 <= float(self.xtr_bottom) <= 1.0:
            raise XFoilValidationError("Forced transition locations must lie in [0, 1].")
        if not -30.0 <= float(self.alpha_start) < float(self.alpha_end) <= 30.0:
            raise XFoilValidationError("Alpha range must lie within [-30, 30] degrees and have positive span.")
        if not 0.05 <= float(self.alpha_step) <= 5.0:
            raise XFoilValidationError("Alpha increment must lie between 0.05 and 5.0 degrees.")
        number_of_points = int(round((self.alpha_end - self.alpha_start) / self.alpha_step)) + 1
        if number_of_points > self.MAX_ALPHA_POINTS:
            raise XFoilValidationError(f"Alpha sweep exceeds {self.MAX_ALPHA_POINTS} points.")
        if not 10 <= int(self.iteration_limit) <= 500:
            raise XFoilValidationError("Iteration limit must lie between 10 and 500.")
        if not 1.0 <= float(self.timeout_seconds) <= 300.0:
            raise XFoilValidationError("Timeout must lie between 1 and 300 seconds.")

    @classmethod
    def from_surfaces(
        cls,
        airfoil_name: str,
        xu: Iterable[float],
        yu: Iterable[float],
        xl: Iterable[float],
        yl: Iterable[float],
        **kwargs,
    ) -> "XFoilRunSpec":
        """Convert project upper/lower surface arrays to TE→LE→TE contour order."""
        upper = list(zip(xu, yu))
        lower = list(zip(xl, yl))
        if not upper or not lower:
            raise XFoilValidationError("Both upper and lower surface arrays are required.")
        contour = list(reversed(upper)) + lower[1:]
        return cls(airfoil_name=airfoil_name, coordinates=contour, **kwargs)


@dataclass
class XFoilRunResult:
    """Structured numerical result; raw logs remain bounded for safe UI display."""

    status: str
    message: str
    rows: list[dict[str, float | bool]] = field(default_factory=list)
    return_code: int | None = None
    duration_ms: float | None = None
    solver_version: str | None = None
    stdout_tail: str = ""
    stderr_tail: str = ""
    manifest: dict = field(default_factory=dict)

    @property
    def completed(self) -> bool:
        return self.status == "completed"


class XFoilAdapter:
    """Run a fixed XFOIL viscous/inviscid polar workflow in an isolated tempdir."""

    _POLAR_FILENAME = "polar.txt"
    _COORDINATE_FILENAME = "airfoil.dat"
    _SCRIPT_FILENAME = "xfoil.in"
    _MAX_LOG_CHARS = 4000

    def __init__(self, executable: str | Path = "xfoil", temp_root: str | Path | None = None):
        self.executable = str(executable)
        self.temp_root = Path(temp_root).resolve() if temp_root is not None else None

    @staticmethod
    def _safe_label(label: str) -> str:
        return re.sub(r"[^A-Za-z0-9_.-]+", "_", label.strip())[:80] or "airfoil"

    @staticmethod
    def _bounded_tail(text: str | None) -> str:
        return (text or "")[-XFoilAdapter._MAX_LOG_CHARS :]

    def _resolve_executable(self) -> str | None:
        candidate = Path(self.executable)
        if candidate.is_absolute() or candidate.parent != Path("."):
            return str(candidate) if candidate.is_file() else None
        return shutil.which(self.executable)

    @staticmethod
    def _write_coordinates(path: Path, spec: XFoilRunSpec) -> None:
        label = XFoilAdapter._safe_label(spec.airfoil_name)
        lines = [label]
        lines.extend(f"{float(x):.10f} {float(y):.10f}" for x, y in spec.coordinates)
        path.write_text("\n".join(lines) + "\n", encoding="ascii")

    @staticmethod
    def build_batch_commands(spec: XFoilRunSpec) -> str:
        """Build a static allowlisted batch script; user text never becomes a command."""
        spec.validate()
        viscous_setup = (
            f"VISC {float(spec.reynolds):.8g}\n"
            f"MACH {float(spec.mach):.6g}\n"
            "VPAR\n"
            f"N {float(spec.ncrit):.6g}\n"
            f"XTR {float(spec.xtr_top):.6g} {float(spec.xtr_bottom):.6g}\n"
            "\n"
            if spec.viscous
            else f"MACH {float(spec.mach):.6g}\n"
        )
        return (
            f"LOAD {XFoilAdapter._COORDINATE_FILENAME}\n"
            "PANE\n"
            "OPER\n"
            f"{viscous_setup}"
            f"ITER {int(spec.iteration_limit)}\n"
            "PACC\n"
            f"{XFoilAdapter._POLAR_FILENAME}\n"
            "\n"
            f"ASEQ {float(spec.alpha_start):.6g} {float(spec.alpha_end):.6g} {float(spec.alpha_step):.6g}\n"
            "PACC\n"
            "QUIT\n"
        )

    @staticmethod
    def parse_polar_text(polar_text: str) -> list[dict[str, float | bool]]:
        """Parse a standard XFOIL polar while preserving only numeric operating points."""
        rows: list[dict[str, float | bool]] = []
        data_started = False
        for raw_line in polar_text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if set(line) <= {"-", " ", "\t"} and "-" in line:
                data_started = True
                continue
            if not data_started:
                continue
            fields = line.split()
            if len(fields) < 3:
                continue
            try:
                values = [float(value.replace("D", "E")) for value in fields]
            except ValueError:
                continue
            row: dict[str, float | bool] = {
                "alpha_deg": values[0],
                "cl": values[1],
                "cd": values[2],
                "converged": True,
            }
            if len(values) > 3:
                row["cdp"] = values[3]
            if len(values) > 4:
                row["cm"] = values[4]
            if len(values) > 5:
                row["top_xtr"] = values[5]
            if len(values) > 6:
                row["bottom_xtr"] = values[6]
            rows.append(row)
        return rows

    def run(self, spec: XFoilRunSpec) -> XFoilRunResult:
        """Run the configured executable in a disposable directory and parse its polar."""
        spec.validate()
        executable = self._resolve_executable()
        manifest = {
            "solver": "xfoil",
            "spec": asdict(spec),
            "command_policy": "allowlisted-batch-only",
            "temporary_directory_isolation": True,
        }
        if executable is None:
            return XFoilRunResult(
                status="executable_not_found",
                message="Configured XFOIL executable is not available on this host.",
                manifest=manifest,
            )

        if self.temp_root is not None:
            self.temp_root.mkdir(parents=True, exist_ok=True)
        started = time.monotonic()
        try:
            with tempfile.TemporaryDirectory(prefix="naca_xfoil_", dir=str(self.temp_root) if self.temp_root else None) as temporary_dir:
                work_dir = Path(temporary_dir)
                self._write_coordinates(work_dir / self._COORDINATE_FILENAME, spec)
                commands = self.build_batch_commands(spec)
                (work_dir / self._SCRIPT_FILENAME).write_text(commands, encoding="ascii")
                manifest["work_dir_policy"] = "ephemeral"
                manifest["input_files"] = [self._COORDINATE_FILENAME, self._SCRIPT_FILENAME]
                completed = subprocess.run(
                    [executable],
                    input=commands,
                    text=True,
                    capture_output=True,
                    cwd=work_dir,
                    timeout=float(spec.timeout_seconds),
                    shell=False,
                    check=False,
                    env={**os.environ, "LC_ALL": "C", "LANG": "C"},
                )
                polar_path = work_dir / self._POLAR_FILENAME
                polar_text = polar_path.read_text(encoding="utf-8", errors="replace") if polar_path.exists() else ""
                rows = self.parse_polar_text(polar_text)
                duration_ms = (time.monotonic() - started) * 1000.0
                message = "Completed." if completed.returncode == 0 and rows else "XFOIL returned no parseable polar rows."
                status = "completed" if completed.returncode == 0 and rows else "process_error"
                return XFoilRunResult(
                    status=status,
                    message=message,
                    rows=rows,
                    return_code=completed.returncode,
                    duration_ms=duration_ms,
                    stdout_tail=self._bounded_tail(completed.stdout),
                    stderr_tail=self._bounded_tail(completed.stderr),
                    manifest=manifest,
                )
        except subprocess.TimeoutExpired as error:
            return XFoilRunResult(
                status="timed_out",
                message=f"XFOIL exceeded the {spec.timeout_seconds:g}-second execution limit.",
                duration_ms=(time.monotonic() - started) * 1000.0,
                stdout_tail=self._bounded_tail(error.stdout if isinstance(error.stdout, str) else ""),
                stderr_tail=self._bounded_tail(error.stderr if isinstance(error.stderr, str) else ""),
                manifest=manifest,
            )
        except OSError as error:
            return XFoilRunResult(
                status="process_error",
                message=f"XFOIL process could not be started: {error}",
                duration_ms=(time.monotonic() - started) * 1000.0,
                manifest=manifest,
            )
