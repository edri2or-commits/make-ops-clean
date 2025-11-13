# L1 Capabilities - What Claude Can Do Now

**Layer**: L1 (Read-Only Inspection + Controlled File Operations)  
**Last Updated**: 2025-11-13  
**Status**: Active and Constrained

---

## 🎯 Overview

This document defines what Claude Desktop can and cannot do at **Layer 1 (L1)**. All capabilities are constrained by the MCP tools available and the policies defined in `platform/manifest/policy_gate.yaml`.

---

## ✅ ALLOWED (Auto - No Approval Needed)

### 1. **System Inspection** (via ps_exec MCP)

**Read-Only PowerShell Commands** (10 whitelisted):

| Command | Purpose | Example Use |
|---------|---------|-------------|
| `whoami` | Current user identity | Check execution context |
| `get_env` | Environment variables | Find paths (TEMP, LOCALAPPDATA) |
| `get_process` | Running processes | Inspect system state |
| `get_service` | Windows services | Check service status |
| `test_path` | File/directory existence | Validate paths before operations |
| `dir` | Directory listing | Explore file structure |
| `type` | File content | Read small config files |
| `test_connection` | Network connectivity | Verify internet/host reachability |
| `get_item_property` | File/registry properties | Get metadata |
| `measure_object` | Count/measure | Count files, lines, etc. |

**Limitations**:
- ❌ Cannot execute arbitrary PowerShell
- ❌ Cannot run scripts (`.ps1`, `.bat`, `.cmd`)
- ❌ Cannot modify system state
- ❌ Cannot write files (use Filesystem MCP instead)

---

### 2. **File Operations** (via Filesystem MCP)

**Full Read/Write Access** within allowed directories:

**Read Operations**:
- ✅ `read_file` - Read complete file contents
- ✅ `read_multiple_files` - Batch read operation
- ✅ `read_media_file` - Images, audio (base64)
- ✅ `list_directory` - Directory contents with [FILE]/[DIR] prefixes
- ✅ `directory_tree` - Recursive JSON tree structure
- ✅ `get_file_info` - Metadata (size, dates, permissions)
- ✅ `search_files` - Recursive pattern search

**Write Operations**:
- ✅ `write_file` - Create or overwrite file
- ✅ `create_file` - Explicit file creation
- ✅ `edit_file` - Line-based editing (str_replace style)
- ✅ `create_directory` - Create directory structures
- ✅ `move_file` - Move/rename files

