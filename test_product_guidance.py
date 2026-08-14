import unittest

from product_guidance import (
    PRELIMINARY_SCOPE_NOTICE,
    VALIDATION_METADATA_FIELDS,
    evidence_readiness,
    normalized_validation_metadata,
)


class ProductGuidanceTests(unittest.TestCase):
    def complete_metadata(self):
        return {field: f"documented {field}" for field, _label in VALIDATION_METADATA_FIELDS}

    def test_screening_only_without_experimental_csv(self):
        readiness = evidence_readiness({}, experimental_rows_loaded=False)
        self.assertEqual(readiness["status"], "screening_only")
        self.assertFalse(readiness["experimental_rows_loaded"])
        self.assertIn("Preliminary", readiness["scope_notice"])

    def test_csv_without_metadata_is_informational_not_validated(self):
        readiness = evidence_readiness({}, experimental_rows_loaded=True)
        self.assertEqual(readiness["status"], "informational_validation")
        self.assertEqual(len(readiness["missing_metadata"]), len(VALIDATION_METADATA_FIELDS))
        self.assertNotIn("validated", readiness["headline"].lower())

    def test_complete_metadata_creates_review_state_not_universal_validation(self):
        readiness = evidence_readiness(self.complete_metadata(), experimental_rows_loaded=True)
        self.assertEqual(readiness["status"], "metadata_complete_validation_review")
        self.assertEqual(readiness["missing_metadata"], [])
        self.assertIn("not a universal validation claim", readiness["guidance"])
        self.assertEqual(readiness["scope_notice"], PRELIMINARY_SCOPE_NOTICE)

    def test_metadata_normalization_ignores_unknown_fields(self):
        normalized = normalized_validation_metadata({"source_identifier": "  Test set  ", "unknown": "ignore"})
        self.assertEqual(normalized["source_identifier"], "Test set")
        self.assertNotIn("unknown", normalized)


if __name__ == "__main__":
    unittest.main()
