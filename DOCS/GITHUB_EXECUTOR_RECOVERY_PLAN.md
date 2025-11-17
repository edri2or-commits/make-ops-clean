# GitHub Executor Recovery Plan

**Phase**: 2 (Task 2.2 OR-APPROVED, Task 2.3a PLANNED, Task 2.3 DESIGN_READY)  
**Date Created**: 2025-11-17  
**Last Updated**: 2025-11-17  
**Status**: ✅ Task 2.2 OR-APPROVED | ⏳ Task 2.3a PR pending | 🔐 Task 2.3 BLOCKED_PENDING_EXECUTOR

---

## 🎯 Executive Summary

**Goal**: Fix the GPTs GO → GitHub integration loop by recovering the `github-executor-api` service.

**Current State**:
- Service code exists with 2 known bugs (both OS_SAFE fixes ready)
- **Runtime status UNKNOWN** (Observability Constraint)
- GPTs GO reports 404 on `/github/update-file`
- **Deployment plan complete** but execution blocked pending Executor

**Blocking Factors**:
- ⏳ PR merges (Or can approve, Executor needed for merge action)
- 🔐 Secrets/Deploy (requires Executor with repo settings / GCP access)

**Approach**: Fix code (2.2 + 2.3a) → Deploy when Executor available (2.3) → Test → Document

---

## 📋 Phase 2 Tasks - Status Table

| Task | Status | Risk | Description | Blocker |
|------|--------|------|-------------|---------|
| 2.1 | ✅ CLOSED | LOW | Verify deployment | Observability constraint (closed as UNVERIFIED) |
| 2.2 | ✅ OR-APPROVED | NONE | Fix Accept header | PR #100 awaits merge (EXECUTOR needed) |
| 2.3a | ⏳ PLANNED | NONE | Fix Dockerfile CMD | Will open PR (OS_SAFE) |
| 2.3 | 🔐 DESIGN_READY | HIGH | Deploy service | EXECUTOR + Secrets + Or approval |
| 2.4-2.7 | ⏳ PENDING | VARIES | Post-deploy tasks | Blocked on 2.3 execution |

---

## 📋 Detailed Task Status

### Task 2.1: Verify Deployment Status ✅ COMPLETED (RUNTIME_UNVERIFIED)

**Outcome**: COMPLETED – RUNTIME_UNVERIFIED (OBSERVABILITY_CONSTRAINT)

**Evidence**: 
- Workflow design: `.github/workflows/verify-github-executor-api.yml`
- Documentation: `CAPABILITIES_MATRIX.md` Section 8.5, Section 10.2
- Closure: `DOCS/STATE_FOR_GPT_SNAPSHOT.md` v3.1

---

### Task 2.2: Fix Accept Header Typo ✅ OR-APPROVED (OS_SAFE)

**Status**: **PR_OPENED (AWAITING_MERGE_FROM_EXECUTOR)**

**Approval**: ✅ **Or has approved the content of this fix** (2025-11-17)

**PR Details**:
- **URL**: https://github.com/edri2or-commits/make-ops-clean/pull/100
- **Branch**: `feature/fix-github-executor-accept-header`
- **Commit**: `ceb6a6d`
- **Change**: `vund.github` → `vnd.github` (line 37, index.js)
- **Risk**: NONE (OS_SAFE - code change only, no deployment)

**Next Step**: 
- Merge action itself = **requires Executor with repo write access**
- Or does NOT click merge buttons (per Or-OS contract)
- Claude cannot merge PRs (no GitHub API permission)

**Note**: Or has given **conceptual approval** to the fix content, not performing merge action

---

### Task 2.3a: Fix Dockerfile CMD Typo ⏳ PLANNED (OS_SAFE)

**Purpose**: Fix critical bug that prevents container from starting

**Bug Details**:
- File: `cloud-run/google-workspace-github-api/Dockerfile`
- Line: 11
- Current (broken): `CLM ["npm", "start"]`
- Fixed: `CMD ["npm", "start"]`

**Impact**: Without this fix, container won't start at all

