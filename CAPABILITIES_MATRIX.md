# CAPABILITIES MATRIX (SSOT)

**Single Source of Truth for Claude's Operational Capabilities**

**Created**: 2025-11-14  
**Last Updated**: 2025-11-14  
**Version**: 1.1.0

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
- ✅ **Verified** - Tested and confirmed working
- 🟡 **Partial** - Works with limitations
- ⚠️ **Planned** - Defined but not yet implemented
- ❌ **Blocked** - Cannot be done (technical/security constraint)
- 🔄 **In Progress** - Currently being built

---

## 1️⃣ GitHub Layer

### 1.1 Repository Operations

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | GitHub API | Read repos | ✅ Verified | Full read access via PAT | None |
| Claude MCP | GitHub API | Create/update files | ✅ Verified | Can create, commit, push | None |
| Claude MCP | GitHub API | Create branches | ✅ Verified | Full branch management | None |
| Claude MCP | GitHub API | Create PRs | ✅ Verified | Open, update, merge PRs | None |
| Claude MCP | GitHub API | Create issues | ✅ Verified | Open, close, comment | None |
| Claude MCP | GitHub API | Search code | ✅ Verified | Full code search | None |
| Claude MCP | GitHub API | List commits | ✅ Verified | Access commit history | None |
| Claude MCP | GitHub API | Fork repos | ✅ Verified | Can fork to account | None |
| | GPT Agent Mode | GitHub Repo (main) | Direct writes (docs/state) | ✅ Verified | Files created directly via Agent Mode (commits 1c64fd5, 81cba22, 52e5e39); OS_SAFE for docs/state | CLOUD_OPS_HIGH for code/workflows |OS_SAFE for docs/state; CLOUD_OPS_HIGH for code/workflows 

**Authentication**: GitHub Personal Access Token (via MCP)  
**Scope**: Full access to `edri2or-commits` repositories

### 1.2 GitHub Actions Integration

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| GitHub Actions | GCP | WIF/OIDC auth | ✅ Verified | Workload Identity Federation active | None - tested with Sheets |
| GitHub Actions | Google Sheets | Append rows | ✅ Verified | Hourly append working (Run 19002923748) | None |
| GitHub Actions | Google Drive | Read/write | 🟡 Partial | WIF configured, not fully tested | Not verified end-to-end |
| GitHub Actions | Secret Manager | Read secrets | 🟡 Partial | WIF configured, not verified | Need verification workflow |
| Claude MCP | GitHub Actions | Trigger workflow | ✅ Verified | Can trigger via API | None |
| Claude MCP | GitHub Actions | Read workflow results | ✅ Verified | Can read logs, artifacts | None |

**Key Evidence**: 
- WIF Provider configured (`${{ vars.WIF_PROVIDER_PATH }}`)
- Service Account active (`${{ vars.GCP_SA_EMAIL }}`)
- Latest success: Index append (2025-11-01, Run 19002923748)

### 1.3 Active Workflows

**68 workflows available** in `.github/workflows/`:

**Critical Workflows**:
- `index-append.yml` ⭐ - Hourly Sheets append (verified working)
- `bootstrap-wif-autonomous.yml` - WIF setup/verification
- `eval-dod.yml` - DoD evaluation (12KB)
- `layer_c_chat_commands.yml` - Chat commands (19KB)
- `control-dispatch.yml` - Main dispatcher

**Gaps to Close**: Need verification runner for Secret Manager access

---

## 2️⃣ Local Layer (Claude's Computer → User's Computer)

### 2.1 Filesystem Access
| GitHub Actions | GitHub Repo (main) | GPT Tasks Executor (run GPT task YAMLs) | 🟡 Partial | Design exists (.github/workflows/gpt_tasks_executor.yml & example task); runtime broken: manual dispatch returns success but no runs; smoke test created via Agent Mode | Requires debugging; do not rely on YAML->Executor loop yet |


| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude (local) | User filesystem | Read files | ✅ Verified | Full text file reading | Allowed dirs only |
| Claude (local) | User filesystem | Write files | ✅ Verified | Create, edit, move files | Allowed dirs only |
| Claude (local) | User filesystem | Directory operations | ✅ Verified | List, create, search | Allowed dirs only |
| Claude (local) | User filesystem | File metadata | ✅ Verified | Get info, sizes, dates | None |
| Claude (local) | User filesystem | Read images | ✅ Verified | Base64 image reading | Allowed dirs only |

