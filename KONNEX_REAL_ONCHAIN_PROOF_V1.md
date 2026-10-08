# Pulse PoPW Guardian — Real Konnex On-chain Job Anchor

**Classification:** `REAL_KONNEX_ONCHAIN_JOB_ANCHOR`

`Official drone request → owner signature → Konnex Testnet extrinsic → unique Konnex job anchor → Guardian evidence binding`

## Verified anchor

- Block/extrinsic: `1,223,966 / 1`
- Signer: `5ERMCLtnV1k6Zsfrv6oNajnX2eNoS3pLevHBsNTr4SwhwqpW`
- Nonce: `29`
- Block hash: `0x19888ed06a97247117edffc03c5f527311a25e0870b4b09e1c6baf298fdb8257`
- Extrinsic hash: `0xd040f04905943078c20608267343f4fcf7cbfd6961fdebc121f096380aa8c035`
- Payload: `konnex-job:v1:4:0xc7705715657ab1dbde65c163678ac359bc4cead3f20eea38cb13a6319158a051`
- Job anchor: `0xc7705715657ab1dbde65c163678ac359bc4cead3f20eea38cb13a6319158a051`

The match was recovered by scanning the reported block window through read-only JSON-RPC and matching the signed extrinsic by signer plus nonce. The canonical JSON preserves the block hash, call bytes, and raw extrinsic.

## Guardian binding

Guardian can bind a future physical-evidence bundle and deterministic receipt to this exact job anchor. The anchor establishes real Konnex provenance; it does not supply telemetry, video, or other physical-work evidence.

## Remaining boundary

Physical evidence verification awaits an official evidence bundle. Protocol-visible validator result and ScoreRoot correlation are not confirmed. This is not classified as complete PoPW or validator-accepted proof.
