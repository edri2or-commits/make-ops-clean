# GitHub Executor Recovery Plan

**Phase**: 2 (Task 2.2 OR-APPROVED, Task 2.3a PR_OPENED, Task 2.3 DESIGN_READY)  
**Date Created**: 2025-11-17  
**Last Updated**: 2025-11-17  
**Status**: ✅ PRs #100, #101 opened | 🔐 Deployment BLOCKED_PENDING_EXECUTOR

---

## 🎯 Executive Summary

**Goal**: Fix the GPTs GO → GitHub integration loop by recovering the `github-executor-api` service.

**Current State**:
- ✅ Code fixes ready: PR #100 (Accept header), PR #101 (Dockerfile CMD)
- ✅ Deployment plan complete: TASK_2.3_DEPLOYMENT_PLAN.md
- 🔐 Execution blocked: Awaits Executor for merges/secrets/deploy

**Blocking Factors**:
- ⏳ PR merges → Need Executor with repo access
- 🔐 Secrets/Deploy → Need Executor with GCP access + Or's GO

---

## 📋 Phase 2 Tasks - Status Table

| Task | Status | Risk | Next Step |
|------|--------|------|-----------|
| 2.1 | ✅ CLOSED | LOW | Observability constraint documented |
| 2.2 | ✅ OR-APPROVED | NONE | PR #100 awaits Executor merge |
| 2.3a | ✅ PR_OPENED | NONE | PR #101 awaits Or approval |
| 2.3 | 🔐 DESIGN_READY | HIGH | Awaits Executor + Or GO |
| 2.4-2.7 | ⏳ PENDING | VARIES | Blocked on 2.3 execution |

---

## 📋 Detailed Task Status

### Task 2.2: Fix Accept Header ✅ OR-APPROVED

**PR**: [#100](https://github.com/edri2or-commits/make-ops-clean/pull/100)  
**Status**: ✅ Or approved content | ⏳ Awaits Executor merge  
**Change**: `vund.github` → `vnd.github`

---

### Task 2.3a: Fix Dockerfile CMD ✅ PR_OPENED

**PR**: [#101](https://github.com/edri2or-commits/make-ops-clean/pull/101)  
**Status**: ⏳ Awaiting Or's content approval  
**Change**: `CLM` → `CMD` (critical for container start)  
**Impact**: Container won't start without this fix

---

### Task 2.3: Deploy Service 🔐 DESIGN_READY (BLOCKED_PENDING_EXECUTOR)

**Plan**: [`TASK_2.3_DEPLOYMENT_PLAN.md`](TASK_2.3_DEPLOYMENT_PLAN.md) (16.8KB)

**Why Blocked**:
- 🔐 Secrets (GITHUB_TOKEN) → Need Executor with repo settings access
- 🔐 Deploy to Cloud Run → Need Executor with GCP access
- 🔐 Or's explicit GO → Strategic approval for production deploy

**Requirements to Unblock**:
1. ✅ PR #100, #101 merged (via Executor)
2. 🔐 Executor with GitHub + GCP access identified
3. 🔐 Secrets configured
4. 🔐 Or gives explicit GO

---

## 🔐 Executor Model

**Or** = Intent + Strategic Approval  
**Claude** = Planner + OS_SAFE Executor  
**Executor** = CLOUD_OPS_HIGH Actions (TBD)

---

## 📊 Status Summary

**OS_SAFE Complete**:
- ✅ Task 2.2: PR #100 (Or-approved)
- ✅ Task 2.3a: PR #101 (opened)
- ✅ Task 2.3 PLAN: Comprehensive design

**CLOUD_OPS_HIGH Blocked**:
- 🔐 PR merges
- 🔐 Secrets configuration
- 🔐 Deployment execution

---

**Current Status**: ✅ All OS_SAFE work complete | 🔐 CLOUD_OPS_HIGH awaits Executor

**Next**: Executor merges PRs → configures secrets → Or gives GO → deployment
