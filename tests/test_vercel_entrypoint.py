import unittest

from api.index import handler
from guardian.web import Handler


class VercelEntrypointTests(unittest.TestCase):
    def test_exports_native_handler(self):
        self.assertTrue(issubclass(handler, Handler))


if __name__ == "__main__":
    unittest.main()
