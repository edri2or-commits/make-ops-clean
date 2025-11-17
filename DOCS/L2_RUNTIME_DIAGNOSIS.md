# L2 Runtime Diagnosis Report

**Phase**: 1.1 (OS_SAFE - Read & Analysis Only)  
**Date**: 2025-11-17  
**Author**: Claude (Executor)  
**Status**: DIAGNOSIS COMPLETE - AWAITING PHASE 1.2 APPROVAL

---

## 🎯 Executive Summary

This diagnosis reveals **critical misalignment** between documented systems and actual implementation:

### Key Findings:
1. **"google-workspace-api" and "github-executor-api" are ONE service**, not two
2. **BUS system has NO implementation** in the codebase
3. **CAPABILITIES_MATRIX contains outdated assumptions**
4. **Google Workspace write capabilities blocked by MCP limitation**, not OAuth

### Impact:
- GPTs GO cannot use GitHub executor (service exists but may not be deployed)
- BUS-based task queue **does not exist**
- Documentation describes non-existent architecture
- Path forward requires: Deploy verification + BUS decision (build or abandon)

---

## 📋 Detailed Findings

### 1️⃣ Cloud Run Service Analysis

#### Finding: Single Unified Service

**What CAPABILITIES_MATRIX Says**:
- Implies two separate services: `google-workspace-api` and `github-executor-api`
- Mentions both in different contexts
- No clear relationship documented

**What the Code Shows**:
```
cloud-run/google-workspace-github-api/
├── index.js (2.4KB)
├── Dockerfile
├── cloudbuild.yaml
└── package.json
```

**Reality**:
- **ONE codebase** at `cloud-run/google-workspace-github-api/`
- **ONE service** deployed as `github-executor-api` (per cloudbuild.yaml)
- **Confusing naming**: directory says "google-workspace-github-api", deploy says "github-executor-api"

#### Implemented Endpoints (from index.js)

**Verified in Code**:
1. `GET /` - Health check
   - Returns: `{ service: 'google-workspace-github-api', status: 'ok' }`

2. `POST /github/update-file` ✅
   - Purpose: Create/update files in GitHub repos
   - Auth: `process.env.GITHUB_TOKEN`
   - Params: `repo`, `branch`, `path`, `content`, `message`
   - Logic: Get SHA if exists → PUT to GitHub API
   - **This is the endpoint GPTs GO needs**

**Missing Endpoints**:
- NO `/bus/process-next-task`
- NO Google Workspace operations (Gmail, Drive, Sheets, etc.)
- NO other GitHub operations beyond file updates

**Critical Note in Code**:
```javascript
// Line 37: Typo in Accept header
Accept: 'application/vund.github+json'
// Should be: 'application/vnd.github+json'
```
This typo could cause API failures.

#### Deployment Status: UNKNOWN ❓

**What we know**:
- `cloudbuild.yaml` exists
- Deploys to: `us-central` region, project `edri2or-mcp`
- Service name: `github-executor-api`
- Image: `us-central-docker.pkg.dev/edri2or-mcp/cloud-run-source-deploy/github-executor-api:$COMMIT_SHA`

**What we DON'T know** (cannot verify without Cloud Run access):
- ❓ Is the service actually deployed?
- ❓ What's the public URL?
- ❓ Is `GITHUB_TOKEN` environment variable set?
- ❓ When was the last successful build?
- ❓ Are there any error logs?

**Why GPTs GO Gets 404**:
Possible causes (ranked by likelihood):
1. **Service not deployed** (most likely)
2. **URL mismatch** - GPTs GO calling wrong URL
3. **Authentication failure** - missing API key
4. **GITHUB_TOKEN not configured** - service returns 500, not 404
5. **Typo in Accept header** breaking requests

---

### 2️⃣ BUS System Analysis

#### Finding: NO IMPLEMENTATION EXISTS

**What CAPABILITIES_MATRIX/docs reference**:
- BUS in Sheets
- Task queue pattern
- `/bus/process-next-task` endpoint
- Sheet-based orchestration

**What the Code Shows**:
```bash
$ grep -r "BUS" --include="*.js" --include="*.py" --include="*.yml"
# NO MATCHES in cloud-run/ directory
# NO MATCHES in .github/workflows/ (checked 10 major workflows)
# NO MATCHES in Python scripts
```

