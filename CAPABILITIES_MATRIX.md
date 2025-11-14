# CAPABILITIES MATRIX (SSOT)

**Single Source of Truth for Claude's Operational Capabilities**

**Created**: 2025-11-14  
**Last Updated**: 2025-11-14  
**Version**: 1.0.0

---

## 🎯 Purpose

This is the **master reference** for all capabilities across the Claude-Ops system. Every chat session, automation, and tool must reference this document to understand what Claude can and cannot do.

**Update Protocol**: When a new capability is added, this file MUST be updated before the capability is considered operational.

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

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude (local) | User filesystem | Read files | ✅ Verified | Full text file reading | Allowed dirs only |
| Claude (local) | User filesystem | Write files | ✅ Verified | Create, edit, move files | Allowed dirs only |
| Claude (local) | User filesystem | Directory operations | ✅ Verified | List, create, search | Allowed dirs only |
| Claude (local) | User filesystem | File metadata | ✅ Verified | Get info, sizes, dates | None |
| Claude (local) | User filesystem | Read images | ✅ Verified | Base64 image reading | Allowed dirs only |

**Allowed Directories**:
- `C:\Users\edri2` (primary)
- `C:\` (secondary)

**Key Directory**: `C:\Users\edri2\Work\AI-Projects\Claude-Ops\`

### 2.2 PowerShell MCP

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | PowerShell | Execute commands | ✅ Verified | 10 whitelisted commands | Whitelist only |

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

**Server**: `mcp-servers/ps_exec/` (Node.js + dispatcher.ps1)  
**SDK**: `@modelcontextprotocol/sdk`

### 2.3 Local Scripts

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
| Claude MCP | Gmail API | Send email | ❌ Blocked | Not in MCP scope | Cannot send |
| Claude MCP | Gmail API | Download attachments | ❌ Blocked | Not in MCP scope | Cannot access |

**Authentication**: OAuth 2.0 via MCP  
**Scopes**: `gmail.readonly`

### 3.2 Google Drive

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | Drive API | Search files | ✅ Verified | Full query syntax | Read-only |
| Claude MCP | Drive API | Fetch documents | ✅ Verified | Get document content | Read-only |
| Claude MCP | Drive API | List folders | ✅ Verified | Navigate folder structure | Read-only |
| Claude MCP | Drive API | Create files | ❌ Blocked | Not in MCP scope | Cannot create |
| Claude MCP | Drive API | Edit files | ❌ Blocked | Not in MCP scope | Cannot edit |

**Authentication**: OAuth 2.0 via MCP  
**Scopes**: `drive.readonly`

### 3.3 Google Calendar

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | Calendar API | List events | ✅ Verified | Full event listing | Read-only |
| Claude MCP | Calendar API | Search events | ✅ Verified | Query-based search | Read-only |
| Claude MCP | Calendar API | Find free time | ✅ Verified | Free/busy lookup | Read-only |
| Claude MCP | Calendar API | Get event details | ✅ Verified | Full event metadata | Read-only |
| Claude MCP | Calendar API | Create events | ❌ Blocked | Not in MCP scope | Cannot create |
| Claude MCP | Calendar API | Edit events | ❌ Blocked | Not in MCP scope | Cannot edit |

**Authentication**: OAuth 2.0 via MCP  
**Scopes**: `calendar.readonly`

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
| Local (אור) | Cloud Shell | SSH access | ✅ Verified | `gcloud cloud-shell ssh` works | Manual only |
| Local (אור) | Cloud Shell | Execute commands | ✅ Verified | Tested and working | Manual only |
| Claude | Cloud Shell | Automated exec | ⚠️ Planned | Need automation bridge | Not built yet |
| GitHub Actions | Cloud Shell | Execute commands | ⚠️ Planned | Possible via workflow | Not built yet |

**Evidence**: Document 6 shows Cloud Shell verified operational  
**Gap**: No automated triggering path from Claude yet

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

**Problem**: PowerShell MCP only supports 10 whitelisted commands, not full script execution

**Solution**: Create wrapper scripts that use whitelisted commands

**Pattern**:
```
Claude → PowerShell MCP (dir, type, test_path)
       → Read script file
       → Analyze content
       → [Manual] או runs script locally
```

**Status**: 🟡 Partial (can read, cannot execute)  
**Gap**: No automated execution path

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

**Issue**: Only 10 whitelisted commands available

**Impact**: ❌ Cannot execute arbitrary scripts

**Workaround**: 
1. Read script via `type` command
2. Analyze and understand
3. Request manual execution if needed

**Status**: Accepted limitation

### 8.3 Script Execution

**Issue**: 56 scripts available locally, but no direct execution path from Claude

**Impact**: Cannot automate Python/Shell scripts

**Workaround**: Either:
1. Manual execution by אור
2. Create GitHub Actions wrappers
3. Use PowerShell MCP where applicable

**Status**: Accepted limitation, automation possible via Actions

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

---

## 🔟 Roadmap to 100%

### Priority 1: Verification Runners (High Value, Low Risk)

**Goal**: Close GitHub Actions → GCP gaps

**Tasks**:
1. ✅ Sheets append (DONE)
2. ⏳ Secret Manager read (need workflow)
3. ⏳ Cloud Shell exec (need workflow)
4. ⏳ Drive write (need workflow)

**Effort**: Low (reuse existing WIF)  
**Risk**: Low (read-only operations)

### Priority 2: OAuth Migration (High Value, Medium Risk)

**Goal**: Complete secret migration

**Tasks**:
1. ✅ GOOGLE/ OAuth (DONE)
2. ⏳ GPT/ OAuth (next)
3. ⏳ GCP SA keys (verify usage first)

**Effort**: Low (proven process)  
**Risk**: Medium (requires testing)

### Priority 3: Script Automation (Medium Value, Medium Effort)

**Goal**: Enable automated script execution

**Tasks**:
1. ⏳ Create GitHub Actions for key scripts
2. ⏳ Build trigger mechanism from Claude
3. ⏳ Establish result retrieval pattern

**Effort**: Medium  
**Risk**: Low

---

## 📝 Update Log

### 2025-11-14
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
3. Commit with message: `L0: update capabilities matrix - [what changed]`

---

**This is the Single Source of Truth. All other capability descriptions must defer to this document.**

---

**Maintained by**: Claude (with אור's approval)  
**Last Verified**: 2025-11-14  
**Next Review**: As capabilities change
