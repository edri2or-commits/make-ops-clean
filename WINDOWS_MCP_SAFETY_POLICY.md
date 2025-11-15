# Windows MCP Safety Policy

**Version**: 1.3  
**Last Updated**: 2025-11-15  
**Purpose**: Define safety boundaries for PowerShell/gcloud execution via MCP

---

## 🎯 Core Principle

**Windows MCP enables execution, but only within strict safety boundaries.**

This policy defines:
- What commands are ALLOWED (safe, auditable)
- What commands are FORBIDDEN (dangerous, destructive)
- Approval requirements for each category

---

## 🛠️ MCP Tools Available

### ps_exec MCP ✅ ACTIVE

**Purpose**: Read-only system inspection  
**Capability**: 11 whitelisted commands ONLY  
**Script Execution**: ❌ NO - Commands whitelist only

**This is by design** - ps_exec remains a minimal, audited tool.

### Windows Shell MCP ✅ ACTIVE

**Purpose**: Policy-enforced shell execution (JEA-style)  
**Capabilities**:
- ✅ gcloud command execution (with constraints)
- ✅ Secret Manager operations (with constraints)
- ✅ Config file management (with backup)
- ✅ Full audit logging

**This is the execution layer for approved operations.**

---

## 📋 Command Categories

### Category: OS_SAFE ✅ ALLOWED (No Approval Required)

**ps_exec Commands** (11 whitelisted):
- `dir` - List directory contents
- `type` - Read file contents
- `test_path` - Check if path exists
- `whoami` - Get current user
- `get_process` - List running processes
- `get_service` - List Windows services
- `get_env` - Get environment variables
- `test_connection` - Test network connectivity
- `get_item_property` - Get registry/file properties
- `measure_object` - Count/measure objects
- `screenshot` - Capture display screenshot

**Windows Shell MCP Tools**:
- `check_gcloud_version` - Get gcloud version info
- `check_powershell_version` - Get PowerShell version info
- `get_execution_log` - Read audit trail
- `read_secret` - Read from Secret Manager (read-only)
- `backup_claude_config` - Backup Claude config file

**Risk**: None - read-only operations  
**Approval**: Not required  
**Execution**: Automatic via MCP

---

### Category: CLOUD_OPS_SAFE ✅ ALLOWED (Approval Required)

**Purpose**: Enable Google APIs for MCP integration

**Execution Layer**: Windows Shell MCP

**Tool**: `enable_google_apis`

**Allowed Operations**:
```bash
gcloud services enable gmail.googleapis.com --project=edri2or-mcp
gcloud services enable drive.googleapis.com --project=edri2or-mcp
gcloud services enable calendar-json.googleapis.com --project=edri2or-mcp
gcloud services enable sheets.googleapis.com --project=edri2or-mcp
gcloud services enable docs.googleapis.com --project=edri2or-mcp
gcloud services enable iap.googleapis.com --project=edri2or-mcp
```

**Constraints**:
- ✅ ONLY `gcloud services enable`
- ✅ ONLY the 6 APIs listed above
- ✅ ONLY `--project=edri2or-mcp`
- ❌ NO other gcloud commands
- ❌ NO other projects
- ❌ NO IAM changes
- ❌ NO deletions

**Risk**: Low
- APIs are within GCP Free Tier
- No billing impact expected
- Read/write scopes require separate OAuth consent
- Reversible (can disable APIs)

**Approval Phrase**: "מאשר הפעלת Google APIs דרך Windows-MCP"  
**Execution**: Via Windows Shell MCP  
**Status**: ✅ Phase 1 COMPLETE (2025-11-15)

**Audit Trail**:
- MCP log: `mcp-servers/windows-shell/logs/execution.log`
- Detailed log: `logs/google_apis_enable.log`

---

### Category: CLOUD_OPS_HIGH ⚠️ ALLOWED (Approval Required)

**Purpose**: OAuth credentials and full Google access management

**Execution Layer**: Windows Shell MCP

**Tools**:
1. **store_secret** - Store OAuth credentials in Secret Manager
2. **update_claude_config** - Update Claude Desktop with Google MCP

**Allowed Operations**:

**store_secret**:
```bash
gcloud secrets create google-mcp-client-id --data-file=- --project=edri2or-mcp
gcloud secrets create google-mcp-client-secret --data-file=- --project=edri2or-mcp
gcloud secrets versions add google-mcp-client-id --data-file=- --project=edri2or-mcp
gcloud secrets versions add google-mcp-client-secret --data-file=- --project=edri2or-mcp
```

**update_claude_config**:
- Backup existing claude_desktop_config.json
- Add 'google-full' MCP server entry
- Configure with OAuth credentials
- Only allowed scopes: gmail.modify, drive, calendar, spreadsheets, documents

**Constraints**:

**store_secret**:
- ✅ ONLY project: edri2or-mcp
- ✅ ONLY secret names starting with: google-mcp-
- ✅ ONLY creates or updates (no deletions)
- ❌ NO other projects
- ❌ NO other secret prefixes
- ❌ NO IAM operations