**Approach** (as approved by Or):
- ✅ Separate PR (not added to #100)
- Branch: `fix/github-executor-dockerfile-cmd`
- Single-line change + optional inline comment
- New PR (will be #101 or similar)

**Status**: ⏳ PLANNED (Claude will open PR next)

**Risk**: NONE (OS_SAFE - Dockerfile edit, no deployment triggered)

**Approval**: ✅ Or has approved this approach (2025-11-17)

---

### Task 2.3: Deploy Service 🔐 DESIGN_READY (EXECUTION_BLOCKED_PENDING_EXECUTOR)

**Purpose**: Deploy github-executor-api to Cloud Run with fixed code

**📄 Complete Deployment Plan**: **[`DOCS/TASK_2.3_DEPLOYMENT_PLAN.md`](TASK_2.3_DEPLOYMENT_PLAN.md)** (16.8KB)

**Plan Status**: ✅ **DESIGN_READY** (comprehensive plan exists)

**Execution Status**: 🔐 **BLOCKED_PENDING_EXECUTOR**

**Why Blocked**:

This task requires capabilities Claude does NOT have:

1. **Secrets Management** (CLOUD_OPS_HIGH):
   - Adding `GITHUB_TOKEN` to GitHub repository secrets
   - Verifying secret exists and is accessible
   - Or will NOT "add a secret" manually (per Or-OS contract)
   - **Requires**: Executor with repo settings access

2. **Deployment Execution** (CLOUD_OPS_HIGH):
   - Triggering Cloud Build
   - Deploying to Cloud Run
   - Configuring service environment variables
   - **Requires**: Executor with GCP access OR GitHub Actions with proper WIF

3. **Explicit Approval** (STRATEGIC):
   - Or's explicit "GO" for production deployment
   - **Not requested at this time** (waiting for Executor first)

**Claude's Constraint**:
```
Claude CANNOT:
- Check if GITHUB_TOKEN secret exists ❌
- Add secrets to GitHub ❌
- Verify secret configuration ❌
- Execute gcloud commands directly ❌
- Deploy to Cloud Run ❌

Claude CAN:
- Design deployment plans ✅
- Create workflow YAML files ✅
- Document requirements ✅
- Write PRs for code fixes ✅
```

**Requirements for Unblocking**:

Before Task 2.3 can execute, need:
1. ✅ Task 2.2 (PR #100) merged
2. ✅ Task 2.3a (Dockerfile fix) merged
3. 🔐 **Executor** (human/system) with:
   - GitHub repository settings access
   - GCP project access (`edri2or-mcp`)
   - Ability to create/verify secrets
   - Or's authorization to act
4. 🔐 Or's explicit approval for CLOUD_OPS_HIGH deployment
5. 🔐 Secret `GITHUB_TOKEN` configured in repository

**Current State**: 
- Plan: ✅ COMPLETE
- Code fixes: ⏳ IN PROGRESS (PRs 100, 101)
- Execution: 🔐 AWAITING EXECUTOR

**Note**: Or is NOT the Executor for DevOps tasks (per Or-OS contract)

---

### Tasks 2.4-2.7: Post-Deployment ⏳ PENDING

All blocked on Task 2.3 execution:

- **2.4**: Verify environment variables
- **2.5**: Test service endpoint
- **2.6**: Configure GPTs GO
- **2.7**: Update documentation

---

## 🔄 Execution Flow (Updated with Executor Model)

```
Phase 2.1: Verify ✅ CLOSED (RUNTIME_UNVERIFIED)
    │
Phase 2.2: Fix Accept Header ✅ OR-APPROVED (OS_SAFE)
    │
    ├─ PR #100 opened by Claude
    ├─ Or approves content ✅
    └─ Merge requires: EXECUTOR with repo access
    │
Phase 2.3a: Fix Dockerfile ⏳ NEXT (OS_SAFE)
    │
    ├─ PR to be opened by Claude
    ├─ Or approves content (expected)
    └─ Merge requires: EXECUTOR with repo access
    │
Phase 2.3: Deploy Service 🔐 BLOCKED
    │
    ├─ Plan: ✅ COMPLETE (DESIGN_READY)
    │
    ├─ Execution requires:
    │  ├─ EXECUTOR with GitHub + GCP access
    │  ├─ Secrets configured (GITHUB_TOKEN)
    │  └─ Or's explicit GO for production deploy
    │
    └─ Current status: WAITING FOR EXECUTOR
    │
Phase 2.4-2.7: Post-Deploy ⏳ PENDING (blocked on 2.3)
```

---

## 🔐 Executor Model - Clear Boundaries

**Or's Role** (Intent + Strategic Approval):
- ✅ Approves/rejects plans conceptually
- ✅ Gives "GO" for CLOUD_OPS_HIGH operations
- ✅ Defines objectives and boundaries
- ❌ Does NOT click merge buttons
- ❌ Does NOT add secrets manually
- ❌ Does NOT open consoles (GitHub/GCP)
- ❌ Does NOT run commands

**Claude's Role** (Planner + OS_SAFE Executor):
- ✅ Creates comprehensive plans
- ✅ Opens PRs for code fixes
- ✅ Designs workflows and automation
- ✅ Updates documentation
- ❌ Cannot merge PRs (no GitHub permission)
- ❌ Cannot add/verify secrets (no repo access)
- ❌ Cannot deploy to Cloud Run (no direct GCP access)

**Executor's Role** (CLOUD_OPS_HIGH Actions):
- ✅ Merges approved PRs
- ✅ Adds/verifies repository secrets
- ✅ Triggers deployments (with Or's GO)
- ✅ Configures cloud resources
- ✅ Has access to GitHub settings + GCP console
- ⏳ **Currently**: Not yet identified/assigned

---

## 📊 Current Bottleneck Analysis

**What's Ready**:
- ✅ PR #100 (Accept header fix) - Or-approved, awaiting merge
- ✅ Task 2.3a (Dockerfile fix) - Ready to PR
- ✅ Deployment plan (16.8KB comprehensive document)

**What's Blocked**:
- 🔐 PR merges (need Executor)
- 🔐 Secrets configuration (need Executor)
- 🔐 Deployment execution (need Executor + Or's GO)

**Path Forward**:
1. Claude opens PR for Dockerfile fix (Task 2.3a) - OS_SAFE ✅
2. Identify/assign Executor with required access
3. Executor merges PRs #100 and #101 (with Or's conceptual approval)
4. Executor configures secrets (GITHUB_TOKEN)
5. Or reviews final plan → gives explicit GO
6. Executor triggers deployment
7. Claude continues with testing/documentation (Tasks 2.4-2.7)

---

## 🔄 Updates Log

### 2025-11-17 - Or-OS Boundaries Clarified
- **Model**: Or = Intent only, NOT DevOps executor
- **Task 2.2**: Status → OR-APPROVED (content), merge awaits EXECUTOR
- **Task 2.3a**: Approved for separate PR approach
- **Task 2.3**: Status → DESIGN_READY, execution BLOCKED_PENDING_EXECUTOR
- **Executor**: Role defined, not yet assigned

### 2025-11-17 - Task 2.3 PLAN Complete
- Document: `TASK_2.3_DEPLOYMENT_PLAN.md` (16.8KB)
- Discovery: Dockerfile bug (CLM → CMD)
- Status: DESIGN_READY, awaiting Executor for execution

### 2025-11-17 - Task 2.2 Started
- PR #100 opened
- Or's conceptual approval received
- Merge action awaits Executor

---

## 📊 Status Summary

**OS_SAFE Complete**:
- ✅ Task 2.1: Documented constraint
- ✅ Task 2.2: PR opened, Or-approved (content)
- ✅ Task 2.3 PLAN: Comprehensive design
- ⏳ Task 2.3a: Will open PR next

**CLOUD_OPS_HIGH Blocked**:
- 🔐 PR merges: Need Executor
- 🔐 Secrets: Need Executor
- 🔐 Deploy: Need Executor + Or's GO

**Next OS_SAFE Action**: Claude opens Dockerfile fix PR (Task 2.3a)

---

**Status**: ✅ Code fixes ready (2.2 OR-APPROVED, 2.3a PLANNED) | 🔐 Execution BLOCKED_PENDING_EXECUTOR

**Immediate Next**: Claude creates Task 2.3a PR (Dockerfile CMD fix)
