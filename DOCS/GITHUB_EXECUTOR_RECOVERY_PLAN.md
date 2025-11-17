# GitHub Executor Recovery Plan

**Phase**: 2 (Task 2.1 CLOSED, Task 2.2-2.3 Ready for Planning)  
**Date Created**: 2025-11-17  
**Status**: ✅ Task 2.1 COMPLETED (RUNTIME_UNVERIFIED) - Observability Constraint  
**Risk Level**: CLOUD_OPS_HIGH (for deployment tasks)

---

## 🎯 Executive Summary

**Goal**: Fix the GPTs GO → GitHub integration loop by recovering the `github-executor-api` service.

**Current State**:
- Service code exists in `cloud-run/google-workspace-github-api/`
- **Runtime status UNKNOWN** (Observability Constraint documented)
- GPTs GO reports 404 on `/github/update-file`
- BUS system not implemented (DEFERRED - approved by Or)

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
- Or clicking \"Run workflow\" buttons
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
   - Code typo: `vund.github` → should be `vnd.github` (line 37)
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
- CAPABILITIES_MATRIX Section 10.3: BUS marked as \"Deferred\"
- STATE_FOR_GPT_SNAPSHOT: BUS status = Deferred

---

## 📋 Phase 2 Tasks (CLOUD_OPS_HIGH)

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
```
Claude lacks:
1. Network access to GitHub Actions API
2. Network access to GCP Cloud Run API
3. Workflow STATUS files (didn't get created)

Or's constraint:
- Will not manually check Actions UI (violates Or-OS contract)
- Will not manually check Cloud Run console

Result: Runtime status remains UNKNOWN
```

**Outcome**: **COMPLETED – RUNTIME_UNVERIFIED (OBSERVABILITY_CONSTRAINT)**

**Evidence**: 
- Workflow design: `.github/workflows/verify-github-executor-api.yml`
- Documentation: `CAPABILITIES_MATRIX.md` Section 8.5, Section 10.2
- Closure notes: `DOCS/STATE_FOR_GPT_SNAPSHOT.md` v3.1

**Approval Status**: ✅ APPROVED (2025-11-17)  
**Execution Status**: ✅ COMPLETED (limitations documented)  
**Next Step**: Proceed to Task 2.2 (code fix) with assumption that deployment may be needed

---

### Task 2.2: Fix Accept Header Typo ⏳ NEXT (OS_SAFE for code change)

**Purpose**: Correct code bug that may cause API failures

**File**: `cloud-run/google-workspace-github-api/index.js`  
**Line**: 37  
**Change**: `Accept: 'application/vund.github+json'` → `Accept: 'application/vnd.github+json'`

**Method**: Pull Request (automated by Claude)

**Steps**:
1. Create branch: `fix/accept-header-typo`
2. Apply fix using str_replace or file edit
3. Create PR with title: \"Fix Accept header typo in github-executor-api\"
4. Wait for Or's review
5. Merge after approval

**Risk**: LOW - Simple typo fix (code change only)  
**Rollback**: Revert commit  
**Evidence**: PR link, commit SHA

**Approval Status**: ⏳ AWAITING APPROVAL (ready to proceed)

---

### Task 2.3: Deploy or Redeploy Service ⏳ PENDING (CLOUD_OPS_HIGH)

**Purpose**: Ensure service is running with latest code

**Assumption**: Based on Task 2.1 results, assume deploy may be needed from scratch

**Method**: GitHub Actions workflow triggers Cloud Build (automated)

**Pre-requisites**:
1. Task 2.2 merged (code fix applied)
2. Or approval for CLOUD_OPS_HIGH deployment operation

**Steps**:
1. Create deployment workflow OR update existing `cloudbuild.yaml`
2. Trigger deployment via workflow
3. Wait for deployment to complete
4. Write deployment status to `OPS/STATUS/github-executor-api-deploy.json`
5. Verify service URL and revision

**Risk**: MEDIUM - Creates/updates Cloud Run service  
**Rollback**: 
- Revert to previous revision: `gcloud run services update-traffic --to-revisions=PREVIOUS=100`
- Or delete service if newly created

**Evidence**: `OPS/STATUS/github-executor-api-deploy.json`, Cloud Build logs (if accessible)

