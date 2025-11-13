# Current State - L1 Active Infrastructure

**Last Updated**: 2025-11-13  
**Status**: L1 Operational | L2 Planning Phase

---

## 🎯 Executive Summary

The infrastructure is at **Layer 1 (L1)** - Read-Only Inspection + Controlled File Operations. We have:
- ✅ GitHub Control Plane with governance (manifest, policies, L1.2 approval flow)
- ✅ Telegram approval workflow via Make.com webhooks
- ✅ Local Python automation controllers (disconnected from Claude Desktop)
- ✅ MCP stack for Claude Desktop (ps_exec, Filesystem, GitHub, Google)

**Key Gap**: Claude Desktop MCP ↔ Local Controllers are not integrated. L2 will bridge this.

---

## ✅ What's Working

### 1. **GitHub Control Plane** (Fully Operational)

**Location**: `edri2or-commits/make-ops-clean`

**Governance Structure**:
```yaml
/platform/manifest/
  ├── capability_registry.yaml  # Intent → Driver mapping
  ├── policy_gate.yaml          # Auto/Approval/Blocked policies
  ├── status.json               # KPIs and health tracking
  ├── manifest.schema.json      # Zero-Touch schema v1
  └── ADRs/ADR-0001-bootstrap.md
```

**Capabilities Defined**:
- `gh.pr.create` → **auto** (no approval needed)
- `google.project.info` → **auto** 
- `local.install` → **requires_approval**
- `iam_change` → **requires_approval**
- `force_push`, `repo_delete` → **blocked**

**Approval Flow (L1.2 Zero-Touch)**:
```
Claude → create-approval-request.sh
  ↓ webhook
Make Scenario #1 → Telegram (inline buttons ✅/❌)
  ↓ callback_query
Make Scenario #2 → GitHub repository_dispatch
  ↓ triggers
GitHub Actions (execute-on-approval.yml)
  ↓ verifies secrets → executes → commits → notifies
Telegram notification to אור
```

**Timeline**: ~50-160 seconds end-to-end

---

### 2. **MCP Stack for Claude Desktop**

**Active MCP Servers**:

#### ps_exec (PowerShell Dispatcher)
- **Location**: `C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\ps_exec\`
- **Capabilities**: 10 whitelisted read-only commands
  - `dir`, `type`, `test_path`, `whoami`, `get_process`, `get_service`, `get_env`, `test_connection`, `get_item_property`, `measure_object`
- **Limitations**: 
  - ❌ Cannot execute PowerShell scripts
  - ❌ Cannot write files
  - ❌ Cannot modify system

#### Filesystem MCP (Native Claude)
- **Capabilities**: Full read/write access
- **Allowed Paths**: 
  - ✅ `C:\Users\edri2\`
  - ✅ `C:\` (with caution)
- **Can**: Create, read, edit, move, delete files and directories

#### GitHub MCP
- **Auth**: PAT-based
- **Repo**: `edri2or-commits/make-ops-clean`
- **Capabilities**: 
  - ✅ Full repo operations (read, write, PR, branches, issues)
  - ✅ Workflows, artifacts, commits

#### Google Services MCP
- **Drive**: Search and fetch documents (read-only)
- **Gmail**: Read and search messages (read-only, no send)
- **Calendar**: List events, find free time (read-only)

---

### 3. **Local Python Controllers** (Disconnected)

**Location**: `C:\Users\edri2\Work\AI-Projects\Claude-Ops\`

#### metacontrol.py
- **Purpose**: Full control system integration
- **Capabilities**:
  - Telegram API (send messages)
  - GitHub API (commit files)
  - OpenAI API (GPT calls)
  - Make.com webhooks
  - State management (autopilot-state.json)
- **Status**: ⚠️ Not accessible via Claude Desktop MCP

#### claude_auto_agent.py
- **Purpose**: File downloader agent
- **Watches**: `claude_command_interface.json`
- **Actions**: Downloads files from URLs (multi-file support)
- **Loop**: 5-second polling
- **Status**: ⚠️ Runs independently, no MCP integration

#### local_controller.py
- **Purpose**: Command executor
- **Watches**: `local_cmd.json`
- **Actions**: `write_file`, `run_file`, `delete_file`
- **Loop**: 5-second polling
- **Status**: ⚠️ Runs independently, no MCP integration

---

### 4. **Evidence & Audit System**

**Location**: `C:\Users\edri2\Work\AI-Projects\Claude-Ops\`

- `/Data/Evidence Index.xlsx` - Centralized evidence tracking
- `/_audit/` - Logs, backups, phase tracking
- `/Documentation/` - ADRs, decision logs, PDFs
- `autopilot-state.json` - System state tracking

---

## ⚠️ What's Disconnected

### 1. **Claude Desktop ↔ Local Controllers Gap**

**Problem**: 
- Claude Desktop uses MCP protocol to interact with tools
- Local Python controllers run independently (polling JSON files)
- No direct communication bridge

**Impact**:
- Claude cannot trigger `metacontrol.py` functions directly
- Claude cannot use `local_controller.py` for execution
- Controllers don't respect `policy_gate.yaml` constraints

**Solution Path**: L2 - MCP-ify controllers (see BRIDGE_PROPOSAL.md)

---

### 2. **ps_exec Limitations**

**Problem**: ps_exec is read-only by design
- Cannot execute PowerShell scripts
- Cannot install software
- Cannot modify system settings

**Impact**: 
- Limited to inspection tasks only
- No automation execution on local machine

**Solution Path**: L2 - Add constrained execution MCP (policy-gated)

---

## 🏗️ Current Architecture

```
┌────────────────────────────────────────────────────────┐
│  אור (Human Approval Gate)                            │
│  ↕ Telegram approvals via L1.2 flow                   │
└────────────────────────────────────────────────────────┘
         ↕
