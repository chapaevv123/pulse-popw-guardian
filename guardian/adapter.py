"""Safe integration boundary. No wallet or network action is implemented."""
from __future__ import annotations


class KonnexIntegrationUnavailable(RuntimeError):
    """Raised when an operation lacks explicit current release configuration."""


class KonnexAdapter:
    def __init__(self, *, rpc_url: str | None = None, release_id: str | None = None):
        self.rpc_url = rpc_url
        self.release_id = release_id

    def readiness(self) -> dict:
        missing = [name for name, value in (("rpc_url", self.rpc_url), ("release_id", self.release_id)) if not value]
        return {"ready": not missing, "missing": missing, "wallet_connected": False,
                "transactions_enabled": False}

    def submit_task(self, *_args, **_kwargs):
        raise KonnexIntegrationUnavailable(
            "Task submission is intentionally disabled until the owner approves a wallet and current official release parameters are supplied."
        )

    def publish_receipt(self, *_args, **_kwargs):
        raise KonnexIntegrationUnavailable(
            "Receipt publication is adapter-ready but disabled; Guardian never invents a ScoreRoot or PoPW transaction."
        )
