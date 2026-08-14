"""Integration tests for broad, deterministic Pareto catalog screening.

The matrix uses generated NACA sections so CI is network-independent. A separate
runner exercises the curated real UIUC catalog and records source provenance.
"""

import unittest

import numpy as np

from airfoil_pro import NACAGeneratorPro, ParetoExplorer


class ParetoCatalogIntegrationTests(unittest.TestCase):
    @staticmethod
    def broad_naca_catalog():
        # 120 distinct NACA 4-digit candidates: 4 cambers × 5 locations × 6 thicknesses.
        return [
            f"{camber}{position}{thickness:02d}"
            for camber in (0, 2, 4, 6)
            for position in (1, 3, 5, 7, 9)
            for thickness in (6, 9, 12, 15, 18, 21)
        ]

    def assert_front_is_non_dominated(self, rows):
        front = [row for row in rows if row["pareto_front"]]
        for candidate in front:
            for challenger in rows:
                dominates = (
                    challenger["best_ld"] >= candidate["best_ld"]
                    and challenger["cl_objective"] >= candidate["cl_objective"]
                    and (
                        challenger["best_ld"] > candidate["best_ld"]
                        or challenger["cl_objective"] > candidate["cl_objective"]
                    )
                )
                if challenger is not candidate:
                    self.assertFalse(dominates, f"{challenger['airfoil']} unexpectedly dominates front member {candidate['airfoil']}")

    def test_large_generated_naca_catalog_has_complete_deterministic_pareto_ranking(self):
        codes = self.broad_naca_catalog()
        alpha_values = np.arange(-3.0, 10.0, 2.0)
        result = ParetoExplorer.screen_naca4(codes, alpha_values, re=750_000, rough=0.0002, n_points=48)
        rows = result["rankings"]
        self.assertEqual(len(rows), len(codes))
        self.assertEqual(len(result["polars"]), len(codes))
        self.assertEqual(len({row["airfoil"] for row in rows}), len(codes))
        self.assertGreaterEqual(sum(row["pareto_front"] for row in rows), 1)
        self.assertTrue(all(row["pareto_rank"] >= 1 for row in rows))
        self.assertTrue(all(len(polar) == len(alpha_values) for polar in result["polars"].values()))
        self.assert_front_is_non_dominated(rows)

    def test_named_geometry_catalog_reuses_shared_pareto_pipeline(self):
        geometries = {
            f"Fixture NACA {code}": NACAGeneratorPro.naca4(code, 48)
            for code in ("0012", "1412", "2412", "4412", "6412", "2424")
        }
        result = ParetoExplorer.screen_geometries(
            geometries,
            [-2.0, 0.0, 2.0, 4.0, 6.0],
            re=1_000_000,
            rough=0.0,
            cl_objective="cl_at_design_alpha",
            design_alpha_deg=4.0,
        )
        self.assertEqual(len(result["rankings"]), len(geometries))
        self.assertEqual(len(result["polars"]), len(geometries))
        self.assertIn("Cl at α = 4.00°", result["objective"]["cl"])
        self.assert_front_is_non_dominated(result["rankings"])


if __name__ == "__main__":
    unittest.main()
