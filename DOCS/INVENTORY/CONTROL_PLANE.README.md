# Control Plane — Inventory & Dispatch (Snapshot)

**Repo:** `edri2or-commits/make-ops-clean`  
**Default branch:** `main`  
**Snapshot:** 2025-11-05T19:22:10Z  

## TL;DR
- **Workflows in `.github/workflows/`: 39**  
- **Dispatchable:** 39/39 (standardized)  
- **OIDC usage:** 2 workflows (`permissions: id-token: write`)  
- **Detected integrations:** `make.com`, `telegram`, `composio`, `mcp`  
- **Status:** All workflows support standardized dispatch (see snippet below)

## Standardized dispatch pattern
```yaml
on:
  workflow_dispatch:
    inputs:
      reason:
        description: "Why run"
        required: false
        default: "ops"
  repository_dispatch:
    types: [ops_run]
permissions:
  contents: read
jobs:
  <first-job>:
    concurrency:
      group: "<workflow-name>"
      cancel-in-progress: true

How to trigger (API)
	•	workflow_dispatch
POST /repos/{owner}/{repo}/actions/workflows/<file>.yml/dispatches
body: { "ref": "main", "inputs": { "reason": "ops" } }
	•	repository_dispatch
POST /repos/{owner}/{repo}/dispatches
body: { "event_type": "ops_run", "client_payload": { "reason": "ops" } }

Inventory Index
	•	ACTIONS.workflows.md
	•	ACTIONS.settings.json
	•	SECRETS.index.md
	•	INTEGRATIONS.discovery.md
	•	POLICY.snapshot.json
	•	NEXT-STEPS.md

Source of truth lives in this repo; updates should land via PRs.
```
