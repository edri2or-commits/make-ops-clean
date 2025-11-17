# Task 2.3 Deployment Plan - github-executor-api

**Document Type**: Deployment Plan (OS_SAFE - Planning Only)  
**Created**: 2025-11-17  
**Status**: 📝 PLAN READY - Awaiting Or's approval for execution  
**Actual Deployment Risk**: CLOUD_OPS_HIGH

---

## 🎯 Executive Summary

**Goal**: Deploy github-executor-api to Cloud Run with fixed code

**Scope of This Document**: PLANNING ONLY
- This document describes what WILL happen during deployment
- NO deployment actions are taken by creating this document
- Actual deployment (CLOUD_OPS_HIGH) requires separate explicit approval

**Prerequisites**:
- ✅ Task 2.1: COMPLETED (runtime status unknown due to observability constraint)
- 🔄 Task 2.2: PR #100 merged (code fix applied)

**Expected Outcome**:
- Service `github-executor-api` deployed to Cloud Run
- URL: `https://github-executor-api-<hash>-uc.a.run.app`
- Health check (`GET /`) returns 200
- Environment variable `GITHUB_TOKEN` configured
- Service ready for testing (Task 2.5)

---

## 🔍 Current State Analysis

### Existing Infrastructure ✅

1. **Docker Configuration**:
   - File: `cloud-run/google-workspace-github-api/Dockerfile`
   - Base image: `node:18-slim`
   - Port: 8080
   - ⚠️ **BUG FOUND**: Line 11 has `CLM` instead of `CMD`
   - **Status**: Needs fix before deployment

2. **Cloud Build Configuration**:
   - File: `cloud-run/google-workspace-github-api/cloudbuild.yaml`
   - Steps: Build → Push → Deploy
   - Image registry: `us-central-docker.pkg.dev/edri2or-mcp/cloud-run-source-deploy/`
   - Service name: `github-executor-api`
   - Region: `us-central`
   - **Status**: Exists and ready (after Dockerfile fix)

3. **Application Code**:
   - File: `cloud-run/google-workspace-github-api/index.js`
   - Dependencies: express, axios, googleapis
   - Entry point: `npm start` → `node index.js`
   - **Status**: Fixed in PR #100 (pending merge)

### Known Issues 🐛

1. **Dockerfile Typo** (CRITICAL):
   - Line 11: `CLM ["npm", "start"]`
   - Should be: `CMD ["npm", "start"]`
   - **Impact**: Container won't start without this fix
   - **Fix required**: BEFORE deployment

2. **Accept Header Typo** (FIXED):
   - Already fixed in PR #100
   - Will be included after merge

3. **Missing Environment Variable** (UNKNOWN):
   - `GITHUB_TOKEN` needs to be configured
   - **Status**: Will verify during deployment

---

## 📋 Deployment Plan (5 Sub-Tasks)

### 2.3.1: Fix Dockerfile Typo (OS_SAFE) ⏳

**Purpose**: Correct critical typo that prevents container from starting

**Method**: PR or direct commit to main (after Task 2.2 merge)

**Change**:
```dockerfile
# Before:
CLM ["npm", "start"]

# After:
CMD ["npm", "start"]
```

**Risk**: NONE (OS_SAFE - code fix only)  
**Can be combined with**: Task 2.2 merge, or separate quick fix

**Decision Point**: 
- Option A: Add to PR #100 before merge (requires PR update)
- Option B: Separate 1-line fix after Task 2.2 merge (faster)
- **Recommendation**: Option B (faster, decoupled)

---

### 2.3.2: Prepare Deployment Workflow (OS_SAFE) ⏳

**Purpose**: Create automated GitHub Actions workflow to trigger Cloud Build

**Why**: Maintains zero-touch principle (no manual gcloud commands)

**Workflow Design**:

**File**: `.github/workflows/deploy-github-executor-api.yml`

