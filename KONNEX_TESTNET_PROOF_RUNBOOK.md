# Konnex Testnet Proof Runbook

Verified against official public Konnex surfaces on 2026-10-08. Re-check every source immediately before wallet action because testnet interfaces can change.

## Current verified Konnex state

| Item | Verified value | Official source |
|---|---|---|
| Testnet task UI | Public simulator task form | https://testnet.konnex.world/ |
| Wallet | SubWallet | https://docs.konnex.world/participate/wallet |
| WebSocket RPC | `wss://testnet-rpc1.konnex.world:39944` | https://docs.konnex.world/participate/wallet |
| Faucet | `https://subnets.testnet.konnex.world/faucet` | https://docs.konnex.world/participate/wallet |
| Task concept | `konnex task submit` documented | https://docs.konnex.world/sdk/cli |
| PoPW concept | `konnex prove --job-id <JOBID> --bundle ./powp.zip` documented | https://docs.konnex.world/sdk/cli |
| Validator output | Validators publish ScoreRoots | https://docs.konnex.world/sdk/validators |

Not verified from a current official release: public explorer URL, active subnet ID, CLI binary/version, real stake/reward parameters, downloadable release, public ScoreRoot lookup, or exact live-subnet bundle schema. Documentation says validator commands and parameters are illustrative.

## Proof objective

Create the smallest honest link:

`owner testnet identity -> official simulator task/JobID -> corresponding evidence -> Guardian receipt -> official protocol receipt if supported`

Never describe a simulator result or Guardian receipt as on-chain proof without an official resolvable protocol identifier.

## Prerequisites

- Dedicated test-only SubWallet account controlled by the owner
- RPC and faucet re-confirmed in current official documentation
- Reachable official simulator task UI and supported task
- No real funds and no seed/private-key sharing
- Before CLI use: official binary/release, subnet, bundle schema, cost, and receipt lookup confirmed by Konnex

## Owner actions

1. Install SubWallet from its official site and create/select a dedicated test account locally.
2. Add the documented RPC and request test KNX from the documented faucet.
3. Save the public address and faucet receipt/transaction identifier; never share wallet secrets.
4. Submit one supported task through the official testnet UI and save every returned task/job/run ID and result page.
5. Stop before signing anything else unless Konnex confirms the current release, subnet, schema, costs, and public lookup surface.

## Pulse/code actions

After the owner supplies only public IDs and non-secret exported evidence:

1. Preserve task instruction, timestamps, simulator output, telemetry/media references, and hashes.
2. Normalize a copy into Guardian's existing bundle without changing source evidence.
3. Bind `task.task_id` to the genuine Konnex job/run ID when one exists.
4. Run Guardian and save the complete JSON output, receipt ID, and input hash.
5. If Konnex publishes an accepted schema, build a separate adapter without changing verifier semantics.
6. If publication is officially supported and owner-approved, prepare—but do not sign—the exact payload for review.
7. Correlate any transaction, protocol receipt, validator result, or ScoreRoot only through an official surface.

## Expected receipts

- Public wallet address and faucet claim/transaction ID
- Testnet task/job/run ID and result URL
- Original exported simulator evidence
- Guardian input hash, receipt ID, verdict, reason codes, and full output
- If supported: task transaction, PoPW submission ID, validator result, and ScoreRoot/public URL

## Success criteria

**Intermediate proof:** official task/run has a stable ID; Guardian verifies evidence tied to it; the receipt reproduces; all non-secret evidence is archived.

**Full Konnex-native proof:** intermediate criteria plus an official protocol-visible transaction or PoPW/validator/ScoreRoot record that a third party can resolve.

## Failure / stop conditions

- Any seed/private-key request outside the owner's wallet UI
- RPC, faucet, subnet, binary, schema, costs, or explorer not confirmed by current official material
- No exportable task ID or evidence
- Only illustrative parameters are available
- Real funds, miner/validator registration, or unclear approval becomes necessary
- Evidence would need fabrication or relabeling to appear protocol-native

## Rollback / safety

- Disconnect and revoke site permissions after the run.
- Abandon unsigned payloads; do not retry unexplained failures.
- Never bridge or substitute real assets for test tokens.
- Keep secrets only in the wallet; rotate the test account after any accidental exposure.

## Evidence to save

Create a dated non-secret folder containing screenshots, public URLs/IDs, raw evidence, SHA-256 hashes, Guardian input/output, exact official source links, and tool/release versions. Never commit wallet secrets or private evidence.

## Builder submission value

The intermediate proof shows Guardian binding an official simulator task to deterministic verification. Full proof would demonstrate Guardian sitting between Physical AI evidence and an independently resolvable Konnex result without confusing raw performance with trusted acceptance.

## Product-to-Konnex gap analysis

### NOW

- Normalized deterministic evidence verification
- Hashing, integrity gates, metrics, reason codes, confidence, and receipts
- Fail-closed adapter boundary and synthetic fixtures

### NEXT

- Confirmed live PoPW schema and release-specific adapter
- Genuine JobID binding
- Transaction/protocol receipt binding
- Official validator result or ScoreRoot correlation

### OPTIONAL

- Device/TEE signature verification
- Subnet-specific sensor adapters
- Automated read-only protocol lookup after an official endpoint exists
- Validator-node packaging; not required for the current proof
