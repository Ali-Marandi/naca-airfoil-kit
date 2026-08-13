import json
import unittest

from airfoil_pro import NACAGeneratorPro, StudyAudit


class StudyAuditTests(unittest.TestCase):
    def setUp(self):
        self.coords = NACAGeneratorPro.naca4("2412", 40)

    def test_geometry_hash_is_stable_for_identical_coordinates(self):
        first_hash = StudyAudit.geometry_sha256(*self.coords)
        second_hash = StudyAudit.geometry_sha256(*self.coords)
        self.assertEqual(first_hash, second_hash)
        self.assertEqual(len(first_hash), 64)

    def test_manifest_contains_reproducibility_fields(self):
        manifest = StudyAudit.build_manifest(
            "NACA 2412",
            *self.coords,
            operating_conditions={"reynolds": 1_000_000, "alpha_deg": 2.0},
            solver={"name": "xfoil", "version": "6.9", "fidelity": "numerical_viscous"},
            source_data={"dataset": "Airfoil 360 v2022"},
        )
        self.assertEqual(manifest["schema_version"], "1.0")
        self.assertEqual(manifest["airfoil"]["name"], "NACA 2412")
        self.assertEqual(manifest["solver"]["name"], "xfoil")
        self.assertEqual(manifest["operating_conditions"]["reynolds"], 1_000_000)
        self.assertIn("geometry_sha256", manifest["airfoil"])
        self.assertIn("created_utc", manifest)
        parsed = json.loads(StudyAudit.to_json(manifest))
        self.assertEqual(parsed["study_id"], manifest["study_id"])


if __name__ == "__main__":
    unittest.main()
