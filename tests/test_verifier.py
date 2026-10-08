import json
from pathlib import Path
from copy import deepcopy
import unittest

from guardian.verifier import verify_bundle

FIXTURES = Path(__file__).parents[1] / "fixtures"

def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

class VerifierTests(unittest.TestCase):
    def test_fixture_verdicts(self):
        for name, verdict in [("valid_success.json", "SUCCESS"), ("tampered_failure.json", "FAILURE"), ("incomplete_inconclusive.json", "INCONCLUSIVE")]:
            with self.subTest(name=name):
                self.assertEqual(verify_bundle(load(name))["verdict"], verdict)

    def test_receipt_is_deterministic(self):
        bundle = load("valid_success.json")
        self.assertEqual(verify_bundle(bundle), verify_bundle(deepcopy(bundle)))

    def test_tamper_reason_and_hash_are_exposed(self):
        result = verify_bundle(load("tampered_failure.json"))
        self.assertIn("EVIDENCE_TAMPER_SUSPECTED", result["reason_codes"])
        self.assertTrue(any(not row["hash_valid"] for row in result["provenance"]))

    def test_incomplete_is_not_failure(self):
        result = verify_bundle(load("incomplete_inconclusive.json"))
        expected = {"EVIDENCE_MISSING", "VIDEO_MISSING", "TELEMETRY_INCOMPLETE", "INSUFFICIENT_EVIDENCE"}
        self.assertLessEqual(expected, set(result["reason_codes"]))

    def test_schema_failure_does_not_raise(self):
        result = verify_bundle({"task": {}, "evidence": "bad", "telemetry": []})
        self.assertEqual(result["verdict"], "INCONCLUSIVE")
        self.assertIn("SCHEMA_INVALID", result["reason_codes"])

    def test_out_of_order_telemetry_fails_consistency(self):
        bundle = load("valid_success.json")
        bundle["telemetry"][1]["timestamp"] = "2026-01-01T12:00:01Z"
        result = verify_bundle(bundle)
        self.assertEqual(result["verdict"], "FAILURE")
        self.assertIn("TIMESTAMP_MISMATCH", result["reason_codes"])

    def test_invalid_metric_configuration_is_inconclusive(self):
        bundle = load("valid_success.json")
        bundle["task"]["requirements"]["metric_weights"] = {name: 0 for name in result_metric_names()}
        result = verify_bundle(bundle)
        self.assertEqual(result["verdict"], "INCONCLUSIVE")
        self.assertIn("METRIC_CONFIGURATION_INVALID", result["reason_codes"])

def result_metric_names():
    return verify_bundle(load("valid_success.json"))["metrics"].keys()

if __name__ == "__main__":
    unittest.main()
