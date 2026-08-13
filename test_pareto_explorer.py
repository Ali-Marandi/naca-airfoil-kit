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


if __name__ == "__main__":
    unittest.main()