**Approval Status**: ⏳ REQUIRES PLAN + Or approval before execution

---

### Task 2.4: Verify Environment Variables ⏳ PENDING

**Purpose**: Confirm `GITHUB_TOKEN` is configured

**Method**: Depends on observability improvements OR manual verification by Executor

**Steps**:
1. Check service configuration for env vars
2. Confirm `GITHUB_TOKEN` exists
3. If missing: Add via workflow

**Risk**: MEDIUM - May need to configure secrets  
**Rollback**: Remove environment variable if added  
**Evidence**: Service configuration output

**Approval Status**: ⏳ Awaiting Task 2.3 completion

---

### Task 2.5: Test Service Endpoint ⏳ PENDING

**Purpose**: Verify `/github/update-file` works

**Method**: Test call via workflow (automated)

**Steps**:
1. Get service URL from Task 2.3 output
2. Create test workflow that calls endpoint
3. Write test results to `OPS/STATUS/github-executor-api-test.json`
4. Clean up test file/branch

**Risk**: LOW - Test operation only  
**Rollback**: Delete test branch  
**Evidence**: `OPS/STATUS/github-executor-api-test.json`, commit SHA

**Approval Status**: ⏳ Awaiting Task 2.4 completion

---

### Task 2.6: Update GPTs GO Configuration ⏳ PENDING

**Purpose**: Ensure GPTs GO calls correct URL

**Prerequisites**: Tasks 2.1-2.5 complete, service verified working

