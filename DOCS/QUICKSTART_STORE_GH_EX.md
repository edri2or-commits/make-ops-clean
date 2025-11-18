# Quick Start: Store GitHub PAT as GH_EX

**For**: Or  
**Time**: 5 minutes  
**Goal**: Store fresh GitHub PAT in Secret Manager → Enable GitHub Executor API

---

## 🎯 Your Actions (One-Time Setup)

### Step 1: Add PAT to GitHub Repository Secrets

1. **Navigate**: https://github.com/edri2or-commits/make-ops-clean/settings/secrets/actions

2. **Click**: "New repository secret"

3. **Fill in**:
   - Name: `GITHUB_EXECUTOR_PAT`
   - Secret: [paste the fresh GitHub PAT you just created]

4. **Save**: Click "Add secret"

**That's it!** No other manual action required from you.

---

### Step 2: Trigger Workflow (Claude Will Monitor)

**Option A - Or triggers manually**:
1. Navigate: https://github.com/edri2or-commits/make-ops-clean/actions/workflows/store-gh-ex-secret.yml
2. Click "Run workflow"
3. In the text field, type: `מאשר כתיבה`
4. Click green "Run workflow" button

**Option B - Claude triggers via API**:
- Just tell Claude "go ahead" in chat
- Claude will trigger workflow automatically
- Claude will monitor execution
- Claude will report results

---

## 🤖 What Happens Automatically

### The Workflow Does:

1. ✅ Authenticates to GCP via WIF (no credentials needed)
2. ✅ Reads `GITHUB_EXECUTOR_PAT` from repo secrets
3. ✅ Creates `GH_EX` secret in Secret Manager (edri2or-mcp project)
4. ✅ Grants access to Cloud Run service account
5. ✅ Verifies secret is accessible
6. ✅ Creates evidence file
7. ✅ Uploads artifact for audit trail

### After Success:

**Claude automatically**:
1. Reads workflow results
2. Deploys GitHub Executor API to Cloud Run (using GH_EX)
3. Tests OS_SAFE endpoints (`/`, `/repo/read-file`, `/repo/update-doc`)
4. Updates CAPABILITIES_MATRIX → VERIFIED
5. Creates test evidence files

**Timeline**: ~30 minutes total (10min storage + 15min deployment + 5min testing)

---

## 🔐 Security Notes

**Your PAT**:
- Stored encrypted in GitHub repo secrets
- Transmitted via GitHub Actions (secure)
- Stored in GCP Secret Manager (encrypted at rest)
- Never written to logs or artifacts
- Only accessible to WIF-authenticated service account

**PAT Requirements**:
- Scope: `repo` (full repository access)
- Organization: `edri2or-commits`
- Expiration: Your choice (recommend 90 days, renewable)

---

## 📊 Verification

**Check if secret was stored successfully**:

```bash
# Via workflow logs (after it runs)
# Look for: ✅ GH_EX secret created successfully

# Or ask Claude to verify:
# "Check if GH_EX exists now"
```

**Check if GitHub Executor API is deployed**:

```bash
# Claude will provide Cloud Run URL after deployment
# Format: https://github-executor-api-<hash>-uc.a.run.app
```

---

## ⏭️ Next Steps (All Automated by Claude)

1. **After you add repo secret** → Tell Claude "ready" or "go ahead"
2. **Claude triggers workflow** → Monitors execution
3. **Secret stored** → Claude deploys Cloud Run service
4. **Service deployed** → Claude tests endpoints
5. **Tests pass** → Claude updates CAPABILITIES_MATRIX
6. **Done** → GitHub Executor API fully operational

**You will not need to run any commands or open any consoles.**

---

## ❓ Troubleshooting

**If workflow fails**:
- Claude will read error logs
- Claude will diagnose issue
- Claude will propose fix (usually another workflow)
- Claude will execute fix automatically

**If you're unsure**:
- Just ask Claude "what's the status?"
- Claude will check workflow runs
- Claude will report current state

---

**Ready?** Add the repo secret, then tell Claude to proceed! 🚀