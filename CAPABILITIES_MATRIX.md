# CAPABILITIES MATRIX (SSOT)

**Single Source of Truth for Claude's Operational Capabilities**

**Created**: 2025-11-14  
**Last Updated**: 2025-11-18  
**Version**: 1.3.0 (מנה R6: הוספת שדות תפקידים)

---

## 🎯 Purpose

This is the **master reference** for all capabilities across the Claude-Ops system. Every chat session, automation, and tool must reference this document to understand what Claude can and cannot do.

**Update Protocol**: When a new capability is added, this file MUST be updated before the capability is considered operational.

---

## ⚡ GLOBAL EXECUTION MODEL

**CRITICAL CONTRACT**

```
┌─────────────────────────────────────────────────────┐
│                   Or (אור)                           │
│                                                      │
│  Role: Intent + Approval ONLY                       │
│  - Defines objectives ("enable Google full access") │
│  - Approves HIGH RISK operations                    │
│  - Clicks OAuth consent (when required by provider) │
│                                                      │
│  NEVER:                                              │
│  ❌ Opens consoles (GCP, Azure, AWS, etc.)          │
│  ❌ Enables APIs manually                           │
│  ❌ Creates credentials manually                    │
│  ❌ Edits config files manually                     │
│  ❌ Runs commands manually                          │
│  ❌ Executes scripts manually                       │
│                                                      │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────┐
│                Claude (Executor)                     │
│                                                      │
│  Role: Technical Execution via Automation           │
│  - Plans automation strategy                        │
│  - Creates GitHub Actions workflows                 │
│  - Triggers workflows via API                       │
│  - Monitors execution                               │
│  - Reads results from artifacts/logs                │
│  - Updates config files via MCP/filesystem          │
│  - Documents changes in CAPABILITIES_MATRIX.md      │
│                                                      │
│  Tools:                                              │
│  ✅ GitHub Actions (WIF → GCP)                      │
│  ✅ Cloud Shell (via Actions)                       │
│  ✅ MCP Servers (filesystem, ps_exec, etc.)         │
│  ✅ REST APIs (GCP, GitHub, etc.)                   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Translation of this model**:
- Or provides **strategic direction** ("I want full Google capabilities")
- Claude provides **tactical execution** (creates workflows, runs automation)
- Or provides **approval gates** for HIGH RISK operations
- Or provides **one-time clicks** when OAuth providers require human consent

**This is not negotiable**. Any plan, workflow, or documentation that asks Or to:
- Run commands
- Open web consoles
- Edit files manually
- Configure systems manually

...is **INVALID** and violates the core contract.

**Replacement strategy**: If a step requires Or's manual action, Claude MUST either:
1. Automate it via GitHub Actions / Cloud Shell / MCP
2. Document it as a ONE-TIME human click (OAuth consent only)
3. Mark it as a gap and propose automation path

---

## 📊 Capability Matrix

### Legend

**Status**:
- ✅ **Verified** - Tested and confirmed working
- 🟡 **Partial** - Works with limitations
- ⚠️ **Planned** - Defined but not yet implemented
- ❌ **Blocked** - Cannot be done (technical/security constraint)
- 🔄 **In Progress** - Currently being built
- 🔍 **Unverified** - Code exists but deployment/runtime status unknown

**Claude at Runtime** (🆕 v1.3.0):
- `Yes` - Claude required during execution (interactive, real-time decisions)
- `No` - Runs autonomously without Claude (scheduled jobs, automated workflows)
- `Builder-Only` - Claude builds automation but not involved in runtime
- `Unknown` - Not yet determined

**GPT-CEO Ready** (🆕 v1.3.0):
- `Yes` - GPT-CEO can serve as Primary Agent now
- `No` - GPT-CEO cannot (lacks tools/capabilities)
- `Planned` - Designed/planned, not yet ready
- `Unknown` - Not yet determined

**Human Approval** (🆕 v1.3.0):
- `Yes` - Explicit approval always required (CLOUD_OPS_HIGH)
- `No` - No approval needed (OS_SAFE, read-only)
- `Depends` - Depends on specific operation context
- `Unknown` - Not yet determined

---

## 1️⃣ GitHub Layer

### 1.1 Repository Operations

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| Claude MCP | GitHub API | Read repos | ✅ Verified | Yes | Yes | No | Full read access via PAT | None |
| Claude MCP | GitHub API | Create/update files | ✅ Verified | Yes | Yes | Depends | Can create, commit, push | Docs=No, Code=Yes approval |
| Claude MCP | GitHub API | Create branches | ✅ Verified | Yes | Planned | No | Full branch management | None |
| Claude MCP | GitHub API | Create PRs | ✅ Verified | Yes | Planned | Depends | Open, update, merge PRs | Merge needs approval |
| Claude MCP | GitHub API | Create issues | ✅ Verified | Yes | Yes | No | Open, close, comment | None |
| Claude MCP | GitHub API | Search code | ✅ Verified | Yes | Yes | No | Full code search | None |
| Claude MCP | GitHub API | List commits | ✅ Verified | Yes | Yes | No | Access commit history | None |
| Claude MCP | GitHub API | Fork repos | ✅ Verified | Yes | Planned | No | Can fork to account | None |
| GPT Agent Mode | GitHub Repo (main) | Direct writes (docs/state) | ✅ Verified | Yes | Yes | No | Files created directly via Agent Mode (commits 1c64fd5, 81cba22, 52e5e39); OS_SAFE for docs/state | CLOUD_OPS_HIGH for code/workflows |

**Authentication**: GitHub Personal Access Token (via MCP)  
**Scope**: Full access to `edri2or-commits` repositories

**Notes on GPT-CEO Readiness**:
- **Yes**: Basic read/write operations that GPT can perform via Actions or direct API
- **Planned**: Complex workflows (PRs, branch management) require orchestration design

### 1.2 GitHub Actions Integration

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| GitHub Actions | GCP | WIF/OIDC auth | ✅ Verified | Builder-Only | Planned | No | Workload Identity Federation active | None - tested with Sheets |
| GitHub Actions | Google Sheets | Append rows | ✅ Verified | No | Planned | No | Hourly append working (Run 19002923748) | None |
| GitHub Actions | Google Drive | Read/write | 🟡 Partial | Builder-Only | Planned | Depends | WIF configured, not fully tested | Not verified end-to-end |
| GitHub Actions | Secret Manager | Read secrets | 🟡 Partial | Builder-Only | Planned | No | WIF configured, not verified | Need verification workflow |
| Claude MCP | GitHub Actions | Trigger workflow | ✅ Verified | Yes | Planned | Depends | Can trigger via API | Depends on workflow risk |
| Claude MCP | GitHub Actions | Read workflow results | ✅ Verified | Yes | Planned | No | Can read logs, artifacts | None |

**Key Evidence**: 
- WIF Provider configured (`${{ vars.WIF_PROVIDER_PATH }}`)
- Service Account active (`${{ vars.GCP_SA_EMAIL }}`)
- Latest success: Index append (2025-11-01, Run 19002923748)

**Notes on Claude at Runtime**:
- `Builder-Only`: Claude builds/designs workflows, but they run autonomously
- `Yes` (Trigger/Read): Claude interacts at runtime to trigger or check results

**Notes on GPT-CEO Readiness**:
- **Planned**: Requires orchestration layer (trigger workflows, read status) - being designed in FLOW specs

### 1.3 Active Workflows

**68 workflows available** in `.github/workflows/`

**Critical Workflows**:
- `index-append.yml` ⭐ - Hourly Sheets append (verified working)
  - Claude at Runtime: `No` (scheduled)
  - GPT-CEO Ready: `Planned`
  - Approval: `No`
- `bootstrap-wif-autonomous.yml` - WIF setup/verification
  - Claude at Runtime: `Builder-Only`
  - GPT-CEO Ready: `Planned`
  - Approval: `Yes` (infrastructure change)
- `eval-dod.yml` - DoD evaluation (12KB)
- `layer_c_chat_commands.yml` - Chat commands (19KB)
- `control-dispatch.yml` - Main dispatcher

**Gaps to Close**: Need verification runner for Secret Manager access

---

## 2️⃣ Local Layer (Claude's Computer → User's Computer)

### 2.1 Filesystem Access

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| Claude (local) | User filesystem | Read files | ✅ Verified | Yes | No | No | Full text file reading | Allowed dirs only; GPT lacks MCP |
| Claude (local) | User filesystem | Write files | ✅ Verified | Yes | No | No | Create, edit, move files | Allowed dirs only; GPT lacks MCP |
| Claude (local) | User filesystem | Directory operations | ✅ Verified | Yes | No | No | List, create, search | Allowed dirs only |
| Claude (local) | User filesystem | File metadata | ✅ Verified | Yes | No | No | Get info, sizes, dates | None |
| Claude (local) | User filesystem | Read images | ✅ Verified | Yes | No | No | Base64 image reading | Allowed dirs only |
| GitHub Actions | GitHub Repo (main) | GPT Tasks Executor (run GPT task YAMLs) | 🟡 Partial | No | Planned | Depends | Design exists (.github/workflows/gpt_tasks_executor.yml & example task); runtime broken: manual dispatch returns success but no runs; smoke test created via Agent Mode | Requires debugging; do not rely on YAML->Executor loop yet |

**Allowed Directories**:
- `C:\\Users\\edri2` (primary)
- `C:\\` (secondary)

**Key Directory**: `C:\\Users\\edri2\\Work\\AI-Projects\\Claude-Ops\\`

**Notes on GPT-CEO Readiness**:
- **No**: GPT does not have MCP filesystem access (architectural limitation)
- GPT can request Claude to perform filesystem operations
- GPT Tasks Executor: **Planned** (designed but broken runtime)

### 2.2 PowerShell MCP

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| Claude MCP | PowerShell | Execute commands | ✅ Verified | Yes | No | No | 11 whitelisted commands | Whitelist only; GPT lacks MCP |
| Claude MCP | PowerShell | Screenshot capture | ✅ Verified | Yes | No | No | Primary display capture | PNG format only; GPT lacks MCP |

**Whitelisted Commands**:
1. `dir` - List directory
2. `type` - Read file content
3. `test_path` - Check if path exists
4. `whoami` - Get current user
5. `get_process` - List processes
6. `get_service` - List services
7. `get_env` - Get environment variables
8. `test_connection` - Test network connectivity
9. `get_item_property` - Get registry/file properties
10. `measure_object` - Count/measure objects
11. `screenshot` - Capture primary display screenshot ⭐ **NEW**

**Server**: `mcp-servers/ps_exec/` (Node.js + dispatcher.ps1)  
**SDK**: `@modelcontextprotocol/sdk`  
**Version**: 0.2.0

**Notes on GPT-CEO Readiness**:
- **No**: GPT lacks MCP access (architectural constraint)
- GPT can request Claude to execute PowerShell commands

---

## 3️⃣ Google Layer (via MCP)

### 3.1 Gmail

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| Claude MCP | Gmail API | Read profile | ✅ Verified | Yes | Yes | No | Get user email | Read-only |
| Claude MCP | Gmail API | Search messages | ✅ Verified | Yes | Yes | No | Full Gmail search syntax | Read-only |
| Claude MCP | Gmail API | Read threads | ✅ Verified | Yes | Yes | No | Full thread context | Read-only |
| Claude MCP | Gmail API | List messages | ✅ Verified | Yes | Yes | No | Pagination supported | Read-only |
| Claude MCP | Gmail API | Send email | ⚠️ Planned | Yes | Planned | Yes | Will require OAuth scope expansion | Automation in progress; CLOUD_OPS_HIGH |
| Claude MCP | Gmail API | Download attachments | ⚠️ Planned | Yes | Planned | No | Will require OAuth scope expansion | Automation in progress |

**Authentication**: OAuth 2.0 via native Claude integration  
**Current Scopes**: `gmail.readonly`  
**Planned Scopes**: Full Gmail access (send, modify, labels, settings)  
**Expansion Method**: Separate Google MCP server with extended scopes  
**Approval Required**: Yes - HIGH RISK operations (send, delete)

**Notes on GPT-CEO Readiness**:
- **Yes** (read): GPT can analyze, search, extract info via Claude or future API bridge
- **Planned** (write): Requires OAuth expansion + approval gates (PILOT flows)

### 3.2 Google Drive

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| Claude MCP | Drive API | Search files | ✅ Verified | Yes | Yes | No | Full query syntax | Read-only |
| Claude MCP | Drive API | Fetch documents | ✅ Verified | Yes | Yes | No | Get document content | Read-only |
| Claude MCP | Drive API | List folders | ✅ Verified | Yes | Yes | No | Navigate folder structure | Read-only |
| Claude MCP | Drive API | Create files | ⚠️ Planned | Yes | Planned | Depends | Will require OAuth scope expansion | Automation in progress; personal=No, shared=Yes approval |
| Claude MCP | Drive API | Edit files | ⚠️ Planned | Yes | Planned | Depends | Will require OAuth scope expansion | Automation in progress |

**Authentication**: OAuth 2.0 via native Claude integration  
**Current Scopes**: `drive.readonly`  
**Planned Scopes**: Full Drive access (create, edit, delete, share)  
**Expansion Method**: Separate Google MCP server with extended scopes  
**Approval Required**: Yes - HIGH RISK operations (delete, share)

**Notes on GPT-CEO Readiness**:
- **Planned**: PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md defines GPT-CEO orchestration

### 3.3 Google Calendar

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| Claude MCP | Calendar API | List events | ✅ Verified | Yes | Yes | No | Full event listing | Read-only |
| Claude MCP | Calendar API | Search events | ✅ Verified | Yes | Yes | No | Query-based search | Read-only |
| Claude MCP | Calendar API | Find free time | ✅ Verified | Yes | Yes | No | Free/busy lookup | Read-only |
| Claude MCP | Calendar API | Get event details | ✅ Verified | Yes | Yes | No | Full event metadata | Read-only |
| Claude MCP | Calendar API | Create events | ⚠️ Planned | Yes | Planned | Depends | Will require OAuth scope expansion | Automation in progress; personal=No, with attendees=Yes approval |
| Claude MCP | Calendar API | Edit events | ⚠️ Planned | Yes | Planned | Depends | Will require OAuth scope expansion | Automation in progress |

**Authentication**: OAuth 2.0 via native Claude integration  
**Current Scopes**: `calendar.readonly`  
**Planned Scopes**: Full Calendar access (create, edit, delete events)  
**Expansion Method**: Separate Google MCP server with extended scopes  
**Approval Required**: Yes - HIGH RISK operations (delete events, send invites)

**Notes on GPT-CEO Readiness**:
- **Planned**: PILOT_CALENDAR_FOCUS_EVENT_FLOW.md defines GPT-CEO orchestration

### 3.4 Google Sheets & Docs (Planned)

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| Claude MCP | Sheets API | Read sheets | ⚠️ Planned | Yes | Planned | No | Via new MCP server | Not yet configured |
| Claude MCP | Sheets API | Update cells | ⚠️ Planned | Yes | Planned | Depends | Via new MCP server | Not yet configured; personal=No, shared=Yes approval |
| Claude MCP | Docs API | Read docs | ⚠️ Planned | Yes | Planned | No | Via new MCP server | Not yet configured |
| Claude MCP | Docs API | Edit docs | ⚠️ Planned | Yes | Planned | Depends | Via new MCP server | Not yet configured |

**Note**: Sheets currently accessible via GitHub Actions → WIF (see section 4.1)  
**Planned**: Direct MCP access with full read/write capabilities  
**Expansion Method**: Same Google MCP server as Gmail/Drive/Calendar  
**Approval Required**: Yes - MEDIUM/HIGH RISK depending on operation

---

## 4️⃣ GCP Layer (via GitHub Actions)

### 4.1 Google Sheets (via WIF)

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| GitHub Actions | Sheets API | Read sheets | ✅ Verified | Builder-Only | Planned | No | Full sheet reading | Via Actions only |
| GitHub Actions | Sheets API | Append rows | ✅ Verified | No | Planned | No | Hourly append working | Via Actions only; runs autonomously |
| GitHub Actions | Sheets API | Update cells | 🟡 Partial | Builder-Only | Planned | Depends | WIF configured | Not tested |
| Claude | Sheets API | Direct access | ❌ Blocked | N/A | No | N/A | Network restrictions | Use Actions bridge |

**Evidence Sheet**: `1PRfN9zLXXdpBkD6m5rpsauOkWRufSwheqxFPh5omEM0`  
**Latest Success**: Run 19002923748 (updatedRange=Index!A14:D14, updatedRows=1)

**Notes on Claude at Runtime**:
- `Builder-Only`: Claude designs/builds workflows
- `No` (Append rows): Runs autonomously on schedule

**Notes on GPT-CEO Readiness**:
- **Planned**: Requires orchestration to trigger workflows + read results

### 4.2 Secret Manager (via WIF)

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| GitHub Actions | Secret Manager | List secrets | 🟡 Partial | Builder-Only | Planned | No | WIF configured | Not verified |
| GitHub Actions | Secret Manager | Read secrets | 🟡 Partial | Builder-Only | Planned | No | WIF configured | Not verified |
| GitHub Actions | Secret Manager | Create secrets | 🟡 Partial | Builder-Only | Planned | Yes | WIF configured | Not verified; CLOUD_OPS_HIGH |
| Claude | Secret Manager | Direct access | ❌ Blocked | N/A | No | N/A | Network restrictions | Use Actions bridge |

**Project**: `edri2or-mcp`  
**Service Account**: Configured via `${{ vars.GCP_SA_EMAIL }}`

**Known Secrets**:
- `oauth-client-secret-mcp` (created 2025-11-14) ✅

**Gap**: Need verification workflow to confirm end-to-end access

### 4.3 Cloud Shell

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| Local (אור) | Cloud Shell | SSH access | ✅ Verified | No | No | Depends | `gcloud cloud-shell ssh` works | Manual only - VIOLATES CONTRACT |
| Local (אור) | Cloud Shell | Execute commands | ✅ Verified | No | No | Depends | Tested and working | Manual only - VIOLATES CONTRACT |
| Claude | Cloud Shell | Automated exec | ⚠️ Planned | Builder-Only | Planned | Depends | Need automation bridge | Not built yet |
| GitHub Actions | Cloud Shell | Execute commands | ⚠️ Planned | Builder-Only | Planned | Depends | Possible via workflow | Not built yet |

**⚠️ CONTRACT VIOLATION**: Current status shows אור executing commands manually  
**Required Fix**: Automate via GitHub Actions (see section 7.3)

**Priority**: HIGH - This enables full GCP automation while respecting the contract

---

## 🔟 Cloud Run APIs (GPTs GO Integration)

### 10.1 Service Overview

**⚠️ CRITICAL NAMING CLARIFICATION**:
- **Repository directory**: `cloud-run/google-workspace-github-api/`
- **Deployed service name**: `github-executor-api`
- **Actual functionality**: GitHub operations only (NO Google Workspace operations)

This is **ONE service**, not two separate services as previously documented.

### 10.2 github-executor-api

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| GPTs GO | Cloud Run | Health check (/) | 🔍 Runtime Unverified | Builder-Only | Yes | No | Code exists, deployment status unknown | **Observability Constraint** - Cannot verify without Actions API access or status files |
| GPTs GO | Cloud Run | GitHub file update (/github/update-file) | 🔍 Runtime Unverified | Builder-Only | Yes | Depends | Code exists, GPTs GO reports 404 | **Observability Constraint** - Deployment status unknown; Depends on file type (docs=No, code=Yes) |

**Code Location**: `cloud-run/google-workspace-github-api/`  
**Service Name**: `github-executor-api`  
**Region**: `us-central1`  
**Project**: `edri2or-mcp`

**Implementation Status**: ✅ **Implemented (code)**  
**Runtime Status**: 🔍 **Unverified** - Cannot confirm deployment without Cloud Run visibility

**Notes on Claude at Runtime**:
- `Builder-Only`: Claude built the service code, but GPT-CEO is the consumer

**Notes on GPT-CEO Readiness**:
- **Yes**: This service is **designed for GPT-CEO** to use! Primary consumer is GPTs GO platform

**Known Issues**:
- ⚠️ **Code typo on line 37**: `Accept: 'application/vund.github+json'` should be `vnd.github`
- This typo may cause GitHub API request failures

**Evidence**: 
- Code analysis 2025-11-17 (`DOCS/L2_RUNTIME_DIAGNOSIS.md`)
- Workflow design 2025-11-17 (`.github/workflows/verify-github-executor-api.yml`)
- Observability gap documented in `DOCS/GITHUB_EXECUTOR_RECOVERY_PLAN.md` Task 2.1

---

## 📝 Update Log

### 2025-11-18 (v1.3.0) - מנה R6: Role Fields Addition ⭐ MAJOR UPDATE
- **Added 3 new columns** to all major capability tables:
  1. `Claude at Runtime?` - Clarifies Claude's involvement during execution
  2. `GPT-CEO Ready?` - Indicates GPT-CEO readiness as Primary Agent
  3. `Human Approval?` - Specifies approval requirements
- **Sections updated**: 1 (GitHub), 2 (Local), 3 (Google), 4 (GCP), 10 (Cloud Run)
- **Total rows updated**: ~54 capability rows
- **Zero Unknown fields**: All capabilities categorized
- **See**: `logs/LOG_CAPABILITIES_MATRIX_ROLE_FIELDS_UPDATE_V2.md` for detailed analysis
- **Patterns identified**: 
  - Builder-Only (workflows/jobs Claude designs)
  - GPT-CEO Planned (requires orchestration layer)
  - Approval Depends (context-based risk assessment)

### 2025-11-17 (v1.2.1) - Task 2.1 Closure
[Previous updates truncated for brevity]

---

## 🔄 Update Protocol

When adding a new capability:

1. **Test** the capability thoroughly
2. **Update** this matrix with:
   - New row in appropriate table
   - Status (Verified/Partial/Planned/Unverified)
   - **Claude at Runtime, GPT-CEO Ready, Human Approval fields** 🆕
   - Limitations (if any)
   - Evidence/notes
3. **Commit** with message: `Phase X.Y: update capabilities matrix - [capability name]`
4. **Reference** this file in any documentation about the new capability

When a capability changes:
1. Update status/limitations/**role fields** 🆕
2. Add note to Update Log
3. Update version number (bump minor for new features, patch for corrections)
4. Commit with message: `Phase X.Y: update capabilities matrix - [what changed]`

---

**This is the Single Source of Truth. All other capability descriptions must defer to this document.**

---

**Maintained by**: Claude (with אור's approval)  
**Last Verified**: 2025-11-18  
**Next Review**: As capabilities change

[Sections 5-9 intentionally omitted for brevity - less relevant for GPT-CEO flows]

## Appendix: GPT / Agent Runtime Notes

### GitHub Layer

**Direct GitHub writes via GPT Agent Mode**  
- Status: ✅ Verified (Implemented & Tested, scope: OS_SAFE – Docs/MD/State only)  
- Claude at Runtime: Yes
- GPT-CEO Ready: Yes
- Approval: No (docs), Yes (code/workflows)
- Evidence (branch main):  
  - commit 1c64fd5 – DOCS/GPT_EXECUTOR_TEST.md  
  - commit 81cba22 – DOCS/STATE_FOR_GPT_SNAPSHOT.md  
  - commit 52e5e39 – STATE_FOR_GPT.md reference update  

**GPT Tasks Executor (GitHub Actions workflow)**  
- Files: `.github/workflows/gpt_tasks_executor.yml`, `.chatops/gpt_tasks/gpt-2025-11-15-001-executor-smoke-test.yml`
- Status: 🟡 Partial / Broken Runtime  
- Claude at Runtime: No (autonomous job)
- GPT-CEO Ready: Planned (requires debugging)
- Approval: Depends (on task content)
- Design exists (task format, workflow, YAML)
- Manual dispatch returns success but no actual runs (0 runs)
- Requires debugging (events/permissions/config)

**GPT GitHub Agent DRY RUN**  
- Capability: Local Python + optional GitHub Actions workflow  
- Status: ✅ Implemented — OS_SAFE only (Docs/Plans, no direct code/config changes)  
- Claude at Runtime: Yes (generates plans)
- GPT-CEO Ready: Yes (consumes plans)
- Approval: No (planning), Yes (execution of code changes)
- Evidence: commits 1c64fd5, 81cba22, 52e5e39, 047eea8  
- Policy: OS_SAFE for planning/documentation; CLOUD_OPS_HIGH for code/config via PR + explicit approval
