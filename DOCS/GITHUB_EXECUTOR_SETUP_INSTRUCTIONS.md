# GitHub Executor API - Complete Setup Instructions

**For**: Or + GPT Unified  
**Status**: 🟡 Ready to Execute  
**Updated**: 2025-11-18

---

## 🎯 Current Situation

**From repository analysis**:
- Code ready: `cloud-run/google-workspace-github-api/index.js`
- Code expects: `GITHUB_TOKEN` env variable
- Docs specify: `github-executor-api-token` secret in Secret Manager
- Reality: PAT exists as `GH_EX` (location TBD - GitHub Actions secret or Secret Manager)

**Solution**: Unified workflow handles everything automatically

---

## ✅ Prerequisites

**Single requirement**: `GH_EX` must exist as GitHub Actions repository secret

**Check**: Settings → Secrets and variables → Actions → Repository secrets  
**Look for**: Secret named `GH_EX` with GitHub PAT value (repo scope)

**If missing**: Add it now
- Name: `GH_EX`
- Value: GitHub Personal Access Token with `repo` scope
- Organization: `edri2or-commits`

---

## 🚀 Execution (One Command)

**Workflow**: `setup-github-executor-complete.yml`

**What it does automatically**:

### Phase 1: Secret Management
1. Reads `GH_EX` from GitHub Actions secrets
2. Creates/updates `github-executor-api-token` in GCP Secret Manager
3. Grants service account access
4. Verifies secret is accessible

### Phase 2: Deployment
1. Deploys GitHub Executor API to Cloud Run
2. Region: us-central1
3. Binds secret: `GITHUB_TOKEN=github-executor-api-token:latest`
4. Sets environment variables

### Phase 3: E2E Testing
1. **Health Check**: `GET /`
2. **Read File**: `POST /repo/read-file` (reads README.md)
3. **Update Doc**: `POST /repo/update-doc` (creates `DOCS/GITHUB_EXECUTOR_API_TEST_RUN.md`)

### Phase 4: Evidence & Documentation
1. Creates evidence JSON in `OPS/EVIDENCE/`
2. Test results document created by API itself (proves write capability)
3. Git commits evidence file
4. Uploads artifacts

---

## 🎮 How to Run

### Option 1: Manual Trigger (Or)

1. Navigate: https://github.com/edri2or-commits/make-ops-clean/actions/workflows/setup-github-executor-complete.yml

2. Click: "Run workflow"

3. Type: `מאשר כתיבה` (CLOUD_OPS_HIGH approval)

4. Click: Green "Run workflow" button

### Option 2: Claude Triggers (Automated)

Claude can trigger via API when instructed:
- "Go ahead and deploy"
- "Execute the setup"
- "Run the GitHub Executor deployment"

---

## 📊 Expected Results

**Success indicators**:
- ✅ Secret `github-executor-api-token` created in Secret Manager
- ✅ Service deployed: `https://github-executor-api-<hash>-uc.a.run.app`
- ✅ All 3 tests pass (health, read, write)
- ✅ File `DOCS/GITHUB_EXECUTOR_API_TEST_RUN.md` created by API
- ✅ Evidence file in `OPS/EVIDENCE/`

**Workflow output**:
- Service URL (copy this!)
- Test results summary
- Links to evidence

**After success, Claude will**:
1. Read workflow results
2. Extract service URL
3. Update `CAPABILITIES_MATRIX.md`:
   - Section 1.1.2: ⚠️ Planned → ✅ VERIFIED
   - Add service URL
   - Link to test evidence
4. Report status in chat

---

## 🔍 Verification Checklist

After workflow completes, verify:

**1. Secret in Secret Manager**:
```bash
# Claude can check via windows-shell:read_secret
gcloud secrets describe github-executor-api-token --project=edri2or-mcp
```

**2. Service deployed**:
```bash
# Claude can check via workflow results
gcloud run services describe github-executor-api --region=us-central1 --project=edri2or-mcp
```

**3. Test file created**:
- Check: `DOCS/GITHUB_EXECUTOR_API_TEST_RUN.md` exists in repo
- Should contain timestamp and test results

**4. Evidence collected**:
- Check: `OPS/EVIDENCE/github_executor_deployed_*.json` exists
- Should contain service URL and test outcomes

---

## 🚨 Troubleshooting

### If GH_EX secret not found

**Error**: "GH_EX not found in repository secrets"

**Fix**:
1. Go to: https://github.com/edri2or-commits/make-ops-clean/settings/secrets/actions
2. Add repository secret:
   - Name: `GH_EX`
   - Value: [GitHub PAT with repo scope]
3. Re-run workflow

### If deployment fails

**Claude will**:
1. Read error logs from workflow
2. Diagnose specific issue
3. Propose automated fix (another workflow)
4. Execute fix automatically

**Common issues**:
- IAM permissions: Claude creates permission-grant workflow
- Service account: Claude verifies and fixes
- Code errors: Claude checks index.js

### If tests fail

**Health check fails**: Service not responding
- Claude checks logs
- Verifies environment variables
- Checks secret binding

**Read file fails**: GitHub token issue
- Claude verifies token has repo scope
- Checks organization access

**Update doc fails**: Permission or path issue
- Claude checks path is OS_SAFE
- Verifies write permissions

---

## 📋 Post-Deployment Actions

**Automated by Claude**:

1. **Update CAPABILITIES_MATRIX.md**:
```markdown
### 1.1.2 GitHub Executor API v1

**Status**: ✅ VERIFIED  
**Service URL**: [extracted from workflow]  
**Evidence**: DOCS/GITHUB_EXECUTOR_API_TEST_RUN.md, OPS/EVIDENCE/github_executor_deployed_*.json

All endpoints operational:
- Health check: ✅
- Read file (OS_SAFE): ✅
- Update doc (OS_SAFE): ✅
```

2. **Create summary document**: Claude reports in chat

3. **Continue with remaining updates**: Executor model, Google Write, Voice/GUI, etc.

---

## 🔐 Security Notes

**Secret handling**:
- PAT never printed in logs
- Stored encrypted in both GitHub and GCP
- Accessed only by WIF-authenticated service account
- Mounted as environment variable at runtime

**API security**:
- Unauthenticated endpoint (by design for GPT access)
- Path validation enforced server-side
- OS_SAFE paths only: DOCS/, logs/, OPS/, STATE_FOR_GPT/
- Other paths return HTTP 403

---

## ⏭️ Ready to Execute

**Action required from Or**:
1. Verify `GH_EX` exists in repo secrets
2. Trigger workflow (or tell Claude to do it)
3. Type approval: `מאשר כתיבה`

**No other manual actions needed.**

**Timeline**: 5-10 minutes from trigger to completion

---

**Let's deploy! 🚀**