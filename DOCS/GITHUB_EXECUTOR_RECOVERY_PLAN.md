# GitHub Executor Recovery Plan

**Phase**: 2 (Task 2.1 CLOSED, Task 2.2 IN PROGRESS - PR OPENED)  
**Date Created**: 2025-11-17  
**Status**: 🔄 Task 2.2 IN PROGRESS - PR #100 awaiting review  
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

**Target State**:
- `github-executor-api` deployed and operational
- GPTs GO can successfully call `/github/update-file`
- Commits appear in GitHub repositories
- CAPABILITIES_MATRIX updated with ✅ Verified status
- **BUS decision: DEFERRED** ✅

**Approach**: Fix code (Task 2.2) → Deploy from scratch (Task 2.3) → Test → Document

---

## ⚠️ CRITICAL: Zero-Touch Execution Protocol

**Or-OS Contract Compliance**:

✅ **ALLOWED**:
- Workflows run automatically on trigger file changes
- Workflows write status to `OPS/STATUS/*.json` and `*.md` files
- Claude reads status files from repo
- Claude updates trigger files to re-run workflows

❌ **FORBIDDEN**:
- Or manually running workflows via UI
- Or checking Actions tab for status
- Or clicking "Run workflow" buttons
- Or opening any cloud consoles

**Status Observation Method**:
```
Workflow → writes status → OPS/STATUS/*.json
                          ↓
                    Claude reads file
                          ↓
                    Claude reports to Or
```

**All workflows must**:
1. Write status to `OPS/STATUS/[task-name].json`
2. Include: timestamp, status, results, next_step, workflow_url
3. Commit with `[skip ci]` to avoid infinite loops
4. Use `contents: write` permission

**Current Limitation**: Observability gap prevents runtime verification  
**Future Requirement**: Executor with Actions/Cloud Run access OR improved CI permissions

---

## 📊 Current Situation (From Phase 1.1 Diagnosis)

### What We Know ✅

1. **ONE service exists** (not two):
   - Code: `cloud-run/google-workspace-github-api/`
   - Deployed name: `github-executor-api`
   - Region: `us-central1`, Project: `edri2or-mcp`

2. **Implemented endpoints**:
   - `GET /` - Health check
   - `POST /github/update-file` - GitHub file operations

3. **Known issues**:
   - Code typo: `vund.github` → should be `vnd.github` (line 37) **[FIX IN PROGRESS]**
   - GPTs GO gets 404 on `/github/update-file`

4. **BUS status**:
   - NOT implemented in code
   - Exists only in documentation
   - DEFERRED to future phase (approved 2025-11-17)

### What We DON'T Know ❓

1. Is `github-executor-api` deployed?
2. What's the public URL?
3. Is `GITHUB_TOKEN` environment variable set?
4. Why does GPTs GO receive 404?

**Reason**: Observability Constraint (no Actions API access, no status files created)

---

## 🎯 Phase 2 Goals

### Primary Goal
**Fix GPTs GO → github-executor-api → GitHub loop**

Success criteria:
1. Service is deployed and reachable
2. Health check (`GET /`) returns 200
3. `/github/update-file` accepts requests from GPTs GO
4. Test commit appears in a GitHub repository
5. CAPABILITIES_MATRIX updated to ✅ Verified

### BUS Decision ✅ APPROVED BY OR

**Decision**: **DEFERRED (Option A)**

**Status**: Deferred to future phase  
**Decision Owner**: Or (approved 2025-11-17)  
**Rationale**:
- Core GitHub operations work without BUS
- BUS adds complexity without immediate benefit
- Can be revisited if async queue becomes necessary

**Documentation Updated**: 
- CAPABILITIES_MATRIX Section 10.3: BUS marked as "Deferred"
- STATE_FOR_GPT_SNAPSHOT: BUS status = Deferred

---

## 📋 Phase 2 Tasks

### Task 2.1: Verify Deployment Status ✅ COMPLETED (RUNTIME_UNVERIFIED)

**Purpose**: Determine if service is deployed and get its URL

**Method**: GitHub Actions workflow (fully automated, zero-touch)

**What Was Accomplished**:
1. ✅ Workflow created: `.github/workflows/verify-github-executor-api.yml`
2. ✅ Trigger mechanism established: `OPS/TRIGGERS/github-executor-verify.trigger`
3. ✅ Zero-touch pattern documented (workflows write to `OPS/STATUS/*.json`)
4. ✅ Workflow triggered automatically (commits `cd7b467`, `8d39cbee`)