**Allowed Directories**:
- `C:\\Users\\edri2` (primary)
- `C:\\` (secondary)

**Key Directory**: `C:\\Users\\edri2\\Work\\AI-Projects\\Claude-Ops\\`

### 2.2 PowerShell MCP

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | PowerShell | Execute commands | ✅ Verified | 11 whitelisted commands | Whitelist only |
| Claude MCP | PowerShell | Screenshot capture | ✅ Verified | Primary display capture | PNG format only |

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

**Screenshot Details**:
- **Output Directory**: `C:\\Users\\edri2\\Work\\AI-Projects\\Claude-Ops\\screenshots\\`
- **Filename Format**: `screenshot_YYYYMMDD_HHmmss.png`
- **Technology**: .NET System.Drawing (System.Windows.Forms + System.Drawing)
- **Capture**: Primary display, full resolution
- **Returns**: JSON with filepath, filename, timestamp, resolution

**Server**: `mcp-servers/ps_exec/` (Node.js + dispatcher.ps1)  
**SDK**: `@modelcontextprotocol/sdk`  
**Version**: 0.2.0

### 2.3 Local CLI Tools

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | gcloud CLI (local) | Detect installation | ✅ Verified | Can confirm presence at known path | Detection only |
| Claude MCP | gcloud CLI (local) | Execute commands | ❌ Blocked | ps_exec whitelist only | Architectural constraint |

**Installation Path**: `C:\\Users\\edri2\\AppData\\Local\\Google\\Cloud SDK\\google-cloud-sdk\\bin\\`  
**Binary**: `gcloud.cmd` (10,925 bytes) + `gcloud.ps1` (3,951 bytes)  
**Status**: Installed and detected (verified 2025-11-14)  
**Last Updated**: 2025-11-12 (inferred from directory timestamps)  
**Version**: Unknown (cannot execute `--version` via MCP)

**Gap**: Cannot execute gcloud commands via MCP due to ps_exec whitelist restrictions. This is **by design** for security.

**Workaround**: Use GitHub Actions → GCP (via WIF) path for Cloud Shell access. This approach:
- Doesn't depend on local gcloud installation
- Uses proven WIF authentication pattern
- Provides full audit trail
- Maintains zero-touch principle

**Evidence**: See `logs/LOG_LOCAL_GCLOUD_STATUS.md` for detailed investigation

---

### 2.4 Local Scripts

**56 scripts available**:
- **33 Python** scripts
- **13 PowerShell** scripts  
- **10 Shell** scripts

**Critical Controllers**:
- `metacontrol.py` - Main orchestrator
- `MCP/local_controller.py` - Local operations
- `claude_auto_agent.py` - Autonomous agent
- `MCP/mcp_agent.py` - MCP protocol handler

**Gap**: Cannot execute Python/Shell scripts directly via MCP (would need automation bridge)

---

## 3️⃣ Google Layer (via MCP)

### 3.1 Gmail

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | Gmail API | Read profile | ✅ Verified | Get user email | Read-only |
| Claude MCP | Gmail API | Search messages | ✅ Verified | Full Gmail search syntax | Read-only |
| Claude MCP | Gmail API | Read threads | ✅ Verified | Full thread context | Read-only |
| Claude MCP | Gmail API | List messages | ✅ Verified | Pagination supported | Read-only |
| Claude MCP | Gmail API | Send email | ⚠️ Planned | Will require OAuth scope expansion | Automation in progress |
| Claude MCP | Gmail API | Download attachments | ⚠️ Planned | Will require OAuth scope expansion | Automation in progress |

**Authentication**: OAuth 2.0 via native Claude integration  
**Current Scopes**: `gmail.readonly`  
**Planned Scopes**: Full Gmail access (send, modify, labels, settings)  
**Expansion Method**: Separate Google MCP server with extended scopes  
**Approval Required**: Yes - HIGH RISK operations (send, delete)

