# GitHub Executor API - GH_EX Secret Status

**Investigation Date**: 2025-11-18  
**Context**: Post-DEEP_SCAN_v1 + Or's strategic decision on GH_EX  
**Status**: 🟡 **PAT EXISTS - SECRET NOT STORED**

---

## 🎯 Strategic Context

Or has confirmed:
- **GitHub PAT created fresh** (minutes ago)
- **GH_EX** designated as canonical secret name for GitHub Executor V1
- **Claude is Executor** - will store and configure secret
- Goal: Store PAT in Secret Manager → Deploy Cloud Run service

---

## 🔍 Current State

### Secret Manager Check

**Result**: ❌ GH_EX does not exist in Secret Manager yet  
**Expected**: PAT was just created, not yet stored in GCP

### Next Steps

**Immediate**: Store PAT in Secret Manager as GH_EX

---

## 🛠️ Execution Plan - Automated Storage

### Phase 1: Store PAT in Secret Manager

**Method**: GitHub Actions workflow (zero manual commands from Or)

**Or's action required**:
1. Navigate to GitHub repo: `edri2or-commits/make-ops-clean`
2. Settings → Secrets and variables → Actions
3. Create new repository secret:
   - Name: `GITHUB_EXECUTOR_PAT`
   - Value: [paste the fresh GitHub PAT]
4. Save

**Claude's automation** (after Or adds secret):
1. Creates workflow: `.github/workflows/store-gh-ex-secret.yml`
2. Workflow uses WIF to authenticate to GCP
3. Workflow stores PAT as `GH_EX` in Secret Manager
4. Workflow grants access to Cloud Run service account
5. Claude triggers workflow via API
6. Claude monitors execution
7. Claude verifies secret created successfully

**Timeline**: ~10 minutes after Or adds repo secret

---

### Phase 2: Deploy GitHub Executor API

**After GH_EX stored**:
1. Claude creates deployment workflow
2. Workflow deploys Cloud Run service with `--set-secrets=GITHUB_TOKEN=GH_EX:latest`
3. Service becomes available at Cloud Run URL
4. Claude tests OS_SAFE endpoints
5. Claude updates CAPABILITIES_MATRIX → VERIFIED

**Timeline**: ~15 minutes after Phase 1 complete

---

## 📋 Technical Details

### Secret Storage Command (via workflow)

```bash
echo "$GITHUB_EXECUTOR_PAT" | gcloud secrets create GH_EX \
  --project=edri2or-mcp \
  --replication-policy=automatic \
  --data-file=-

gcloud secrets add-iam-policy-binding GH_EX \
  --project=edri2or-mcp \
  --member="serviceAccount:github-actions@edri2or-mcp.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### PAT Requirements

- **Scope**: `repo` (full repository access)
- **Organization**: `edri2or-commits`
- **Type**: Classic PAT or fine-grained (both work)
- **Expiration**: Recommend 90 days (can be updated later)

---

## 🎯 Decision: Proceed with Automated Storage

**Or confirms**: PAT created and ready  
**Claude executes**: Automated storage workflow  
**Approval required**: "מאשר כתיבה" (CLOUD_OPS_HIGH - storing secret)

**Waiting for**: Or to add `GITHUB_EXECUTOR_PAT` to repo secrets

---

**Status**: 🟡 **READY TO EXECUTE**  
**Blocker**: Repo secret not added yet  
**Next**: Claude creates storage workflow immediately

---

**Updated**: 2025-11-18  
**Author**: Claude (Executor)