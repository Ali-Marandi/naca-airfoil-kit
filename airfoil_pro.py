import numpy as np
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
        """Generate NACA 4-digit airfoil coordinates."""
        try:
            m = int(code[0]) / 100.0
            p = int(code[1]) / 10.0
            t = int(code[2:]) / 100.0
        except:
            return None

        x = NACAGeneratorPro.get_spacing(n_points, spacing)
        
        # Thickness distribution
        a0, a1, a2, a3 = 0.2969, -0.1260, -0.3516, 0.2843
        a4 = -0.1015 if not closed_te else -0.1036
        yt = 5 * t * (a0 * np.sqrt(x) + a1 * x + a2 * x**2 + a3 * x**3 + a4 * x**4)

        # Camber line
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
        xu = x - yt * np.sin(theta)
        yu = yc + yt * np.cos(theta)
        xl = x + yt * np.sin(theta)
        yl = yc - yt * np.cos(theta)

        return xu, yu, xl, yl

    @staticmethod
    def naca5(code, n_points=100, spacing='cosine', closed_te=False):
        """Generate NACA 5-digit airfoil coordinates."""
        try:
            L = int(code[0]) * 0.15
            P = int(code[1]) * 0.05
            T = int(code[2:]) / 100.0
        except:
            return None

        data = {
            0.05: (0.0580, 361.4),
            0.10: (0.1260, 51.64),
            0.15: (0.2025, 15.957),
            0.20: (0.2900, 6.643),
            0.25: (0.3910, 3.230)
        }
        
        if P in data:
            r, k1 = data[P]
        else:
            ps = sorted(data.keys())
            p_low = max([p for p in ps if p <= P] or [ps[0]])
            p_high = min([p for p in ps if p >= P] or [ps[-1]])
            if p_low == p_high:
                r, k1 = data[p_low]
            else:
                f = (P - p_low) / (p_high - p_low)
                r = data[p_low][0] + f * (data[p_high][0] - data[p_low][0])
                k1 = data[p_low][1] + f * (data[p_high][1] - data[p_low][1])

        x = NACAGeneratorPro.get_spacing(n_points, spacing)
        a0, a1, a2, a3 = 0.2969, -0.1260, -0.3516, 0.2843
        a4 = -0.1015 if not closed_te else -0.1036
        yt = 5 * T * (a0 * np.sqrt(x) + a1 * x + a2 * x**2 + a3 * x**3 + a4 * x**4)

        yc = np.zeros_like(x)
        dyc_dx = np.zeros_like(x)
        
        mask = x <= r
        yc[mask] = (k1 / 6.0) * (x[mask]**3 - 3 * r * x[mask]**2 + r**2 * (3 - r) * x[mask])
        dyc_dx[mask] = (k1 / 6.0) * (3 * x[mask]**2 - 6 * r * x[mask] + r**2 * (3 - r))
        
        mask = x > r
        yc[mask] = (k1 * r**3 / 6.0) * (1 - x[mask])
        dyc_dx[mask] = np.full_like(x[mask], -k1 * r**3 / 6.0)

        theta = np.arctan(dyc_dx)
        xu = x - yt * np.sin(theta)
        yu = yc + yt * np.cos(theta)
        xl = x + yt * np.sin(theta)
        yl = yc - yt * np.cos(theta)

        return xu, yu, xl, yl