### 3.2 Google Drive

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | Drive API | Search files | ✅ Verified | Full query syntax | Read-only |
| Claude MCP | Drive API | Fetch documents | ✅ Verified | Get document content | Read-only |
| Claude MCP | Drive API | List folders | ✅ Verified | Navigate folder structure | Read-only |
| Claude MCP | Drive API | Create files | ⚠️ Planned | Will require OAuth scope expansion | Automation in progress |
| Claude MCP | Drive API | Edit files | ⚠️ Planned | Will require OAuth scope expansion | Automation in progress |

**Authentication**: OAuth 2.0 via native Claude integration  
**Current Scopes**: `drive.readonly`  
**Planned Scopes**: Full Drive access (create, edit, delete, share)  
**Expansion Method**: Separate Google MCP server with extended scopes  
**Approval Required**: Yes - HIGH RISK operations (delete, share)

### 3.3 Google Calendar

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | Calendar API | List events | ✅ Verified | Full event listing | Read-only |
| Claude MCP | Calendar API | Search events | ✅ Verified | Query-based search | Read-only |
| Claude MCP | Calendar API | Find free time | ✅ Verified | Free/busy lookup | Read-only |
| Claude MCP | Calendar API | Get event details | ✅ Verified | Full event metadata | Read-only |
| Claude MCP | Calendar API | Create events | ⚠️ Planned | Will require OAuth scope expansion | Automation in progress |
| Claude MCP | Calendar API | Edit events | ⚠️ Planned | Will require OAuth scope expansion | Automation in progress |

**Authentication**: OAuth 2.0 via native Claude integration  
**Current Scopes**: `calendar.readonly`  
**Planned Scopes**: Full Calendar access (create, edit, delete events)  
**Expansion Method**: Separate Google MCP server with extended scopes  
**Approval Required**: Yes - HIGH RISK operations (delete events, send invites)

### 3.4 Google Sheets & Docs (Planned)

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | Sheets API | Read sheets | ⚠️ Planned | Via new MCP server | Not yet configured |
| Claude MCP | Sheets API | Update cells | ⚠️ Planned | Via new MCP server | Not yet configured |
| Claude MCP | Docs API | Read docs | ⚠️ Planned | Via new MCP server | Not yet configured |
| Claude MCP | Docs API | Edit docs | ⚠️ Planned | Via new MCP server | Not yet configured |

**Note**: Sheets currently accessible via GitHub Actions → WIF (see section 4.1)  
**Planned**: Direct MCP access with full read/write capabilities  
**Expansion Method**: Same Google MCP server as Gmail/Drive/Calendar  
**Approval Required**: Yes - MEDIUM/HIGH RISK depending on operation

---

## 4️⃣ GCP Layer (via GitHub Actions)

### 4.1 Google Sheets (via WIF)

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| GitHub Actions | Sheets API | Read sheets | ✅ Verified | Full sheet reading | Via Actions only |
| GitHub Actions | Sheets API | Append rows | ✅ Verified | Hourly append working | Via Actions only |
| GitHub Actions | Sheets API | Update cells | 🟡 Partial | WIF configured | Not tested |
| Claude | Sheets API | Direct access | ❌ Blocked | Network restrictions | Use Actions bridge |

**Evidence Sheet**: `1PRfN9zLXXdpBkD6m5rpsauOkWRufSwheqxFPh5omEM0`  
**Latest Success**: Run 19002923748 (updatedRange=Index!A14:D14, updatedRows=1)

### 4.2 Secret Manager (via WIF)

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| GitHub Actions | Secret Manager | List secrets | 🟡 Partial | WIF configured | Not verified |
| GitHub Actions | Secret Manager | Read secrets | 🟡 Partial | WIF configured | Not verified |
| GitHub Actions | Secret Manager | Create secrets | 🟡 Partial | WIF configured | Not verified |
| Claude | Secret Manager | Direct access | ❌ Blocked | Network restrictions | Use Actions bridge |

**Project**: `edri2or-mcp`  
**Service Account**: Configured via `${{ vars.GCP_SA_EMAIL }}`

**Known Secrets**:
- `oauth-client-secret-mcp` (created 2025-11-14) ✅

**Gap**: Need verification workflow to confirm end-to-end access

