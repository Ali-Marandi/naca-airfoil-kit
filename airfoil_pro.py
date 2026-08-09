import numpy as np
import requests
from math import atan2, cos, sin, sqrt, pi

class NACAGeneratorPro:
    @staticmethod
    def get_spacing(n_points, spacing_type='cosine'):
        if spacing_type == 'linear':
            return np.linspace(0, 1, n_points)
        elif spacing_type == 'cosine':
            return 0.5 * (1 - np.cos(np.linspace(0, pi, n_points)))
        elif spacing_type == 'half-cosine':
            return 1 - np.cos(np.linspace(0, pi/2, n_points))
        else:
            raise ValueError("Spacing type must be 'linear', 'cosine', or 'half-cosine'")

    @staticmethod
    def naca4(code, n_points=100, spacing='cosine', closed_te=False):
        try:
            m = int(code[0]) / 100.0
            p = int(code[1]) / 10.0
            t = int(code[2:]) / 100.0
        except:
            return None
        x = NACAGeneratorPro.get_spacing(n_points, spacing)
        a0, a1, a2, a3 = 0.2969, -0.1260, -0.3516, 0.2843
        a4 = -0.1015 if not closed_te else -0.1036
        yt = 5 * t * (a0 * np.sqrt(x) + a1 * x + a2 * x**2 + a3 * x**3 + a4 * x**4)
        yc = np.zeros_like(x)
        dyc_dx = np.zeros_like(x)
        if p > 0:
            mask = x <= p
            yc[mask] = (m / p**2) * (2 * p * x[mask] - x[mask]**2)
            dyc_dx[mask] = (2 * m / p**2) * (p - x[mask])
            mask = x > p
            yc[mask] = (m / (1 - p)**2) * ((1 - 2 * p) + 2 * p * x[mask] - x[mask]**2)
            dyc_dx[mask] = (2 * m / (1 - p)**2) * (p - x[mask])
        theta = np.arctan(dyc_dx)
        xu, yu = x - yt * np.sin(theta), yc + yt * np.cos(theta)
        xl, yl = x + yt * np.sin(theta), yc - yt * np.cos(theta)
        return xu, yu, xl, yl

    @staticmethod
    def naca5(code, n_points=100, spacing='cosine', closed_te=False):
        try:
            L = int(code[0]) * 0.15
            P = int(code[1]) * 0.05
            T = int(code[2:]) / 100.0
        except:
            return None
        data = {0.05: (0.0580, 361.4), 0.10: (0.1260, 51.64), 0.15: (0.2025, 15.957), 0.20: (0.2900, 6.643), 0.25: (0.3910, 3.230)}
        if P in data: r, k1 = data[P]
        else:
            ps = sorted(data.keys())
            p_low = max([p for p in ps if p <= P] or [ps[0]])
            p_high = min([p for p in ps if p >= P] or [ps[-1]])
            f = (P - p_low) / (p_high - p_low) if p_low != p_high else 0
            r = data[p_low][0] + f * (data[p_high][0] - data[p_low][0])
            k1 = data[p_low][1] + f * (data[p_high][1] - data[p_low][1])
        x = NACAGeneratorPro.get_spacing(n_points, spacing)
        a0, a1, a2, a3 = 0.2969, -0.1260, -0.3516, 0.2843
        a4 = -0.1015 if not closed_te else -0.1036
        yt = 5 * T * (a0 * np.sqrt(x) + a1 * x + a2 * x**2 + a3 * x**3 + a4 * x**4)
        yc, dyc_dx = np.zeros_like(x), np.zeros_like(x)
        mask = x <= r
        yc[mask] = (k1 / 6.0) * (x[mask]**3 - 3 * r * x[mask]**2 + r**2 * (3 - r) * x[mask])
        dyc_dx[mask] = (k1 / 6.0) * (3 * x[mask]**2 - 6 * r * x[mask] + r**2 * (3 - r))
        mask = x > r
        yc[mask] = (k1 * r**3 / 6.0) * (1 - x[mask])
        dyc_dx[mask] = np.full_like(x[mask], -k1 * r**3 / 6.0)
        theta = np.arctan(dyc_dx)
        xu, yu = x - yt * np.sin(theta), yc + yt * np.cos(theta)
        xl, yl = x + yt * np.sin(theta), yc - yt * np.cos(theta)
        return xu, yu, xl, yl

class UIUCLoader:
    @staticmethod
    def load_from_url(url):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200: return None
            lines = response.text.splitlines()
            coords = []
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 2:
                    try: coords.append([float(parts[0]), float(parts[1])])
                    except: continue
            coords = np.array(coords)
            le_idx = np.argmin(coords[:, 0])
            upper = coords[:le_idx+1][::-1]
            lower = coords[le_idx:]
            return upper[:, 0], upper[:, 1], lower[:, 0], lower[:, 1]
        except: return None

