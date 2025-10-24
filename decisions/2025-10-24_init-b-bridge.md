# Decision: Close bridge `init-b` with Proof

## Summary
DoD met: successful job + artifact + JSON printed.

- Run URL: https://github.com/edri2or-commits/make-ops-clean/actions/runs/18785058322
- Artifact: initb_bridge_proof/webhook_info.json (artifact id 4364863684)
- Commit (log update): 8e3247f
- JSON head (from logs):
  {
    "bridge": "init-b",
    "scenario_id": "unknown",
    "timestamp": "2025-10-24T05:53:56Z",
    "runner": "edri2or-commits",
    ...
  }

## Root Cause
Invalid YAML in `.github/workflows/init-b-bridge.yml` (broken `curl/-H/| jq .`) blocked runner creation.

## Fix
Single-file PR replaced the workflow with valid YAML that generates `initb_bridge_proof/webhook_info.json` and uploads the artifact.

## DoD (met)
- [x] ≥1 job succeeded
- [x] Artifact `initb_bridge_proof/webhook_info.json` exists
- [x] First 3–5 JSON lines printed in logs
- [x] Decision log recorded

## Evidence (first-party)
- Run: https://github.com/edri2or-commits/make-ops-clean/actions/runs/18785058322
- Artifact: https://github.com/edri2or-commits/make-ops-clean/actions/runs/18785058322/artifacts/4364863684

## Registry/Gates
Integrations run **proof-only** until tokens validated (Make/Telegram).

## Decision Log line (index)
init-b bridge | DoD met (run+artifact+json_head) | run: 18785058322 | artifact: 4364863684 | commit: 8e3247f | gate: integrations-proof-only-until-tokens