# STATE FOR GPT – SNAPSHOT (Canonical)

## 1. Repo Overview

- owner/repo: `edri2or-commits/make-ops-clean`
- default_branch: `main`
- visibility: `public`

This repo is the Source of Truth for the MCP/GPT automation system.

## 2. Key Files

- `CAPABILITIES_MATRIX.md`  
  Single source of truth for all MCP / Claude / GPT capabilities and integrations
  (GitHub, Google, GCP, Windows MCP, etc.).

- `MCP_GPT_CAPABILITIES_BRIDGE.md`  
  Bridge between the capabilities matrix and concrete agents (Claude, GPT Agents, Agent Mode).

- `GPT_REPO_ACCESS_BRIDGE.md`  
  Describes how GPT/Agents are expected to access this repo (branches, workflows, policies).

- `STATE_FOR_GPT.md`  
  Legacy high-level state file. The canonical, up-to-date state is now this file:
  `DOCS/STATE_FOR_GPT_SNAPSHOT.md`.

- `DOCS/GPT_TASKS_SPEC.md`  
  Specification for GPT task files (YAML) under `.chatops/gpt_tasks/`.

- `DOCS/GPT_EXECUTOR_TEST.md`  
  Smoke-test file created directly by GPT Agent Mode, committed to `main`
  (commit `1c64fd5`) to prove direct write access.

- `.github/workflows/gpt_tasks_executor.yml`  
  Intended GitHub Actions workflow to execute GPT task YAMLs.

- `.chatops/gpt_tasks/`  
  Folder for GPT tasks in YAML format, e.g.:
  - `gpt-2025-11-15-001-executor-smoke-test.yml`

## 3. GitHub Capabilities Status (High-level)

- **Direct writes via Agent Mode**:  
  - CONFIRMED WORKING – Agent Mode can create and update files on `main`
    (for example `DOCS/GPT_EXECUTOR_TEST.md`, commit `1c64fd5`).

- **Existing GitHub Actions workflows**:  
  - `codeql.yml`, `python-app.yml`, `release.yml`: regular CI/automation flows.
  - `gpt_tasks_executor.yml`: design exists, runtime currently BROKEN (see below).

## 4. GPT Tasks Executor – Design vs Runtime

- **Design:**
  - `DOCS/GPT_TASKS_SPEC.md` defines the format for GPT tasks as YAML.
  - `.chatops/gpt_tasks/gpt-2025-11-15-001-executor-smoke-test.yml` is an example task
    intended to create `DOCS/GPT_EXECUTOR_TEST.md` and optionally open a PR.

- **Runtime (actual behavior today):**
  - The workflow `gpt_tasks_executor.yml` is configured with `workflow_dispatch`
    and triggers on changes in `.chatops/gpt_tasks/*.yml`.
  - Attempts to trigger it from the GitHub UI report
    “Workflow run was successfully requested”, but **no runs actually appear**
    (0 runs in the Actions UI).
  - The task `gpt-2025-11-15-001-executor-smoke-test.yml` did NOT run to completion
    via Actions (no PR created, and the test file was not created by the executor).

- **Workaround in use now:**
  - `DOCS/GPT_EXECUTOR_TEST.md` was created directly by GPT Agent Mode
    via a direct commit to `main` (commit `1c64fd5`),
    without relying on the GPT Tasks Executor workflow.
  - Therefore, the GPT Tasks Executor is currently considered **BROKEN at runtime**.
  - Until it is debugged and fixed, GPT/Agents should assume direct writes to the repo
    (under Or’s approval) are the primary mechanism.

## 5. GPT / Agent Control Model

- **Or (human owner):**
  - Defines high-level intent and goals.
  - Gives explicit “מאשר” / approval before any strong or risky change.
  - Does NOT perform technical actions: no GitHub editing, no commands, no secrets.

- **GPT strategic (MCP מלא):**
  - Designs the autonomy layers, policies and loops.
  - Produces canonical content for state files and specs
    (like this snapshot and future design docs).
  - Coordinates agents and keeps `CAPABILITIES_MATRIX` and state files consistent.

- **Execution Agents (Agent Mode / future GPT Agents / MCP tools):**
  - Hold actual technical access (GitHub write, future Google/GCP/Windows operations).
  - Execute file changes, PRs, and automations **only after** Or’s explicit approval.
  - Must first read state files (`STATE_FOR_GPT_SNAPSHOT`, `CAPABILITIES_MATRIX`, bridges),
    then present a plan, wait for approval, and only then act.

## 6. Known Issues / Backlog

1. **GPT Tasks Executor (GitHub Actions) – Runtime BROKEN**
   - Needs systematic debugging of `gpt_tasks_executor.yml` and GitHub Actions state
     to understand why `workflow_dispatch` creates no runs.
   - Until fixed, no agent should rely on the YAML→Executor loop.

2. **Alignment between CAPABILITIES_MATRIX and this snapshot**
   - For every capability/integration listed in the matrix,
     the corresponding status should either be reflected here,
     or this file should explicitly point to the matrix as the full source.

3. **Future GPT-Agent service**
   - This snapshot is the basis for a future standalone GPT-Agent (Cloud Run or similar)
     that will orchestrate GitHub, Google, GCP and Windows MCP using the same model:
     Or = intent + approval, agents = execution.