class AirfoilAnalysis:
    @staticmethod
    def compute_aerodynamics(xu, yu, xl, yl, alpha_deg, reynolds=1e6):
        x = np.concatenate([xu[::-1], xl[1:]])
        y = np.concatenate([yu[::-1], yl[1:]])
        n_panels = len(x) - 1
        alpha = np.radians(alpha_deg)
        xc, yc = 0.5 * (x[:-1] + x[1:]), 0.5 * (y[:-1] + y[1:])
        dx, dy = x[1:] - x[:-1], y[1:] - y[:-1]
        l = np.sqrt(dx**2 + dy**2)
        phi = np.arctan2(dy, dx)
        beta = phi + 0.5 * np.pi
        A = np.zeros((n_panels + 1, n_panels + 1))
        b = np.zeros(n_panels + 1)
        for i in range(n_panels):
            for j in range(n_panels):
                if i == j: A[i, j] = 0.5
                else:
                    r = np.sqrt((xc[i] - xc[j])**2 + (yc[i] - yc[j])**2)
                    A[i, j] = (1.0 / (2 * np.pi * r)) * l[j] * np.sin(beta[i] - np.arctan2(yc[i]-yc[j], xc[i]-xc[j]))
            b[i] = np.cos(beta[i] - alpha)
        A[n_panels, 0], A[n_panels, n_panels-1], b[n_panels] = 1, 1, 0
        try:
            gamma = np.linalg.solve(A, b)
            cl = 2 * np.sum(gamma[:-1] * l)
            cp = 1 - (gamma[:-1])**2
            
            # --- Advanced Empirical Aero ---
            # 1. Skin Friction Drag (Schlichting formula for turbulent)
            cf = 0.455 / (np.log10(reynolds)**2.58)
            cd_skin = cf * 2 # Both sides
            
            # 2. Form Drag (based on thickness)
            # Find max thickness
            thickness = np.max(yu - np.interp(xu, xl, yl))
            cd_form = cd_skin * (2 * thickness + 60 * thickness**4)
            
            # 3. Stall Estimation (Empirical)
            # Max Cl typically around 1.2-1.6 for NACA airfoils
            cl_max = 1.5 + (thickness - 0.12) * 2
            if abs(cl) > cl_max:
                # Post-stall behavior
                cl = cl_max * np.sign(cl) * np.exp(-0.2 * (abs(cl) - cl_max))
                cd_form += 0.1 * (abs(cl) - cl_max)**2
                
            cd = cd_skin + cd_form
            return cl, cd, cp, xc
        except:
            return 0.0, 0.0, np.zeros(n_panels), xc

class GeometryOptimizer:
    @staticmethod
    def match_cl(code, target_cl, series='4-digit'):
        best_m = 0
        min_diff = 100
        for m in range(0, 10):
            test_code = f"{m}{code[1:]}"
            if series == '4-digit':
                coords = NACAGeneratorPro.naca4(test_code)
            else:
                coords = NACAGeneratorPro.naca5(test_code)
            if coords:
                cl, _, _, _ = AirfoilAnalysis.compute_aerodynamics(*coords, 0)
                diff = abs(cl - target_cl)
                if diff < min_diff:
                    min_diff = diff
                    best_m = m
        return f"{best_m}{code[1:]}"

def export_stl(xu, yu, xl, yl, filename, thickness=0.1):
    with open(filename, 'w') as f:
        f.write("solid airfoil\n")
        z1, z2 = 0, thickness
        for i in range(len(xu)-1):
            pts = [(xu[i], yu[i], z1), (xu[i+1], yu[i+1], z1), (xu[i+1], yu[i+1], z2), (xu[i], yu[i], z2)]
            for tri in [[0,1,2], [0,2,3]]:
                f.write("facet normal 0 0 0\nouter loop\n")
                for j in tri: f.write(f"vertex {pts[j][0]} {pts[j][1]} {pts[j][2]}\n")
                f.write("endloop\nendfacet\n")
        for i in range(len(xl)-1):
            pts = [(xl[i], yl[i], z1), (xl[i+1], yl[i+1], z1), (xl[i+1], yl[i+1], z2), (xl[i], yl[i], z2)]
            for tri in [[0,1,2], [0,2,3]]:
                f.write("facet normal 0 0 0\nouter loop\n")
                for j in tri: f.write(f"vertex {pts[j][0]} {pts[j][1]} {pts[j][2]}\n")
                f.write("endloop\nendfacet\n")
        f.write("endsolid airfoil\n")