class AirfoilAnalysis:
    @staticmethod
    def compute_aerodynamics(xu, yu, xl, yl, alpha_deg):
        """Simple Vortex Panel Method to estimate Cl and Cp."""
        # Combine upper and lower surfaces into a single loop (clockwise)
        x = np.concatenate([xu[::-1], xl[1:]])
        y = np.concatenate([yu[::-1], yl[1:]])
        
        n_panels = len(x) - 1
        alpha = np.radians(alpha_deg)
        
        # Panel properties
        xc = 0.5 * (x[:-1] + x[1:])
        yc = 0.5 * (y[:-1] + y[1:])
        dx = x[1:] - x[:-1]
        dy = y[1:] - y[:-1]
        l = np.sqrt(dx**2 + dy**2)
        phi = np.arctan2(dy, dx)
        beta = phi + 0.5 * np.pi
        
        # Influence matrix
        A = np.zeros((n_panels + 1, n_panels + 1))
        b = np.zeros(n_panels + 1)
        
        for i in range(n_panels):
            for j in range(n_panels):
                if i == j:
                    A[i, j] = 0.5
                else:
                    # Simplified vortex influence
                    r = np.sqrt((xc[i] - xc[j])**2 + (yc[i] - yc[j])**2)
                    A[i, j] = (1.0 / (2 * np.pi * r)) * l[j] * np.sin(beta[i] - np.arctan2(yc[i]-yc[j], xc[i]-xc[j]))
            
            b[i] = np.cos(beta[i] - alpha)
        
        # Kutta condition (simplified)
        A[n_panels, 0] = 1
        A[n_panels, n_panels-1] = 1
        b[n_panels] = 0
        
        try:
            gamma = np.linalg.solve(A, b)
            cl = 2 * np.sum(gamma[:-1] * l)
            cp = 1 - (gamma[:-1])**2
            return cl, cp, xc
        except:
            return 0.0, np.zeros(n_panels), xc

def export_stl(xu, yu, xl, yl, filename, thickness=0.1):
    """Export airfoil to STL format for 3D printing."""
    with open(filename, 'w') as f:
        f.write("solid airfoil\n")
        # Simplified STL: two faces (front and back) and connecting strips
        # This is a 2.5D extrusion
        z1, z2 = 0, thickness
        for i in range(len(xu)-1):
            # Upper surface strips
            pts = [
                (xu[i], yu[i], z1), (xu[i+1], yu[i+1], z1), (xu[i+1], yu[i+1], z2), (xu[i], yu[i], z2)
            ]
            f.write(f"facet normal 0 0 0\nouter loop\n")
            f.write(f"vertex {pts[0][0]} {pts[0][1]} {pts[0][2]}\n")
            f.write(f"vertex {pts[1][0]} {pts[1][1]} {pts[1][2]}\n")
            f.write(f"vertex {pts[2][0]} {pts[2][1]} {pts[2][2]}\n")
            f.write("endloop\nendfacet\n")
            f.write(f"facet normal 0 0 0\nouter loop\n")
            f.write(f"vertex {pts[0][0]} {pts[0][1]} {pts[0][2]}\n")
            f.write(f"vertex {pts[2][0]} {pts[2][1]} {pts[2][2]}\n")
            f.write(f"vertex {pts[3][0]} {pts[3][1]} {pts[3][2]}\n")
            f.write("endloop\nendfacet\n")
        
        for i in range(len(xl)-1):
            # Lower surface strips
            pts = [
                (xl[i], yl[i], z1), (xl[i+1], yl[i+1], z1), (xl[i+1], yl[i+1], z2), (xl[i], yl[i], z2)
            ]
            f.write(f"facet normal 0 0 0\nouter loop\n")
            f.write(f"vertex {pts[0][0]} {pts[0][1]} {pts[0][2]}\n")
            f.write(f"vertex {pts[1][0]} {pts[1][1]} {pts[1][2]}\n")
            f.write(f"vertex {pts[2][0]} {pts[2][1]} {pts[2][2]}\n")
            f.write("endloop\nendfacet\n")
            f.write(f"facet normal 0 0 0\nouter loop\n")
            f.write(f"vertex {pts[0][0]} {pts[0][1]} {pts[0][2]}\n")
            f.write(f"vertex {pts[2][0]} {pts[2][1]} {pts[2][2]}\n")
            f.write(f"vertex {pts[3][0]} {pts[3][1]} {pts[3][2]}\n")
            f.write("endloop\nendfacet\n")
        f.write("endsolid airfoil\n")