**What Could NOT Be Verified**:
- ❌ Runtime deployment status (workflow may have run but no status files created)
- ❌ Service URL
- ❌ Environment variables
- ❌ Whether service is actually deployed

**Root Cause**: **Observability Constraint**

**Outcome**: **COMPLETED – RUNTIME_UNVERIFIED (OBSERVABILITY_CONSTRAINT)**

**Evidence**: 
- Workflow design: `.github/workflows/verify-github-executor-api.yml`
- Documentation: `CAPABILITIES_MATRIX.md` Section 8.5, Section 10.2
- Closure notes: `DOCS/STATE_FOR_GPT_SNAPSHOT.md` v3.1

**Approval Status**: ✅ APPROVED (2025-11-17)  
**Execution Status**: ✅ COMPLETED (limitations documented)

---

### Task 2.2: Fix Accept Header Typo 🔄 IN PROGRESS (OS_SAFE)

**Purpose**: Correct code bug that may cause API failures

**File**: `cloud-run/google-workspace-github-api/index.js`  
**Line**: 37  
**Change**: `Accept: 'application/vund.github+json'` → `Accept: 'application/vnd.github+json'`

**Method**: Pull Request

**Execution**:
1. ✅ Branch created: `feature/fix-github-executor-accept-header`
2. ✅ Code fixed: Single-character typo corrected + inline comment added
3. ✅ **PR opened**: [#100](https://github.com/edri2or-commits/make-ops-clean/pull/100)
4. ⏳ **Awaiting Or's review and merge approval**

**PR Details**:
- **URL**: https://github.com/edri2or-commits/make-ops-clean/pull/100
- **Commit**: `ceb6a6d`
- **Changes**: 1 file, 1 line changed (`vund` → `vnd`)
- **Comment added**: `// Fixed: was 'vund.github', now 'vnd.github'`

**Risk**: LOW - Simple typo fix (code change only)  
**Rollback**: Revert commit  
**Evidence**: PR #100

**Approval Status**: ⏳ AWAITING OR'S MERGE APPROVAL  
**Execution Status**: 🔄 IN PROGRESS (PR opened 2025-11-17)

**Next Step**: After merge, proceed to Task 2.3 PLAN

---

### Task 2.3: Deploy or Redeploy Service ⏳ NEXT (PLAN ONLY - OS_SAFE)

**Purpose**: Create detailed deployment plan for github-executor-api

**Scope**: PLAN creation only (OS_SAFE) - NO actual deployment yet

**Pre-requisites**:
1. Task 2.2 merged (code fix applied)
2. Or approval for CLOUD_OPS_HIGH deployment operation

**What Will Be Planned**:
1. Deployment mechanism (Cloud Build / GitHub Actions)
2. Which files are responsible (`cloudbuild.yaml` / workflows)
3. Exact commands that will run
4. Required permissions and environment variables
5. Post-deployment checks/smoke tests
6. Rollback strategy if deployment fails

**Plan Structure** (will be added to this document):
```
Task 2.3 PLAN:
├── 2.3.1: Deployment Method Selection
├── 2.3.2: Workflow/CloudBuild Configuration
├── 2.3.3: Environment Variable Strategy
├── 2.3.4: Smoke Tests Design
└── 2.3.5: Rollback Procedures
```

**Risk**: NONE (planning only)  
**Actual Deployment Risk**: MEDIUM (when executed)

**Approval Status**: ⏳ PLAN creation awaiting Task 2.2 merge  
**Execution Status**: ⏳ NOT STARTED (waiting for Task 2.2)

**Note**: Actual deployment (CLOUD_OPS_HIGH) will require separate approval

---

### Task 2.4: Verify Environment Variables ⏳ PENDING

**Purpose**: Confirm `GITHUB_TOKEN` is configured

**Method**: Part of Task 2.3 execution OR manual verification by Executor

**Approval Status**: ⏳ Awaiting Task 2.3 completion

---

### Task 2.5: Test Service Endpoint ⏳ PENDING

**Purpose**: Verify `/github/update-file` works

**Method**: Test call via workflow (automated)

**Approval Status**: ⏳ Awaiting Task 2.4 completion

---

### Task 2.6: Update GPTs GO Configuration ⏳ PENDING

**Purpose**: Ensure GPTs GO calls correct URL

**Prerequisites**: Tasks 2.1-2.5 complete, service verified working

**Approval Status**: ⏳ Awaiting Task 2.5 completion + Or's guidance

---

### Task 2.7: Update Documentation ⏳ PENDING

**Purpose**: Mark capability as ✅ Verified

**Approval Status**: ⏳ Will execute after Task 2.6 completes

---

## 🔄 Execution Flow

```
Phase 2.1: Verify ✅ COMPLETED (RUNTIME_UNVERIFIED)
    │
Phase 2.2: Fix Typo 🔄 IN PROGRESS (PR #100 opened)
    │
    └─ Or reviews PR → Merge
    │
Phase 2.3: Deploy PLAN ⏳ NEXT (OS_SAFE - planning only)
    │
    └─ Claude creates detailed plan
    │
Phase 2.3 (Execution): Deploy (CLOUD_OPS_HIGH - future)
    │
    └─ Requires separate approval + Executor with Cloud Run access
    │
Phase 2.4-2.7: Test, Configure, Document ⏳ PENDING
```

---

## 🔐 Risk Management

### Risk Matrix

| Task | Risk Level | Impact if Fails | Mitigation | Status |
|------|-----------|-----------------|------------|--------|
| 2.1 Verify | LOW | Can't proceed | Document constraint | ✅ CLOSED |
| 2.2 Fix Typo | LOW | Typo remains | Can fix later | 🔄 IN PROGRESS |
| 2.3 PLAN | NONE | No plan | Create plan | ⏳ NEXT |
| 2.3 Deploy | MEDIUM | Service unavailable | Rollback plan | ⏳ FUTURE |
| 2.4 Env Vars | MEDIUM | Auth fails | Secure token config | ⏳ PENDING |
| 2.5 Test | LOW | Know it doesn't work | Debug and iterate | ⏳ PENDING |
| 2.6 GPTs GO | MEDIUM | GPTs GO broken | Revert config | ⏳ PENDING |
| 2.7 Docs | NONE | Docs outdated | Fix anytime | ⏳ PENDING |

---

## 📊 Success Metrics

**Phase 2 is successful when**:
1. ✅ `github-executor-api` is deployed and reachable
2. ✅ Health check returns 200
3. ✅ `/github/update-file` accepts test requests
4. ✅ Test commit appears in GitHub
5. ✅ GPTs GO can successfully call the service (no 404)
6. ✅ CAPABILITIES_MATRIX updated to Verified
7. ✅ BUS decision made and documented (DEFERRED - approved 2025-11-17)

**Evidence of Success**:
- Service URL documented
- Test commit SHA
- Updated CAPABILITIES_MATRIX
- GPTs GO test results

---

## 🔄 Updates Log

### 2025-11-17 - Task 2.2 Started (PR Opened)
- **Status**: IN PROGRESS
- **PR**: #100 opened
- **Branch**: `feature/fix-github-executor-accept-header`
- **Change**: Fixed Accept header typo (`vund` → `vnd`)
- **Commit**: `ceb6a6d`
- **Next**: Awaiting Or's review and merge approval

### 2025-11-17 - Task 2.1 Closed (RUNTIME_UNVERIFIED)
- **Status**: COMPLETED with Observability Constraint
- **Outcome**: Workflow design pattern established, but runtime verification blocked
- **Documentation**: Updated CAPABILITIES_MATRIX, STATE_FOR_GPT_SNAPSHOT, this PLAN
- **Next Step**: Proceed to Task 2.2 (code fix)
- **Lesson Learned**: Observability gap must be addressed for future autonomous operations

### 2025-11-17 - BUS Decision Approved
- **BUS Status**: DEFERRED (Option A)
- **Approved by**: Or
- **Rationale**: Focus on core GitHub operations

### 2025-11-17 - Initial Plan
- Created recovery plan based on Phase 1.1 diagnosis
- Outlined 7 tasks with approval gates

---

**Status**: 🔄 Task 2.2 IN PROGRESS (PR #100) | ⏳ Task 2.3 PLAN awaiting Task 2.2 merge

**Next Action**: Or reviews PR #100 → Claude creates Task 2.3 deployment PLAN
