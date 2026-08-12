import numpy as np
import requests
from math import pi

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
            m, p, t = int(code[0])/100.0, int(code[1])/10.0, int(code[2:])/100.0
        except: return None
        x = NACAGeneratorPro.get_spacing(n_points, spacing)
        a = [0.2969, -0.1260, -0.3516, 0.2843, -0.1015 if not closed_te else -0.1036]
        yt = 5 * t * (a[0]*np.sqrt(x) + a[1]*x + a[2]*x**2 + a[3]*x**3 + a[4]*x**4)
        yc, dyc_dx = np.zeros_like(x), np.zeros_like(x)
        if p > 0:
            m1 = x <= p
            yc[m1] = (m / p**2) * (2*p*x[m1] - x[m1]**2)
            dyc_dx[m1] = (2*m / p**2) * (p - x[m1])
            m2 = x > p
            yc[m2] = (m / (1-p)**2) * ((1-2*p) + 2*p*x[m2] - x[m2]**2)
            dyc_dx[m2] = (2*m / (1-p)**2) * (p - x[m2])
        theta = np.arctan(dyc_dx)
        return x - yt*np.sin(theta), yc + yt*np.cos(theta), x + yt*np.sin(theta), yc - yt*np.cos(theta)

    @staticmethod
    def naca5(code, n_points=100, spacing='cosine', closed_te=False):
        try:
            L, P, T = int(code[0])*0.15, int(code[1])*0.05, int(code[2:])/100.0
        except: return None
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
        a = [0.2969, -0.1260, -0.3516, 0.2843, -0.1015 if not closed_te else -0.1036]
        yt = 5 * T * (a[0]*np.sqrt(x) + a[1]*x + a[2]*x**2 + a[3]*x**3 + a[4]*x**4)
        yc, dyc_dx = np.zeros_like(x), np.zeros_like(x)
        m1 = x <= r
        yc[m1] = (k1/6.0) * (x[m1]**3 - 3*r*x[m1]**2 + r**2*(3-r)*x[m1])
        dyc_dx[m1] = (k1/6.0) * (3*x[m1]**2 - 6*r*x[m1] + r**2*(3-r))
        m2 = x > r
        yc[m2] = (k1*r**3/6.0) * (1 - x[m2])
        dyc_dx[m2] = np.full_like(x[m2], -k1*r**3/6.0)
        theta = np.arctan(dyc_dx)
        return x - yt*np.sin(theta), yc + yt*np.cos(theta), x + yt*np.sin(theta), yc - yt*np.cos(theta)

class UIUCLoader:
    @staticmethod
    def load_from_url(url):
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code != 200: return None
            coords = np.array([[float(p) for p in l.split()[:2]] for l in resp.text.splitlines()[1:] if len(l.split()) >= 2])
            le = np.argmin(coords[:, 0])
            up, lo = coords[:le+1][::-1], coords[le:]
            return up[:,0], up[:,1], lo[:,0], lo[:,1]
        except: return None

class AirfoilAnalysis:
    @staticmethod
    def compute_aerodynamics(xu, yu, xl, yl, alpha_deg, re=1e6, rough=0.0):
        x, y = np.concatenate([xu[::-1], xl[1:]]), np.concatenate([yu[::-1], yl[1:]])
        n = len(x) - 1
        alpha = np.radians(alpha_deg)
        xc, yc = 0.5*(x[:-1]+x[1:]), 0.5*(y[:-1]+y[1:])
        dx, dy = np.diff(x), np.diff(y)
        l = np.sqrt(dx**2 + dy**2)
        beta = np.arctan2(dy, dx) + 0.5*pi
        
        # Optimized Influence Matrix Construction
        A = np.zeros((n + 1, n + 1))
        for i in range(n):
            dx_ij, dy_ij = xc[i] - xc, yc[i] - yc
            r2 = dx_ij**2 + dy_ij**2 + 1e-9
            A[i, :n] = (1.0 / (2 * pi * np.sqrt(r2))) * l * np.sin(beta[i] - np.arctan2(dy_ij, dx_ij))
            A[i, i] = 0.5
            
        A[n, 0], A[n, n-1] = 1, 1
        b = np.append(np.cos(beta - alpha), 0)
        
        try:
            # Least-squares solution remains stable for closely spaced cosine panels.
            gamma = np.linalg.lstsq(A, b, rcond=None)[0][:-1]
            cl = 2 * np.sum(gamma * l)
            cp = 1 - gamma**2
            cf = max(0.455/(np.log10(re)**2.58), (1.89+1.62*np.log10(1.0/max(rough, 1e-9)))**-2.5 if rough > 1e-7 else 0)
            t = np.max(yu - np.interp(xu, xl, yl))
            cd = cf * 2 * (1 + 2*t + 60*t**4)
            cl_m = (1.5 + (t-0.12)*2) * (1.0 - 50.0*rough)
            if abs(cl) > cl_m:
                cl = cl_m * np.sign(cl) * np.exp(-0.2*(abs(cl)-cl_m))
                cd += 0.1*(abs(cl)-cl_m)**2
            return cl, cd, cp, xc, gamma, xc, yc, l
        except:
            return 0.0, 0.0, np.zeros(n), xc, np.zeros(n), xc, yc, l

    @staticmethod
    def get_streamlines(xu, yu, xl, yl, alpha_deg, gamma, xc, yc, l):
        alpha = np.radians(alpha_deg)
        X, Y = np.meshgrid(np.linspace(-0.5, 1.5, 30), np.linspace(-0.5, 0.5, 20))
        u, v = np.cos(alpha)*np.ones_like(X), np.sin(alpha)*np.ones_like(X)
        for i in range(len(gamma)):
            r2 = (X-xc[i])**2 + (Y-yc[i])**2 + 1e-6
            u += (gamma[i]*l[i]/(2*pi*r2)) * (Y-yc[i])
            v -= (gamma[i]*l[i]/(2*pi*r2)) * (X-xc[i])
        return X, Y, u, v

class GeometryOptimizer:
    @staticmethod
    def optimize_ld(code, alpha, re, series='4-digit'):
        best_ld, best_code = -1e9, code
        for m in range(10):
            for p in range(1, 10):
                c = f"{m}{p}{code[2:]}"
                res = NACAGeneratorPro.naca4(c) if series=='4-digit' else NACAGeneratorPro.naca5(c)
                if res:
                    cl, cd = AirfoilAnalysis.compute_aerodynamics(*res, alpha, re)[:2]
                    if cd > 0 and cl/cd > best_ld: best_ld, best_code = cl/cd, c
        return best_code, best_ld

    @staticmethod
    def match_cl(code, target, series='4-digit'):
        best_m, min_d = 0, 100
        for m in range(10):
            c = f"{m}{code[1:]}"
            res = NACAGeneratorPro.naca4(c) if series=='4-digit' else NACAGeneratorPro.naca5(c)
            if res:
                cl = AirfoilAnalysis.compute_aerodynamics(*res, 0)[0]
                if abs(cl-target) < min_d: min_d, best_m = abs(cl-target), m
        return f"{best_m}{code[1:]}"
