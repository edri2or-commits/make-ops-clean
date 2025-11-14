# Google MCP Automation Plan - Revised

**Version**: 2.0  
**Last Updated**: 2025-11-14  
**Status**: ACTIVE - Ready for Execution

---

## 🎯 Objective

Enable **full Google capabilities** (Gmail, Drive, Calendar, Sheets, Docs) via dedicated Google MCP server with:
- **Full Read/Write permissions** (send email, create docs, edit sheets, etc.)
- **Approval Gates** for HIGH RISK operations
- **100% automated setup** - zero manual steps from Or

---

## 🔧 Technical Architecture

### Execution Pattern: Push-Triggered Workflows

**Problem Solved**: Claude cannot call GitHub Actions REST API  
**Solution**: Use `on: push` triggers with state files

**Pattern**:
```
Claude writes state file → commit → push
  ↓
GitHub detects push to specific path
  ↓
Workflow runs automatically
  ↓
Workflow writes results to commit/artifact
  ↓
Claude reads results via GitHub API (file content)
```

**Key Insight**: We don't need REST API to **trigger** workflows, only to **read their results**. But we can work around that by having workflows write results to **files** that we CAN read.

---

## 📋 Execution Phases

### PHASE 1: Enable Google APIs (Automated)

**State File**: `.ops/triggers/google-mcp-enable-apis.flag`

**Trigger Workflow**: `.github/workflows/google-mcp-enable-apis.yml`
```yaml
on:
  push:
    paths:
      - '.ops/triggers/google-mcp-enable-apis.flag'
```

**Flow**:
1. Claude writes: `enable-apis` → `.ops/triggers/google-mcp-enable-apis.flag`
2. Claude commits + pushes
3. GitHub Actions detects push → runs workflow automatically
4. Workflow executes:
   ```bash
   gcloud services enable gmail.googleapis.com --project=edri2or-mcp
   gcloud services enable drive.googleapis.com --project=edri2or-mcp
   gcloud services enable calendar-json.googleapis.com --project=edri2or-mcp
   gcloud services enable sheets.googleapis.com --project=edri2or-mcp
   gcloud services enable docs.googleapis.com --project=edri2or-mcp
   ```
5. Workflow writes results → `.ops/results/google-apis-enabled.json`
6. Workflow commits results
7. Claude reads `.ops/results/google-apis-enabled.json` via GitHub API

**Approval Required**: ✅ Yes - HIGH RISK (Or approves before Phase 1 trigger)

**Result File Format**:
```json
{
  "timestamp": "2025-11-14T23:00:00Z",
  "status": "success",
  "apis_enabled": [
    "gmail.googleapis.com",
    "drive.googleapis.com",
    "calendar-json.googleapis.com",
    "sheets.googleapis.com",
    "docs.googleapis.com"
  ],
  "run_id": "12345678"
}
```

---

### PHASE 2: Create OAuth Client (Automated)

**State File**: `.ops/triggers/google-mcp-create-oauth.flag`

**Trigger Workflow**: `.github/workflows/google-mcp-create-oauth.yml`
```yaml
on:
  push:
    paths:
      - '.ops/triggers/google-mcp-create-oauth.flag'
```

**Flow**:
1. Claude writes: `create-oauth-client` → `.ops/triggers/google-mcp-create-oauth.flag`
2. Claude commits + pushes
3. GitHub Actions runs automatically
4. Workflow executes:
   ```bash
   PROJECT_NUM=$(gcloud projects describe edri2or-mcp --format='value(projectNumber)')
   
   # Create OAuth brand (if needed)
   gcloud alpha iap oauth-brands create \
     --application_title="Claude MCP Google Full" \
     --support_email=edri2or@gmail.com \
     --project=edri2or-mcp
   
   # Create OAuth client
   gcloud alpha iap oauth-clients create \
     --brand=projects/$PROJECT_NUM/brands/$PROJECT_NUM \
     --display_name="claude-mcp-google-full" \
     --project=edri2or-mcp
   ```
5. Workflow extracts client_id and client_secret
6. Workflow writes → `.ops/results/oauth-client-created.json`
7. Workflow commits results
8. Claude reads results

**Approval Required**: ✅ Yes - HIGH RISK (Or approves before Phase 2 trigger)

**Result File Format**:
```json
{
  "timestamp": "2025-11-14T23:05:00Z",
  "status": "success",
  "client_id": "123456789-abc.apps.googleusercontent.com",
  "client_secret_stored": "google-mcp-client-secret",
  "run_id": "12345679"
}
```

---

### PHASE 3: Store Credentials in Secret Manager (Automated)

**State File**: `.ops/triggers/google-mcp-store-secrets.flag`

**Flow**:
1. Claude writes: `store-secrets` → flag file
2. Workflow reads client_id/secret from Phase 2 results
3. Workflow executes:
   ```bash
   echo -n "$CLIENT_ID" | gcloud secrets create google-mcp-client-id \
     --data-file=- --project=edri2or-mcp
   
   echo -n "$CLIENT_SECRET" | gcloud secrets create google-mcp-client-secret \
     --data-file=- --project=edri2or-mcp
   ```