### 4.3 Cloud Shell

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Local (אור) | Cloud Shell | SSH access | ✅ Verified | `gcloud cloud-shell ssh` works | Manual only - VIOLATES CONTRACT |
| Local (אור) | Cloud Shell | Execute commands | ✅ Verified | Tested and working | Manual only - VIOLATES CONTRACT |
| Claude | Cloud Shell | Automated exec | ⚠️ Planned | Need automation bridge | Not built yet |
| GitHub Actions | Cloud Shell | Execute commands | ⚠️ Planned | Possible via workflow | Not built yet |

**⚠️ CONTRACT VIOLATION**: Current status shows אור executing commands manually  
**Required Fix**: Automate via GitHub Actions (see section 7.3)

**Evidence**: Document 6 shows Cloud Shell verified operational  
**Gap**: No automated triggering path from Claude yet

**Recommended Path**: GitHub Actions → gcloud CLI (in Actions runner) → Cloud Shell
- Bypasses local gcloud dependency
- Uses proven WIF authentication pattern
- Full automation and audit trail
- Maintains zero-touch principle

**Priority**: HIGH - This enables full GCP automation while respecting the contract

---

## 5️⃣ Canva Layer

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | Canva API | Generate designs | ✅ Verified | AI design generation | Multiple types |
| Claude MCP | Canva API | Search designs | ✅ Verified | Full search capability | None |
| Claude MCP | Canva API | Get design | ✅ Verified | Metadata + thumbnail | No content access |
| Claude MCP | Canva API | Export design | ✅ Verified | PDF, PNG, JPG, etc | None |
| Claude MCP | Canva API | Edit design | ✅ Verified | Via editing transaction | Complex workflow |
| Claude MCP | Canva API | Create folder | ✅ Verified | Folder management | None |
| Claude MCP | Canva API | Comment on design | ✅ Verified | Add/list comments | None |

**Authentication**: OAuth 2.0 via MCP  
**Design Types**: 24+ types (presentation, document, poster, etc.)

---

## 6️⃣ Web Layer

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude | Web | Search | ✅ Verified | Brave search engine | None |
| Claude | Web | Fetch URLs | ✅ Verified | Get webpage content | User-provided URLs only |
| Claude | Web | Extract text from PDFs | ✅ Verified | PDF text extraction | Via web_fetch |

**Search Engine**: Brave  
**Rate Limits**: Standard Brave API limits

---

## 7️⃣ Integration Bridges

### 7.1 Claude → GCP (Indirect)

**Problem**: Claude's environment cannot directly access GCP APIs (network/proxy restrictions)

**Solution**: GitHub Actions as bridge

**Pattern**:
```
Claude → GitHub (create workflow/trigger)
       → GitHub Actions (runs in GCP-accessible env)
       → GCP APIs (via WIF)
       → Results as artifact/commit
       → Claude reads results
```

**Status**: ✅ Proven working (Sheets append)  
**Gaps**: Need more runners for Secret Manager, Cloud Shell, etc.

### 7.2 Claude → Local Scripts (Indirect)

**Problem**: PowerShell MCP only supports 11 whitelisted commands, not full script execution

**Solution**: Create wrapper scripts that use whitelisted commands

**Pattern**:
```
Claude → PowerShell MCP (dir, type, test_path)
       → Read script file
       → Analyze content
       → GitHub Actions wrapper (automated execution)
```

**Status**: 🟡 Partial (can read, automation possible)  
**Gap**: Need to build GitHub Actions wrappers for key scripts

**⚠️ IMPORTANT**: The pattern "Or runs script locally" is NO LONGER VALID per the global execution model.

### 7.3 Claude → Cloud Shell (Recommended)

**Problem**: Cannot execute local gcloud commands due to MCP restrictions

**Solution**: GitHub Actions → Cloud Shell execution

**Pattern**:
```
Claude → GitHub (create/trigger cloud-shell-exec workflow)
       → GitHub Actions runner (has gcloud pre-installed)
       → Authenticate via WIF
       → Execute: gcloud cloud-shell ssh --command "..."
       → Store output as artifact
       → Claude reads artifact
```

**Status**: ⚠️ Planned  
**Priority**: HIGH (enables full Cloud Shell automation while respecting contract)  
**Evidence**: See `logs/LOG_LOCAL_GCLOUD_STATUS.md` for design rationale

---

