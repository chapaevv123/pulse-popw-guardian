import unittest
import json
import threading
from urllib.parse import quote
from urllib.request import Request, urlopen

from api.index import handler
from guardian.web import Handler
from http.server import ThreadingHTTPServer


class VercelEntrypointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_exports_native_handler(self):
        self.assertTrue(issubclass(handler, Handler))

    def rewritten_url(self, public_path):
        return self.base + "/api?path=" + quote(public_path, safe="")

    def test_rewritten_root_returns_demo_html(self):
        with urlopen(self.rewritten_url(""), timeout=2) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers.get_content_type(), "text/html")
            self.assertIn(b"PoPW Guardian", response.read())

    def test_rewritten_fixture_and_verify_routes(self):
        with urlopen(self.rewritten_url("api/fixtures/valid_success"), timeout=2) as response:
            self.assertEqual(response.status, 200)
            bundle = response.read()
        request = Request(
            self.rewritten_url("api/verify"), data=bundle, method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urlopen(request, timeout=2) as response:
            self.assertEqual(response.status, 200)
            result = json.load(response)
        self.assertEqual(result["verdict"], "SUCCESS")


if __name__ == "__main__":
    unittest.main()