```yaml
name: Deploy github-executor-api to Cloud Run

on:
  workflow_dispatch:
    inputs:
      trigger_reason:
        description: 'Reason for deployment'
        required: true
        default: 'Manual deployment'

# Trigger via file: OPS/TRIGGERS/github-executor-deploy.trigger

permissions:
  contents: write  # For writing status files
  id-token: write  # For WIF

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Authenticate to GCP via WIF
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ vars.WIF_PROVIDER_PATH }}
          service_account: ${{ vars.GCP_SA_EMAIL }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Trigger Cloud Build
        id: build
        run: |
          cd cloud-run/google-workspace-github-api
          
          # Submit build to Cloud Build
          BUILD_ID=$(gcloud builds submit \
            --config=cloudbuild.yaml \
            --substitutions=COMMIT_SHA=${{ github.sha }} \
            --format="value(id)")
          
          echo "build_id=$BUILD_ID" >> $GITHUB_OUTPUT
          
          # Wait for build to complete
          gcloud builds log $BUILD_ID --stream

      - name: Get service URL
        id: service
        run: |
          SERVICE_URL=$(gcloud run services describe github-executor-api \
            --region=us-central \
            --format="value(status.url)")
          
          echo "service_url=$SERVICE_URL" >> $GITHUB_OUTPUT
          
          # Get environment variables (check if GITHUB_TOKEN exists)
          ENV_VARS=$(gcloud run services describe github-executor-api \
            --region=us-central \
            --format="json" | jq -r '.spec.template.spec.containers[0].env')
          
          echo "env_vars=$ENV_VARS" >> $GITHUB_OUTPUT

      - name: Write deployment status
        run: |
          mkdir -p OPS/STATUS
          
          cat > OPS/STATUS/github-executor-api-deploy.json <<EOF
          {
            "task": "2.3",
            "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
            "status": "deployed",
            "build_id": "${{ steps.build.outputs.build_id }}",
            "service_url": "${{ steps.service.outputs.service_url }}",
            "revision": "${{ github.sha }}",
            "region": "us-central",
            "project": "edri2or-mcp",
            "environment_variables": ${{ steps.service.outputs.env_vars }},
            "workflow_run": "${{ github.run_id }}",
            "workflow_url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
          }
          EOF
          
          # Also create markdown version
          cat > OPS/STATUS/github-executor-api-deploy.md <<EOF
          # Deployment Status - github-executor-api
          
          **Task**: 2.3  
          **Timestamp**: $(date -u +%Y-%m-%dT%H:%M:%SZ)  
          **Status**: ✅ DEPLOYED
          
          ## Service Details
          - **URL**: ${{ steps.service.outputs.service_url }}
          - **Region**: us-central
          - **Project**: edri2or-mcp
          - **Revision**: ${{ github.sha }}
          - **Build ID**: ${{ steps.build.outputs.build_id }}
          
          ## Next Steps
          - Task 2.4: Verify environment variables
          - Task 2.5: Test endpoint
          EOF
          
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add OPS/STATUS/github-executor-api-deploy.*
          git commit -m "[skip ci] Task 2.3: Deployment status - github-executor-api deployed"
          git push

      - name: Handle deployment failure
        if: failure()
        run: |
          mkdir -p OPS/STATUS
          
          cat > OPS/STATUS/github-executor-api-deploy.json <<EOF
          {
            "task": "2.3",
            "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
            "status": "failed",
            "error": "Deployment failed - check workflow logs",
            "workflow_run": "${{ github.run_id }}",
            "workflow_url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
          }
          EOF
          
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add OPS/STATUS/github-executor-api-deploy.json
          git commit -m "[skip ci] Task 2.3: Deployment FAILED"
          git push || true
```

**Trigger Mechanism**:
```bash
# Claude creates/updates this file to trigger deployment:
echo "trigger" > OPS/TRIGGERS/github-executor-deploy.trigger
git add OPS/TRIGGERS/github-executor-deploy.trigger
git commit -m "Task 2.3: Trigger github-executor-api deployment"
git push
```

**Risk**: NONE (OS_SAFE - workflow creation only)

---

### 2.3.3: Configure Environment Variables (CLOUD_OPS_HIGH) ⏳

**Purpose**: Ensure `GITHUB_TOKEN` is configured in Cloud Run service

**Method**: Two approaches available

**Option A: Via gcloud command (in workflow)**:
```yaml
- name: Set environment variables
  run: |
    gcloud run services update github-executor-api \
      --region=us-central \
      --set-env-vars="GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}" \
      --quiet
```

**Option B: Via cloudbuild.yaml update**:
```yaml
# Add to deploy step in cloudbuild.yaml:
- '--set-env-vars=GITHUB_TOKEN=$$GITHUB_TOKEN'

# And add substitutions:
substitutions:
  _GITHUB_TOKEN: ${_GITHUB_TOKEN}
```

**Recommended**: Option A (cleaner, decoupled from build)