## 8️⃣ Critical Gaps & Blockers

### 8.1 Network Restrictions

**Issue**: Claude's environment cannot directly access:
- GCP APIs (Secret Manager, Cloud Shell, etc.)
- Most external APIs requiring network calls

**Impact**: ❌ Cannot verify Secret Manager, ❌ Cannot trigger Cloud Shell

**Workaround**: Use GitHub Actions as execution environment

**Status**: Workaround proven effective

### 8.2 PowerShell Limitations

**Issue**: Only 11 whitelisted commands available (was 10, now 11 with screenshot)

**Impact**: ❌ Cannot execute arbitrary scripts, ❌ Cannot run gcloud locally

**Workaround**: 
1. Read script via `type` command
2. Analyze and understand
3. Execute via GitHub Actions (automated wrapper)

**Status**: Accepted limitation, architectural constraint by design

### 8.3 Script Execution

**Issue**: 56 scripts available locally, but no direct execution path from Claude

**Impact**: Cannot automate Python/Shell scripts from Claude directly

**Workaround**:
1. Create GitHub Actions wrappers (automated)
2. Use PowerShell MCP where applicable (limited)

**Status**: Automation via Actions is the path forward (respects contract)

**⚠️ REMOVED**: "Manual execution by אור" - this violates the contract

### 8.4 Local gcloud CLI Access

**Issue**: gcloud installed locally but cannot be executed via MCP

**Impact**: Cannot use local gcloud for Cloud Shell, cannot verify version

**Workaround**: Use GitHub Actions runners (have gcloud pre-installed, WIF auth works)

**Status**: ✅ Workaround designed (see 7.3), waiting for implementation

---

## 9️⃣ Security Posture

### 9.1 Secret Storage

| Secret Type | Location | Status | Notes |
|-------------|----------|--------|-------|
| GitHub PAT | Windows Credential Manager | ✅ Secured | Via DPAPI |
| GitHub App Key | Windows Credential Manager | ✅ Secured | Purged 2025-11-11 |
| OAuth (GOOGLE/) | GCP Secret Manager | ✅ Secured | Migrated 2025-11-14 |
| OAuth (GPT/) | Local plaintext | ⚠️ Pending | Next in migration queue |
| GCP SA Keys (3x) | Local plaintext | ⚠️ Pending | Usage verification needed |

**Migration Progress**: 56% (5 of 9 secrets secured)

### 9.2 Access Control

**GitHub**: Full access via PAT (appropriate for ops automation)  
**Google MCP**: Read-only scopes (appropriate for safety)  
**PowerShell**: Whitelist-only (appropriate for security)  
**Filesystem**: Allowed directories only (appropriate for scope)  
**gcloud**: Detection only, no execution (appropriate for zero-touch model)

---

## 🔟 Roadmap to 100%

### Priority 0: Google MCP Full Setup (HIGHEST PRIORITY)

**Goal**: Enable full Google capabilities (Gmail, Drive, Calendar, Sheets, Docs) with approval gates

**Tasks**:
1. 🔄 Create GitHub Actions workflows for OAuth setup (automated)
2. 🔄 Enable required GCP APIs (automated)
3. 🔄 Create OAuth client credentials (automated)
4. 🔄 Store credentials in Secret Manager (automated)
5. 🔄 Update claude_desktop_config.json (automated)
6. 🔄 Verification tests (automated)
7. ⏳ Or: Click OAuth consent (one-time human action)

**Executor**: Claude (via automation)  
**Or's Role**: Intent + Approval + One OAuth click  
**Effort**: Low (automation-first approach)  
**Risk**: Low (approval gates in place)  
**Impact**: Unlocks full Google productivity suite

**See**: `plans/GOOGLE_MCP_AUTOMATION_PLAN.md` for detailed execution plan

### Priority 1: Cloud Shell via Actions (High Value, Low Risk)

**Goal**: Enable automated Cloud Shell command execution

**Tasks**:
1. ⏳ Create `.github/workflows/cloud-shell-exec.yml`
2. ⏳ Use WIF auth (proven with Sheets)
3. ⏳ Execute gcloud commands in runner
4. ⏳ Return output as artifact

