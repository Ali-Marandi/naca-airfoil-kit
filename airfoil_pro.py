"""Core geometry and aerodynamic screening tools for NACA Airfoil Kit Pro.

The solver is intended for preliminary design studies. It uses a lightweight
panel/empirical model, so results must be validated with experimental data or a
higher-fidelity viscous solver before safety-critical or certification decisions.
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
from math import pi
from typing import Iterable, Mapping
from uuid import uuid4

import numpy as np
import requests


class NACAGeneratorPro:
    """Generate normalized NACA four- and five-digit airfoil coordinates."""

    @staticmethod
    def get_spacing(n_points: int, spacing_type: str = "cosine") -> np.ndarray:
        if n_points < 4:
            raise ValueError("At least four points are required per surface.")
        if spacing_type == "linear":
            return np.linspace(0.0, 1.0, n_points)
        if spacing_type == "cosine":
            return 0.5 * (1.0 - np.cos(np.linspace(0.0, pi, n_points)))
        if spacing_type == "half-cosine":
            return 1.0 - np.cos(np.linspace(0.0, pi / 2.0, n_points))
        raise ValueError("Spacing must be 'linear', 'cosine', or 'half-cosine'.")

    @staticmethod
    def naca4(code: str, n_points: int = 100, spacing: str = "cosine", closed_te: bool = False):
        code = str(code).strip()
        if len(code) != 4 or not code.isdigit():
            return None
        m, p, t = int(code[0]) / 100.0, int(code[1]) / 10.0, int(code[2:]) / 100.0
        x = NACAGeneratorPro.get_spacing(n_points, spacing)
        coefficients = [0.2969, -0.1260, -0.3516, 0.2843, -0.1036 if closed_te else -0.1015]
        yt = 5.0 * t * sum(c * x**i for i, c in enumerate(coefficients[1:], start=1))
        yt += 5.0 * t * coefficients[0] * np.sqrt(x)

        yc, dyc_dx = np.zeros_like(x), np.zeros_like(x)
        if p > 0.0:
            front = x <= p
            rear = ~front
            yc[front] = (m / p**2) * (2.0 * p * x[front] - x[front] ** 2)
            dyc_dx[front] = (2.0 * m / p**2) * (p - x[front])
            yc[rear] = (m / (1.0 - p) ** 2) * ((1.0 - 2.0 * p) + 2.0 * p * x[rear] - x[rear] ** 2)
            dyc_dx[rear] = (2.0 * m / (1.0 - p) ** 2) * (p - x[rear])

        theta = np.arctan(dyc_dx)
        return x - yt * np.sin(theta), yc + yt * np.cos(theta), x + yt * np.sin(theta), yc - yt * np.cos(theta)

    @staticmethod
    def naca5(code: str, n_points: int = 100, spacing: str = "cosine", closed_te: bool = False):
        code = str(code).strip()
        if len(code) != 5 or not code.isdigit():
            return None
        p_design, thickness = int(code[1]) * 0.05, int(code[2:]) / 100.0
        design_table = {
            0.05: (0.0580, 361.4),
            0.10: (0.1260, 51.64),
            0.15: (0.2025, 15.957),
            0.20: (0.2900, 6.643),
            0.25: (0.3910, 3.230),
        }
        p_values = np.array(sorted(design_table))
        r = np.interp(p_design, p_values, [design_table[p][0] for p in p_values])
        k1 = np.interp(p_design, p_values, [design_table[p][1] for p in p_values])

        x = NACAGeneratorPro.get_spacing(n_points, spacing)
        coefficients = [0.2969, -0.1260, -0.3516, 0.2843, -0.1036 if closed_te else -0.1015]
        yt = 5.0 * thickness * sum(c * x**i for i, c in enumerate(coefficients[1:], start=1))
        yt += 5.0 * thickness * coefficients[0] * np.sqrt(x)

        yc, dyc_dx = np.zeros_like(x), np.zeros_like(x)
        front = x <= r
        rear = ~front
        yc[front] = (k1 / 6.0) * (x[front] ** 3 - 3.0 * r * x[front] ** 2 + r**2 * (3.0 - r) * x[front])
        dyc_dx[front] = (k1 / 6.0) * (3.0 * x[front] ** 2 - 6.0 * r * x[front] + r**2 * (3.0 - r))
        yc[rear] = (k1 * r**3 / 6.0) * (1.0 - x[rear])
        dyc_dx[rear] = -k1 * r**3 / 6.0

        theta = np.arctan(dyc_dx)
        return x - yt * np.sin(theta), yc + yt * np.cos(theta), x + yt * np.sin(theta), yc - yt * np.cos(theta)


class UIUCLoader:
    """Load UIUC-format coordinate files while tolerating headers and comments."""

    @staticmethod
    def parse_coordinate_text(text: str):
        """Parse common UIUC coordinate orientations into ascending x surfaces.

        Most UIUC files begin at the trailing edge, follow the upper surface to
        the leading edge and return over the lower surface. Some legacy files
        begin at the leading edge, traverse the upper surface to the trailing
        edge, then return over the lower surface. Both conventions are accepted.
        """
        points = []
        for line in text.splitlines():
            fields = line.split()
            if len(fields) < 2:
                continue
            try:
                x_value, y_value = float(fields[0]), float(fields[1])
            except ValueError:
                continue
            # UIUC legacy files may include a numeric point-count line (for
            # example ``66. 66.``). Airfoil coordinates are normalized and the
            # broad envelope avoids mistaking those counts for geometry.
            if -5.0 <= x_value <= 5.0 and -5.0 <= y_value <= 5.0:
                points.append((x_value, y_value))
        coords = np.asarray(points, dtype=float)
        if coords.shape[0] < 8 or not np.all(np.isfinite(coords)):
            return None
        leading_edge = int(np.argmin(coords[:, 0]))
        if leading_edge == 0:
            trailing_edge = int(np.argmax(coords[:, 0]))
            if trailing_edge <= 1 or trailing_edge >= coords.shape[0] - 1:
                return None
            upper = coords[: trailing_edge + 1]
            lower = coords[trailing_edge:][::-1]
        elif leading_edge == coords.shape[0] - 1:
            trailing_edge = int(np.argmax(coords[:, 0]))
            if trailing_edge <= 0 or trailing_edge >= coords.shape[0] - 2:
                return None
            lower = coords[: trailing_edge + 1]
            upper = coords[trailing_edge:][::-1]
        else:
            upper, lower = coords[: leading_edge + 1][::-1], coords[leading_edge:]
        upper = upper[np.argsort(upper[:, 0])]
        lower = lower[np.argsort(lower[:, 0])]
        if upper.shape[0] < 4 or lower.shape[0] < 4:
            return None
        return upper[:, 0], upper[:, 1], lower[:, 0], lower[:, 1]

    @staticmethod
    def load_from_url(url: str):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return UIUCLoader.parse_coordinate_text(response.text)
        except requests.RequestException:
            return None


class AirfoilAnalysis:
    """Lightweight panel/empirical analysis and engineering-study helpers."""

    @staticmethod
    def _prepare_panel_system(xu, yu, xl, yl):
        xu, yu, xl, yl = (np.asarray(v, dtype=float) for v in (xu, yu, xl, yl))
        x = np.concatenate([xu[::-1], xl[1:]])
        y = np.concatenate([yu[::-1], yl[1:]])
        if len(x) < 8:
            raise ValueError("At least eight contour points are required.")

        xc, yc = 0.5 * (x[:-1] + x[1:]), 0.5 * (y[:-1] + y[1:])
        dx, dy = np.diff(x), np.diff(y)
        lengths = np.hypot(dx, dy)
        if np.any(lengths < 1e-12):
            raise ValueError("Duplicate contour points create zero-length panels.")
        beta = np.arctan2(dy, dx) + 0.5 * pi
        n = len(lengths)

        dx_ij = xc[:, None] - xc[None, :]
        dy_ij = yc[:, None] - yc[None, :]
        radius_sq = dx_ij**2 + dy_ij**2 + 1e-9
        theta_ij = np.arctan2(dy_ij, dx_ij)
        influence = (lengths[None, :] / (2.0 * pi * np.sqrt(radius_sq))) * np.sin(beta[:, None] - theta_ij)
        np.fill_diagonal(influence, 0.5)

        matrix = np.zeros((n + 1, n + 1), dtype=float)
        matrix[:n, :n] = influence
        matrix[n, 0] = 1.0
        matrix[n, n - 1] = 1.0
        return {"xu": xu, "yu": yu, "xl": xl, "yl": yl, "xc": xc, "yc": yc, "lengths": lengths, "beta": beta, "matrix": matrix}

    @staticmethod
    def _solve_polar(prepared, alpha_values: Iterable[float], re: float, rough: float):
        alphas = np.atleast_1d(np.asarray(alpha_values, dtype=float))
        if alphas.size == 0:
            raise ValueError("At least one angle of attack is required.")
        reynolds = max(float(re), 1e4)
        roughness = max(float(rough), 0.0)
        beta = prepared["beta"]
        rhs = np.vstack([np.cos(beta[:, None] - np.radians(alphas)[None, :]), np.zeros((1, alphas.size))])
        gamma = np.linalg.lstsq(prepared["matrix"], rhs, rcond=None)[0][:-1, :]
        cl = 2.0 * np.sum(gamma * prepared["lengths"][:, None], axis=0)
        cp = 1.0 - gamma**2

        xu, yu, xl, yl = prepared["xu"], prepared["yu"], prepared["xl"], prepared["yl"]
        x_grid = np.linspace(0.0, 1.0, 401)
        thickness = np.interp(x_grid, xu, yu) - np.interp(x_grid, xl, yl)
        thickness_ratio = max(float(np.max(thickness)), 1e-4)
        smooth_cf = 0.455 / (np.log10(reynolds) ** 2.58)
        rough_cf = (1.89 + 1.62 * np.log10(1.0 / max(roughness, 1e-9))) ** -2.5 if roughness > 1e-7 else 0.0
        skin_friction = max(smooth_cf, rough_cf)
        cd = np.full_like(cl, skin_friction * 2.0 * (1.0 + 2.0 * thickness_ratio + 60.0 * thickness_ratio**4))

        cl_limit = max(0.15, (1.5 + (thickness_ratio - 0.12) * 2.0) * (1.0 - 50.0 * roughness))
        stalled = np.abs(cl) > cl_limit
        if np.any(stalled):
            exceedance = np.abs(cl[stalled]) - cl_limit
            cl[stalled] = cl_limit * np.sign(cl[stalled]) * np.exp(-0.2 * exceedance)
            cd[stalled] += 0.1 * exceedance**2
        ld = np.divide(cl, cd, out=np.full_like(cl, np.nan), where=cd > 1e-12)
        return {"alpha": alphas, "cl": cl, "cd": cd, "ld": ld, "cp": cp, "gamma": gamma, "stalled": stalled}

    @staticmethod
    def compute_aerodynamics(xu, yu, xl, yl, alpha_deg, re: float = 1e6, rough: float = 0.0):
        """Return legacy single-point result tuple for UI compatibility."""
        try:
            prepared = AirfoilAnalysis._prepare_panel_system(xu, yu, xl, yl)
            solved = AirfoilAnalysis._solve_polar(prepared, [alpha_deg], re, rough)
            return (
                float(solved["cl"][0]),
                float(solved["cd"][0]),
                solved["cp"][:, 0],
                prepared["xc"],
                solved["gamma"][:, 0],
                prepared["xc"],
                prepared["yc"],
                prepared["lengths"],
            )
        except (ValueError, np.linalg.LinAlgError):
            zeros = np.zeros(max(1, len(xu) + len(xl) - 2))
            return 0.0, 0.0, zeros, zeros, zeros, zeros, zeros, zeros

    @staticmethod
    def compute_polar(xu, yu, xl, yl, alpha_values: Iterable[float], re: float = 1e6, rough: float = 0.0):
        """Compute a reusable alpha sweep with a single prepared panel system."""
        prepared = AirfoilAnalysis._prepare_panel_system(xu, yu, xl, yl)
        solved = AirfoilAnalysis._solve_polar(prepared, alpha_values, re, rough)
        rows = []
        for index, alpha in enumerate(solved["alpha"]):
            rows.append(
                {
                    "alpha_deg": float(alpha),
                    "cl": float(solved["cl"][index]),
                    "cd": float(solved["cd"][index]),
                    "ld": float(solved["ld"][index]),
                    "stalled_estimate": bool(solved["stalled"][index]),
                }
            )
        return {"rows": rows, "prepared": prepared, "raw": solved}

    @staticmethod
    def geometry_metrics(xu, yu, xl, yl):
        """Return normalized geometry QA metrics for preliminary manufacturing checks."""
        xu, yu, xl, yl = (np.asarray(v, dtype=float) for v in (xu, yu, xl, yl))
        grid = np.linspace(0.0, 1.0, 501)
        upper = np.interp(grid, xu, yu)
        lower = np.interp(grid, xl, yl)
        thickness = upper - lower
        camber = 0.5 * (upper + lower)
        thickness_index = int(np.argmax(thickness))
        camber_index = int(np.argmax(np.abs(camber)))
        return {
            "max_thickness_pct": float(thickness[thickness_index] * 100.0),
            "max_thickness_xc": float(grid[thickness_index]),
            "max_camber_pct": float(camber[camber_index] * 100.0),
            "max_camber_xc": float(grid[camber_index]),
            "trailing_edge_gap_pct": float(abs(upper[-1] - lower[-1]) * 100.0),
            "section_area_ratio": float(np.trapezoid(thickness, grid)),
        }

    @staticmethod
    def summarize_polar(polar_rows):
        if not polar_rows:
            return {"best_ld": np.nan, "best_alpha_deg": np.nan, "cl_max": np.nan, "cd_min": np.nan}
        ld_values = np.asarray([row["ld"] for row in polar_rows], dtype=float)
        cl_values = np.asarray([row["cl"] for row in polar_rows], dtype=float)
        cd_values = np.asarray([row["cd"] for row in polar_rows], dtype=float)
        best_index = int(np.nanargmax(ld_values)) if np.any(np.isfinite(ld_values)) else 0
        return {
            "best_ld": float(ld_values[best_index]),
            "best_alpha_deg": float(polar_rows[best_index]["alpha_deg"]),
            "cl_max": float(np.nanmax(cl_values)),
            "cd_min": float(np.nanmin(cd_values)),
        }

    @staticmethod
    def get_streamlines(xu, yu, xl, yl, alpha_deg, gamma, xc, yc, lengths):
        alpha = np.radians(alpha_deg)
        x_mesh, y_mesh = np.meshgrid(np.linspace(-0.5, 1.5, 36), np.linspace(-0.5, 0.5, 28))
        u = np.cos(alpha) * np.ones_like(x_mesh)
        v = np.sin(alpha) * np.ones_like(x_mesh)
        for index in range(len(gamma)):
            radius_sq = (x_mesh - xc[index]) ** 2 + (y_mesh - yc[index]) ** 2 + 1e-6
            u += (gamma[index] * lengths[index] / (2.0 * pi * radius_sq)) * (y_mesh - yc[index])
            v -= (gamma[index] * lengths[index] / (2.0 * pi * radius_sq)) * (x_mesh - xc[index])
        return x_mesh, y_mesh, u, v


class EngineeringStudy:
    """Batch NACA screening and export-ready design-study helpers."""

    @staticmethod
    def parse_naca4_codes(text: str):
        values = [value.strip().replace("NACA", "").strip() for value in str(text).replace("\n", ",").split(",")]
        return [value for value in values if len(value) == 4 and value.isdigit()]

    @staticmethod
    def screen_naca4(codes: Iterable[str], alpha_values: Iterable[float], re: float, rough: float = 0.0, n_points: int = 100):
        rankings, polars = [], {}
        for code in codes:
            coords = NACAGeneratorPro.naca4(code, n_points)
            if coords is None:
                continue
            polar = AirfoilAnalysis.compute_polar(*coords, alpha_values, re=re, rough=rough)
            summary = AirfoilAnalysis.summarize_polar(polar["rows"])
            metrics = AirfoilAnalysis.geometry_metrics(*coords)
            rankings.append(
                {
                    "airfoil": f"NACA {code}",
                    "best_ld": summary["best_ld"],
                    "best_alpha_deg": summary["best_alpha_deg"],
                    "cl_max": summary["cl_max"],
                    "cd_min": summary["cd_min"],
                    "max_thickness_pct": metrics["max_thickness_pct"],
                    "max_camber_pct": metrics["max_camber_pct"],
                }
            )
            polars[f"NACA {code}"] = polar["rows"]
        rankings.sort(key=lambda row: row["best_ld"], reverse=True)
        return {"rankings": rankings, "polars": polars}


class ParetoExplorer:
    """Multi-objective preliminary screening based on L/D and lift objectives.

    A candidate dominates another candidate when it is at least as good in both
    objectives and strictly better in one. Results are model-screening outputs,
    not a substitute for viscous analysis or validated design margins.
    """

    @staticmethod
    def _is_dominated(candidate: dict, challenger: dict, ld_key: str, cl_key: str) -> bool:
        candidate_ld, candidate_cl = float(candidate[ld_key]), float(candidate[cl_key])
        challenger_ld, challenger_cl = float(challenger[ld_key]), float(challenger[cl_key])
        return (
            challenger_ld >= candidate_ld
            and challenger_cl >= candidate_cl
            and (challenger_ld > candidate_ld or challenger_cl > candidate_cl)
        )

    @staticmethod
    def non_dominated_sort(rows: Iterable[dict], ld_key: str = "best_ld", cl_key: str = "cl_objective"):
        """Assign one-based Pareto front ranks for two maximization objectives."""
        normalized_rows = [dict(row) for row in rows]
        remaining = set(range(len(normalized_rows)))
        rank = 1
        while remaining:
            front = [
                index
                for index in remaining
                if not any(
                    ParetoExplorer._is_dominated(normalized_rows[index], normalized_rows[other], ld_key, cl_key)
                    for other in remaining
                    if other != index
                )
            ]
            if not front:
                break
            for index in front:
                normalized_rows[index]["pareto_rank"] = rank
                normalized_rows[index]["pareto_front"] = rank == 1
            remaining.difference_update(front)
            rank += 1
        normalized_rows.sort(key=lambda row: (row.get("pareto_rank", 999), -float(row[ld_key]), -float(row[cl_key])))
        return normalized_rows

    @staticmethod
    def screen_geometries(
        geometries: Mapping[str, tuple],
        alpha_values: Iterable[float],
        re: float,
        rough: float = 0.0,
        cl_objective: str = "cl_max",
        design_alpha_deg: float | None = None,
    ):
        """Return a Pareto study for named, already-loaded airfoil geometries.

        The method deliberately accepts coordinate data rather than URLs. Callers
        are responsible for provenance and trusted acquisition; this preserves a
        deterministic analysis boundary and enables UIUC fixture integration tests.
        """
        if cl_objective not in {"cl_max", "cl_at_design_alpha"}:
            raise ValueError("cl_objective must be 'cl_max' or 'cl_at_design_alpha'.")
        alpha_array = np.asarray(list(alpha_values), dtype=float)
        if alpha_array.size < 2:
            raise ValueError("At least two alpha values are required for Pareto screening.")
        if cl_objective == "cl_at_design_alpha" and design_alpha_deg is None:
            raise ValueError("design_alpha_deg is required when using the design-alpha lift objective.")
        if design_alpha_deg is not None and not float(alpha_array.min()) <= float(design_alpha_deg) <= float(alpha_array.max()):
            raise ValueError("design_alpha_deg must lie within the supplied alpha envelope.")

        candidates, polars = [], {}
        for airfoil_name, coords in geometries.items():
            if not isinstance(airfoil_name, str) or not airfoil_name.strip():
                raise ValueError("Each geometry requires a non-empty airfoil name.")
            if len(coords) != 4:
                raise ValueError(f"{airfoil_name} must contain upper/lower x/y coordinate arrays.")
            xu, yu, xl, yl = coords
            polar = AirfoilAnalysis.compute_polar(xu, yu, xl, yl, alpha_array, re=float(re), rough=float(rough))
            summary = AirfoilAnalysis.summarize_polar(polar["rows"])
            metric = AirfoilAnalysis.geometry_metrics(xu, yu, xl, yl)
            if cl_objective == "cl_max":
                cl_value = float(summary["cl_max"])
                objective_label = "Maximum Cl over envelope"
            else:
                polar_alpha = np.asarray([row["alpha_deg"] for row in polar["rows"]], dtype=float)
                polar_cl = np.asarray([row["cl"] for row in polar["rows"]], dtype=float)
                cl_value = float(np.interp(float(design_alpha_deg), polar_alpha, polar_cl))
                objective_label = f"Cl at α = {float(design_alpha_deg):.2f}°"
            candidates.append(
                {
                    "airfoil": airfoil_name.strip(),
                    "best_ld": float(summary["best_ld"]),
                    "best_ld_alpha_deg": float(summary["best_alpha_deg"]),
                    "cl_objective": cl_value,
                    "cl_objective_name": objective_label,
                    "cl_max": float(summary["cl_max"]),
                    "cd_min": float(summary["cd_min"]),
                    "max_thickness_pct": float(metric["max_thickness_pct"]),
                    "max_camber_pct": float(metric["max_camber_pct"]),
                }
            )
            polars[airfoil_name.strip()] = polar["rows"]
        ranked = ParetoExplorer.non_dominated_sort(candidates)
        return {
            "rankings": ranked,
            "polars": polars,
            "objective": {
                "ld": "Maximum L/D over envelope",
                "cl": ranked[0]["cl_objective_name"] if ranked else "Cl objective",
                "reynolds": float(re),
                "roughness_k_over_c": float(rough),
                "alpha_values_deg": [float(value) for value in alpha_array],
                "design_alpha_deg": float(design_alpha_deg) if design_alpha_deg is not None else None,
            },
        }

    @staticmethod
    def screen_naca4(
        codes: Iterable[str],
        alpha_values: Iterable[float],
        re: float,
        rough: float = 0.0,
        cl_objective: str = "cl_max",
        design_alpha_deg: float | None = None,
        n_points: int = 100,
    ):
        """Generate valid NACA 4-digit geometries and call ``screen_geometries``."""
        code_values = EngineeringStudy.parse_naca4_codes(codes) if isinstance(codes, str) else EngineeringStudy.parse_naca4_codes(",".join(str(value) for value in codes))
        geometries = {}
        for code in code_values:
            coords = NACAGeneratorPro.naca4(code, n_points)
            if coords is not None:
                geometries[f"NACA {code}"] = coords
        return ParetoExplorer.screen_geometries(
            geometries,
            alpha_values,
            re=float(re),
            rough=float(rough),
            cl_objective=cl_objective,
            design_alpha_deg=design_alpha_deg,
        )


class GeometryOptimizer:
    @staticmethod
    def optimize_ld(code, alpha, re, series="4-digit"):
        best_ld, best_code = -np.inf, code
        for camber in range(10):
            for position in range(1, 10):
                candidate = f"{camber}{position}{str(code)[2:]}"
                coords = NACAGeneratorPro.naca4(candidate) if series == "4-digit" else NACAGeneratorPro.naca5(candidate)
                if coords is None:
                    continue
                cl, cd = AirfoilAnalysis.compute_aerodynamics(*coords, alpha, re)[:2]
                if cd > 0.0 and cl / cd > best_ld:
                    best_ld, best_code = cl / cd, candidate
        return best_code, float(best_ld)

    @staticmethod
    def match_cl(code, target, series="4-digit"):
        best_m, min_distance = 0, np.inf
        for camber in range(10):
            candidate = f"{camber}{str(code)[1:]}"
            coords = NACAGeneratorPro.naca4(candidate) if series == "4-digit" else NACAGeneratorPro.naca5(candidate)
            if coords is None:
                continue
            cl = AirfoilAnalysis.compute_aerodynamics(*coords, 0.0)[0]
            if abs(cl - target) < min_distance:
                min_distance, best_m = abs(cl - target), camber
        return f"{best_m}{str(code)[1:]}"


class GeometryTools:
    """Geometry transformations for preliminary design studies."""

    @staticmethod
    def apply_hinged_flap(xu, yu, xl, yl, hinge_x: float = 0.75, deflection_deg: float = 0.0):
        """Apply a rigid hinged trailing-edge flap.

        Positive deflection moves the trailing edge downward. The operation is a
        geometric convenience for preliminary studies and does not model hinge
        gaps, seals, deformation, or viscous flap aerodynamics.
        """
        xu, yu, xl, yl = (np.asarray(value, dtype=float).copy() for value in (xu, yu, xl, yl))
        if abs(float(deflection_deg)) < 1e-12:
            return xu, yu, xl, yl
        hinge_x = float(np.clip(hinge_x, 0.5, 0.95))
        hinge_y = 0.5 * (np.interp(hinge_x, xu, yu) + np.interp(hinge_x, xl, yl))
        theta = -np.radians(float(deflection_deg))
        cosine, sine = np.cos(theta), np.sin(theta)

        def rotate_branch(x_values, y_values):
            affected = x_values >= hinge_x
            dx = x_values[affected] - hinge_x
            dy = y_values[affected] - hinge_y
            x_values[affected] = hinge_x + cosine * dx - sine * dy
            y_values[affected] = hinge_y + sine * dx + cosine * dy
            order = np.argsort(x_values)
            return x_values[order], y_values[order]

        xu, yu = rotate_branch(xu, yu)
        xl, yl = rotate_branch(xl, yl)
        return xu, yu, xl, yl


class ExperimentalValidation:
    """Compare model polars to user-provided experimental measurements."""

    REQUIRED_ALPHA_FIELDS = ("alpha_deg", "alpha", "aoa", "angle_of_attack")
    CL_FIELDS = ("cl", "c_l", "lift_coefficient")
    CD_FIELDS = ("cd", "c_d", "drag_coefficient")

    @staticmethod
    def _find_field(fieldnames, accepted):
        lower_to_original = {str(name).strip().lower(): name for name in fieldnames}
        for candidate in accepted:
            if candidate in lower_to_original:
                return lower_to_original[candidate]
        return None

    @staticmethod
    def parse_csv_text(csv_text: str):
        """Parse a user CSV with alpha_deg/alpha and optional cl/cd columns."""
        import csv
        import io

        reader = csv.DictReader(io.StringIO(csv_text.lstrip("\ufeff")))
        if not reader.fieldnames:
            raise ValueError("The CSV must have a header row.")
        alpha_key = ExperimentalValidation._find_field(reader.fieldnames, ExperimentalValidation.REQUIRED_ALPHA_FIELDS)
        cl_key = ExperimentalValidation._find_field(reader.fieldnames, ExperimentalValidation.CL_FIELDS)
        cd_key = ExperimentalValidation._find_field(reader.fieldnames, ExperimentalValidation.CD_FIELDS)
        if alpha_key is None or (cl_key is None and cd_key is None):
            raise ValueError("CSV requires alpha_deg (or alpha) and at least one of cl or cd.")

        rows = []
        for source_row in reader:
            try:
                alpha = float(source_row[alpha_key])
            except (TypeError, ValueError):
                continue
            record = {"alpha_deg": alpha}
            for canonical, key in (("cl", cl_key), ("cd", cd_key)):
                if key is None or source_row.get(key, "") in (None, ""):
                    record[canonical] = np.nan
                    continue
                try:
                    record[canonical] = float(source_row[key])
                except (TypeError, ValueError):
                    record[canonical] = np.nan
            rows.append(record)
        if len(rows) < 2:
            raise ValueError("At least two numeric measurement rows are required.")
        return rows

    @staticmethod
    def _error_metrics(observed, predicted):
        observed, predicted = np.asarray(observed, dtype=float), np.asarray(predicted, dtype=float)
        valid = np.isfinite(observed) & np.isfinite(predicted)
        if not np.any(valid):
            return {"n": 0, "mae": np.nan, "rmse": np.nan, "bias": np.nan, "mape_pct": np.nan}
        residual = predicted[valid] - observed[valid]
        nonzero = np.abs(observed[valid]) > 1e-10
        mape = np.mean(np.abs(residual[nonzero] / observed[valid][nonzero])) * 100.0 if np.any(nonzero) else np.nan
        return {
            "n": int(valid.sum()),
            "mae": float(np.mean(np.abs(residual))),
            "rmse": float(np.sqrt(np.mean(residual**2))),
            "bias": float(np.mean(residual)),
            "mape_pct": float(mape),
        }

    @staticmethod
    def compare_polar(xu, yu, xl, yl, experimental_rows, re: float, rough: float = 0.0):
        """Evaluate model points at the experimental alpha values and calculate residuals."""
        if not experimental_rows:
            raise ValueError("Experimental rows are required for validation.")
        alpha_values = [float(row["alpha_deg"]) for row in experimental_rows]
        model_rows = AirfoilAnalysis.compute_polar(xu, yu, xl, yl, alpha_values, re, rough)["rows"]
        comparison = []
        for experimental, model in zip(experimental_rows, model_rows):
            experiment_cl = float(experimental.get("cl", np.nan))
            experiment_cd = float(experimental.get("cd", np.nan))
            comparison.append(
                {
                    "alpha_deg": float(experimental["alpha_deg"]),
                    "experimental_cl": experiment_cl,
                    "model_cl": float(model["cl"]),
                    "cl_error": float(model["cl"] - experiment_cl) if np.isfinite(experiment_cl) else np.nan,
                    "experimental_cd": experiment_cd,
                    "model_cd": float(model["cd"]),
                    "cd_error": float(model["cd"] - experiment_cd) if np.isfinite(experiment_cd) else np.nan,
                    "stalled_estimate": bool(model["stalled_estimate"]),
                }
            )
        return {
            "comparison": comparison,
            "cl_metrics": ExperimentalValidation._error_metrics(
                [row["experimental_cl"] for row in comparison], [row["model_cl"] for row in comparison]
            ),
            "cd_metrics": ExperimentalValidation._error_metrics(
                [row["experimental_cd"] for row in comparison], [row["model_cd"] for row in comparison]
            ),
        }


class RobustStudy:
    """Deterministic condition-sensitivity tools for preliminary design robustness."""

    @staticmethod
    def condition_envelope(xu, yu, xl, yl, alpha_values, reynolds_values, roughness_values):
        """Return min/mean/max model response over user-defined Re and roughness grids.

        This is a model sensitivity envelope, not a statistical uncertainty
        interval or a replacement for experimental measurement uncertainty.
        """
        alpha_values = np.asarray(alpha_values, dtype=float)
        reynolds_values = np.asarray(reynolds_values, dtype=float)
        roughness_values = np.asarray(roughness_values, dtype=float)
        if alpha_values.size == 0 or reynolds_values.size == 0 or roughness_values.size == 0:
            raise ValueError("Alpha, Reynolds, and roughness samples are required.")
        prepared = AirfoilAnalysis._prepare_panel_system(xu, yu, xl, yl)
        cl_samples, cd_samples, ld_samples = [], [], []
        for reynolds in reynolds_values:
            for roughness in roughness_values:
                result = AirfoilAnalysis._solve_polar(prepared, alpha_values, float(reynolds), float(roughness))
                cl_samples.append(result["cl"])
                cd_samples.append(result["cd"])
                ld_samples.append(result["ld"])
        cl_samples, cd_samples, ld_samples = np.asarray(cl_samples), np.asarray(cd_samples), np.asarray(ld_samples)
        rows = []
        for index, alpha in enumerate(alpha_values):
            rows.append(
                {
                    "alpha_deg": float(alpha),
                    "cl_min": float(np.nanmin(cl_samples[:, index])),
                    "cl_mean": float(np.nanmean(cl_samples[:, index])),
                    "cl_max": float(np.nanmax(cl_samples[:, index])),
                    "cd_min": float(np.nanmin(cd_samples[:, index])),
                    "cd_mean": float(np.nanmean(cd_samples[:, index])),
                    "cd_max": float(np.nanmax(cd_samples[:, index])),
                    "ld_min": float(np.nanmin(ld_samples[:, index])),
                    "ld_mean": float(np.nanmean(ld_samples[:, index])),
                    "ld_max": float(np.nanmax(ld_samples[:, index])),
                    "condition_samples": int(cl_samples.shape[0]),
                }
            )
        return rows


class StudyAudit:
    """Create versioned, exportable manifests for reproducible engineering studies."""

    SCHEMA_VERSION = "1.0"

    @staticmethod
    def _geometry_payload(xu, yu, xl, yl):
        surfaces = []
        for label, x_values, y_values in (("upper", xu, yu), ("lower", xl, yl)):
            x_values, y_values = np.asarray(x_values, dtype=float), np.asarray(y_values, dtype=float)
            if x_values.shape != y_values.shape or x_values.size < 4:
                raise ValueError(f"{label.title()} surface requires matching arrays with at least four points.")
            surfaces.append(
                {
                    "surface": label,
                    "points": [[round(float(x), 10), round(float(y), 10)] for x, y in zip(x_values, y_values)],
                }
            )
        return surfaces

    @staticmethod
    def geometry_sha256(xu, yu, xl, yl) -> str:
        """Return a stable geometry signature from normalized coordinate values."""
        payload = StudyAudit._geometry_payload(xu, yu, xl, yl)
        encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        return sha256(encoded).hexdigest()

    @staticmethod
    def build_manifest(
        airfoil_name: str,
        xu,
        yu,
        xl,
        yl,
        operating_conditions: dict,
        solver: dict | None = None,
        study_label: str | None = None,
        source_data: dict | None = None,
    ) -> dict:
        """Build a JSON-serializable record suitable for engineering handoff and review.

        The manifest is a provenance record, not a certification artifact. Callers
        should attach their raw polar, validation residual, and solver logs where
        an auditable study package is required.
        """
        if not isinstance(airfoil_name, str) or not airfoil_name.strip():
            raise ValueError("A non-empty airfoil name is required.")
        if not isinstance(operating_conditions, dict):
            raise ValueError("Operating conditions must be a dictionary.")
        geometry = StudyAudit._geometry_payload(xu, yu, xl, yl)
        geometry_hash = StudyAudit.geometry_sha256(xu, yu, xl, yl)
        normalized_solver = solver or {
            "name": "naca-airfoil-kit-preliminary-panel-empirical",
            "fidelity": "preliminary_screening",
        }
        manifest = {
            "schema_version": StudyAudit.SCHEMA_VERSION,
            "study_id": str(uuid4()),
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "study_label": study_label or airfoil_name.strip(),
            "airfoil": {
                "name": airfoil_name.strip(),
                "geometry_sha256": geometry_hash,
                "upper_point_count": len(geometry[0]["points"]),
                "lower_point_count": len(geometry[1]["points"]),
                "geometry_metrics": AirfoilAnalysis.geometry_metrics(xu, yu, xl, yl),
            },
            "operating_conditions": operating_conditions,
            "solver": normalized_solver,
            "source_data": source_data or {},
            "scope_notice": "Preliminary engineering screening; validate independently before safety-critical or production decisions.",
        }
        return manifest

    @staticmethod
    def to_json(manifest: dict) -> str:
        """Serialize a manifest with stable indentation for review and archiving."""
        return json.dumps(manifest, indent=2, sort_keys=True, default=str) + "\n"
