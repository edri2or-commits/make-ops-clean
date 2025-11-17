# GitHub Executor Recovery Plan

**Phase**: 2 (EXECUTION APPROVED - Task 2.1 Ready)  
**Date Created**: 2025-11-17  
**Status**: ✅ APPROVED BY OR - Ready for Task 2.1 execution  
**Risk Level**: CLOUD_OPS_HIGH (when executed)

---

## 🎯 Executive Summary

**Goal**: Fix the GPTs GO → GitHub integration loop by recovering the `github-executor-api` service.

**Current State**:
- Service code exists in `cloud-run/google-workspace-github-api/`
- Deployment status unknown (🔍 Unverified)
- GPTs GO reports 404 on `/github/update-file`
- BUS system not implemented (design only)

**Target State**:
- `github-executor-api` deployed and operational
- GPTs GO can successfully call `/github/update-file`
- Commits appear in GitHub repositories
- CAPABILITIES_MATRIX updated with ✅ Verified status
- **BUS decision: DEFERRED** ✅

**Approach**: Fix and deploy (Option A), NOT build BUS in Phase 2

---

## 📊 Current Situation (From Phase 1.1 Diagnosis)

### What We Know ✅

1. **ONE service exists** (not two):
   - Code: `cloud-run/google-workspace-github-api/`
   - Deployed name: `github-executor-api`
   - Region: `us-central`, Project: `edri2or-mcp`

2. **Implemented endpoints**:
   - `GET /` - Health check
   - `POST /github/update-file` - GitHub file operations

3. **Known issues**:
   - Code typo: `vund.github` → should be `vnd.github` (line 37)
   - GPTs GO gets 404 on `/github/update-file`

4. **BUS status**:
   - NOT implemented in code
   - Exists only in documentation
   - No Sheet ID, no polling, no `/bus/process-next-task`

### What We DON'T Know ❓

1. Is `github-executor-api` deployed?
2. What's the public URL?
3. Is `GITHUB_TOKEN` environment variable set?
4. Why does GPTs GO receive 404?
5. What URL is GPTs GO calling?

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

**Revisit Criteria**:
- When there's a clear need for task queuing
- When GPTs GO requires async operation patterns
- When we see performance/scaling issues with direct calls

**Documentation Updated**: 
- CAPABILITIES_MATRIX Section 10.3: BUS marked as "Deferred"
- STATE_FOR_GPT_SNAPSHOT: BUS status = Deferred

---

## 📋 Phase 2 Tasks (CLOUD_OPS_HIGH)

### Task 2.1: Verify Deployment Status ✅ APPROVED BY OR

**Purpose**: Determine if service is deployed and get its URL

**Method**: GitHub Actions workflow (automated, not manual)

**Steps**:
1. Create `.github/workflows/verify-cloud-run-service.yml`
2. Workflow authenticates via WIF
3. Executes: `gcloud run services describe github-executor-api --region=us-central --project=edri2or-mcp`
4. Returns output as artifact
5. Claude reads artifact and determines:
   - Is service deployed? (yes/no)
   - Service URL
   - Last deployment date
   - Environment variables (names only, not values)

**Risk**: LOW - Read-only operation  
**Rollback**: N/A (read-only)  
**Evidence**: Workflow run logs + artifact

**Approval Status**: ✅ APPROVED (2025-11-17)

---

### Task 2.2: Fix Accept Header Typo ⏳ PENDING

**Purpose**: Correct code bug that may cause API failures

**File**: `cloud-run/google-workspace-github-api/index.js`  
**Line**: 37  
**Change**: `Accept: 'application/vund.github+json'` → `Accept: 'application/vnd.github+json'`

**Method**: Pull Request

**Steps**:
1. Create branch: `fix/accept-header-typo`
2. Apply fix using str_replace
3. Create PR with title: "Fix Accept header typo in github-executor-api"
4. Wait for Or's review
5. Merge after approval

**Risk**: LOW - Simple typo fix  
**Rollback**: Revert commit  
**Evidence**: PR link, commit SHA

**Approval Status**: ⏳ Awaiting approval after Task 2.1 results

---

### Task 2.3: Deploy or Redeploy Service ⏳ PENDING

**Purpose**: Ensure service is running with latest code

**Condition**: Execute only if Task 2.1 shows service is NOT deployed OR if we fix the typo

**Method**: GitHub Actions workflow triggers Cloud Build

**Steps**:
1. If service NOT deployed:
   - Trigger `cloudbuild.yaml` manually via `gcloud builds submit`
2. If service exists but needs update:
   - Same process (will update existing service)
3. Wait for deployment to complete
4. Verify new revision is live

**Risk**: MEDIUM - Creates/updates Cloud Run service  
**Rollback**: 
- Revert to previous revision: `gcloud run services update-traffic --to-revisions=PREVIOUS=100`
- Or delete service if newly created

**Evidence**: Cloud Build logs, service URL, revision ID

**Approval Status**: ⏳ Awaiting approval after Task 2.1/2.2

---

### Task 2.4: Verify Environment Variables ⏳ PENDING

**Purpose**: Confirm `GITHUB_TOKEN` is configured

