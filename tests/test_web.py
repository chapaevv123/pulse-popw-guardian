import json
import threading
import unittest
from urllib.request import Request, urlopen

from guardian.web import Handler, ThreadingHTTPServer

class WebTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_home_page(self):
        with urlopen(self.base + "/", timeout=2) as response:
            page = response.read().decode("utf-8")
        self.assertIn("PoPW Guardian", page)
        self.assertIn("Final verdict", page)
        self.assertIn("Integrity violation", page)
        self.assertIn("Raw task score: ", page)
        self.assertIn("EVIDENCE_TAMPER_SUSPECTED", page)
        self.assertIn("integrityFailure?x.verdict:x.verdict+' \\u00b7 '+x.final_pct+'%'", page)
        self.assertIn("Evidence-first verification for Konnex Proof of Physical Work", page)
        self.assertIn("BUILT FOR KONNEX PoPW WORKFLOWS", page)
        self.assertIn("A trust boundary for physical work.", page)
        self.assertIn("How the trust boundary works", page)
        self.assertIn("@media(max-width:600px)", page)

    def test_verify_endpoint(self):
        with urlopen(self.base + "/api/fixtures/valid_success", timeout=2) as response:
            bundle = response.read()
        request = Request(self.base + "/api/verify", data=bundle, method="POST", headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=2) as response:
            result = json.load(response)
        self.assertEqual(result["verdict"], "SUCCESS")
        self.assertTrue(result["audit_receipt"]["receipt_id"].startswith("pgr_"))

    def test_all_demo_api_results_are_unchanged(self):
        expected = {
            "valid_success": ("SUCCESS", 95, []),
            "tampered_failure": ("FAILURE", 97, ["EVIDENCE_TAMPER_SUSPECTED"]),
            "incomplete_inconclusive": ("INCONCLUSIVE", 58, [
                "EVIDENCE_MISSING", "INSUFFICIENT_EVIDENCE", "LOW_CONFIDENCE",
                "TELEMETRY_INCOMPLETE", "VIDEO_MISSING",
            ]),
        }
        for fixture, (verdict, score, exact_reasons) in expected.items():
            with self.subTest(fixture=fixture):
                with urlopen(self.base + "/api/fixtures/" + fixture, timeout=2) as response:
                    bundle = response.read()
                request = Request(self.base + "/api/verify", data=bundle, method="POST", headers={"Content-Type": "application/json"})
                with urlopen(request, timeout=2) as response:
                    result = json.load(response)
                self.assertEqual((result["verdict"], result["final_pct"]), (verdict, score))
                self.assertEqual(result["reason_codes"], exact_reasons)

if __name__ == "__main__":
    unittest.main()