**Reality**:
- ❌ NO BUS endpoint in `index.js`
- ❌ NO Sheet ID referenced anywhere
- ❌ NO Workflow that polls BUS
- ❌ NO Python script that manages BUS
- ❌ NO mention of BUS pattern in actual code

**BUS appears ONLY in documentation**, not in implementation.

#### What This Means

**The BUS-based architecture described in docs is PLANNED, not IMPLEMENTED.**

Either:
- A) Build the BUS system (CLOUD_OPS_HIGH effort)
- B) Abandon BUS, document alternative (GPTs GO → Direct Cloud Run calls)

---

### 3️⃣ Google Workspace API Status

#### Finding: Naming Confusion

**Issue**: 
- Directory named `google-workspace-github-api`
- Service only implements GitHub operations
- NO Google Workspace operations in code
- MCP Google Workspace server is separate (already working for READ)

**Hypothesis**:
- Original plan: Unified API for both Google + GitHub
- Current reality: Only GitHub implemented
- MCP handles Google READ operations
- Google WRITE operations **blocked by MCP server limitation** (see FULL_CAPABILITIES_REPORT_2025-11-17.md)

**Recommendation**:
- Rename service to avoid confusion
- OR: Add Google Workspace write endpoints (CLOUD_OPS_HIGH)
- Document clearly: What this service IS vs ISN'T

---

## 🔍 Gap Analysis: MATRIX vs Reality

### Gaps in CAPABILITIES_MATRIX.md

| What MATRIX Says | Reality | Gap Type |
|------------------|---------|----------|
| "google-workspace-api" exists | ONE service, confusingly named | NAMING |
| "github-executor-api" is separate | Same service as above | ARCHITECTURE |
| BUS integration works | NO BUS implementation | MISSING FEATURE |
| Google Workspace write via Cloud Run | NO Google endpoints in code | MISSING FEATURE |
| Service is operational | Deployment status unknown | VERIFICATION |

### Gaps in STATE_FOR_GPT_SNAPSHOT.md

| What STATE Says | Reality | Gap Type |
|-----------------|---------|----------|
| GPT Tasks Executor runtime broken | Correct, verified | ACCURATE |
| `/bus/process-next-task` mentioned | Endpoint doesn't exist | PLANNED FEATURE |
| Multiple systems coordinated | Only one partial service exists | ARCHITECTURE |

---

## 📊 What We Can Confirm (OS_SAFE Evidence)

### ✅ Confirmed via Code Reading

1. **Single Cloud Run Service Exists**
   - Location: `cloud-run/google-workspace-github-api/`
   - Implements: `/github/update-file`
   - Purpose: GitHub file operations only

2. **GPT Tasks Executor Broken**
   - Workflow exists: `.github/workflows/gpt_tasks_executor.yml`
   - Runtime issue confirmed (per STATE snapshot)

3. **BUS Not Implemented**
   - No code references
   - No Sheet integration
   - Purely architectural concept

4. **Typo in Production Code**
   - `Accept: 'application/vund.github+json'`
   - Should be: `vnd.github`

### ❌ Cannot Confirm (Need CLOUD_OPS_HIGH)

1. **Deployment Status**
   - Need: `gcloud run services describe github-executor-api`
   - Need: Cloud Run logs
   - Need: Service URL

2. **Environment Variables**
   - Is `GITHUB_TOKEN` set?
   - What's the token scope?

3. **GPTs GO Integration**
   - What URL is GPTs GO calling?
   - What's the exact 404 error?
   - Is there an OpenAPI spec mismatch?

4. **WIF Status**
   - Is WIF provider still active?
   - Does service have WIF-based authentication option?

---

## 🎯 Recommendations for Phase 1.2 (OS_SAFE)

### Priority 1: Update CAPABILITIES_MATRIX (OS_SAFE)

**Section to update**: Section 4 (GCP Layer) + New Section 10

**Changes**:
1. Clarify: ONE service, not two
2. Document actual endpoints: `/` and `/github/update-file` only
3. Mark BUS as "PLANNED, not implemented"
4. Add "Deployment Status: UNVERIFIED"
5. Note the Accept header typo

**Impact**: High - Aligns documentation with reality  
**Effort**: Low - Text edits only  
**Risk**: None - OS_SAFE

