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
            self.assertIn(b"PoPW Guardian", response.read())

    def test_verify_endpoint(self):
        with urlopen(self.base + "/api/fixtures/valid_success", timeout=2) as response:
            bundle = response.read()
        request = Request(self.base + "/api/verify", data=bundle, method="POST", headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=2) as response:
            result = json.load(response)
        self.assertEqual(result["verdict"], "SUCCESS")
        self.assertTrue(result["audit_receipt"]["receipt_id"].startswith("pgr_"))

if __name__ == "__main__":
    unittest.main()
