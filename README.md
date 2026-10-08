# Pulse PoPW Guardian

[Public repository](https://github.com/chapaevv123/pulse-popw-guardian) · Live demo pending Vercel authentication

Pulse PoPW Guardian is a deterministic, offline evidence verifier for Proof-of-Physical-Work demonstrations. It validates evidence structure and provenance, evaluates Konnex-aligned metrics, detects consistency and tamper failures, assigns confidence, and emits a stable audit receipt.

It makes **no wallet calls**, submits **no transactions**, and requires neither miner nor validator registration. This repository contains synthetic public-safe examples only.

## Quick start

Requires Python 3.10+.

```bash
python -m unittest discover -s tests -v
python -m guardian.cli fixtures/valid_success.json --pretty
python -m guardian.web --host 127.0.0.1 --port 8080
```

Open `http://127.0.0.1:8080`. The web demo uses only Python's standard library.
An optional editable install is `python -m pip install --no-build-isolation -e .`; the no-build-isolation flag keeps setup offline when a compatible local setuptools is already present.

## Public deployment

The repository includes a native Vercel Python Function entry point in `api/index.py`. It reuses the exact local `BaseHTTPRequestHandler`; `vercel.json` routes the demo and JSON endpoints to that handler and explicitly bundles the fixtures. No environment variables or secrets are required.

After authenticating the Vercel CLI, deploy from the repository root with `vercel --prod`. The permanent live URL will be recorded here after the first successful production deployment.

## Verification contract

Input is a JSON object with `task`, `evidence`, and `telemetry`. Every evidence item binds its inline payload to a SHA-256 digest and identifies a source. The verifier checks required evidence, hash provenance, ordered timestamps within the task window, telemetry coverage, plausible distance progression, safety, and configured thresholds.

Outputs are `SUCCESS`, `FAILURE`, or `INCONCLUSIVE`, with machine-readable reason codes, six integer metrics from 0–100, confidence from 0–1, check details, provenance observations, and a deterministic receipt ID. `issued_at` derives from the evidence bundle rather than wall-clock time, so identical input and rules produce identical output.

The six public metrics match the current Konnex verifier schema: `accuracy`, `speed`, `safety`, `optimal_track`, `energy_efficiency`, and `trajectory_stability`. Guardian's schema, confidence, reason codes, and receipt envelope are project-local extensions—not claimed protocol fields.

## Konnex boundary and testnet readiness

`guardian/adapter.py` is deliberately fail-closed. Official documentation currently shows task submission and proof commands, but validator parameters are explicitly illustrative and release-specific. No network identifiers, faucet URL, explorer URL, stake values, or transaction parameters are guessed here.

Safest later owner-approved sequence:

1. Confirm the active official release, explorer, supported subnet, and SDK version from Konnex release materials.
2. Create/connect a dedicated SubWallet test wallet and add the currently documented WebSocket endpoint, `wss://testnet-rpc1.konnex.world:39944`; never place its seed or key in this repository.
3. Obtain test KNX only from the currently documented official faucet at `https://subnets.testnet.konnex.world/faucet`.
4. Install the official SDK from its pinned source/release and confirm the active subnet.
5. Submit a zero/approved-value test task using the official task interface, sign it in the wallet, retain the job ID and transaction hash.
6. Attach the Guardian receipt to the evidence package through the release-supported proof path.
7. Record the explorer/protocol URL and exported non-secret receipt as proof.

This is a readiness runbook, not an executed proof. Owner approval and confirmed release parameters are required before any wallet action.

## Official references

- [Konnex documentation](https://docs.konnex.world/)
- [Konnex AI Verifier metrics](https://docs.konnex.world/supported-ai-models/verifier)
- [Konnex SDK overview](https://docs.konnex.world/sdk/sdk)
- [Konnex CLI](https://docs.konnex.world/sdk/cli)
- [Konnex Python SDK](https://docs.konnex.world/sdk/python)
- [Konnex validator guidance](https://docs.konnex.world/sdk/validators)
- [Konnex wallet guidance](https://docs.konnex.world/participate/wallet)

## Scope and limitations

- Payload hashing demonstrates integrity of inline evidence; production systems should use signed device manifests, durable object URIs, and trusted capture identities.
- Metrics are transparent heuristics over normalized telemetry, not Konnex consensus or a substitute for subnet-specific validators.
- The demo holds request bodies in memory and is intended for local/public showcase use, not untrusted production hosting.
- No testnet transaction, protocol ScoreRoot, miner registration, or validator registration has been performed.

MIT licensed. See [LICENSE](LICENSE).