### Priority 2: Update STATE_FOR_GPT_SNAPSHOT (OS_SAFE)

**Changes**:
1. Correct service naming
2. Remove BUS references or mark as "Design only"
3. Update endpoint list to match reality

**Impact**: Medium - Improves GPT context accuracy  
**Effort**: Low - Text edits  
**Risk**: None - OS_SAFE

### Priority 3: Create DIAGNOSIS_EVIDENCE.md (OS_SAFE)

**Purpose**: Document what was checked and how

**Contents**:
- Code file hashes (SHA)
- Search queries used
- Absence proofs (no BUS references)
- Timestamp of diagnosis

**Impact**: High - Audit trail  
**Effort**: Low  
**Risk**: None - OS_SAFE

---

## 🚀 Recommendations for Phase 2 (CLOUD_OPS_HIGH)

### Priority 1: Verify Deployment Status

**Actions** (requires approval):
1. Check if `github-executor-api` is deployed
   ```bash
   gcloud run services describe github-executor-api \
     --region=us-central \
     --project=edri2or-mcp
   ```
2. Get service URL
3. Test `/` endpoint (health check)
4. Verify `GITHUB_TOKEN` environment variable

**Who**: Via GitHub Actions workflow (not manual by Or)  
**Risk**: Low - read-only operations  
**Outcome**: Know if service exists and is reachable

### Priority 2: Fix Accept Header Typo

**File**: `cloud-run/google-workspace-github-api/index.js`  
**Line**: 37  
**Change**: `vund.github` → `vnd.github`

**Who**: Claude via PR  
**Risk**: Low - simple bug fix  
**Outcome**: Correct GitHub API headers

### Priority 3: Decision Point - BUS or Direct?

**Option A: Build BUS System**
- Effort: HIGH (new Sheet, polling logic, task schema)
- Benefit: Async task queue for GPTs GO
- Timeline: 3-5 sessions

**Option B: Direct Cloud Run Calls**
- Effort: LOW (GPTs GO calls service directly)
- Benefit: Simpler architecture
- Timeline: 1 session (after deployment verification)

**Option C: Abandon github-executor-api**
- GPTs GO uses GitHub API directly (has credentials)
- Remove Cloud Run service
- Update docs

**Recommendation**: Option B (Direct) or C (Abandon)  
**Reason**: BUS adds complexity without clear benefit

### Priority 4: Deploy or Redeploy Service (if missing)

**Trigger**: `gcloud builds submit` via GitHub Actions  
**Who**: Automated workflow  
**Risk**: Medium - creates/updates Cloud Run service  
**Outcome**: Service becomes reachable

---

## 📝 Next Steps Summary

### Immediate (Phase 1.2 - OS_SAFE)
1. Update CAPABILITIES_MATRIX with findings
2. Update STATE_FOR_GPT_SNAPSHOT
3. Create evidence document
4. Get Or's approval for Phase 2

### After Approval (Phase 2 - CLOUD_OPS_HIGH)
1. Verify deployment status (Workflow)
2. Fix typo (PR)
3. Decision: BUS vs Direct vs Abandon
4. Deploy/test service
5. Update OpenAPI for GPTs GO

---

## 🔐 Compliance Check

### OS_SAFE Operations Performed ✅
- ✅ Read CAPABILITIES_MATRIX.md
- ✅ Read STATE_FOR_GPT_SNAPSHOT.md
- ✅ Read MCP_GPT_CAPABILITIES_BRIDGE.md
- ✅ Read cloud-run service code
- ✅ Searched for BUS references
- ✅ Analyzed workflows
- ✅ Created diagnosis document

### CLOUD_OPS_HIGH Operations NOT Performed ✅
- ❌ Did NOT verify deployment (no gcloud commands)
- ❌ Did NOT call service endpoints
- ❌ Did NOT modify any code
- ❌ Did NOT trigger any workflows
- ❌ Did NOT access Cloud Run console
- ❌ Did NOT check logs

**Conclusion**: Phase 1.1 complete within OS_SAFE boundaries.

---

**END OF PHASE 1.1 DIAGNOSIS**

Awaiting Or's approval to proceed with Phase 1.2 (documentation updates) and Phase 2 planning.
