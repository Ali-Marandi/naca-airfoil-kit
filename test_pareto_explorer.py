import unittest

import numpy as np

from airfoil_pro import ParetoExplorer


class ParetoExplorerTests(unittest.TestCase):
    def test_non_dominated_sort_marks_front_and_dominated_rows(self):
        rows = [
            {"airfoil": "A", "best_ld": 10.0, "cl_objective": 0.40},
            {"airfoil": "B", "best_ld": 9.0, "cl_objective": 0.50},
            {"airfoil": "C", "best_ld": 8.0, "cl_objective": 0.30},
        ]
        ranked = ParetoExplorer.non_dominated_sort(rows)
        by_name = {row["airfoil"]: row for row in ranked}
        self.assertTrue(by_name["A"]["pareto_front"])
        self.assertTrue(by_name["B"]["pareto_front"])
        self.assertFalse(by_name["C"]["pareto_front"])
        self.assertEqual(by_name["C"]["pareto_rank"], 2)

    def test_screen_naca4_returns_ranked_tradeoffs(self):
        result = ParetoExplorer.screen_naca4(
            "0012, 2412, 4412, 6409",
            np.arange(-4.0, 13.0, 1.0),
            re=1_000_000,
            rough=0.0,
        )
        self.assertEqual(len(result["rankings"]), 4)
        self.assertGreaterEqual(sum(row["pareto_front"] for row in result["rankings"]), 1)
        self.assertEqual(result["objective"]["cl"], "Maximum Cl over envelope")
        self.assertTrue(all(row["pareto_rank"] >= 1 for row in result["rankings"]))

    def test_design_alpha_objective_requires_in_range_alpha(self):
        result = ParetoExplorer.screen_naca4(
            ["0012", "2412"],
            [-2.0, 0.0, 2.0, 4.0],
            re=1_000_000,
            cl_objective="cl_at_design_alpha",
            design_alpha_deg=2.0,
        )
        self.assertIn("Cl at α = 2.00°", result["objective"]["cl"])
        with self.assertRaises(ValueError):
            ParetoExplorer.screen_naca4(
                ["0012", "2412"],
                [-2.0, 0.0, 2.0, 4.0],
                re=1_000_000,
                cl_objective="cl_at_design_alpha",
                design_alpha_deg=8.0,
            )

    def test_multi_objective_sort_requires_strength_at_every_condition(self):
        rows = [
            {"airfoil": "A", "ld_re_low": 10.0, "cl_re_low": 0.50, "ld_re_high": 20.0, "cl_re_high": 0.70},
            {"airfoil": "B", "ld_re_low": 9.0, "cl_re_low": 0.40, "ld_re_high": 19.0, "cl_re_high": 0.60},
            {"airfoil": "C", "ld_re_low": 12.0, "cl_re_low": 0.45, "ld_re_high": 18.0, "cl_re_high": 0.65},
        ]
        ranked = ParetoExplorer.non_dominated_sort_multi(rows, ["ld_re_low", "cl_re_low", "ld_re_high", "cl_re_high"])
        by_name = {row["airfoil"]: row for row in ranked}
        self.assertTrue(by_name["A"]["pareto_front"])
        self.assertFalse(by_name["B"]["pareto_front"])
        self.assertTrue(by_name["C"]["pareto_front"])

    def test_multi_re_screen_returns_robust_condition_metrics(self):
        from airfoil_pro import NACAGeneratorPro

        geometries = {
            f"NACA {code}": NACAGeneratorPro.naca4(code, 60)
            for code in ("0012", "2412", "4412")
        }
        result = ParetoExplorer.screen_geometries_multi_re(
            geometries,
            np.arange(-4.0, 13.0, 1.0),
            [100_000, 500_000, 1_000_000],
            cl_objective="cl_at_design_alpha",
            design_alpha_deg=4.0,
        )
        self.assertEqual(len(result["rankings"]), 3)
        self.assertEqual(result["objective"]["reynolds_values"], [100_000.0, 500_000.0, 1_000_000.0])
        keys = result["objective"]["robust_objective_keys"]
        for row in result["rankings"]:
            self.assertEqual(len(row["per_re_metrics"]), 3)
            self.assertGreaterEqual(row["best_ld_std"], 0.0)
            self.assertGreaterEqual(row["worst_case_best_ld"], 0.0)
            self.assertTrue(all(key in row for key in keys))
        for front_row in (row for row in result["rankings"] if row["pareto_front"]):
            self.assertFalse(
                any(
                    all(other[key] >= front_row[key] for key in keys)
                    and any(other[key] > front_row[key] for key in keys)
                    for other in result["rankings"]
                    if other["airfoil"] != front_row["airfoil"]
                )
            )

    def test_multi_re_screen_requires_two_distinct_conditions(self):
        from airfoil_pro import NACAGeneratorPro

        geometries = {"NACA 0012": NACAGeneratorPro.naca4("0012", 40)}
        with self.assertRaises(ValueError):
            ParetoExplorer.screen_geometries_multi_re(geometries, [-2.0, 0.0, 2.0], [100_000])


if __name__ == "__main__":
    unittest.main()
