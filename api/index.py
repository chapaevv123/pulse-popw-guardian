"""Vercel Python Function entry point.

Vercel's Python runtime natively hosts BaseHTTPRequestHandler subclasses, so
the public deployment uses the same request handler as the local demo.
"""
from guardian.web import Handler
from urllib.parse import parse_qs, urlsplit


class handler(Handler):  # noqa: N801 - Vercel requires this export name
    """Restore the public path carried through the Vercel rewrite."""

    def _restore_public_path(self) -> None:
        parsed = urlsplit(self.path)
        forwarded = parse_qs(parsed.query, keep_blank_values=True).get("path")
        if forwarded is not None:
            public_path = forwarded[0].lstrip("/")
            self.path = "/" + public_path

    def do_GET(self) -> None:  # noqa: N802
        self._restore_public_path()
        super().do_GET()

    def do_POST(self) -> None:  # noqa: N802
        self._restore_public_path()
        super().do_POST()
