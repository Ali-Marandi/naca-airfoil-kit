"""Generate coordinates for classic NACA four-digit airfoils."""

from math import atan, cos, pi, sin, sqrt


def naca4(code: str, points: int = 51) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    if len(code) != 4 or not code.isdigit() or points < 2:
        raise ValueError("code must be four digits and points at least 2")
    m, p, thickness = int(code[0]) / 100, int(code[1]) / 10, int(code[2:]) / 100
    xs = [(1 - cos(pi * i / (points - 1))) / 2 for i in range(points)]
    upper, lower = [], []
    for x in xs:
        yt = 5 * thickness * (
            0.2969 * sqrt(x) - 0.1260 * x - 0.3516 * x**2
            + 0.2843 * x**3 - 0.1015 * x**4
        )
        if m == 0 or p == 0:
            yc = dy = 0.0
        elif x < p:
            yc = m / p**2 * (2 * p * x - x**2)
            dy = 2 * m / p**2 * (p - x)
        else:
            yc = m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * x - x**2)
            dy = 2 * m / (1 - p) ** 2 * (p - x)
        theta = atan(dy)
        upper.append((x - yt * sin(theta), yc + yt * cos(theta)))
        lower.append((x + yt * sin(theta), yc - yt * cos(theta)))
    return upper, lower