**Secret Source**: `${{ secrets.GITHUB_TOKEN }}` (must be added to GitHub Secrets)

**Verification**:
- Workflow will capture env vars in status file
- Task 2.4 will verify explicitly

**Risk**: MEDIUM (modifies service configuration)  
**Rollback**: Remove env var via `gcloud run services update --clear-env-vars`

---

### 2.3.4: Smoke Tests (CLOUD_OPS_SAFE) ⏳

**Purpose**: Verify basic service health immediately after deployment

**Method**: Built into deployment workflow

```yaml
- name: Smoke test - Health check
  run: |
    SERVICE_URL="${{ steps.service.outputs.service_url }}"
    
    # Test health endpoint
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SERVICE_URL/")
    
    if [ "$HTTP_CODE" != "200" ]; then
      echo "❌ Health check failed: HTTP $HTTP_CODE"
      exit 1
    fi
    
    echo "✅ Health check passed: HTTP 200"
    
    # Test response content
    RESPONSE=$(curl -s "$SERVICE_URL/")
    echo "Response: $RESPONSE"
    
    # Verify expected response
    if echo "$RESPONSE" | grep -q '"status":"ok"'; then
      echo "✅ Service response valid"
    else
      echo "❌ Unexpected service response"
      exit 1
    fi
```

**Expected Results**:
- HTTP 200 status code
- Response body: `{"service":"google-workspace-github-api","status":"ok"}`

**On Failure**: 
- Deployment marked as failed
- Rollback triggered (see 2.3.5)

**Risk**: LOW (read-only operation)

---

### 2.3.5: Rollback Strategy (CLOUD_OPS_HIGH) ⏳

**Purpose**: Revert to previous working state if deployment fails

**Trigger Conditions**:
1. Build failure (Docker build fails)
2. Deployment failure (Cloud Run deploy fails)
3. Smoke test failure (health check fails)
4. Post-deployment issues reported by Or

**Rollback Methods**:

**Method 1: Revert to previous revision (if service existed)**:
```bash
# Get previous revision
PREVIOUS_REV=$(gcloud run revisions list \
  --service=github-executor-api \
  --region=us-central \
  --format="value(REVISION)" \
  --limit=2 | tail -n 1)

# Route 100% traffic back to previous revision
gcloud run services update-traffic github-executor-api \
  --region=us-central \
  --to-revisions=$PREVIOUS_REV=100 \
  --quiet
```

**Method 2: Delete service (if this was first deployment)**:
```bash
gcloud run services delete github-executor-api \
  --region=us-central \
  --quiet
```

**Method 3: Emergency stop**:
```bash
# Set min instances to 0 (stop serving traffic)
gcloud run services update github-executor-api \
  --region=us-central \
  --min-instances=0 \
  --quiet
```

**Automated Rollback** (built into workflow):
```yaml
- name: Rollback on failure
  if: failure()
  run: |
    echo "⚠️ Deployment failed, attempting rollback..."
    
    # Try to revert to previous revision
    PREVIOUS_REV=$(gcloud run revisions list \
      --service=github-executor-api \
      --region=us-central \
      --format="value(REVISION)" \
      --limit=2 | tail -n 1 || echo "")
    
    if [ -n "$PREVIOUS_REV" ]; then
      echo "Rolling back to revision: $PREVIOUS_REV"
      gcloud run services update-traffic github-executor-api \
        --region=us-central \
        --to-revisions=$PREVIOUS_REV=100 \
        --quiet
      echo "✅ Rollback complete"
    else
      echo "⚠️ No previous revision found - service may be new"
    fi
```

**Risk**: MEDIUM (modifies service state)  
**Success Rate**: High (proven gcloud commands)

---

## 🔄 Execution Sequence

```
Pre-Deployment (OS_SAFE):
  ├─ 2.3.1: Fix Dockerfile (CLM → CMD)
  ├─ 2.3.2: Create deployment workflow
  └─ Or approves for CLOUD_OPS_HIGH execution
       │
Deployment (CLOUD_OPS_HIGH):
  ├─ Trigger workflow via file commit
  ├─ WIF authentication
  ├─ Cloud Build: Build → Push image
  ├─ Cloud Run: Deploy service
  ├─ 2.3.3: Configure GITHUB_TOKEN env var
  ├─ 2.3.4: Smoke tests (health check)
  └─ Write status to OPS/STATUS/*.json
       │
       ├─ SUCCESS → Proceed to Task 2.4
       └─ FAILURE → 2.3.5: Automatic rollback
```

