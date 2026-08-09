import unittest
import numpy as np
from airfoil import NACAGeneratorPro

class AirfoilTests(unittest.TestCase):
    def test_symmetric_section(self):
        coords = NACAGeneratorPro.naca4("0012", 11)
        self.assertIsNotNone(coords)
        xu, yu, xl, yl = coords
        for u, l in zip(yu, yl):
            self.assertAlmostEqual(u, -l, places=5)

    def test_endpoints_and_count(self):
        coords = NACAGeneratorPro.naca4("2412", 51)
        self.assertIsNotNone(coords)
        xu, yu, xl, yl = coords
        self.assertEqual(len(xu), 51)
        self.assertEqual(len(xl), 51)
        # In our generator, x[0] is 0
        self.assertAlmostEqual(xu[0], 0, places=5)
        self.assertAlmostEqual(xl[0], 0, places=5)

if __name__ == "__main__":
    unittest.main()
