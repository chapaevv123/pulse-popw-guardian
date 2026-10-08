# Konnex Builder Application — Copy-ready Draft

> Owner review and submission required. No application has been submitted.

## Project / team name

Pulse PoPW Guardian

## Role

Builder / Developer

## One-line pitch (122 characters)

Deterministic evidence verification for Konnex PoPW, with provenance, integrity gates, explainable verdicts, and receipts.

## Category

**Recommended:** Proof-of-Physical-Work / Verification Infrastructure

The current public application category list was not discoverable in official indexed sources. If the live form differs, select its closest exact option to **Developer Infrastructure**, **Verification**, or **Physical AI / PoPW**. Do not select validator operation unless the project actually begins operating a validator.

## Stage

Working demo

## Demo link

https://pulse-popw-guardian.vercel.app/

## GitHub

https://github.com/chapaevv123/pulse-popw-guardian

## Description

Pulse PoPW Guardian is an evidence-first verification boundary for Konnex Proof of Physical Work. It checks whether physical-task evidence is complete, internally consistent, and unchanged before the result is trusted. It evaluates Konnex-aligned metrics, separates raw task performance from evidence integrity, and emits explainable `SUCCESS`, `FAILURE`, or `INCONCLUSIVE` verdicts with reproducible receipts.

This matters for Physical AI because a high-performing task result is not trustworthy when its sensor or media evidence has been altered. Guardian makes that failure mode explicit: a tampered fixture retains its 97% raw score but receives a final `FAILURE` through an integrity hard gate.

## Technical differentiation

- Fully deterministic and offline: no hidden model, mutable state, or network dependency
- SHA-256 evidence provenance and explicit tamper checks
- Integrity hard gates independent from raw metric scoring
- Six metrics aligned with the current Konnex verifier schema
- Machine-readable reason codes, check traces, and confidence
- Content-bound receipt IDs reproducible from the same input and rules
- Fail-closed adapter: no invented network parameters or wallet actions

## What is already built

- Public Konnex-native demo and CLI
- Evidence schema, provenance, temporal, trajectory, safety, and coverage checks
- Success, tamper-failure, and incomplete-evidence fixtures
- Explainable verdict console and deterministic audit receipts
- Automated route, API, adapter, determinism, and verifier tests
- MIT-licensed public repository and practical testnet proof runbook

## What we want to build next on Konnex

1. Bind normalized evidence and Guardian receipts to a genuine Konnex JobID.
2. Implement the smallest release-specific PoPW bundle adapter from an official schema.
3. Preserve protocol receipts and correlate validator/ScoreRoot results when a public interface is confirmed.
4. Add signed device manifests or hardware-rooted evidence without weakening deterministic checks.

## Why Konnex

Konnex treats physical evidence, independent validation, and PoPW as core protocol concerns rather than application metadata. Guardian is designed for that boundary: deciding whether evidence is trustworthy enough to proceed from task performance toward protocol acceptance. Its deterministic channel also complements Konnex's documented two-tier validator design.

## Team

Owner/builder details to be entered by the owner. No people are inferred or invented.

## Grant ask

Do not enter a number unless required and owner-approved. If numeric input is mandatory, derive a milestone-based range after confirming program norms:

- Milestone 1: official bundle/JobID adapter and testnet receipt capture
- Milestone 2: ScoreRoot or validator-result correlation via a published interface
- Milestone 3: signed capture provenance and end-to-end reference integration

Base the amount on agreed deliverables, engineering time, and simulator/hardware costs—not an arbitrary headline figure.

## Funding history

To be completed by the owner. No funding history is asserted.

## Current integration status

**Implemented:** deterministic verification, public demo/API, fixtures, reason codes, integrity gates, and Guardian receipts.

**Testnet-ready:** owner-controlled wallet/faucet setup and a safe discovery path for a genuine Konnex JobID/proof interface.

**Not claimed:** on-chain Guardian receipt, protocol-accepted PoPW, published ScoreRoot, validator consensus, or miner/validator operation.

## Proof links

- Live demo: https://pulse-popw-guardian.vercel.app/
- Repository: https://github.com/chapaevv123/pulse-popw-guardian
- Testnet/protocol proof: pending owner-approved execution and official release parameters

## License

MIT
