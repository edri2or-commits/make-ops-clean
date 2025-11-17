# GitHub Executor Recovery Plan

**Phase**: 2 (Task 2.1 CLOSED, Task 2.2 IN PROGRESS, Task 2.3 PLAN COMPLETE)  
**Date Created**: 2025-11-17  
**Status**: 🔄 Task 2.2 PR #100 awaiting review | ✅ Task 2.3 PLAN complete  
**Risk Level**: CLOUD_OPS_HIGH (for deployment tasks)

---

## 🎯 Executive Summary

**Goal**: Fix the GPTs GO → GitHub integration loop by recovering the `github-executor-api` service.

**Current State**:
- Service code exists in `cloud-run/google-workspace-github-api/`
- **Runtime status UNKNOWN** (Observability Constraint documented)
- GPTs GO reports 404 on `/github/update-file`
- BUS system not implemented (DEFERRED - approved by Or)
- **Code fix in progress**: PR #100 fixes Accept header typo
- **Deployment plan complete**: TASK_2.3_DEPLOYMENT_PLAN.md created

**Target State**:
- `github-executor-api` deployed and operational
- GPTs GO can successfully call `/github/update-file`
- Commits appear in GitHub repositories
- CAPABILITIES_MATRIX updated with ✅ Verified status
- **BUS decision: DEFERRED** ✅

**Approach**: Fix code (Task 2.2) → Deploy from scratch (Task 2.3) → Test → Document

---

## 📋 Phase 2 Tasks - Quick Reference

| Task | Status | Description | Document |
|------|--------|-------------|----------|
| 2.1 | ✅ CLOSED | Verify deployment | Observability constraint |
| 2.2 | 🔄 IN PROGRESS | Fix Accept header | PR #100 |
| 2.3 | ✅ PLAN COMPLETE | Deploy service | [`TASK_2.3_DEPLOYMENT_PLAN.md`](TASK_2.3_DEPLOYMENT_PLAN.md) |
| 2.4 | ⏳ PENDING | Verify env vars | Part of 2.3 execution |
| 2.5 | ⏳ PENDING | Test endpoint | Separate workflow |
| 2.6 | ⏳ PENDING | Configure GPTs GO | Needs Or's guidance |
| 2.7 | ⏳ PENDING | Update docs | After all tests pass |

---

## 📋 Detailed Task Status

### Task 2.1: Verify Deployment Status ✅ COMPLETED (RUNTIME_UNVERIFIED)

**Outcome**: COMPLETED – RUNTIME_UNVERIFIED (OBSERVABILITY_CONSTRAINT)

**Evidence**: 
- Workflow design: `.github/workflows/verify-github-executor-api.yml`
- Documentation: `CAPABILITIES_MATRIX.md` Section 8.5, Section 10.2

---

### Task 2.2: Fix Accept Header Typo 🔄 IN PROGRESS (OS_SAFE)

**PR Details**:
- **URL**: https://github.com/edri2or-commits/make-ops-clean/pull/100
- **Commit**: `ceb6a6d`
- **Changes**: 1 file, 1 line changed (`vund` → `vnd`)

**Status**: ⏳ AWAITING OR'S MERGE APPROVAL

---

### Task 2.3: Deploy Service ✅ PLAN COMPLETE → ⏳ AWAITING APPROVAL (CLOUD_OPS_HIGH)

**Purpose**: Deploy github-executor-api to Cloud Run with fixed code

**📄 Complete Deployment Plan**: **[`DOCS/TASK_2.3_DEPLOYMENT_PLAN.md`](TASK_2.3_DEPLOYMENT_PLAN.md)** ⭐

**Plan Components** (all OS_SAFE planning):
1. ✅ **2.3.1: Dockerfile Fix** - Critical bug found: `CLM` → `CMD` (line 11)
2. ✅ **2.3.2: Deployment Workflow** - Full GitHub Actions workflow with WIF auth
3. ✅ **2.3.3: Environment Variables** - `GITHUB_TOKEN` configuration strategy
4. ✅ **2.3.4: Smoke Tests** - Automated health check verification
5. ✅ **2.3.5: Rollback Strategy** - Multiple rollback methods documented

**Key Findings**:
- ⚠️ **New bug discovered**: Dockerfile has `CLM` instead of `CMD` (prevents container start)
- ✅ Existing `cloudbuild.yaml` ready to use
- ✅ Deployment workflow designed with zero-touch automation
- ✅ Status reporting to `OPS/STATUS/*.json` included

**Decision Points for Or**:
1. **Dockerfile fix approach**:
   - Option A: Add to PR #100 (delays merge)
   - Option B: Separate quick fix after #100 merge
   - **Recommendation**: Option B (faster, decoupled)

