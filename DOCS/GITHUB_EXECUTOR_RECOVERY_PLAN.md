# GitHub Executor Recovery Plan

**Phase**: 2 (PLANNING ONLY - NO EXECUTION YET)  
**Date Created**: 2025-11-17  
**Status**: 📋 PLAN - Awaiting Or's Approval  
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
- Clear decision on BUS (build/abandon)

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

### Secondary Goal
**Clarify BUS decision**

Options:
- **Option A**: Defer BUS to future phase (RECOMMENDED)
- **Option B**: Build BUS system (high effort, questionable value)
- **Option C**: Document BUS as abandoned

Recommendation: **Option A** (defer) - Focus on core GitHub operations first

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

**Approval Required**: ✅ Yes (CLOUD_OPS_HIGH - GCP operation)

---

### Task 2.2: Fix Accept Header Typo ✅ APPROVED BY OR

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

**Approval Required**: ✅ Yes (CLOUD_OPS_HIGH - code change in production service)

---

### Task 2.3: Deploy or Redeploy Service

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

**Approval Required**: ✅ Yes (CLOUD_OPS_HIGH - service deployment)

---

### Task 2.4: Verify Environment Variables

**Purpose**: Confirm `GITHUB_TOKEN` is configured

**Method**: Via Cloud Run describe (from Task 2.1) or separate check

**Steps**:
1. List environment variable names (not values)
2. Confirm `GITHUB_TOKEN` exists
3. If missing: Add via `gcloud run services update`

**Risk**: MEDIUM - May need to configure secrets  
**Rollback**: Remove environment variable if added  
**Evidence**: Service configuration output

**Approval Required**: ✅ Yes (CLOUD_OPS_HIGH - secret configuration)

---

### Task 2.5: Test Service Endpoint

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

**Approval Required**: ✅ Yes (CLOUD_OPS_HIGH - API call with GitHub write)

---

### Task 2.6: Update GPTs GO Configuration

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

**Approval Required**: ✅ Yes (CLOUD_OPS_HIGH - external system configuration)

**Note**: This task may require Or's input on where GPTs GO config lives

---

### Task 2.7: Update Documentation

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

**Approval Required**: ❌ No (OS_SAFE)

---

## 🔄 Execution Flow

```
Phase 2.1: Verify (LOW RISK)
    │
    ├─ Is service deployed?
    │  ├─ YES → Skip to 2.2
    │  └─ NO  → Continue to 2.3
    │
Phase 2.2: Fix Typo (LOW RISK, optional if deploying new)
    │
    └─ PR → Merge
    │
Phase 2.3: Deploy/Redeploy (MEDIUM RISK)
    │
    ├─ Deployment successful?
    │  ├─ YES → Continue to 2.4
    │  └─ NO  → STOP, debug, get Or approval to continue
    │
Phase 2.4: Verify Env Vars (MEDIUM RISK)
    │
    └─ GITHUB_TOKEN configured?
    │
Phase 2.5: Test Endpoint (LOW RISK)
    │
    ├─ Test successful?
    │  ├─ YES → Continue to 2.6
    │  └─ NO  → STOP, debug, iterate 2.3-2.5
    │
Phase 2.6: Update GPTs GO (MEDIUM RISK)
    │
    └─ GPTs GO can call service?
    │
Phase 2.7: Update Docs (OS_SAFE)
    │
    └─ ✅ COMPLETE
```

---

## ⚠️ Decision Point: BUS System

**Question**: Should we build BUS in Phase 2?

**Analysis**:

| Aspect | BUS System | Direct Calls |
|--------|-----------|--------------|
| Effort | HIGH (new Sheet, polling, schema) | NONE (already works with fix) |
| Complexity | HIGH (async queue, error handling) | LOW (synchronous) |
| Benefit | Async task queue | Simple, direct |
| Maintenance | Ongoing | Minimal |
| Time to complete | 3-5 sessions | Already done after Phase 2 |

**Recommendation**: **Defer BUS to future phase**

**Reasoning**:
1. Core need is GitHub file updates - this works without BUS
2. BUS adds architectural complexity without clear immediate benefit
3. Can always add BUS later if async queue becomes necessary
4. Focus on making simple thing work first

**Options**:
- **A) Defer BUS** (recommended) - Document as "Planned for Phase 3+"
- **B) Build BUS now** - Only if Or sees specific need for async queue
- **C) Abandon BUS** - Remove from documentation entirely

**Approval Required**: Or's decision on BUS direction

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
7. ✅ Clear decision made on BUS (defer/build/abandon)

**Evidence of Success**:
- Service URL documented
- Test commit SHA
- Successful workflow run logs
- Updated CAPABILITIES_MATRIX
- GPTs GO test results

---

## 📝 Next Steps

**After Plan Approval**:
1. Or reviews this plan
2. Or approves/adjusts BUS decision (recommend: defer)
3. Or approves overall Phase 2 approach
4. Claude executes Task 2.1 (verification workflow)
5. Based on results, proceed through tasks 2.2-2.7
6. Each CLOUD_OPS_HIGH task gets separate approval

**Timeline Estimate**: 2-3 sessions (assuming no major issues)

**Dependencies**:
- Or's approval on this plan
- Or's decision on BUS
- Access to Cloud Run via GitHub Actions (we have WIF)
- Access to GPTs GO configuration (may need Or's help)

---

## 🔄 Updates Log

### 2025-11-17 - Initial Plan
- Created recovery plan based on Phase 1.1 diagnosis
- Outlined 7 tasks with approval gates
- Recommended deferring BUS to future phase
- Defined success criteria and rollback procedures

---

**Status**: 📋 PLAN READY - Awaiting Or's approval to begin Phase 2 execution

**Next Action**: Or reviews and approves/adjusts this plan
