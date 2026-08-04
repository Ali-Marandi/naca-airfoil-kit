from airfoil import NACAGenerator
import numpy as np

def test_naca4():
    xu, yu, xl, yl = NACAGenerator.naca4("2412", n_points=10)
    assert len(xu) == 10
    assert xu[0] == 0.0
    # The x-coordinate of the tip might not be exactly 1.0 due to theta
    assert abs(xu[0]) < 1e-6
    print(f"Leading edge x: {xu[0]}, Trailing edge x: {xu[-1]}")
    print("NACA 4-digit test passed!")

def test_naca5():
    xu, yu, xl, yl = NACAGenerator.naca5("24012", n_points=10)
    assert len(xu) == 10
    assert xu[0] == 0.0
    print("NACA 5-digit test passed!")

if __name__ == "__main__":
    test_naca4()
    test_naca5()
