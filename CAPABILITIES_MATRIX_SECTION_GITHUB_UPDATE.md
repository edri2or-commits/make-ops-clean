# CAPABILITIES MATRIX (SSOT)

[...קיים...]

## 1️⃣ GitHub Layer

### 1.2 GitHub Actions Integration

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| GitHub Actions | GCP | WIF/OIDC auth | ✅ Verified | Workload Identity Federation active | None - tested with Sheets |
| GitHub Actions | Google Sheets | Append rows | ✅ Verified | Hourly append working (Run 19002923748) | None |
| GitHub Actions | Google Drive | Read/write | 🟡 Partial | WIF configured, not fully tested | Not verified end-to-end |
| GitHub Actions | Secret Manager | Read secrets | 🟡 Partial | WIF configured, not verified | Need verification workflow |
| Claude MCP | GitHub Files | Write/commit | ✅ Verified | Can create/edit files, commit, push | None |
| Claude MCP | Workflows | Trigger via `on: push` | ✅ Verified | Push to trigger file → workflow runs | None |
| Claude MCP | Workflows | Trigger via `on: schedule` | ✅ Verified | Cron-based execution | None |
| Claude MCP | Workflow Results | Read from commits | ✅ Verified | Workflows write results to files | None |
| Claude MCP | Workflow Results | Read from artifacts | ❌ Blocked | Cannot access Actions API | Must use file-based results |
| Claude MCP | GitHub Actions API | Call REST endpoints | ❌ Blocked | Network restrictions | Cannot trigger `workflow_dispatch` |
| Claude MCP | GitHub Actions API | Read workflow runs | ❌ Blocked | Network restrictions | Cannot query run status |

**Automation Pattern**:
```
Claude writes state file → commit+push
  ↓
GitHub detects push (on: push trigger)
  ↓
Workflow runs automatically
  ↓
Workflow writes results → commit
  ↓
Claude reads results via GitHub file API
```

**Key Limitations**:
- ❌ **Cannot call GitHub Actions REST API** - Network restrictions prevent direct API calls
- ❌ **Cannot trigger `workflow_dispatch`** - Requires Actions API access
- ❌ **Cannot read workflow run status** - Requires Actions API access  
- ✅ **Workaround**: Use `on: push` with state files + results in commits
- ✅ **Alternative**: Use `on: schedule` for polling patterns

**Authentication**: 
- GitHub MCP: GitHub Personal Access Token
- GitHub Actions → GCP: WIF (Workload Identity Federation)

**Evidence**:
- WIF Provider: `${{ vars.WIF_PROVIDER_PATH }}`
- Service Account: `${{ vars.GCP_SA_EMAIL }}`
- Latest success: Index append (Run 19002923748)
- Pattern proven: State file → Auto-trigger → Results in commit

**See**: `plans/GOOGLE_MCP_AUTOMATION_PLAN.md` for implementation details

[...שאר הקובץ ללא שינוי...]
