# L1 Inventory Report - System Baseline

**Generated**: 2025-11-13T15:01:00Z  
**Layer**: L1 (Read-Only Inspection)  
**Scope**: Limited baseline scan (environment, processes, services, directory structure)

---

## 🎯 Executive Summary

This report establishes a baseline understanding of the local Windows environment using **read-only L1 tools only** (ps_exec + Filesystem MCP). No system modifications were made.

**Key Findings**:
- ✅ System architecture: AMD64 (x64)
- ✅ User profile: `C:\Users\edri2\`
- ✅ Project root: `C:\Users\edri2\Work\AI-Projects\Claude-Ops\`
- ✅ Active processes: ChatGPT, Chrome, Adobe services
- ✅ Critical services: Running normally

---

## 🖥️ System Information

### Environment Variables (Key Paths)

| Variable | Value |
|----------|-------|
| **USERNAME** | edri2 |
| **COMPUTERNAME** | DESKTOP-D9F52CF |
| **USERPROFILE** | C:\Users\edri2 |
| **TEMP** | C:\Users\edri2\AppData\Local\Temp |
| **LOCALAPPDATA** | C:\Users\edri2\AppData\Local |
| **APPDATA** | C:\Users\edri2\AppData\Roaming |
| **SYSTEMDRIVE** | C: |
| **SYSTEMROOT** | C:\WINDOWS |
| **PROCESSOR_ARCHITECTURE** | AMD64 |

**PATH** (partial):
- C:\Program Files\nodejs
- C:\Program Files\Python314\Scripts\
- C:\Program Files\Python314\

**Notable**:
- PowerShell Execution Policy: **Bypass** (via PSExecutionPolicyPreference)
- System is 64-bit (AMD64)
- Python 3.14 and Node.js are installed

---

## 📊 Running Processes (Top 20)

**Snapshot Time**: 2025-11-13T15:00:28Z

### AI/Automation Tools:
| Process | PID | CPU(s) | Memory(MB) | Notes |
|---------|-----|--------|------------|-------|
| ChatGPT | 22492 | 18.80 | 136.2 | Primary instance |
| ChatGPT | 11724 | 7.19 | 126.7 | Secondary instance |
| chrome | 10892 | 37.14 | 160.8 | Browser (main) |
| chrome | 11752 | 37.14 | 166.5 | Browser (renderer) |

### Adobe Services:
| Process | PID | CPU(s) | Memory(MB) |
|---------|-----|--------|------------|
| ace_engine | 14392 | 19.05 | 81.2 |
| AdobeCollabSync | 23932 | 2.89 | 17.4 |
| AdobeCollabSync | 24276 | 0.14 | 7.4 |

### System Services:
| Process | PID | CPU(s) | Memory(MB) |
|---------|-----|--------|------------|
| AdminService | 4532 | - | 2.5 |
| AggregatorHost | 10568 | - | 2.7 |
| armsvc | 4536 | - | 1.8 |

**Total Processes Scanned**: 20 (truncated from full list)

**CPU Activity**:
- Highest CPU: chrome (37.14s), ChatGPT (18.80s), ace_engine (19.05s)
- System is moderately active

---

## 🔧 Windows Services (Top 20 Running)

**Snapshot Time**: 2025-11-13T15:01:06Z

### Critical Services (Running):

| Name | Display Name | Status |
|------|--------------|--------|
| **AudioEndpointBuilder** | Windows Audio Endpoint Builder | Running |
| **Audiosrv** | Windows Audio | Running |
| **BFE** | Base Filtering Engine | Running |
| **BITS** | Background Intelligent Transfer Service | Running |
| **BrokerInfrastructure** | Background Tasks Infrastructure | Running |
| **BDESVC** | BitLocker Drive Encryption Service | Running |

### Third-Party Services (Running):

| Name | Display Name | Status |
|------|--------------|--------|
| **AdobeARMservice** | Adobe Acrobat Update Service | Running |
| **AtherosSvc** | Atheros Service | Running |

### Security/Network:
| Name | Display Name | Status |
|------|--------------|--------|
| **Appinfo** | Application Information | Running |
| **AppXSvc** | AppX Deployment Service | Running |

**Notes**:
- Essential Windows services are running normally
- BitLocker is active (BDESVC)
- Audio services operational
- Adobe update service running

---

## 📁 Project Directory Structure

**Root**: `C:\Users\edri2\Work\AI-Projects\Claude-Ops\`

### Top-Level Directories:

| Directory | Purpose (Inferred) |
|-----------|-------------------|
| **Archives** | Archived packages and zips |
| **Assets** | Images and media files |
| **canvas_draw** | Canvas drawing app project |
| **Config** | Configuration files |
| **Credentials** | Keys and secrets (sensitive!) |
| **Data** | Evidence, proofs, spreadsheets |
| **Documentation** | ADRs, PDFs, markdown docs |
| **edri2or-mcp** | MCP server project |
| **gh-controls-draft** | GitHub governance drafts |
| **Github** | Empty directory |
| **GOOGLE** | Google API related |
| **GPT** | GPT integration files |
| **Logs** | System logs |
| **MAKE** | Empty directory |
| **MCP** | MCP infrastructure (controllers, repo clone) |
| **mcp-servers** | MCP server implementations |
| **ops** | Operations directory |
| **Scripts** | PowerShell/shell scripts |
| **_audit** | Audit logs and backups |
| **טוקנים** | Hebrew: Tokens directory |
| **טלגרם** | Hebrew: Telegram directory |
| **קבצים גיט האב וורקפלוו** | Hebrew: GitHub workflow files |
| **קנולג 2.11.25** | Hebrew: Knowledge pack (dated 2.11.25) |

### Key Files (Root Level):

**Python Controllers**:
- `metacontrol.py` - Main control system
- `claude_auto_agent.py` - Auto downloader agent
- `claude_writer.py` - File writer agent

**Configuration**:
- `config.json` - System config
- `autopilot-state.json` - Autopilot state
- `claude_desktop_config.json` - Claude Desktop config

**PowerShell Scripts**:
- `FULL_AUTOPILOT.ps1`
- `run_autopilot.ps1`
- `CLAUDE_TRIGGER.ps1`
- Multiple cloudshell test scripts

**Documentation**:
- `README.md`
- `DEPLOYMENT_CHECKLIST.md`
- `GAPS_AND_RISKS.md`
- `ONBOARDING_MAP.md`
- `RUNBOOK_APPROVAL_FLOW.md`

**Executables**:
- `Docker Desktop Installer.exe`

---

## 🔍 Security Observations

### ⚠️ Sensitive Directories Detected:
1. **Credentials/** - Contains keys and secrets
   - `auditor-ops.*.private-key.pem` files
   - `client_secret_*.json` files
   - ⚠️ Should be encrypted or moved to vault

2. **_audit/** - Contains backups
   - Purged credentials from 2025-11-11
   - GitHub App metadata
   - ⚠️ Should verify no active secrets in backups

3. **טוקנים/** - Contains bootstrap env files
   - `claude_bootstrap.env`
   - ⚠️ Should be encrypted or removed

### ✅ Good Practices Observed:
- Evidence tracking system in place (`Data/Evidence Index.xlsx`)
- Audit logging enabled (`_audit/` directory)
- Documentation comprehensive
- Structured project layout

---

## 📊 Directory Statistics

**Top-Level Items**:
- Directories: 20
- Files: 117+ (many configuration, scripts, docs)
- Hebrew-named directories: 3 (טוקנים, טלגרם, קבצים גיט האב וורקפלוו, קנולג 2.11.25 = 4)

**File Types** (partial scan):
- Python scripts (`.py`): ~15+
- PowerShell scripts (`.ps1`): ~10+
- Batch files (`.bat`): ~10+
- Markdown docs (`.md`): ~15+
- Configuration (`.json`, `.xml`, `.yaml`): ~10+
- Archives (`.zip`): ~5+
- Executables (`.exe`): 1

---

## 🎯 L1 Tool Usage Summary

### Tools Used:
1. ✅ `ps_exec:get_env` - Environment variables
2. ✅ `ps_exec:get_process` - Running processes
3. ✅ `ps_exec:get_service` - Windows services
4. ✅ `Filesystem:list_directory` - Directory structure

### Limitations Encountered:
- ❌ Cannot execute scripts to gather deeper metrics
- ❌ Cannot read file sizes recursively (would be slow)
- ❌ Cannot check registry for installed software
- ❌ Cannot query WMI for hardware details

### What Would Require L2:
- Recursive disk usage analysis
- Installed software inventory (via registry/WMI)
- Network configuration details
- Performance counters over time

---

## ✅ Validation

**L1 Constraints Respected**:
- ✅ Read-only operations only
- ✅ No file modifications
- ✅ No script executions
- ✅ No system changes
- ✅ Limited scope (environment, processes, services, top-level dirs)

**Evidence Trail**:
- ✅ All commands logged to GitHub (this report)
- ✅ Timestamps recorded
- ✅ No sensitive data exposed in report

---

## 🚀 Next Steps

### Immediate:
1. **Review this report** - Verify findings with אור
2. **Security audit** - Review Credentials/, _audit/, טוקנים/ for active secrets
3. **Decision point** - Approve L2 planning or stay at L1

### L2 Planning (if approved):
1. **Option A**: MCP-ify metacontrol.py and local_controller.py
2. **Option B**: Enhance ps_exec for signed script execution
3. **Governance**: Update allowlist.json with approved scripts

### Documentation:
1. ✅ CURRENT_STATE.md - Created
2. ✅ L1_CAPABILITIES.md - Created
3. ✅ BRIDGE_PROPOSAL.md - Created
4. ✅ L1_INVENTORY_REPORT.md - This document

---

## 📋 Summary

**System Status**: ✅ Healthy
- Windows services: Running normally
- Key processes: ChatGPT, Chrome, Adobe tools active
- Project structure: Well-organized with evidence tracking
- Security: Some sensitive files detected (Credentials/, _audit/, טוקנים/)

**L1 Capabilities**: ✅ Validated
- Read-only inspection: Working as expected
- File operations: Available via Filesystem MCP
- GitHub operations: Available via GitHub MCP
- Execution: Blocked (by design)

**Readiness for L2**: ⏳ Pending Decision
- Infrastructure: In place (controllers, governance files)
- Security: Requires secrets audit before L2
- Documentation: Complete
- Approval: Awaiting אור decision on Option A/B/C

---

**End of L1 Inventory Report**

**Generated by**: Claude Desktop (L1 Read-Only Tools)  
**Approval Status**: ⏳ Awaiting Review  
**Next Action**: אור reviews → Return to GPT → Decide L2 path

---

See also:
- [CURRENT_STATE.md](https://github.com/edri2or-commits/make-ops-clean/blob/main/CURRENT_STATE.md)
- [L1_CAPABILITIES.md](https://github.com/edri2or-commits/make-ops-clean/blob/main/L1_CAPABILITIES.md)
- [BRIDGE_PROPOSAL.md](https://github.com/edri2or-commits/make-ops-clean/blob/main/BRIDGE_PROPOSAL.md)