**update_claude_config**:
- ✅ ONLY allowed OAuth scopes (5 specific scopes)
- ✅ ONLY adds 'google-full' MCP server
- ✅ Creates backup before modification
- ❌ NO scope expansion beyond approved list
- ❌ NO removal of existing MCP servers

**Risk**: HIGH
- Credentials grant full Gmail/Drive/Calendar/Sheets/Docs access
- Can send emails, modify files, create events
- Stored securely in Secret Manager (encrypted at rest)
- OAuth consent still required (user-controlled)
- Reversible (can delete secrets, remove MCP config, revoke OAuth)

**Approval Phrases**:
- store_secret: "מאשר אחסון credentials ב-Secret Manager"
- update_claude_config: "מאשר עדכון Claude config עם Google MCP"

**Execution**: Via Windows Shell MCP  
**Status**: ⏸️ Tools built, awaiting execution approval

**Audit Trail**:
- MCP execution log: `mcp-servers/windows-shell/logs/execution.log`
- Config backup: `claude_desktop_config.backup.{timestamp}.json`
- Secret Manager audit logs (GCP)

**Why HIGH Risk**:
- Full Google account access via OAuth
- Credentials with broad scopes
- Persistent access (stored credentials)
- Requires strict approval gates

---

### Category: CLOUD_OPS_MODERATE ⚠️ REVIEW REQUIRED

**Not Yet Approved** - requires separate approval:
- OAuth client creation (manual Console path approved)
- Cloud Shell execution
- Additional Secret Manager operations
- Service account operations

**These will be addressed in future phases with explicit approval.**

---

### Category: DANGEROUS ❌ FORBIDDEN

**Never Allowed** - even with approval:

**IAM Operations**:
- `gcloud iam *` (any IAM changes)
- Service account key creation
- Role bindings
- Permission changes

**Destructive Operations**:
- `gcloud projects delete`
- `gcloud services disable` (without explicit case-by-case approval)
- Resource deletion commands
- Billing changes

**Project Changes**:
- `gcloud config set project` (to different project)
- Operations on projects other than `edri2or-mcp`

**System-Level**:
- Registry modifications (except via approved scripts)
- Service installations
- Firewall changes
- User account modifications

**Reasoning**: These operations are irreversible, high-risk, or violate security boundaries.

---

## 🔐 Approval Flow

### For CLOUD_OPS_SAFE Operations

1. **Claude proposes operation**:
   - Shows exact commands
   - Explains risk/impact
   - Provides audit trail location

2. **Or reviews and approves**:
   - Hebrew approval phrase required
   - Approval is time-bounded (single session)
   - Approval covers specific operation only

3. **Claude executes via Windows Shell MCP**:
   - Tool calls with validated parameters
   - Logs all output
   - Reports results
   - Updates documentation

4. **Claude updates documentation**:
   - CAPABILITIES_MATRIX
   - Relevant plan files
   - Audit logs

### For CLOUD_OPS_HIGH Operations

**Same as CLOUD_OPS_SAFE, plus**:
- Full transparency on credentials being stored
- Explicit scope listing
- Confirmation of reversibility
- Tool-specific approval phrases

---

## 📊 Safety Checklist

Before executing ANY Windows Shell MCP tool:

- [ ] Tool matches allowed category exactly
- [ ] Approval obtained (if required)
- [ ] Operation creates audit log
- [ ] Operation is reversible OR low-risk
- [ ] Project constraint verified (`edri2or-mcp` only)
- [ ] No IAM/destructive operations
- [ ] Results will be documented

---

## 🚨 Emergency Stop

If at ANY point during execution:
- Unexpected permission errors occur
- Commands behave differently than documented
- Safety boundaries are unclear

**Claude MUST**:
1. STOP execution immediately
2. Document what happened
3. Report to Or with full context
4. Wait for explicit guidance

**Claude MUST NOT**:
- Try alternate commands without approval
- Escalate privileges
- Modify safety policy without approval
- Continue on error

---

## 📝 Update Log

### 2025-11-15 (v1.3)
- **Added CLOUD_OPS_HIGH category** ⭐
- Added store_secret tool (Secret Manager)
- Added update_claude_config tool (Claude Desktop config)
- Defined HIGH risk level for OAuth credentials
- Tool-specific approval phrases
- Updated OS_SAFE category with new tools
- Commit: "Add CLOUD_OPS_HIGH category for OAuth credentials"

### 2025-11-15 (v1.2)
- Distinguished ps_exec from Windows Shell MCP
- ps_exec: NO_SCRIPT_EXECUTION - commands whitelist only
- Windows Shell MCP: Policy-enforced execution layer
- Clarified execution layers

### 2025-11-15 (v1.1)
- Added CLOUD_OPS_SAFE category
- Approved `gcloud services enable` for 6 Google APIs
- Defined project constraint (edri2or-mcp only)
- Specified audit trail requirements

### 2025-11-14 (v1.0)
- Initial version
- Defined OS_SAFE category (11 ps_exec commands)
- Established approval flow
- Created safety checklist

---

**This policy is binding. All Windows MCP operations must comply.**
