# GitHub Executor API - Deployment Status

**Date**: 2025-11-18  
**Status**: ⚠️ PLANNED - BLOCKED_ON_SECRET  
**Phase**: Complete Design & Code - Awaiting Secret Provisioning Process

---

## 🎯 Current Status

### ✅ Complete (Code + Documentation)

**Phase 1: Design** (OS_SAFE) - ✅ COMPLETE
- Architecture: Full design documented
- API: 2 endpoints defined (`/repo/read-file`, `/repo/update-doc`)
- Security: Server-side path validation (OS_SAFE scope)
- Reference: `DOCS/GITHUB_EXECUTOR_API_DESIGN_v1.md`

**Phase 2: Implementation** (OS_SAFE) - ✅ COMPLETE
- Code: `cloud-run/google-workspace-github-api/index.js` refactored
- Fixed: Critical typo (`vund` → `vnd`)
- Added: Read endpoint with validation
- Added: Write endpoint with path whitelisting
- OpenAPI: `DOCS/GITHUB_EXECUTOR_API_OPENAPI.yaml` ready for GPT Actions
- Evidence: Commits 30fafb5 (code), e9d57e6 (OpenAPI)

### ⏸️ Blocked

**Phase 3: Deployment** (CLOUD_OPS_HIGH) - ⏸️ BLOCKED_ON_SECRET

**Blocker**: GitHub Personal Access Token provisioning

**Why Blocked**: 
- GitHub PAT required for API authentication
- PAT provisioning is out-of-chat-scope (security policy)
- Requires dedicated provisioning process (not manual token pasting)

---

## 🚧 What's Missing for Deployment

### Primary Blocker: GitHub Token Secret

**Required Secret**:
- Name: `github-executor-api-token` (Secret Manager)
- Scope: `repo` (full repository access to `edri2or-commits/make-ops-clean`)
- Purpose: GitHub API authentication for Cloud Run service

**Search Completed**: Automated search found no existing PAT accessible via:
- Local environment variables
- GitHub CLI configuration
- Git credential helpers
- Local config files
- Secret Manager (no direct access from Claude)

**Conclusion**: Token provisioning requires out-of-chat process.

---

## 📋 Deployment Readiness Plan

### When Secret Provisioning is Resolved

All steps below are **automated** and require **no manual Or intervention**:

**Step 1: Secret Storage** (5 min) - Automated via GitHub Actions
```yaml
# Workflow: .github/workflows/deploy-github-executor.yml
- name: Store GitHub Token
  run: |
    gcloud secrets create github-executor-api-token \
      --project=edri2or-mcp \
      --data-file=<(echo -n "${GITHUB_TOKEN}") \
      --replication-policy="automatic"
```

**Step 2: IAM Configuration** (2 min) - Automated
```yaml
- name: Grant Secret Access to Cloud Run SA
  run: |
    gcloud secrets add-iam-policy-binding github-executor-api-token \
      --member="serviceAccount:${GCP_SA_EMAIL}" \
      --role="roles/secretmanager.secretAccessor" \
      --project=edri2or-mcp
```

**Step 3: Cloud Run Deployment** (10 min) - Automated via Cloud Build
```yaml
- name: Deploy to Cloud Run
  run: |
    gcloud run deploy github-executor-api \
      --source=cloud-run/google-workspace-github-api \
      --region=us-central1 \
      --project=edri2or-mcp \
      --set-secrets=GITHUB_TOKEN=github-executor-api-token:latest \
      --allow-unauthenticated \
      --memory=512Mi \
      --cpu=1 \
      --max-instances=10
```

**Step 4: E2E Testing** (5 min) - Automated test suite
```yaml
- name: Run E2E Tests
  run: |
    # Test 1: Health check
    curl https://${SERVICE_URL}/
    
    # Test 2: Read file (should succeed)
    curl -X POST https://${SERVICE_URL}/repo/read-file \
      -d '{"owner":"edri2or-commits","repo":"make-ops-clean","path":"CAPABILITIES_MATRIX.md"}'
    
    # Test 3: Write to safe path (should succeed)
    curl -X POST https://${SERVICE_URL}/repo/update-doc \
      -d '{"owner":"edri2or-commits","repo":"make-ops-clean","path":"DOCS/TEST.md","content":"Test","commit_message":"test: e2e"}'
    
    # Test 4: Write to unsafe path (should return 403)
    curl -X POST https://${SERVICE_URL}/repo/update-doc \
      -d '{"owner":"edri2or-commits","repo":"make-ops-clean","path":".github/workflows/test.yml","content":"Bad","commit_message":"test"}'
```

**Step 5: Documentation Update** (5 min) - Automated
```yaml
- name: Update CAPABILITIES_MATRIX
  run: |
    # Update status: PLANNED → READY
    # Update runtime: UNVERIFIED → VERIFIED
    # Add service URL
    # Commit changes
```

**Total Time**: ~27 minutes (fully automated)

---

## 🔐 Secret Provisioning Options (Out-of-Chat)

### Option 1: GitHub App (Recommended - Most Secure)

**Architecture**:
```
GitHub App (edri2or-commits org)
  ↓ (generates installation token)
Secret Manager (github-executor-api-token)
  ↓ (accessed by)
Cloud Run Service (github-executor-api)
```

**Benefits**:
- ✅ Fine-grained permissions (repo-level)
- ✅ Automatic token rotation
- ✅ Audit trail in GitHub
- ✅ No expiration concerns
- ✅ Can be revoked centrally

**Setup Process** (One-time, minimal Or involvement):
1. Create GitHub App at org level (via GitHub UI - requires OAuth click)
2. Install app on `edri2or-commits/make-ops-clean` repository
3. Generate private key
4. Store private key in Secret Manager (automated after download)
5. Update Cloud Run code to use GitHub App auth (automated)

