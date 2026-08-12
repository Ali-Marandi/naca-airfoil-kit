import unittest

import numpy as np

from airfoil_pro import AirfoilAnalysis, EngineeringStudy, NACAGeneratorPro


class CommercialFeatureTests(unittest.TestCase):
    def setUp(self):
        self.coords = NACAGeneratorPro.naca4("2412", 60)

    def test_geometry_metrics_are_physical(self):
        metrics = AirfoilAnalysis.geometry_metrics(*self.coords)
        self.assertGreater(metrics["max_thickness_pct"], 5.0)
        self.assertLess(metrics["max_thickness_pct"], 20.0)
        self.assertGreater(metrics["max_camber_pct"], 0.1)
        self.assertGreaterEqual(metrics["trailing_edge_gap_pct"], 0.0)
        self.assertGreater(metrics["section_area_ratio"], 0.0)

    def test_polar_contains_one_result_per_alpha(self):
        alpha_values = np.array([-2.0, 0.0, 2.0, 4.0, 6.0])
        polar = AirfoilAnalysis.compute_polar(*self.coords, alpha_values, re=1e6, rough=0.0)
        self.assertEqual(len(polar["rows"]), len(alpha_values))
        self.assertEqual([row["alpha_deg"] for row in polar["rows"]], alpha_values.tolist())
        self.assertTrue(all(row["cd"] > 0.0 for row in polar["rows"]))
        self.assertTrue(all(np.isfinite(row["ld"]) for row in polar["rows"]))
        summary = AirfoilAnalysis.summarize_polar(polar["rows"])
        self.assertTrue(np.isfinite(summary["best_ld"]))

    def test_batch_screening_ranks_valid_naca_codes(self):
        study = EngineeringStudy.screen_naca4(["0012", "2412", "4412"], [-2.0, 0.0, 2.0, 4.0], 1e6)
        self.assertEqual(len(study["rankings"]), 3)
        self.assertEqual(len(study["polars"]), 3)
        efficiencies = [row["best_ld"] for row in study["rankings"]]
        self.assertEqual(efficiencies, sorted(efficiencies, reverse=True))

    def test_candidate_parser_filters_invalid_codes(self):
        parsed = EngineeringStudy.parse_naca4_codes("0012, abc, NACA 2412, 12345, 4412")
        self.assertEqual(parsed, ["0012", "2412", "4412"])


if __name__ == "__main__":
    unittest.main()
