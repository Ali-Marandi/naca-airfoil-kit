"""Core geometry and aerodynamic screening tools for NACA Airfoil Kit Pro.

The solver is intended for preliminary design studies. It uses a lightweight
panel/empirical model, so results must be validated with experimental data or a
higher-fidelity viscous solver before safety-critical or certification decisions.
"""

from math import pi
from typing import Iterable

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
    def load_from_url(url: str):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            points = []
            for line in response.text.splitlines():
                fields = line.split()
                if len(fields) < 2:
                    continue
                try:
                    points.append((float(fields[0]), float(fields[1])))
                except ValueError:
                    continue
            coords = np.asarray(points, dtype=float)
            if coords.shape[0] < 8:
                return None
            leading_edge = int(np.argmin(coords[:, 0]))
            upper, lower = coords[: leading_edge + 1][::-1], coords[leading_edge:]
            return upper[:, 0], upper[:, 1], lower[:, 0], lower[:, 1]
        except (requests.RequestException, ValueError, IndexError):
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
