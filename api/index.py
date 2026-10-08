"""Vercel Python Function entry point.

Vercel's Python runtime natively hosts BaseHTTPRequestHandler subclasses, so
the public deployment uses the same request handler as the local demo.
"""
from guardian.web import Handler


class handler(Handler):  # noqa: N801 - Vercel requires this export name
    pass
