import unittest

import numpy as np

from airfoil_pro import UIUCLoader


class UIUCLoaderTests(unittest.TestCase):
    def assert_surfaces(self, parsed):
        self.assertIsNotNone(parsed)
        xu, yu, xl, yl = parsed
        self.assertTrue(np.all(np.diff(xu) >= 0))
        self.assertTrue(np.all(np.diff(xl) >= 0))
        self.assertGreater(float(np.max(yu)), 0.0)
        self.assertLess(float(np.min(yl)), 0.0)

    def test_parses_standard_trailing_edge_first_contour(self):
        text = """Demo profile
1.0 0.0
0.75 0.04
0.5 0.06
0.25 0.04
0.0 0.0
0.25 -0.04
0.5 -0.06
0.75 -0.04
1.0 0.0
"""
        self.assert_surfaces(UIUCLoader.parse_coordinate_text(text))

    def test_parses_legacy_leading_edge_first_contour(self):
        text = """NACA 0012
66. 66.
0.0 0.0
0.25 0.04
0.5 0.06
0.75 0.04
1.0 0.0
0.75 -0.04
0.5 -0.06
0.25 -0.04
0.0 0.0
"""
        self.assert_surfaces(UIUCLoader.parse_coordinate_text(text))


if __name__ == "__main__":
    unittest.main()
