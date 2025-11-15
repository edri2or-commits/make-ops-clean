# Google MCP Automation Plan - BLOCKED

**Version**: 2.1  
**Last Updated**: 2025-11-15  
**Status**: ❌ BLOCKED - Awaiting GitHub Actions Fix

---

## 🎯 Objective

Enable **full Google capabilities** (Gmail, Drive, Calendar, Sheets, Docs) via dedicated Google MCP server with:
- **Full Read/Write permissions** (send email, create docs, edit sheets, etc.)
- **Approval Gates** for HIGH RISK operations
- **100% automated setup** - zero manual steps from Or

**Current Status**: **Cannot proceed** - See "Known Limitations" section below

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

### PHASE 1: Enable Google APIs (Automated) ❌ BLOCKED

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

**Current Status**: ❌ **BLOCKED** - Workflow does not trigger (Step 3 fails)

**Result File Format** (when unblocked):
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

### PHASE 2-6: ❌ BLOCKED (Depend on Phase 1)

All subsequent phases require Phase 1 completion.

**Phase 2**: Create OAuth Client → BLOCKED  
**Phase 3**: Store Credentials → BLOCKED  
**Phase 4**: Generate MCP Config → BLOCKED  
**Phase 5**: OAuth Consent → BLOCKED  
**Phase 6**: Verification → BLOCKED

---

## ⚠️ Known Limitations

### GitHub Actions Workflow Triggering

**Issue**: Workflows created by Claude via GitHub MCP do not trigger automatically on `on: push` events.

**Evidence**: 
- 7+ workflows created with various trigger patterns
- 0 automated executions observed over 90+ minutes
- Existing workflows (created manually or via other means) work fine
- One modified workflow (health.yml) RAN but FAILED

**Impact**: **HARD BLOCKER for all phases (1-6)**
- Phase 1 (Enable APIs) cannot execute → all subsequent phases blocked
- Cannot enable Google APIs → cannot create OAuth client → cannot expand MCP scopes

**Root Cause**: Unknown - likely permission/approval requirement for API-created workflows

**Contract Compliance**: Manual execution (Or runs `gcloud` commands or clicks "Run workflow") violates automation-first contract:
```
Or = Intent + Approval ONLY
Claude = Technical Execution via Automation
Manual execution is NOT acceptable
```

**Current Status**: ❌ **BLOCKED**

**Documentation**:
- Technical details: `GITHUB_ACTIONS_TRIGGER_BUG.md`
- Comprehensive analysis: `L2_PHASE1_BLOCKED.md`
- Capability matrix: `CAPABILITIES_MATRIX.md` (section 3.5)

### Mitigation Strategy

**Short-term**: Continue with other high-value work
- Windows MCP hardening (ps_exec expansion)
- Governance framework development
- Policy documentation
- Agent architecture design
- Other automation paths (non-Google-dependent)

**Long-term**: Investigate and fix workflow triggering
- Research GitHub Actions permissions
- Check repository/organization settings
- Consider GitHub support escalation
- Explore alternative automation infrastructure

**Alternative Paths Considered**:
1. ❌ Manual execution by Or → violates contract
2. ❌ `workflow_dispatch` with Or clicking → violates contract
3. ❌ Cloud Shell with Or → violates contract
4. ⏳ Fix workflow triggering → under investigation
5. ⏳ Infrastructure change → requires Or's strategic decision

**This is a BLOCKER, not a limitation we can work around while maintaining contract compliance.**

---

## 🔐 Approval Gates (When Unblocked)

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

## 🚫 What This Plan Does NOT Require

❌ Or opening GCP console  
❌ Or running gcloud commands  
❌ Or creating OAuth clients manually  
❌ Or editing config files manually  
❌ REST API calls from Claude  
❌ `workflow_dispatch` triggers  

---

## ✅ What This Plan DOES Require (When Unblocked)

✅ Or's approval (3 approval phrases)  
✅ Or's OAuth consent click (one-time, mandatory by Google)  
✅ Claude writing state files via GitHub MCP  
✅ GitHub Actions running automatically on push ← **CURRENTLY BLOCKED**  
✅ Claude reading result files via GitHub API  

---

## 🎬 Execution Checklist

- [ ] **BLOCKER**: Fix GitHub Actions workflow triggering
- [ ] Phase 1: Enable APIs (approval + auto-execute)
- [ ] Phase 2: Create OAuth (approval + auto-execute)
- [ ] Phase 3: Store Secrets (approval + auto-execute)
- [ ] Phase 4: Generate Config (auto-execute)
- [ ] Phase 5: OAuth Consent (Or clicks "Allow")
- [ ] Phase 6: Verification (auto-execute)
- [ ] Update CAPABILITIES_MATRIX.md → Google MCP: ACTIVE

---

**This plan respects the contract**: Or = Intent + Approval, Claude = Executor  
**This plan is BLOCKED**: Cannot proceed until GitHub Actions triggering is fixed
