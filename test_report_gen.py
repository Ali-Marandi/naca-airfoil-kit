import os
import tempfile
import unittest

from product_guidance import evidence_readiness
from report_gen import generate_pdf_report


class ReportGenerationTests(unittest.TestCase):
    def test_generates_preliminary_evidence_aware_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "study.pdf")
            generate_pdf_report(
                path,
                {
                    "name": "NACA 2412",
                    "params": {"Reynolds number": "1.0e6", "Alpha [deg]": 2.0},
                    "cl": 0.4,
                    "cd": 0.02,
                    "evidence_readiness": evidence_readiness({}, experimental_rows_loaded=False),
                    "audit_manifest_note": "Companion manifest required for study handoff.",
                },
            )
            self.assertTrue(os.path.exists(path))
            self.assertGreater(os.path.getsize(path), 100)
            with open(path, "rb") as handle:
                self.assertEqual(handle.read(4), b"%PDF")


if __name__ == "__main__":
    unittest.main()