**Allowed Paths**:
- ✅ `C:\Users\edri2\` (home directory - primary workspace)
- ✅ `C:\Users\edri2\Work\AI-Projects\Claude-Ops\` (project root)
- ⚠️ `C:\` (root - use with caution, avoid system directories)

**Safety Notes**:
- No execution: Files created cannot be run by Claude
- Version control: Use GitHub for critical changes
- Evidence: Document significant file operations

---

### 3. **GitHub Operations** (via GitHub MCP)

**Full Repository Access** to `edri2or-commits/make-ops-clean`:

**Read Operations**:
- ✅ Search repositories, code, issues, users
- ✅ Get file contents (including specific branches)
- ✅ List commits, branches, PRs, issues
- ✅ Get PR details, status, files, reviews

**Write Operations**:
- ✅ Create/update files (single or batch)
- ✅ Create branches
- ✅ Create pull requests
- ✅ Create issues
- ✅ Add comments (issues, PRs)
- ✅ Create reviews on PRs
- ✅ Merge pull requests

**Governance**:
- Intent: `gh.pr.create` → **auto** (per `policy_gate.yaml`)
- All changes should follow:
  1. Feature branch creation
  2. Pull request (not direct to main)
  3. Human review (optional at L1, mandatory at L2+)

**Safety Notes**:
- Blocked: `force_push`, `repo_delete` (per policy)
- Best practice: Always use PRs, never direct main commits
- Evidence: Git history serves as audit trail

---

### 4. **Google Services** (via Google MCP)

**Read-Only Access**:

**Google Drive**:
- ✅ `google_drive_search` - Search documents by API query or semantic query
- ✅ `google_drive_fetch` - Read document contents by ID
- ❌ Cannot create or edit documents

**Gmail**:
- ✅ `search_gmail_messages` - Search with Gmail operators
- ✅ `read_gmail_thread` - Get full thread context
- ✅ `read_gmail_profile` - User email and profile
- ❌ Cannot send emails
- ❌ Cannot access attachments

**Google Calendar**:
- ✅ `list_gcal_calendars` - List available calendars
- ✅ `list_gcal_events` - Search events with filters
- ✅ `fetch_gcal_event` - Get event details
- ✅ `find_free_time` - Find free slots across calendars
- ❌ Cannot create or edit events

**Use Cases**:
- Research: Find internal documents
- Context: Read past emails for project info
- Scheduling: Check availability for meetings

---

## ⚠️ REQUIRES APPROVAL (Not Yet Implemented at L1)

### 1. **Local Installation** 

**Intent**: `local.install` (per `capability_registry.yaml`)

**Examples**:
- Installing npm packages
- Installing Python packages
- Installing Windows software

**Status**: ⏳ Not available at L1 - will be implemented in L2 via:
- MCP-wrapped `metacontrol.py` (Option A)
- Enhanced `ps_exec` with signed script execution (Option B)

**Approval Flow** (future):
```
Claude proposes → GitHub PR created → Telegram notification → 
אור approves → GitHub Actions executes → Result logged
```

---

### 2. **IAM Changes**

**Intent**: `iam_change` (per `policy_gate.yaml`)

**Examples**:
- Modifying GitHub repository permissions
- Changing Google Drive sharing settings
- Updating service account roles

**Status**: ⏳ Not available at L1 - will require explicit approval flow

---

## ❌ BLOCKED (Permanently)

### 1. **Destructive Git Operations**

**Intents**: `force_push`, `repo_delete` (per `policy_gate.yaml`)

**Examples**:
- `git push --force`
- Repository deletion
- Branch force deletion

**Reason**: Irreversible data loss risk

---

### 2. **Arbitrary Code Execution**

**What's Blocked**:
- Running PowerShell scripts (`.ps1`)
- Running batch files (`.bat`, `.cmd`)
- Running executables (`.exe`, `.msi`)
- System command execution beyond ps_exec whitelist

**Reason**: Security and control requirements

**Alternative**: Propose scripts for approval → L2 signed execution

---

### 3. **System Modifications**

**What's Blocked**:
- Registry edits (beyond read via `get_item_property`)
- Service start/stop
- User/permission modifications
- Network configuration changes

**Reason**: System stability and security

---

## 🔍 L1 Use Cases

### What Claude Can Do Effectively at L1:

**1. Documentation and Analysis**:
- ✅ Read system state (processes, services, env)
- ✅ Create comprehensive reports in Markdown
- ✅ Analyze file structures and contents
- ✅ Generate architecture diagrams (text-based)

**2. Code and Configuration Management**:
- ✅ Read/edit configuration files
- ✅ Create/update code files
- ✅ Refactor code with line-based edits
- ✅ Manage version control via GitHub PRs

**3. Research and Context Gathering**:
- ✅ Search Google Drive for internal docs
- ✅ Read Gmail for project context
- ✅ Check calendar for scheduling info
- ✅ Search GitHub for code patterns

**4. Planning and Proposal**:
- ✅ Design L2 architecture
- ✅ Propose automation workflows
- ✅ Create ADRs and decision logs
- ✅ Plan playbooks for future execution

### What Claude Cannot Do at L1:

**Execution Tasks**:
- ❌ Run automation scripts
- ❌ Install dependencies
- ❌ Execute system commands
- ❌ Trigger local Python controllers directly

**System Changes**:
- ❌ Modify system settings
- ❌ Start/stop services
- ❌ Change permissions
- ❌ Configure network

**External Modifications**:
- ❌ Send emails
- ❌ Create calendar events
- ❌ Edit Google Docs
- ❌ Post to Telegram directly

---

## 📊 Capability Matrix

| Category | Tool | Read | Write | Execute |
|----------|------|------|-------|---------|
| **Local System** | ps_exec | ✅ (10 commands) | ❌ | ❌ |
| **Files** | Filesystem MCP | ✅ | ✅ | ❌ |
| **GitHub** | GitHub MCP | ✅ | ✅ | ❌ (CI only) |
| **Drive** | Google MCP | ✅ | ❌ | ❌ |
| **Gmail** | Google MCP | ✅ | ❌ | ❌ |
| **Calendar** | Google MCP | ✅ | ❌ | ❌ |
| **Telegram** | None | ❌ | ❌ | ❌ |
| **Make.com** | None | ❌ | ❌ | ❌ |
| **Execution** | None | ❌ | ❌ | ❌ |

---

## 🎯 Upgrade Path to L2

**L2 will add**:
- ✅ Controlled script execution (policy-gated)
- ✅ MCP-wrapped local controllers
- ✅ Approval-required operations (install, IAM)
- ✅ Integration with Telegram (via metacontrol_mcp)

**See**: `BRIDGE_PROPOSAL.md` for L2 architecture

---

## 🔒 Security Principles at L1

1. **Least Privilege**: Only read-only system inspection + controlled file ops
2. **Human-in-the-Loop**: GitHub PRs for significant changes (optional but recommended)
3. **Evidence Trail**: All operations logged (GitHub commits, Evidence Index)
4. **No Execution**: Cannot run code, only create/edit files
5. **Policy-Constrained**: All capabilities defined in `policy_gate.yaml`

---

## 📋 Quick Reference

**What can I ask Claude to do?**
- ✅ "Read my environment variables"
- ✅ "List all running processes"
- ✅ "Create a markdown report about X"
- ✅ "Search my Drive for documents about Y"
- ✅ "Create a PR with these changes"
- ✅ "Edit this config file"

**What will Claude refuse?**
- ❌ "Run this PowerShell script"
- ❌ "Install this package"
- ❌ "Send an email to X"
- ❌ "Start this Windows service"
- ❌ "Execute this program"

---

**End of L1 Capabilities Document**

For L2 planning, see: `BRIDGE_PROPOSAL.md`  
For current infrastructure status, see: `CURRENT_STATE.md`
