# Konnex Builder Submission Draft — Pulse PoPW Guardian

> Draft only. The owner must review and submit it; this repository performs no application submission.

## One-line pitch

Pulse PoPW Guardian turns physical-work evidence into a deterministic, explainable verification result and content-bound audit receipt before it reaches a Konnex protocol boundary.

## What is built

- Offline schema and provenance validation with SHA-256 tamper checks
- Transparent evaluation of the six metrics in the official Konnex verifier schema
- SUCCESS / FAILURE / INCONCLUSIVE outcomes with machine-readable reason codes
- Confidence calculation, check-by-check diagnostics, and deterministic audit receipts
- Three synthetic fixtures covering success, tamper failure, and insufficient evidence
- Dependency-free local web demo, CLI, tests, and fail-closed Konnex adapter boundary

## Why it matters

PoPW systems need a clean separation between captured evidence, local validation, subnet-specific verification, and protocol publication. Guardian makes the first boundary inspectable and reproducible while avoiding claims that local heuristics equal validator consensus.

## Demo

```bash
python -m unittest discover -s tests -v
python -m guardian.web --host 127.0.0.1 --port 8080
```

Load each fixture in the UI and compare the verdict, confidence, reason codes, provenance state, and receipt ID.

## Konnex integration

The output retains Konnex's documented six metric names and verdict concept. Guardian-specific diagnostics are namespaced by the local receipt envelope. The adapter intentionally refuses network writes until an owner supplies a confirmed official release, RPC/API endpoint, active subnet, wallet approval, and supported proof publication path.

## Testnet proof plan

After owner approval: confirm the current release parameters in official materials, use a dedicated test wallet, obtain faucet-only tokens, submit a signed test task with the official SDK/CLI, attach the evidence bundle and Guardian receipt via the supported proof command, then record the job ID and explorer/protocol-visible transaction URL. No registration is required for the standalone MVP; validator or miner operation is a separate future decision.

## Current evidence

- Local deterministic verifier and demo: complete
- Automated tests: complete
- Public repository URL: https://github.com/chapaevv123/pulse-popw-guardian
- Live demo URL: pending owner-authenticated hosting
- Testnet transaction/explorer proof: pending owner wallet approval and confirmed active release parameters

## Links to insert before submission

- Repository: https://github.com/chapaevv123/pulse-popw-guardian
- Live demo: `TBD`
- Testnet/explorer proof: `TBD`

## License

MIT
