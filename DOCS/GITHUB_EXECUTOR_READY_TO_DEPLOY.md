# GitHub Executor API v1 - Ready for Deployment

**Status**: 🟢 **READY TO DEPLOY**  
**Updated**: 2025-11-18 (after GH_EX created)

---

## ✅ Prerequisites Complete

1. **GH_EX Secret**: ✅ Created in Secret Manager (13 minutes ago per screenshot)
2. **Code**: ✅ Complete in `cloud-run/google-workspace-github-api/`
3. **Deployment Workflow**: ✅ Created (`.github/workflows/deploy-github-executor.yml`)
4. **Documentation**: ✅ Complete (Design, OpenAPI, Status docs)

---

## 🚀 Deployment Instructions

### For Or: Single Action Required

**Type**: "מאשר כתיבה" (CLOUD_OPS_HIGH approval)  
**Reason**: Deploying Cloud Run service + running tests

**How to deploy**:

1. Navigate to: https://github.com/edri2or-commits/make-ops-clean/actions/workflows/deploy-github-executor.yml

2. Click "Run workflow"

3. In the confirmation field, type: `מאשר כתיבה`

4. Click green "Run workflow" button

**That's it!** The workflow will:
- Verify GH_EX is accessible
- Grant service account permissions if needed
- Deploy to Cloud Run (us-central1)
- Test 3 endpoints (health, read-file, update-doc)
- Create evidence file
- Provide service URL

**Timeline**: ~5-10 minutes

---

## 🤖 What the Workflow Does

### Phase 1: Verification
- Checks GH_EX exists in Secret Manager ✅
- Verifies service account can access it
- Grants permissions if needed

### Phase 2: Deployment
- Deploys GitHub Executor API to Cloud Run
- Region: us-central1
- Service: github-executor-api
- Secret binding: GITHUB_TOKEN=GH_EX:latest
- Environment: GITHUB_OWNER=edri2or-commits, GITHUB_REPO=make-ops-clean

### Phase 3: Testing (OS_SAFE)
- **Health check**: `GET /`
- **Read file**: `POST /repo/read-file` (reads DOCS/QUICKSTART_STORE_GH_EX.md)
- **Update doc**: `POST /repo/update-doc` (creates test file in OPS/EVIDENCE/)

### Phase 4: Evidence
- Creates JSON evidence file
- Uploads as workflow artifact
- Updates GitHub step summary with results

---

## 📊 Expected Outcomes

**If all tests pass**:
- Service URL: `https://github-executor-api-<hash>-uc.a.run.app`
- Status: VERIFIED (all 3 endpoints operational)
- Next: Claude updates CAPABILITIES_MATRIX → GitHub Executor API v1 = VERIFIED

**If tests fail**:
- Workflow logs will show specific error
- Claude will diagnose and propose fix
- Usually: IAM permissions or code issue
- Fix via another workflow (no manual commands)

---

## 🎯 Post-Deployment

**After successful deployment, Claude will**:
1. Read workflow results
2. Extract service URL
3. Update CAPABILITIES_MATRIX.md:
   - Section 1.1.2: GitHub Executor API v1
   - Status: ⚠️ Planned → ✅ VERIFIED
   - Service URL documented
   - Evidence links added
4. Update deployment status docs
5. Test additional scenarios (if needed)

**GPT-CEO will then have**:
- Stable API endpoint for GitHub operations
- OS_SAFE read/write (DOCS/, OPS/STATUS/, STATE_FOR_GPT/)
- Alternative to GPT Agent Mode
- Both paths working (Agent Mode + API)

---

## 🔐 Security Notes

**Secret Access**:
- GH_EX stored encrypted in Secret Manager
- Accessed only by WIF-authenticated service account
- Mounted as environment variable in Cloud Run
- Never logged or exposed in responses

**API Authorization**:
- Service is `--allow-unauthenticated` (by design for GPT access)
- Path validation enforced server-side
- OS_SAFE paths only (DOCS/, logs/, OPS/STATUS/, STATE_FOR_GPT/)
- CLOUD_OPS_HIGH paths return HTTP 403

---

## ⚡ Quick Commands for Or

**Deploy now**:
```
Navigate to Actions → "Deploy GitHub Executor API v1" → Run workflow
Type: מאשר כתיבה
```

**Check status after**:
```
Just ask Claude: "What's the deployment status?"
Claude will check workflow results and report
```

**If issues**:
```
Ask Claude: "Diagnose the deployment error"
Claude will read logs and propose automated fix
```

---

**Ready to deploy!** 🚀

**No manual commands needed from Or beyond the workflow trigger + approval phrase.**