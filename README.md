# Pulse PoPW Guardian

**Evidence-first verification for Konnex Proof of Physical Work.**

[Live demo](https://pulse-popw-guardian.vercel.app/) | [Public repository](https://github.com/chapaevv123/pulse-popw-guardian)

**Real Konnex Testnet proof case:** Guardian is bound to an owner-signed drone-request anchor at block `1,223,966`, extrinsic `1`, with canonical proof classification `REAL_KONNEX_ONCHAIN_JOB_ANCHOR`. This verifies real protocol provenance, not physical execution, validator acceptance, or a ScoreRoot.

Pulse PoPW Guardian is a deterministic trust boundary for Physical AI evidence. It validates evidence completeness and provenance, detects tampering and inconsistent telemetry, evaluates the six metrics documented by Konnex, applies integrity gates, and emits explainable verdicts with reproducible audit receipts.

## Why it exists

Konnex describes PoPW as binding a task instruction, policy execution trace, sensor bundle, and independent scoring into an on-chain or on-chain-anchored record. Before a physical-work result is trusted, its evidence should be complete, internally consistent, and unchanged.

Guardian makes that pre-protocol boundary inspectable. A task can score highly on raw performance and still fail when its evidence integrity is broken:

- Valid evidence: `SUCCESS · 95%`
- Tampered evidence: `FAILURE`, integrity violation, raw task score `97%`
- Incomplete evidence: `INCONCLUSIVE · 58%`

## Implemented now

- Deterministic JSON evidence-schema validation
- SHA-256 provenance checks and tamper detection
- Timestamp, telemetry-coverage, safety, and trajectory consistency checks
- Konnex-aligned accuracy, speed, safety, optimal-track, energy-efficiency, and trajectory-stability metrics
- `SUCCESS`, `FAILURE`, and `INCONCLUSIVE` verdicts with machine-readable reason codes
- Integrity hard gates that override raw performance without hiding its score
- Confidence, check diagnostics, and content-bound reproducible audit receipts
- CLI, public web demo, synthetic fixtures, Vercel adapter, and automated tests
- Fail-closed Konnex integration boundary with no wallet or network writes
- Real Konnex Testnet job-anchor parsing, provenance display, and evidence-binding boundary

## Testnet-ready / next integration

- Bind Guardian input and receipt to a genuine Konnex JobID
- Normalize a release-specific Konnex PoPW bundle without weakening validation
- Preserve the official transaction or protocol receipt alongside Guardian's receipt
- Correlate a published ScoreRoot or validator result when an official public interface is confirmed

Current official wallet documentation names SubWallet, `wss://testnet-rpc1.konnex.world:39944`, and `https://subnets.testnet.konnex.world/faucet`. A public simulator task interface exists at `https://testnet.konnex.world/`. Release-specific subnets, stake values, SDK binaries, and explorer locations are deliberately not inferred from examples.

See [KONNEX_TESTNET_PROOF_RUNBOOK.md](KONNEX_TESTNET_PROOF_RUNBOOK.md) for the owner-approved proof path.

## Future work

- Hardware-rooted capture signatures or TEE/secure-element attestations
- Subnet-specific evidence adapters
- Official PoPW/ScoreRoot publication after a current release interface is confirmed
- Multi-validator correlation and durable external evidence storage

These are not claimed by the demo. A Guardian receipt is not a Konnex ScoreRoot or validator-consensus result.

## Run locally

Requires Python 3.10+ and has no runtime dependencies.

```bash
python -m unittest discover -s tests -v
python -m guardian.cli fixtures/valid_success.json --pretty
python -m guardian.web --host 127.0.0.1 --port 8080
```

## Verification contract

Input is JSON with `task`, `evidence`, and `telemetry`. Each evidence record binds an inline payload to a SHA-256 digest and names its source. Identical input and rules produce identical output, including receipt ID; `issued_at` comes from evidence rather than wall-clock time.

Konnex metric names are preserved. Confidence, reason codes, provenance observations, checks, and the receipt envelope are Guardian extensions rather than claimed protocol fields.

## Official Konnex references

- [Konnex documentation](https://docs.konnex.world/)
- [Proof-of-Physical-Work](https://docs.konnex.world/understand-konnex/contracts-and-popw)
- [AI Verifier metrics](https://docs.konnex.world/supported-ai-models/verifier)
- [Testnet wallet and faucet](https://docs.konnex.world/participate/wallet)
- [Public testnet task interface](https://testnet.konnex.world/)
- [CLI](https://docs.konnex.world/sdk/cli)
- [Python SDK](https://docs.konnex.world/sdk/python)
- [Validator guidance](https://docs.konnex.world/sdk/validators)

## Safety and limitations

- Matching hashes demonstrate integrity, not trusted device identity or authenticity.
- Metrics are transparent local heuristics, not Konnex consensus or a subnet validator replacement.
- No wallet transaction, ScoreRoot, validator/miner registration, or Builder application has been performed by this repository.
- Never place seed phrases, private keys, wallet exports, or tokens in the project.

MIT licensed. See [LICENSE](LICENSE).