**Executor**: Claude (via automation)  
**Or's Role**: Approval only  
**Effort**: Low (copy existing Sheets pattern)  
**Risk**: Low (read operations)  
**Impact**: Unblocks full GCP automation while respecting contract

### Priority 2: Verification Runners (High Value, Low Risk)

**Goal**: Close GitHub Actions → GCP gaps

**Tasks**:
1. ✅ Sheets append (DONE)
2. ⏳ Secret Manager read (need workflow)
3. ⏳ Drive write (need workflow)

**Executor**: Claude (via automation)  
**Or's Role**: Approval only  
**Effort**: Low (reuse existing WIF)  
**Risk**: Low (read-only operations)

### Priority 3: OAuth Migration (High Value, Medium Risk)

**Goal**: Complete secret migration

**Tasks**:
1. ✅ GOOGLE/ OAuth (DONE)
2. ⏳ GPT/ OAuth (next)
3. ⏳ GCP SA keys (verify usage first)

**Executor**: Claude (via automation)  
**Or's Role**: Approval only  
**Effort**: Low (proven process)  
**Risk**: Medium (requires testing)

### Priority 4: Script Automation (Medium Value, Medium Effort)

**Goal**: Enable automated script execution

**Tasks**:
1. ⏳ Create GitHub Actions wrappers for key scripts
2. ⏳ Build trigger mechanism from Claude
3. ⏳ Establish result retrieval pattern

**Executor**: Claude (via automation)  
**Or's Role**: Approval only  
**Effort**: Medium  
**Risk**: Low

---

## 📝 Update Log

### 2025-11-14 (v1.1.0)
- **Added GLOBAL EXECUTION MODEL section** ⭐ CRITICAL
- Defined contract: Or = Intent + Approval, Claude = Executor
- Updated all sections to remove manual execution by Or
- Marked Cloud Shell manual usage as contract violation
- Updated Google Layer (3.x) with planned full capabilities
- Added Priority 0: Google MCP Full Setup to roadmap
- Updated all roadmap items with "Executor: Claude" and "Or's Role: Approval only"
- Referenced `plans/GOOGLE_MCP_AUTOMATION_PLAN.md` for execution details
- Commit message: "L0: Add global execution model - Or = Intent+Approval, Claude = Executor"

### 2025-11-14 (v1.0.2)
- **Added screenshot capability to ps_exec MCP server**
- Section 2.2: Expanded PowerShell MCP table with screenshot row
- Updated whitelisted commands: 10 → 11 (added `screenshot`)
- Added screenshot details subsection with implementation specifics
- Updated version in section 2.2: ps_exec now 0.2.0
- Updated section 7.2: PowerShell limitation note (10 → 11 commands)
- Updated section 8.2: PowerShell limitation note (10 → 11 commands)
- Commit evidence: 1580581a2c8fc6dfd1325ec94202d2be350f0ce0

### 2025-11-14 (v1.0.1)
- Added section 2.3: Local CLI Tools (gcloud)
- Documented gcloud installation detection capability
- Clarified architectural constraint preventing local gcloud execution
- Added bridge pattern 7.3 for Cloud Shell via GitHub Actions
- Updated gap 8.4 with gcloud-specific blocker and workaround
- Created evidence log: `logs/LOG_LOCAL_GCLOUD_STATUS.md`
- Updated roadmap: Cloud Shell via Actions now Priority 1

### 2025-11-14 (v1.0.0)
- Initial version created
- Documented all verified capabilities
- Identified 3 main gaps (GCP direct access, script execution, secret migration)
- Established update protocol

---

## 🔄 Update Protocol

When adding a new capability:

1. **Test** the capability thoroughly
2. **Update** this matrix with:
   - New row in appropriate table
   - Status (Verified/Partial/Planned)
   - Limitations (if any)
   - Evidence/notes
3. **Commit** with message: `L0: update capabilities matrix - [capability name]`
4. **Reference** this file in any documentation about the new capability

When a capability changes:
1. Update status/limitations
2. Add note to Update Log
3. Update version number
4. Commit with message: `L0: update capabilities matrix - [what changed]`

---

**This is the Single Source of Truth. All other capability descriptions must defer to this document.**

---

**Maintained by**: Claude (with אור's approval)  
**Last Verified**: 2025-11-14  
**Next Review**: As capabilities change
