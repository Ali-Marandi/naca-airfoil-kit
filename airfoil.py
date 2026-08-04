import numpy as np
from math import atan2, cos, sin, sqrt, pi

class NACAGenerator:
    @staticmethod
    def get_spacing(n_points, spacing_type='cosine'):
        if spacing_type == 'linear':
            return np.linspace(0, 1, n_points)
        elif spacing_type == 'cosine':
            return 0.5 * (1 - np.cos(np.linspace(0, pi, n_points)))
        else:
            raise ValueError("Spacing type must be 'linear' or 'cosine'")

    @staticmethod
    def naca4(code, n_points=100, spacing='cosine', closed_te=False):
        """Generate NACA 4-digit airfoil coordinates."""
        m = int(code[0]) / 100.0
        p = int(code[1]) / 10.0
        t = int(code[2:]) / 100.0

        x = NACAGenerator.get_spacing(n_points, spacing)
        
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
        # Standard NACA 5-digit parameters
        L = int(code[0]) * 0.15  # Design lift coefficient
        P = int(code[1]) * 0.05  # Position of max camber
        T = int(code[2:]) / 100.0 # Thickness

        # Camber line constants
        data = {
            0.05: (0.0580, 361.4),
            0.10: (0.1260, 51.64),
            0.15: (0.2025, 15.957),
            0.20: (0.2900, 6.643),
            0.25: (0.3910, 3.230)
        }
        
        if P not in data:
            # Linear interpolation for p if not in standard values
            ps = sorted(data.keys())
            p_low = max([p for p in ps if p <= P] or [ps[0]])
            p_high = min([p for p in ps if p >= P] or [ps[-1]])
            if p_low == p_high:
                r, k1 = data[p_low]
            else:
                f = (P - p_low) / (p_high - p_low)
                r = data[p_low][0] + f * (data[p_high][0] - data[p_low][0])
                k1 = data[p_low][1] + f * (data[p_high][1] - data[p_low][1])
        else:
            r, k1 = data[P]

        x = NACAGenerator.get_spacing(n_points, spacing)
        
        # Thickness distribution (same as 4-digit)
        a0, a1, a2, a3 = 0.2969, -0.1260, -0.3516, 0.2843
        a4 = -0.1015 if not closed_te else -0.1036
        yt = 5 * T * (a0 * np.sqrt(x) + a1 * x + a2 * x**2 + a3 * x**3 + a4 * x**4)

        # Camber line
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