**Method**: Via Cloud Run describe (from Task 2.1) or separate check

**Steps**:
1. List environment variable names (not values)
2. Confirm `GITHUB_TOKEN` exists
3. If missing: Add via `gcloud run services update`

**Risk**: MEDIUM - May need to configure secrets  
**Rollback**: Remove environment variable if added  
**Evidence**: Service configuration output

**Approval Status**: ⏳ Awaiting approval after Task 2.3

---

### Task 2.5: Test Service Endpoint ⏳ PENDING

**Purpose**: Verify `/github/update-file` works

**Method**: Test call via workflow

**Steps**:
1. Get service URL from Task 2.1
2. Create test workflow that calls:
   ```
   POST {SERVICE_URL}/github/update-file
   {
     "repo": "edri2or-commits/make-ops-clean",
     "branch": "test-branch",
     "path": "TEST_github_executor.md",
     "content": "Test from github-executor-api recovery",
     "message": "Test: github-executor-api verification"
   }
   ```
3. Verify:
   - Response is 200 OK
   - Commit appears in GitHub
4. Clean up test file/branch

**Risk**: LOW - Test operation only  
**Rollback**: Delete test branch  
**Evidence**: API response, commit SHA

**Approval Status**: ⏳ Awaiting approval after Task 2.4

---

### Task 2.6: Update GPTs GO Configuration ⏳ PENDING

**Purpose**: Ensure GPTs GO calls correct URL

**Prerequisites**: Tasks 2.1-2.5 complete, service verified working

**Method**: Update OpenAPI spec / configuration (TBD - need to see GPTs GO setup)

**Steps**:
1. Identify where GPTs GO stores API endpoint URLs
2. Update to correct URL from Task 2.1
3. Test GPTs GO → github-executor-api connection
4. Verify 404 is resolved

**Risk**: MEDIUM - May affect GPTs GO functionality  
**Rollback**: Revert to previous configuration  
**Evidence**: GPTs GO test results

**Approval Status**: ⏳ Awaiting approval after Task 2.5

**Note**: This task may require Or's input on where GPTs GO config lives

---

### Task 2.7: Update Documentation ⏳ PENDING

**Purpose**: Mark capability as ✅ Verified

**Files to update**:
1. `CAPABILITIES_MATRIX.md`:
   - Section 10.2: Change status from 🔍 Unverified → ✅ Verified
   - Add service URL
   - Add evidence from Tasks 2.1-2.6
   
2. `DOCS/STATE_FOR_GPT_SNAPSHOT.md`:
   - Update github-executor-api status
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
Phase 2.1: Verify (LOW RISK) ✅ APPROVED
    │
    ├─ Is service deployed?
    │  ├─ YES → Skip to 2.2
    │  └─ NO  → Continue to 2.3
    │
Phase 2.2: Fix Typo (LOW RISK, optional if deploying new) ⏳ PENDING
    │
    └─ PR → Merge
    │
Phase 2.3: Deploy/Redeploy (MEDIUM RISK) ⏳ PENDING
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

| Task | Risk Level | Impact if Fails | Mitigation |
|------|-----------|-----------------|------------|
| 2.1 Verify | LOW | Can't proceed | Use existing docs, skip if needed |
| 2.2 Fix Typo | LOW | Typo remains | Can fix later |
| 2.3 Deploy | MEDIUM | Service unavailable | Rollback to previous revision |
| 2.4 Env Vars | MEDIUM | Auth fails | Add token via secure method |
| 2.5 Test | LOW | Know it doesn't work | Debug and iterate |
| 2.6 GPTs GO | MEDIUM | GPTs GO broken | Revert config |
| 2.7 Docs | NONE | Docs outdated | Fix anytime |

### Approval Gates

Each CLOUD_OPS_HIGH task requires:
1. **PLAN presentation** to Or
2. **Explicit approval** before execution
3. **Evidence collection** during execution
4. **Status update** to Or after completion

### Rollback Strategy

If anything goes wrong:
1. **Immediate**: Stop execution
2. **Assess**: Determine impact
3. **Rollback**: Use task-specific rollback procedure
4. **Report**: Document what happened
5. **Plan**: Adjust approach before retry

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
- Successful workflow run logs
- Updated CAPABILITIES_MATRIX
- GPTs GO test results

---

## 🔄 Updates Log

### 2025-11-17 - BUS Decision Approved
- **BUS Status**: DEFERRED (Option A)
- **Approved by**: Or
- **Rationale**: Focus on core GitHub operations; can revisit if async queue needed
- **Documentation**: Updated PLAN, MATRIX, and STATE

### 2025-11-17 - Task 2.1 Approved
- **Approval**: Or approved execution of Task 2.1
- **Next Step**: Create verification workflow (YAML review before execution)

### 2025-11-17 - Initial Plan
- Created recovery plan based on Phase 1.1 diagnosis
- Outlined 7 tasks with approval gates
- Recommended deferring BUS to future phase
- Defined success criteria and rollback procedures

---

**Status**: ✅ APPROVED - Task 2.1 ready for execution

**Next Action**: Claude presents Task 2.1 workflow YAML for Or's final review before execution