2. **GitHub Token setup**:
   - Add `GITHUB_TOKEN` to GitHub repository secrets
   - **Recommendation**: Do now to avoid deployment delays

3. **Deployment timing**:
   - Deploy immediately after Task 2.2 merge
   - Wait for Or's explicit "GO" command
   - **Recommendation**: Wait for explicit GO

**Pre-Execution Checklist** (before CLOUD_OPS_HIGH execution):
- [ ] Task 2.2 (PR #100) merged
- [ ] Dockerfile typo fixed (CLM → CMD)
- [ ] Deployment workflow created (`.github/workflows/deploy-github-executor-api.yml`)
- [ ] `GITHUB_TOKEN` added to GitHub Secrets
- [ ] Or has reviewed `TASK_2.3_DEPLOYMENT_PLAN.md`
- [ ] Or has explicitly approved CLOUD_OPS_HIGH execution

**Current Status**:
- Plan Status: ✅ COMPLETE (16.8KB, comprehensive)
- Plan Created: 2025-11-17
- Approval Status: ⏳ AWAITING OR'S REVIEW
- Execution Status: ⏳ NOT STARTED (waiting for approval)

**Risk Assessment**:
- Planning: NONE (OS_SAFE, already complete)
- Execution: MEDIUM (Cloud Run deployment with automated rollback)

**Note**: Actual deployment (CLOUD_OPS_HIGH) requires separate explicit approval

---

### Task 2.4-2.7: Post-Deployment Tasks ⏳ PENDING

**Task 2.4**: Verify Environment Variables  
**Task 2.5**: Test Service Endpoint  
**Task 2.6**: Update GPTs GO Configuration  
**Task 2.7**: Update Documentation  

**Status**: All pending Task 2.3 execution

---

## 🔄 Execution Flow

```
Phase 2.1: Verify ✅ CLOSED (RUNTIME_UNVERIFIED)
    │
Phase 2.2: Fix Accept Header 🔄 IN PROGRESS (PR #100)
    │
    └─ Or reviews PR #100 → Merge
    │
Phase 2.3: Deployment ✅ PLAN COMPLETE
    │
    ├─ Planning (OS_SAFE) ✅ DONE
    │  └─ Document: TASK_2.3_DEPLOYMENT_PLAN.md
    │
    └─ Execution (CLOUD_OPS_HIGH) ⏳ AWAITING APPROVAL
       │
       ├─ Or reviews plan
       ├─ Or approves CLOUD_OPS_HIGH
       └─ Claude triggers deployment
    │
Phase 2.4-2.7: Test, Configure, Document ⏳ PENDING
```

---

## 🔄 Updates Log

### 2025-11-17 - Task 2.3 PLAN Complete
- **Status**: PLAN COMPLETE (OS_SAFE)
- **Document**: `DOCS/TASK_2.3_DEPLOYMENT_PLAN.md` created (16.8KB)
- **Discovery**: Dockerfile bug found (CLM → CMD)
- **Components**: 5 sub-tasks fully planned
- **Next**: Or reviews plan → Approves CLOUD_OPS_HIGH execution

### 2025-11-17 - Task 2.2 Started (PR Opened)
- **Status**: IN PROGRESS
- **PR**: #100 opened
- **Change**: Fixed Accept header typo (`vund` → `vnd`)
- **Next**: Awaiting Or's review and merge

### 2025-11-17 - Task 2.1 Closed (RUNTIME_UNVERIFIED)
- **Status**: COMPLETED with Observability Constraint
- **Lesson**: Observability gap documented for future

### 2025-11-17 - BUS Decision Approved
- **BUS Status**: DEFERRED (Option A)
- **Approved by**: Or

---

## 📊 Current State Summary

**Completed**:
- ✅ Task 2.1: Observability constraint documented
- ✅ Task 2.3 PLAN: Comprehensive deployment plan created

**In Progress**:
- 🔄 Task 2.2: PR #100 awaiting Or's review

**Awaiting Approval**:
- ⏳ Task 2.3 EXECUTION: Deployment plan awaiting Or's approval

**Blocked On**:
- Task 2.2 merge → Unblocks Dockerfile fix
- Or's approval → Unblocks Task 2.3 execution
- Task 2.3 execution → Unblocks Tasks 2.4-2.7

---

**Status**: 🔄 Task 2.2 (PR #100) + ✅ Task 2.3 PLAN complete | ⏳ Awaiting Or's review & approval

**Next Actions**:
1. **Or**: Review PR #100 → Merge
2. **Or**: Review TASK_2.3_DEPLOYMENT_PLAN.md
3. **Or**: Approve CLOUD_OPS_HIGH execution (if satisfied with plan)
4. **Claude**: Execute deployment when approved
