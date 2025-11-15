# GitHub Actions Trigger Issue - Documentation

**Date**: 2025-11-15  
**Status**: UNRESOLVED - Under Investigation  
**Impact**: Workflows created by Claude do not trigger automatically

---

## Summary

Workflows created or modified by Claude via GitHub MCP **do not trigger** via `on: push` or `on: schedule`, despite:
- Correct YAML syntax
- Proper permissions
- Valid trigger paths
- Successful commits

**Evidence**: 7+ workflows created, 0 automatic executions observed over 90+ minutes.

---

## Verified Facts

### ✅ GitHub Actions Works (Repo-Level)
- **999+ workflow runs** in repository (verified by OPS_AGENT)
- Existing workflows execute successfully:
  - `index-append` (scheduled, hourly)
  - `health` (scheduled, weekly + manual)
  - `enable-rube-file-control` (manual)
- **Conclusion**: GitHub Actions infrastructure is OPERATIONAL

### ❌ Claude-Created Workflows Don't Trigger

| Workflow | Trigger Type | Commits | Runs | Status |
|----------|-------------|---------|------|--------|
| `google-mcp-enable-apis.yml` | `on: push` + `paths` | 1 | 0 | Never ran |
| `google-mcp-enable-apis-poller.yml` | `on: schedule` | 1 | 0 | Never ran |
| `heartbeat-verify-schedule.yml` | `on: schedule` | 1 | 0 | Never ran |
| `gcp-enable-google-apis-state.yml` | `on: push` + `paths` | 1 | 0 | Never ran |
| `health.yml` (modified) | `on: push` + job added | 1 | 1 | **RAN but FAILED** |
| `enable-google-apis-direct.yml` | `on: push` + `paths` | 1 | 0 | Never ran |
| `l2-phase1-enable-apis.yml` | `on: push` (self-trigger) | 1 | 0 | Never ran |

**Pattern**: All workflows created/modified by Claude fail to trigger automatically.

---

## Attempted Solutions

### 1. Fixed Missing `branches:` Filter
**Attempt**: Added `branches: [main]` to `on: push` triggers  
**Result**: No change - workflow still didn't run

### 2. State File Triggers
**Attempt**: Created `.ops/state/*.json` files with `paths:` filters  
**Result**: No runs observed

### 3. Schedule-Based Polling
**Attempt**: `on: schedule: cron: '*/5 * * * *'`  
**Result**: No runs after 15+ minutes

### 4. Self-Triggering Workflow
**Attempt**: Workflow watches own file path  
**Result**: No execution on creation

### 5. Adding Job to Existing Workflow
**Attempt**: Modified `health.yml` (known working workflow)  
**Result**: Workflow RAN but FAILED (progress!)

---

## Hypotheses

### Most Likely: Permission/Authorization Issue
- Workflows created via GitHub API/MCP may require additional approval
- GitHub may have security restrictions on auto-executing new workflows
- Service account/PAT may lack workflow execution permissions

### Possible: GitHub Delay
- New workflows may have activation delay (hours/days)
- Schedule triggers often have first-run delay

### Unlikely: Syntax Errors
- YAML validates correctly
- Workflows based on working examples
- One workflow (health.yml) DID execute

---

## What Works

✅ **GitHub MCP Capabilities**:
- Create/edit workflow files
- Commit changes
- Read repository content
- List commits

✅ **Existing Workflows**:
- Execute on schedule
- Execute on manual dispatch
- Have WIF/GCP authentication
- Can commit results

❌ **New Workflow Triggers**:
- `on: push` - not triggering
- `on: schedule` - not triggering
- Self-modification - not triggering

---

## Impact on L2 Phase 1

**Objective**: Enable Google APIs for MCP  
**Blocker**: Cannot automatically execute `gcloud services enable`

**Workaround Path**: Direct execution without GitHub Actions automation  
**Status**: Proceeding with alternative approach

---

## Next Steps

1. **Short-term**: Use manual workflow_dispatch OR direct gcloud execution
2. **Investigation**: Determine why workflows don't auto-trigger
3. **Long-term**: Fix automation OR document as known limitation

---

## Evidence Files

All workflows created:
- `.github/workflows/google-mcp-enable-apis.yml`
- `.github/workflows/google-mcp-enable-apis-poller.yml`
- `.github/workflows/heartbeat-verify-schedule.yml`
- `.github/workflows/gcp-enable-google-apis-state.yml`
- `.github/workflows/enable-google-apis-direct.yml`
- `.github/workflows/l2-phase1-enable-apis.yml`

State files created:
- `.ops/state/enable-google-apis.json`
- `.ops/triggers/google-mcp-enable-apis.flag`
- `.ops/state/enable-apis-trigger.flag`

**Result**: ZERO automated executions across all attempts.
