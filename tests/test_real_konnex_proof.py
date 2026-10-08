import json
from pathlib import Path
import unittest
from urllib.request import urlopen

from guardian.web import Handler, ThreadingHTTPServer
import threading


ROOT = Path(__file__).parents[1]
ANCHOR = "0xc7705715657ab1dbde65c163678ac359bc4cead3f20eea38cb13a6319158a051"
PAYLOAD = "konnex-job:v1:4:" + ANCHOR


class RealKonnexProofTests(unittest.TestCase):
    def test_source_and_canonical_proof_match_exactly(self):
        source = json.loads((ROOT / "KONNEX_NONCE29_EXACT_MATCH.json").read_text(encoding="utf-8"))[0]
        proof = json.loads((ROOT / "KONNEX_REAL_ONCHAIN_PROOF_V1.json").read_text(encoding="utf-8"))
        for key in ("block_number", "block_hash", "extrinsic_index", "extrinsic_hash", "signer", "nonce", "konnex_job_payload", "raw_extrinsic"):
            self.assertEqual(proof[key], source[key])
        self.assertEqual(proof["proof_classification"], "REAL_KONNEX_ONCHAIN_JOB_ANCHOR")

    def test_job_anchor_is_exact_payload_suffix(self):
        proof = json.loads((ROOT / "KONNEX_REAL_ONCHAIN_PROOF_V1.json").read_text(encoding="utf-8"))
        self.assertEqual(proof["konnex_job_payload"], PAYLOAD)
        self.assertEqual(proof["job_anchor"], proof["konnex_job_payload"].removeprefix("konnex-job:v1:4:"))

    def test_proof_does_not_fabricate_full_popw(self):
        proof = json.loads((ROOT / "KONNEX_REAL_ONCHAIN_PROOF_V1.json").read_text(encoding="utf-8"))
        self.assertFalse(proof["status"]["full_popw_verified"])
        self.assertFalse(proof["status"]["score_root_verified"])
        self.assertEqual(proof["status"]["physical_evidence_verification"], "AWAITING_OFFICIAL_EVIDENCE_BUNDLE")

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

    def test_anchor_fixture_and_provenance_rendering(self):
        with urlopen(self.base + "/api/fixtures/real_konnex_anchor", timeout=2) as response:
            fixture = json.load(response)
        self.assertEqual(fixture["job_anchor"], ANCHOR)
        self.assertFalse(fixture["full_popw_verified"])
        with urlopen(self.base + "/", timeout=2) as response:
            page = response.read().decode("utf-8")
        for text in ("Real Konnex anchor", "On-chain provenance", "ANCHOR VERIFIED", "SCORE ROOT NOT VERIFIED"):
            self.assertIn(text, page)


if __name__ == "__main__":
    unittest.main()