---

## 📊 Success Criteria

**Deployment is successful when**:
1. ✅ Cloud Build completes without errors
2. ✅ Service deployed to Cloud Run (revision created)
3. ✅ Health check returns HTTP 200
4. ✅ Service URL is accessible
5. ✅ `GITHUB_TOKEN` environment variable is set
6. ✅ Status files written to `OPS/STATUS/`

**Evidence Required**:
- Build ID from Cloud Build
- Service URL from Cloud Run
- HTTP 200 response from health check
- Environment variables list (redacted token value)
- Status JSON file in repo

---

## 🔐 Security & Permissions

### Required GCP Permissions (via WIF)

Service account `${{ vars.GCP_SA_EMAIL }}` needs:
- `cloudbuild.builds.create` - Submit builds
- `cloudbuild.builds.get` - Monitor build status
- `run.services.create` - Create Cloud Run service (if new)
- `run.services.update` - Update Cloud Run service
- `run.services.get` - Get service details
- `iam.serviceAccounts.actAs` - Deploy as service account

**Verification**: These permissions should already be configured from previous WIF setup

### Required GitHub Secrets

- `GITHUB_TOKEN` - Must be added to repository secrets
  - Scope: Repo access for github-executor-api operations
  - Will be passed to Cloud Run as environment variable

### Network & IAM

- Service will be deployed with `--allow-unauthenticated` (for GPTs GO access)
- Alternative: Use IAM for GPTs GO authentication (future enhancement)

---

## ⚠️ Risk Assessment

| Component | Risk Level | Mitigation |
|-----------|-----------|------------|
| Dockerfile fix | LOW | Simple 1-char change, easy to verify |
| Workflow creation | NONE | OS_SAFE, no execution |
| Cloud Build | MEDIUM | Automated rollback on failure |
| Cloud Run deploy | MEDIUM | Previous revision rollback available |
| Env var config | MEDIUM | Can be removed/updated easily |
| Smoke tests | LOW | Read-only verification |
| Overall deployment | MEDIUM | Multiple safety mechanisms in place |

---

## 📋 Pre-Execution Checklist

Before triggering Task 2.3 deployment:

- [ ] Task 2.2 (PR #100) merged
- [ ] Dockerfile typo fixed (CLM → CMD)
- [ ] Deployment workflow created (`.github/workflows/deploy-github-executor-api.yml`)
- [ ] `GITHUB_TOKEN` added to GitHub repository secrets
- [ ] WIF permissions verified
- [ ] Or has reviewed and approved this PLAN
- [ ] Or has explicitly approved CLOUD_OPS_HIGH execution

---

## 🔄 Post-Deployment Actions

After successful deployment:

1. **Immediate** (automated):
   - Status files written to `OPS/STATUS/`
   - Service URL documented
   - Revision SHA recorded

2. **Task 2.4** (next):
   - Verify environment variables explicitly
   - Confirm `GITHUB_TOKEN` is accessible

3. **Task 2.5** (next):
   - Test `/github/update-file` endpoint
   - Verify full functionality

4. **Documentation** (Task 2.7):
   - Update CAPABILITIES_MATRIX
   - Update STATE_FOR_GPT_SNAPSHOT
   - Mark github-executor-api as ✅ Verified

---

## 💡 Decision Points for Or

**Before approving Task 2.3 execution, Or needs to decide**:

1. **Dockerfile Fix Approach**:
   - [ ] Option A: Add to PR #100 (delays merge slightly)
   - [ ] Option B: Separate quick fix after Task 2.2 merge
   - **Recommendation**: Option B

2. **Env Var Configuration**:
   - [ ] Add `GITHUB_TOKEN` to GitHub Secrets now
   - [ ] Defer until deployment time
   - **Recommendation**: Add now to avoid delays

3. **Deployment Timing**:
   - [ ] Deploy immediately after Task 2.2 merge
   - [ ] Wait for Or's explicit "GO" command
   - **Recommendation**: Wait for explicit GO

---

## 📝 Status

**Document Status**: ✅ PLAN COMPLETE (OS_SAFE)  
**Deployment Status**: ⏳ AWAITING OR'S APPROVAL  
**Next Action**: Or reviews plan → Approves CLOUD_OPS_HIGH execution → Claude triggers deployment

---

**Maintained by**: Claude  
**Created**: 2025-11-17  
**Last Updated**: 2025-11-17
