import unittest

from airfoil import naca4


class AirfoilTests(unittest.TestCase):
    def test_symmetric_section(self):
        upper, lower = naca4("0012", 11)
        for (_, yu), (_, yl) in zip(upper, lower):
            self.assertAlmostEqual(yu, -yl)

    def test_endpoints_and_count(self):
        upper, lower = naca4("2412", 51)
        self.assertEqual((len(upper), len(lower)), (51, 51))
        self.assertAlmostEqual(upper[0][0], 0)
        self.assertAlmostEqual(lower[0][1], 0)


if __name__ == "__main__":
    unittest.main()
