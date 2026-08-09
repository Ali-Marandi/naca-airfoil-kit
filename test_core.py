import unittest
from airfoil import NACAGeneratorPro

class CoreTests(unittest.TestCase):
    def test_naca4_valid(self):
        coords = NACAGeneratorPro.naca4("2412")
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords[0]), 100)

    def test_naca5_valid(self):
        coords = NACAGeneratorPro.naca5("24012")
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords[0]), 100)

if __name__ == "__main__":
    unittest.main()
