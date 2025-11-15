# Windows MCP Safety Policy

**Version**: 1.2  
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

### Windows-MCP (Filesystem + Shell) ✅ ACTIVE

**Purpose**: File operations + controlled shell execution  
**Capabilities**:
- ✅ Filesystem operations (read, write, create, delete)
- ✅ Shell command execution (with policy constraints)
- ✅ Script execution (with whitelist)

**This is the execution layer for approved operations.**

---

## 📋 Command Categories

### Category: READ_ONLY ✅ ALLOWED (No Approval Required)

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

**Windows-MCP.SHELL (read-only)**:
- `gcloud projects list`
- `gcloud services list --enabled`
- `gcloud services list --available`
- `gcloud config get-value project`
- `gcloud auth list`

**Risk**: None - read-only operations  
**Approval**: Not required  
**Execution**: Automatic via MCP

---

### Category: CLOUD_OPS_SAFE ✅ ALLOWED (Approval Required)

**Purpose**: Enable Google APIs for MCP integration

**Execution Layer**: Windows-MCP.SHELL (NOT ps_exec)

**Allowed Operations**:
```powershell
gcloud services enable gmail.googleapis.com --project=edri2or-mcp
gcloud services enable drive.googleapis.com --project=edri2or-mcp
gcloud services enable calendar-json.googleapis.com --project=edri2or-mcp
gcloud services enable sheets.googleapis.com --project=edri2or-mcp
gcloud services enable docs.googleapis.com --project=edri2or-mcp
gcloud services enable iap.googleapis.com --project=edri2or-mcp
```

**Can be executed via**:
- ✅ Direct shell commands (Windows-MCP)
- ✅ PowerShell script (Windows-MCP runs script)

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

**Approval**: Required via Hebrew phrase  
**Approval Phrase**: "מאשר הפעלת Google APIs דרך Windows-MCP"  
**Execution**: Via Windows-MCP.SHELL

**Audit Trail**:
- Script: `scripts/enable_google_apis.ps1` (if used)
- Log: `logs/google_apis_enable.log`
- Commit to Git for full audit

---

### Category: CLOUD_OPS_MODERATE ⚠️ REVIEW REQUIRED

**Not Yet Approved** - requires separate approval:
- OAuth client creation
- Secret Manager operations
- Cloud Shell execution
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

3. **Claude executes via Windows-MCP**:
   - Direct shell commands OR script execution
   - Logs all output
   - Reports results
   - Commits evidence

4. **Claude updates documentation**:
   - CAPABILITIES_MATRIX
   - Relevant plan files
   - Audit logs

---

## 📊 Safety Checklist

Before executing ANY gcloud command via Windows MCP:

- [ ] Command matches allowed category exactly
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

### 2025-11-15 (v1.2)
- **Distinguished ps_exec from Windows-MCP.SHELL**
- ps_exec: NO_SCRIPT_EXECUTION - commands whitelist only
- Windows-MCP.SHELL: CLOUD_OPS_SAFE execution layer
- Clarified that script execution happens via Windows-MCP, not ps_exec
- Updated approval flow to specify Windows-MCP as execution layer
- Commit: "Separate ps_exec (read-only) from Windows-MCP.SHELL (execution)"

### 2025-11-15 (v1.1)
- Added CLOUD_OPS_SAFE category
- Approved `gcloud services enable` for 6 Google APIs
- Defined project constraint (edri2or-mcp only)
- Specified audit trail requirements
- Added FORBIDDEN category for dangerous ops

### 2025-11-14 (v1.0)
- Initial version
- Defined READ_ONLY category (11 ps_exec commands)
- Established approval flow
- Created safety checklist

---

**This policy is binding. All Windows MCP operations must comply.**