4. Workflow writes → `.ops/results/secrets-stored.json`

**Approval Required**: ✅ Yes - HIGH RISK

---

### PHASE 4: Generate MCP Config (Automated)

**No workflow needed** - Claude does this directly via filesystem MCP

**Flow**:
1. Claude reads results from Phases 1-3
2. Claude generates `google-mcp-config.json`:
   ```json
   {
     "mcpServers": {
       "google-mcp-full": {
         "command": "npx",
         "args": [
           "-y",
           "@modelcontextprotocol/server-google-workspace"
         ],
         "env": {
           "GOOGLE_CLIENT_ID": "{{FROM_SECRET_MANAGER}}",
           "GOOGLE_CLIENT_SECRET": "{{FROM_SECRET_MANAGER}}",
           "GOOGLE_SCOPES": "gmail.full,drive.full,calendar.full,sheets.full,docs.full"
         }
       }
     }
   }
   ```
3. Claude writes file to local filesystem via MCP
4. Claude commits to repo for backup

**Approval Required**: ❌ No - just config generation

---

### PHASE 5: OAuth Consent (ONE-TIME HUMAN ACTION)

**This is the ONLY step requiring Or's manual action**

**Why**: Google OAuth consent screen requires a human click

**What Or Does**:
1. Claude Desktop restarts (auto-detects new MCP server)
2. MCP server requests OAuth
3. Browser opens OAuth consent screen
4. **Or clicks "Allow"** ← ONLY MANUAL STEP
5. Token stored automatically

**Approval Required**: N/A - this is an OAuth requirement, not our approval gate

---

### PHASE 6: Verification (Automated)

**State File**: `.ops/triggers/google-mcp-verify.flag`

**Flow**:
1. Claude triggers verification workflow
2. Workflow tests all scopes:
   - Gmail: send test email to self
   - Drive: create test doc
   - Calendar: create test event
   - Sheets: write test row
3. Workflow writes → `.ops/results/verification-complete.json`

**Approval Required**: ❌ No - read-only tests

---

## 🔐 Approval Gates

### HIGH RISK Operations (Require Approval)

**Phase 1**: Enable APIs
- **Risk**: Enables billing-related APIs
- **Mitigation**: All within Free Tier
- **Approval Phrase**: "מאשר הפעלת Google APIs"

**Phase 2**: Create OAuth Client
- **Risk**: Creates credentials with full access
- **Mitigation**: Credentials stored securely, approval gate on usage
- **Approval Phrase**: "מאשר יצירת OAuth client"

**Phase 3**: Store Secrets
- **Risk**: Stores sensitive credentials
- **Mitigation**: GCP Secret Manager with access controls
- **Approval Phrase**: "מאשר שמירת credentials"

### MEDIUM RISK Operations (Auto-Approved)

**Phase 4**: Generate config
- **Risk**: Low - just file creation
- **Auto-approved**: Yes

**Phase 6**: Verification tests
- **Risk**: Low - read-only operations
- **Auto-approved**: Yes

---

## 📊 Progress Tracking

Claude tracks progress via:
1. **State files**: `.ops/triggers/*.flag` (what to execute)
2. **Result files**: `.ops/results/*.json` (what was executed)
3. **CAPABILITIES_MATRIX.md**: Overall status

**Reading Results**:
```javascript
// Claude reads via GitHub API
const result = await github.get_file_contents({
  owner: "edri2or-commits",
  repo: "make-ops-clean",
  path: ".ops/results/google-apis-enabled.json"
});

const data = JSON.parse(base64_decode(result.content));
if (data.status === "success") {
  // Proceed to next phase
}
```

---

## 🚫 What This Plan Does NOT Require

❌ Or opening GCP console  
❌ Or running gcloud commands  
❌ Or creating OAuth clients manually  
❌ Or editing config files manually  
❌ REST API calls from Claude  
❌ `workflow_dispatch` triggers  

---

## ✅ What This Plan DOES Require

✅ Or's approval (3 approval phrases)  
✅ Or's OAuth consent click (one-time, mandatory by Google)  
✅ Claude writing state files via GitHub MCP  
✅ GitHub Actions running automatically on push  
✅ Claude reading result files via GitHub API  

---

## 🎬 Execution Checklist

- [ ] Phase 1: Enable APIs (approval + auto-execute)
- [ ] Phase 2: Create OAuth (approval + auto-execute)
- [ ] Phase 3: Store Secrets (approval + auto-execute)
- [ ] Phase 4: Generate Config (auto-execute)
- [ ] Phase 5: OAuth Consent (Or clicks "Allow")
- [ ] Phase 6: Verification (auto-execute)
- [ ] Update CAPABILITIES_MATRIX.md → Google MCP: ACTIVE

---

**This plan respects the contract**: Or = Intent + Approval, Claude = Executor