**Method**: Update OpenAPI spec / configuration (TBD - requires Or's guidance)

**Steps**:
1. Identify where GPTs GO stores API endpoint URLs
2. Update to correct URL
3. Test GPTs GO → github-executor-api connection
4. Verify 404 is resolved

**Risk**: MEDIUM - May affect GPTs GO functionality  
**Rollback**: Revert to previous configuration  
**Evidence**: Test results

**Approval Status**: ⏳ Awaiting Task 2.5 completion + Or's guidance

---

### Task 2.7: Update Documentation ⏳ PENDING

**Purpose**: Mark capability as ✅ Verified

**Files to update**:
1. `CAPABILITIES_MATRIX.md`:
   - Section 10.2: Change status from \"Runtime Unverified\" → ✅ Verified
   - Add service URL
   - Add evidence from Tasks 2.2-2.6
   
2. `DOCS/STATE_FOR_GPT_SNAPSHOT.md`:
   - Update github-executor-api status to VERIFIED
   - Document successful recovery

3. `DOCS/L2_RUNTIME_DIAGNOSIS.md`:
   - Add resolution notes

**Risk**: NONE (OS_SAFE)  
**Rollback**: N/A  
**Evidence**: Updated documentation commits

**Approval Status**: ⏳ Will execute after Task 2.6 completes

---

## 🔄 Execution Flow

```
Phase 2.1: Verify (LOW RISK) ✅ COMPLETED (RUNTIME_UNVERIFIED)
    │
    └─ Observability Constraint documented
    │
    ├─ Assumption: Deploy may be needed from scratch
    │
Phase 2.2: Fix Typo (OS_SAFE) ⏳ NEXT
    │
    └─ PR → Merge
    │
Phase 2.3: Deploy/Redeploy (CLOUD_OPS_HIGH) ⏳ REQUIRES PLAN + APPROVAL
    │
    ├─ Deployment successful?
    │  ├─ YES → Continue to 2.4
    │  └─ NO  → STOP, debug, get Or approval to continue
    │
Phase 2.4: Verify Env Vars (MEDIUM RISK) ⏳ PENDING
    │
    └─ GITHUB_TOKEN configured?
    │
Phase 2.5: Test Endpoint (LOW RISK) ⏳ PENDING
    │
    ├─ Test successful?
    │  ├─ YES → Continue to 2.6
    │  └─ NO  → STOP, debug, iterate 2.3-2.5
    │
Phase 2.6: Update GPTs GO (MEDIUM RISK) ⏳ PENDING
    │
    └─ GPTs GO can call service?
    │
Phase 2.7: Update Docs (OS_SAFE) ⏳ PENDING
    │
    └─ ✅ COMPLETE
```

---

## 🔐 Risk Management

### Risk Matrix

| Task | Risk Level | Impact if Fails | Mitigation | Status |
|------|-----------|-----------------|------------|--------|
| 2.1 Verify | LOW | Can't proceed | Document constraint, proceed with assumption | ✅ CLOSED |
| 2.2 Fix Typo | LOW | Typo remains | Can fix later | ⏳ NEXT |
| 2.3 Deploy | MEDIUM | Service unavailable | Rollback to previous revision | ⏳ REQUIRES PLAN |
| 2.4 Env Vars | MEDIUM | Auth fails | Add token via secure method | ⏳ PENDING |
| 2.5 Test | LOW | Know it doesn't work | Debug and iterate | ⏳ PENDING |
| 2.6 GPTs GO | MEDIUM | GPTs GO broken | Revert config | ⏳ PENDING |
| 2.7 Docs | NONE | Docs outdated | Fix anytime | ⏳ PENDING |

### Approval Gates

Each CLOUD_OPS_HIGH task requires:\n1. **PLAN presentation** to Or\n2. **Explicit approval** before execution\n3. **Automated execution** (no manual clicks)\n4. **Status written to repo** for observation (where possible)\n5. **Evidence collection**

### Rollback Strategy

If anything goes wrong:\n1. **Immediate**: Stop execution\n2. **Assess**: Read status files (if available) OR gather evidence\n3. **Rollback**: Use task-specific rollback procedure\n4. **Report**: Document in repo files\n5. **Plan**: Adjust approach before retry

---

## 📊 Success Metrics

**Phase 2 is successful when**:\n1. ✅ `github-executor-api` is deployed and reachable\n2. ✅ Health check returns 200\n3. ✅ `/github/update-file` accepts test requests\n4. ✅ Test commit appears in GitHub\n5. ✅ GPTs GO can successfully call the service (no 404)\n6. ✅ CAPABILITIES_MATRIX updated to Verified\n7. ✅ BUS decision made and documented (DEFERRED - approved 2025-11-17)\n\n**Evidence of Success**:\n- Service URL documented\n- Test commit SHA\n- Updated CAPABILITIES_MATRIX\n- GPTs GO test results\n- Status files in `OPS/STATUS/` (where observability permits)\n\n---\n\n## 🔄 Updates Log\n\n### 2025-11-17 - Task 2.1 Closed (RUNTIME_UNVERIFIED)\n- **Status**: COMPLETED with Observability Constraint\n- **Outcome**: Workflow design pattern established, but runtime verification blocked\n- **Root Cause**: No Network access to Actions API + no status files created + Or won't check UIs\n- **Documentation**: Updated CAPABILITIES_MATRIX, STATE_FOR_GPT_SNAPSHOT, this PLAN\n- **Next Step**: Proceed to Task 2.2 (code fix) with assumption deploy may be needed\n- **Lesson Learned**: Observability gap must be addressed for future autonomous operations\n\n### 2025-11-17 - Task 2.1 Execution Started\n- **Status**: Workflow triggered automatically\n- **Protocol**: Zero-touch, designed to write to `OPS/STATUS/*.json`\n- **Compliance**: Or-OS contract enforced (no manual UI checks)\n- **Trigger**: Commits `cd7b467`, `8d39cbee` to workflow and trigger files\n\n### 2025-11-17 - BUS Decision Approved\n- **BUS Status**: DEFERRED (Option A)\n- **Approved by**: Or\n- **Rationale**: Focus on core GitHub operations; can revisit if async queue needed\n- **Documentation**: Updated PLAN, MATRIX, and STATE\n\n### 2025-11-17 - Task 2.1 Approved\n- **Approval**: Or approved execution of Task 2.1\n- **Method**: Automated workflow with repo status output\n\n### 2025-11-17 - Initial Plan\n- Created recovery plan based on Phase 1.1 diagnosis\n- Outlined 7 tasks with approval gates\n- Recommended deferring BUS to future phase\n- Defined success criteria and rollback procedures\n\n---\n\n**Status**: ✅ Task 2.1 CLOSED (RUNTIME_UNVERIFIED) | ⏳ Task 2.2 READY FOR APPROVAL\n\n**Next Action**: Claude presents Task 2.2 PR (code fix) for Or's approval, then Task 2.3 PLAN (deployment)
