import unittest
import numpy as np
from airfoil_pro import NACAGeneratorPro, AirfoilAnalysis

class AirfoilTests(unittest.TestCase):
    def test_symmetric_section(self):
        coords = NACAGeneratorPro.naca4("0012", 11)
        self.assertIsNotNone(coords)
        xu, yu, xl, yl = coords
        for u, l in zip(yu, yl):
            self.assertAlmostEqual(u, -l, places=5)

    def test_aero_results(self):
        coords = NACAGeneratorPro.naca4("0012", 50)
        res = AirfoilAnalysis.compute_aerodynamics(*coords, 0)
        self.assertEqual(len(res), 8) # cl, cd, cp, xc, gamma, xc, yc, l
        cl = res[0]
        self.assertAlmostEqual(cl, 0, places=2)

if __name__ == "__main__":
    unittest.main()
