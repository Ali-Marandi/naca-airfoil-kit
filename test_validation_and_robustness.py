import unittest

import numpy as np

from airfoil_pro import AirfoilAnalysis, ExperimentalValidation, GeometryTools, NACAGeneratorPro, RobustStudy


class ValidationAndRobustnessTests(unittest.TestCase):
    def setUp(self):
        self.coords = NACAGeneratorPro.naca4("2412", 60)

    def test_hinged_flap_changes_trailing_edge_geometry(self):
        original = tuple(np.asarray(value) for value in self.coords)
        transformed = GeometryTools.apply_hinged_flap(*original, hinge_x=0.75, deflection_deg=10.0)
        self.assertEqual(len(transformed[0]), len(original[0]))
        self.assertLess(transformed[1][-1], original[1][-1])
        self.assertLess(transformed[3][-1], original[3][-1])

    def test_csv_parser_accepts_standard_polar_columns(self):
        rows = ExperimentalValidation.parse_csv_text("alpha_deg,cl,cd\n-2,-0.1,0.008\n0,0.1,0.007\n")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["alpha_deg"], -2.0)
        self.assertAlmostEqual(rows[1]["cl"], 0.1)

    def test_validation_metrics_match_identical_model_rows(self):
        alpha_values = [-2.0, 0.0, 2.0]
        polar = AirfoilAnalysis.compute_polar(*self.coords, alpha_values, re=1e6, rough=0.0)["rows"]
        experimental = [
            {"alpha_deg": row["alpha_deg"], "cl": row["cl"], "cd": row["cd"]}
            for row in polar
        ]
        result = ExperimentalValidation.compare_polar(*self.coords, experimental, re=1e6, rough=0.0)
        self.assertLess(result["cl_metrics"]["rmse"], 1e-12)
        self.assertLess(result["cd_metrics"]["rmse"], 1e-12)
        self.assertEqual(result["cl_metrics"]["n"], len(alpha_values))

    def test_condition_envelope_contains_all_model_conditions(self):
        rows = RobustStudy.condition_envelope(
            *self.coords,
            alpha_values=[0.0, 2.0, 4.0],
            reynolds_values=[5e5, 1e6],
            roughness_values=[0.0, 0.0005],
        )
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(row["condition_samples"] == 4 for row in rows))
        self.assertTrue(all(row["ld_min"] <= row["ld_mean"] <= row["ld_max"] for row in rows))


if __name__ == "__main__":
    unittest.main()