┌────────────────────────────────────────────────────────┐
│  GitHub: make-ops-clean (Control Plane)               │
│  • Governance: manifest, policies, registry           │
│  • Workflows: L1.2 approval flow                      │
│  • Evidence: ADRs, status tracking                    │
└────────────────────────────────────────────────────────┘
         ↕
┌────────────────────────────────────────────────────────┐
│  Claude Desktop (MCP Client)                           │
│  ├─ ps_exec (Read-Only PowerShell)                    │
│  ├─ Filesystem (Full R/W)                             │
│  ├─ GitHub (Full R/W)                                 │
│  └─ Google (Read-Only)                                │
└────────────────────────────────────────────────────────┘
         ↕ (GAP - No Integration)
┌────────────────────────────────────────────────────────┐
│  Local Controllers (Independent)                       │
│  ├─ metacontrol.py (Telegram, GitHub, OpenAI, Make)  │
│  ├─ claude_auto_agent.py (File downloader)           │
│  └─ local_controller.py (Command executor)           │
└────────────────────────────────────────────────────────┘
         ↕
┌────────────────────────────────────────────────────────┐
│  Windows Local Machine                                 │
│  C:\Users\edri2\Work\AI-Projects\Claude-Ops\          │
└────────────────────────────────────────────────────────┘
```

---

## 📊 L1 Definition

### What L1 Allows:

**Read-Only Inspection**:
- System information (processes, services, environment)
- File content reading
- Directory structure exploration

**Controlled File Operations**:
- File creation/editing (via Filesystem MCP)
- File movement/deletion (with caution)

**GitHub Operations**:
- PR creation
- Branch management
- Issue tracking

**No Execution**:
- ❌ Cannot run scripts
- ❌ Cannot install software
- ❌ Cannot modify system settings
- ❌ Cannot execute commands beyond ps_exec whitelist

---

## 🎯 Next Steps

1. **Document L1 Capabilities** → L1_CAPABILITIES.md
2. **Design L2 Bridge** → BRIDGE_PROPOSAL.md
3. **Run L1 Inventory PoC** → Validate current tooling
4. **Decision Point**: Choose L2 approach
   - Option A: MCP-ify controllers (strategic, future-proof)
   - Option B: Enhanced ps_exec (tactical, quick win)
   - Option C: Stay L1 (document only, defer L2)

---

## 📋 Governance Status

**Current Layer**: L1 (Read-Only + File Operations)  
**Approval Mechanism**: L1.2 Zero-Touch (Telegram → Make → GitHub Actions)  
**Evidence Tracking**: Active (Evidence Index + _audit/)  
**Security Posture**: Conservative (no execution, human-in-loop for approvals)

**Ready for**: L2 Planning and Implementation

---

**End of Current State Assessment**
