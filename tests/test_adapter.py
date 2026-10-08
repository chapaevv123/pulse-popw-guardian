import unittest

from guardian.adapter import KonnexAdapter, KonnexIntegrationUnavailable

class AdapterTests(unittest.TestCase):
    def test_adapter_is_safe_by_default(self):
        status = KonnexAdapter().readiness()
        self.assertFalse(status["ready"])
        self.assertFalse(status["transactions_enabled"])

    def test_adapter_never_submits_transaction(self):
        with self.assertRaises(KonnexIntegrationUnavailable):
            KonnexAdapter(rpc_url="https://example.invalid", release_id="release").submit_task({})

if __name__ == "__main__":
    unittest.main()