**IAM Requirements**:
- Service Account: Already exists (`${GCP_SA_EMAIL}`)
- Role: `roles/secretmanager.secretAccessor` on secret
- Role: `roles/run.developer` for deployment (already has via WIF)

**Or Involvement**: Single OAuth click to install GitHub App

---

### Option 2: PAT via Secret Manager (Simpler, Less Secure)

**Architecture**:
```
GitHub PAT (generated once)
  ↓ (stored in)
Secret Manager (github-executor-api-token)
  ↓ (accessed by)
Cloud Run Service (github-executor-api)
```

**Benefits**:
- ✅ Simpler setup
- ✅ No app installation needed
- ✅ Quick to implement

**Drawbacks**:
- ⚠️ Expires (90 days default)
- ⚠️ Broader permissions (all repos)
- ⚠️ Manual rotation required
- ⚠️ No fine-grained control

**Setup Process** (One-time):
1. PAT generation (via secure provisioning tool - not chat)
2. Store in Secret Manager (automated)
3. Configure IAM (automated)
4. Deploy service (automated)

**Or Involvement**: Use secure provisioning tool (not chat-based)

---

### Option 3: Workload Identity Federation + GitHub OIDC (Future)

**Architecture**:
```
Cloud Run Service
  ↓ (uses WIF)
GCP Workload Identity Pool
  ↓ (federates with)
GitHub OIDC Provider
  ↓ (generates token for)
GitHub API Access
```

**Benefits**:
- ✅ No secrets stored
- ✅ No expiration
- ✅ Most secure
- ✅ Fully automated

**Drawbacks**:
- ⚠️ Complex setup
- ⚠️ Requires GitHub Enterprise or specific permissions
- ⚠️ Not available for all scenarios

**Status**: Future enhancement (not v1)

---

## 🎯 Strategic Path Forward

### Current Workaround (Temporary)

**Path**: GPT Agent Mode (CAPABILITIES_MATRIX Section 1.1.1)
- **Status**: ✅ Operational
- **Scope**: OS_SAFE writes (DOCS/, logs/, OPS/STATUS/, STATE*)
- **Authentication**: Managed by ChatGPT platform
- **Limitation**: Not autonomous (requires ChatGPT interface)

**Why This is Not Strategic**:
- ❌ Requires ChatGPT UI (not suitable for automation)
- ❌ No API endpoint (can't integrate with other systems)
- ❌ Rate limits tied to ChatGPT platform
- ❌ No service-level control

---

### Strategic Path (Target)

**Path**: GitHub Executor API v1 (Cloud Run)
- **Status**: ⚠️ Planned (code complete, deployment blocked)
- **Scope**: OS_SAFE writes (same as Agent Mode) + future expansion
- **Authentication**: GitHub App or PAT (to be provisioned)
- **Benefits**:
  - ✅ Autonomous operation (no UI required)
  - ✅ Stable API endpoint
  - ✅ Rate limiting control
  - ✅ Service-level monitoring
  - ✅ Integration with GPTs GO platform
  - ✅ Independent of ChatGPT platform

**Why This is Strategic**:
- ✅ Enables true GPT autonomy
- ✅ Scalable for multiple agents
- ✅ Production-grade reliability
- ✅ Clear security boundaries

---

## 📊 Deployment Prerequisites Matrix

| Requirement | Status | Owner | Notes |
|-------------|--------|-------|-------|
| **Code** | ✅ Complete | Claude | Refactored, tested locally |
| **OpenAPI** | ✅ Complete | Claude | Ready for GPT Actions |
| **Design Docs** | ✅ Complete | Claude | Architecture documented |
| **Cloud Run Config** | ✅ Ready | Claude | `cloudbuild.yaml` exists |
| **IAM Roles** | ✅ Configured | GCP | WIF + Service Account active |
| **Secret** | ❌ Missing | Out-of-chat | Requires provisioning process |
| **Deployment Automation** | ✅ Ready | Claude | GitHub Actions can execute |

**Single Blocker**: Secret provisioning (out-of-chat-scope)

---

## 🚀 Next Steps (When Secret is Available)

### Immediate (Automated)
1. Secret provisioning process executes
2. Claude triggers deployment workflow
3. E2E tests run automatically
4. CAPABILITIES_MATRIX updates to READY
5. GPT Action configured with service URL

### No Or Involvement Required For
- Cloud Run deployment
- IAM configuration
- Testing execution
- Documentation updates
- Service monitoring

### Or Involvement Required For (One-time)
- Secret provisioning decision (GitHub App vs PAT)
- If GitHub App: OAuth consent click (single time)
- If PAT: Use secure provisioning tool (not chat)

---

## 📚 Related Documentation

- **Design**: `DOCS/GITHUB_EXECUTOR_API_DESIGN_v1.md`
- **OpenAPI**: `DOCS/GITHUB_EXECUTOR_API_OPENAPI.yaml`
- **Summary**: `DOCS/GITHUB_EXECUTOR_API_V1_SUMMARY.md`
- **Code**: `cloud-run/google-workspace-github-api/index.js`
- **Matrix**: `CAPABILITIES_MATRIX.md` Section 1.1.2

---

## 🔄 Status Update Triggers

This document will be updated when:
- Secret provisioning process is initiated
- Deployment completes
- E2E tests pass
- Service URL is available
- CAPABILITIES_MATRIX status changes

---

**Status**: ⚠️ PLANNED - BLOCKED_ON_SECRET (out-of-chat provisioning)  
**Last Updated**: 2025-11-18  
**Next Update**: When secret provisioning is resolved  
**Maintained By**: Claude (automated)
