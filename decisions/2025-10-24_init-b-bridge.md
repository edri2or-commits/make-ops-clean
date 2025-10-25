# Decision: Close bridge `init-b` with Proof

**Status:** CLOSED (bridge `init-b`)  
**Gate | Integrations (Make/Telegram):** OPEN — proof-only until tokens validated (`token-sanity-check` → expect `make_http_code=200` AND `telegram_ok=true`)  
**When:** 2025-10-24  
**Owner:** [TBD]  
**Commit (log update):** 8e3247f

---

## Summary
DoD met for `init-b`: successful job + artifact + JSON printed.

- **Run URL:** https://github.com/edri2or-commits/make-ops-clean/actions/runs/18785058322  
- **Artifact:** `initb_bridge_proof/webhook_info.json` (artifact id **4364863684**)  
- **JSON head (from logs):**
  {
    "bridge": "init-b",
    "scenario_id": "unknown",
    "timestamp": "2025-10-24T05:53:56Z",
    "runner": "edri2or-commits",
    "run_id": "...",
    "repo": "..."
  }

---

## Root Cause
Invalid YAML in `.github/workflows/init-b-bridge.yml` (broken `curl/-H/| jq .`) blocked runner job creation.

## Fix
Single-file PR replaced the workflow with valid YAML that generates `initb_bridge_proof/webhook_info.json` and uploads the artifact.

## Decisions & Rationale
- **[PR-first + Proof]** Close `init-b` only with artifact + JSON in logs → objective evidence before merge.  
- **[Gate Integrations ACTIVE]** Last sanity check previously returned `401/true` → no “real” runs until credentials/zone/ID validated.  
- **[Authorization header = `Token …`]** Aligns with Make API; avoids 401 due to header format.  
- **[Re-test before rotating token]** Prevents unnecessary token churn.

## DoD (met)
- [x] ≥ 1 job succeeded  
- [x] Artifact `initb_bridge_proof/webhook_info.json` exists  
- [x] First 3–5 JSON lines printed in logs  
- [x] Decision recorded in log (commit **8e3247f**)

## Evidence (first-party)
- **Run:** https://github.com/edri2or-commits/make-ops-clean/actions/runs/18785058322  
- **Artifact:** https://github.com/edri2or-commits/make-ops-clean/actions/runs/18785058322/artifacts/4364863684

## Registry / Gates
- **Integrations Gate (Make/Telegram):** OPEN — operate in **proof-only** mode until `token-sanity-check` reports `make_http_code=200` **and** `telegram_ok=true`.  
- **Next action:** Run `token-sanity-check` (branch `main`) and update this decision + the Gate issue accordingly.

## Next Steps (traceable)
- **T-201** — Run `token-sanity-check` manually (Branch=`main`). **Owner:** [TBD] • **Due:** [TBD]  
- **T-202** — Download `token_check_report/report.json`, record `make_http_code`, `telegram_ok`, `run_url`. **Owner:** [TBD]  
- **T-203** — If `200/true`: update `DECISION_LOG.md` with “Gate CLOSED” line + close Gate issue. **Owner:** [TBD]  
- **T-204** — Else: verify/rotate `MAKE_API_TOKEN`, confirm `MAKE_BASE` (e.g., `eu2`) and `MAKE_SCENARIO_ID`, rerun. **Owner:** [TBD]  
- **T-205** — Archive run URL in this decision (Evidence section). **Owner:** [TBD]

---

## Decision Log — index line
init-b bridge | DoD met (run+artifact+json_head) | run: 18785058322 | artifact: 4364863684 | commit: 8e3247f | gate: integrations-proof-only-until-tokens
