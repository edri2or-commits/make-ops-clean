# Decision Log – init-b bridge proof fix (2025-10-24)

## Context
The init-b bridge workflow was failing before the runner started due to invalid YAML syntax in `.github/workflows/init-b-bridge.yml` (broken curl line). This prevented any jobs from running and disabled the `workflow_dispatch` run button【137324009814540†L40-L47】【393331820324565†L153-L178】.

## Sources and Evidence
- Workflow file raw: showed mis‑indented curl lines causing YAML parse error【137324009814540†L40-L47】.
- GitHub Actions run summaries: reported "Invalid workflow file" errors with no jobs【393331820324565†L153-L178】.
- Actions settings: repository allows all actions but `GITHUB_TOKEN` is read‑only【919239060807350†screenshot】.
- Secrets & variables: `MAKE_API_TOKEN` and `TELEGRAM_BOT_TOKEN` exist, others missing【913381093250319†L166-L214】【57866600911459†L158-L168】.
- Registry: `.chatops/registry.v1.json` defines scenario_id for `init.b`【105384134904972†L174-L190】.

## Decision
Fix the broken YAML by rewriting `.github/workflows/init-b-bridge.yml` with valid syntax, retaining `push: branches: ["main"]` and `workflow_dispatch` triggers, adding an artifact upload step, and providing a fallback `env`. Open PR to main for review. After merge, run the workflow to produce `initb_bridge_proof/webhook_info.json`.

## DoD
1. At least one job runs successfully.
2. Artifact `initb_bridge_proof/webhook_info.json` is generated.
3. The JSON file's first lines are printed in logs.
4. No changes to repository policies or secret values.
5. Decision log recorded in repo.

## Alternatives Considered
- Running workflow on branch via `workflow_dispatch`: not possible because the invalid YAML on main disables the run button.
- Changing repository actions settings: unnecessary; problem caused by syntax error.
init-b bridge | DoD met (run+artifact+json_head) | run: 18785058322 | artifact: 4364863684 | commit: 8e3247f | gate: integrations-proof-only-until-tokens
integrations gate | OPEN (fix required) | make_http_code=401 | telegram_ok=true | action: update Make token/scopes/region and re-run token-sanity-check | run:[TBD] | artifact: token_check_report/report.json