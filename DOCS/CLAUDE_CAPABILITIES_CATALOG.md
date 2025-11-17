# CLAUDE CAPABILITIES CATALOG

**Purpose**: Complete catalog of ALL capabilities available to Claude across Google Workspace, GitHub, and BUS/Orchestration systems.

**Created**: 2025-11-17  
**For**: Or (Strategic Decision Making)  
**Mode**: OS_SAFE Documentation Only

---

## 📊 SUMMARY DASHBOARD

| Category | AVAILABLE_NOW | INFRA_PRESENT | NOT_AVAILABLE | Total |
|----------|---------------|---------------|---------------|-------|
| **Google Workspace** | 9 | 0 | 15 | 24 |
| **GitHub** | 12 | 2 | 0 | 14 |
| **BUS/Orchestration** | 3 | 4 | 0 | 7 |
| **TOTAL** | 24 | 6 | 15 | 45 |

---

## A. GOOGLE WORKSPACE CAPABILITIES

### A.1 Gmail

| Name | Area | Type | Current_Status | Risk_Level | Or_Touch | Source_of_Truth | Or_Benefit_Type | Notes |
|------|------|------|----------------|------------|----------|-----------------|-----------------|-------|
| Gmail - Read Profile | Google | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP server-google-workspace (verified 2025-11-17) | COGNITIVE_LOAD↓ | Tool: read_gmail_profile |
| Gmail - Search Messages | Google | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP server-google-workspace (verified 2025-11-17) | COGNITIVE_LOAD↓ | Tool: search_gmail_messages, full search syntax |
| Gmail - Read Thread | Google | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP server-google-workspace (verified 2025-11-17) | COGNITIVE_LOAD↓ | Tool: read_gmail_thread |
| Gmail - Read Message | Google | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP server-google-workspace (verified 2025-11-17) | COGNITIVE_LOAD↓ | Tool: read_gmail_message |
| Gmail - Send Email | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_HIGH | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | LEVERAGE↑ | Needs Path A/B/C implementation |
| Gmail - Modify Labels | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | COGNITIVE_LOAD↓ | Needs Path A/B/C implementation |
| Gmail - Create Draft | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | COGNITIVE_LOAD↓ | Needs Path A/B/C implementation |
| Gmail - Delete Message | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_HIGH | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | PROTECTION↑ | Needs Path A/B/C implementation |
| Gmail - Download Attachment | Google | READ | NOT_AVAILABLE | OS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | COGNITIVE_LOAD↓ | Needs Path A/B/C implementation |

### A.2 Google Drive

| Name | Area | Type | Current_Status | Risk_Level | Or_Touch | Source_of_Truth | Or_Benefit_Type | Notes |
|------|------|------|----------------|------------|----------|-----------------|-----------------|-------|
| Drive - Search Files | Google | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP server-google-workspace (verified 2025-11-17) | COGNITIVE_LOAD↓ | Tool: google_drive_search, full query syntax |
| Drive - Fetch Document | Google | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP server-google-workspace (verified 2025-11-17) | COGNITIVE_LOAD↓ | Tool: google_drive_fetch |
| Drive - List Folders | Google | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP server-google-workspace (verified 2025-11-17) | COGNITIVE_LOAD↓ | Part of search capability |
| Drive - Create File | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | LEVERAGE↑ | Needs Path A/B/C implementation |
| Drive - Edit File | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | LEVERAGE↑ | Needs Path A/B/C implementation |
| Drive - Delete File | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_HIGH | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | PROTECTION↑ | Needs Path A/B/C implementation |
| Drive - Share File | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | LEVERAGE↑ | Needs Path A/B/C implementation |
| Drive - Upload File | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | LEVERAGE↑ | Needs Path A/B/C implementation |

### A.3 Google Calendar

| Name | Area | Type | Current_Status | Risk_Level | Or_Touch | Source_of_Truth | Or_Benefit_Type | Notes |
|------|------|------|----------------|------------|----------|-----------------|-----------------|-------|
| Calendar - List Calendars | Google | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP server-google-workspace (verified 2025-11-17) | COGNITIVE_LOAD↓ | Tool: list_gcal_calendars |
| Calendar - List Events | Google | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP server-google-workspace (verified 2025-11-17) | COGNITIVE_LOAD↓ | Tool: list_gcal_events |
| Calendar - Get Event Details | Google | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP server-google-workspace (verified 2025-11-17) | COGNITIVE_LOAD↓ | Tool: fetch_gcal_event |
| Calendar - Find Free Time | Google | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP server-google-workspace (verified 2025-11-17) | COGNITIVE_LOAD↓ | Tool: find_free_time |
| Calendar - Create Event | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | LEVERAGE↑ | Needs Path A/B/C implementation |
| Calendar - Update Event | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | COGNITIVE_LOAD↓ | Needs Path A/B/C implementation |
| Calendar - Delete Event | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_HIGH | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks this tool | PROTECTION↑ | Needs Path A/B/C implementation |

### A.4 Google Sheets

| Name | Area | Type | Current_Status | Risk_Level | Or_Touch | Source_of_Truth | Or_Benefit_Type | Notes |
|------|------|------|----------------|------------|----------|-----------------|-----------------|-------|
| Sheets - Read Spreadsheet | Google | READ | NOT_AVAILABLE | OS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks Sheets entirely | COGNITIVE_LOAD↓ | OAuth scope granted, MCP doesn't implement |
| Sheets - Update Cells | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks Sheets entirely | LEVERAGE↑ | Needs Path A/B/C implementation |
| Sheets - Create Spreadsheet | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks Sheets entirely | LEVERAGE↑ | Needs Path A/B/C implementation |
| Sheets - Append Rows | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks Sheets entirely | LEVERAGE↑ | Note: GitHub Actions CAN do this via WIF |

### A.5 Google Docs

| Name | Area | Type | Current_Status | Risk_Level | Or_Touch | Source_of_Truth | Or_Benefit_Type | Notes |
|------|------|------|----------------|------------|----------|-----------------|-----------------|-------|
| Docs - Read Document | Google | READ | NOT_AVAILABLE | OS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks Docs entirely | COGNITIVE_LOAD↓ | OAuth scope granted, MCP doesn't implement |
| Docs - Create Document | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks Docs entirely | LEVERAGE↑ | Needs Path A/B/C implementation |
| Docs - Edit Document | Google | WRITE | NOT_AVAILABLE | CLOUD_OPS_SAFE | APPROVAL_ONLY | אין באפשרותי לאשר - MCP lacks Docs entirely | LEVERAGE↑ | Needs Path A/B/C implementation |

---

## B. GITHUB CAPABILITIES

### B.1 GitHub - Read Operations

| Name | Area | Type | Current_Status | Risk_Level | Or_Touch | Source_of_Truth | Or_Benefit_Type | Notes |
|------|------|------|----------------|------------|----------|-----------------|-----------------|-------|
| GitHub - Read Repository | GitHub | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP github (verified via CAPABILITIES_MATRIX) | COGNITIVE_LOAD↓ | Full repo access |
| GitHub - Read File Contents | GitHub | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP github (verified via CAPABILITIES_MATRIX) | COGNITIVE_LOAD↓ | github:get_file_contents |
| GitHub - Search Code | GitHub | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP github (verified via CAPABILITIES_MATRIX) | COGNITIVE_LOAD↓ | github:search_code |
| GitHub - List Commits | GitHub | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP github (verified via CAPABILITIES_MATRIX) | COGNITIVE_LOAD↓ | Full commit history |
| GitHub - List Branches | GitHub | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP github (verified via CAPABILITIES_MATRIX) | COGNITIVE_LOAD↓ | Branch management |

### B.2 GitHub - Write Operations

| Name | Area | Type | Current_Status | Risk_Level | Or_Touch | Source_of_Truth | Or_Benefit_Type | Notes |
|------|------|------|----------------|------------|----------|-----------------|-----------------|-------|
| GitHub - Create/Update File | GitHub | WRITE | AVAILABLE_NOW | CLOUD_OPS_SAFE | APPROVAL_ONLY | MCP github (verified via CAPABILITIES_MATRIX) | LEVERAGE↑ | github:create_or_update_file |
| GitHub - Push Multiple Files | GitHub | WRITE | AVAILABLE_NOW | CLOUD_OPS_SAFE | APPROVAL_ONLY | MCP github (verified via CAPABILITIES_MATRIX) | LEVERAGE↑ | github:push_files |
| GitHub - Create Branch | GitHub | WRITE | AVAILABLE_NOW | CLOUD_OPS_SAFE | APPROVAL_ONLY | MCP github (verified via CAPABILITIES_MATRIX) | LEVERAGE↑ | Branch creation |
| GitHub - Create Pull Request | GitHub | WRITE | AVAILABLE_NOW | CLOUD_OPS_SAFE | APPROVAL_ONLY | MCP github (verified via CAPABILITIES_MATRIX) | LEVERAGE↑ | PR workflow |
| GitHub - Create Issue | GitHub | WRITE | AVAILABLE_NOW | CLOUD_OPS_SAFE | APPROVAL_ONLY | MCP github (verified via CAPABILITIES_MATRIX) | LEVERAGE↑ | Issue tracking |
| GitHub - Merge PR | GitHub | WRITE | AVAILABLE_NOW | CLOUD_OPS_HIGH | APPROVAL_ONLY | MCP github (verified via CAPABILITIES_MATRIX) | PROTECTION↑ | Code merge |
| GitHub - Fork Repository | GitHub | WRITE | AVAILABLE_NOW | CLOUD_OPS_SAFE | APPROVAL_ONLY | MCP github (verified via CAPABILITIES_MATRIX) | LEVERAGE↑ | Repo forking |

### B.3 GitHub - Via github-executor-api

| Name | Area | Type | Current_Status | Risk_Level | Or_Touch | Source_of_Truth | Or_Benefit_Type | Notes |
|------|------|------|----------------|------------|----------|-----------------|-----------------|-------|
| GitHub - Execute from BUS | GitHub | EXEC | INFRA_PRESENT_BUT_NOT_WIRED | CLOUD_OPS_HIGH | APPROVAL_ONLY | Code in cloud-run/google-workspace-github-api/cloudbuild.yaml | LEVERAGE↑ | אין באפשרותי לאשר deployment status |
| GitHub - Trigger Workflow | GitHub | EXEC | INFRA_PRESENT_BUT_NOT_WIRED | CLOUD_OPS_HIGH | APPROVAL_ONLY | Docs only (design in CAPABILITIES_MATRIX) | LEVERAGE↑ | Mentioned in matrix, not verified |

### B.4 GitHub - Via GitHub Actions (WIF)

| Name | Area | Type | Current_Status | Risk_Level | Or_Touch | Source_of_Truth | Or_Benefit_Type | Notes |
|------|------|------|----------------|------------|----------|-----------------|-----------------|-------|
| GitHub Actions - Trigger Workflow | GitHub | EXEC | AVAILABLE_NOW | CLOUD_OPS_SAFE | APPROVAL_ONLY | MCP github + WIF (verified via CAPABILITIES_MATRIX) | LEVERAGE↑ | Can trigger via API |
| GitHub Actions - Read Results | GitHub | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP github (verified via CAPABILITIES_MATRIX) | COGNITIVE_LOAD↓ | Read logs/artifacts |

---

## C. BUS / ORCHESTRATION CAPABILITIES

### C.1 Google Sheets BUS

| Name | Area | Type | Current_Status | Risk_Level | Or_Touch | Source_of_Truth | Or_Benefit_Type | Notes |
|------|------|------|----------------|------------|----------|-----------------|-----------------|-------|
| BUS - Append to Index | BUS | WRITE | AVAILABLE_NOW | CLOUD_OPS_SAFE | APPROVAL_ONLY | GitHub Actions WIF + Sheets API (verified Run 19002923748) | LEVERAGE↑ | Hourly append working |
| BUS - Read Task Queue | BUS | READ | INFRA_PRESENT_BUT_NOT_WIRED | OS_SAFE | APPROVAL_ONLY | Docs only (design in CAPABILITIES_MATRIX) | COGNITIVE_LOAD↓ | אין באפשרותי לאשר actual implementation |
| BUS - Process Next Task | BUS | EXEC | INFRA_PRESENT_BUT_NOT_WIRED | CLOUD_OPS_HIGH | APPROVAL_ONLY | Docs only (design, github-executor-api) | LEVERAGE↑ | אין באפשרותי לאשר deployment |

### C.2 Cloud Run - google-workspace-api

| Name | Area | Type | Current_Status | Risk_Level | Or_Touch | Source_of_Truth | Or_Benefit_Type | Notes |
|------|------|------|----------------|------------|----------|-----------------|-----------------|-------|
| Cloud Run - Gmail Send | BUS | WRITE | INFRA_PRESENT_BUT_NOT_WIRED | CLOUD_OPS_HIGH | APPROVAL_ONLY | Docs only (design in FULL_CAPABILITIES_REPORT) | LEVERAGE↑ | אין באפשרותי לאשר code/deployment |
| Cloud Run - Drive Create | BUS | WRITE | INFRA_PRESENT_BUT_NOT_WIRED | CLOUD_OPS_SAFE | APPROVAL_ONLY | Docs only (design in FULL_CAPABILITIES_REPORT) | LEVERAGE↑ | אין באפשרותי לאשר code/deployment |
| Cloud Run - Sheets Update | BUS | WRITE | INFRA_PRESENT_BUT_NOT_WIRED | CLOUD_OPS_SAFE | APPROVAL_ONLY | Docs only (design in FULL_CAPABILITIES_REPORT) | LEVERAGE↑ | אין באפשרותי לאשר code/deployment |
| Cloud Run - Docs Create | BUS | WRITE | INFRA_PRESENT_BUT_NOT_WIRED | CLOUD_OPS_SAFE | APPROVAL_ONLY | Docs only (design in FULL_CAPABILITIES_REPORT) | LEVERAGE↑ | אין באפשרותי לאשר code/deployment |

### C.3 MCP Architecture

| Name | Area | Type | Current_Status | Risk_Level | Or_Touch | Source_of_Truth | Or_Benefit_Type | Notes |
|------|------|------|----------------|------------|----------|-----------------|-----------------|-------|
| MCP - Google Workspace READ | BUS | READ | AVAILABLE_NOW | OS_SAFE | NONE | MCP server-google-workspace (verified 2025-11-17) | COGNITIVE_LOAD↓ | 9 tools working |
| MCP - GitHub Operations | BUS | READ/WRITE | AVAILABLE_NOW | CLOUD_OPS_SAFE | APPROVAL_ONLY | MCP github (verified via CAPABILITIES_MATRIX) | LEVERAGE↑ | 12 tools working |
| MCP - PowerShell (11 cmds) | BUS | EXEC | AVAILABLE_NOW | OS_SAFE | NONE | MCP ps_exec (verified via CAPABILITIES_MATRIX) | COGNITIVE_LOAD↓ | Whitelisted commands only |

---

## 📊 DETAILED SUMMARY BY STATUS

### AVAILABLE_NOW (24 capabilities)
**Can be used TODAY with appropriate approvals**

**Google (9)**:
- Gmail: Read (4 tools)
- Drive: Read (3 tools)
- Calendar: Read (4 tools)

**GitHub (12)**:
- Read: 5 operations
- Write: 7 operations

**BUS/Orchestration (3)**:
- Sheets BUS append
- MCP Google READ
- MCP GitHub

### INFRA_PRESENT_BUT_NOT_WIRED (6 capabilities)
**Code/design exists, needs connection**

**GitHub (2)**:
- github-executor-api operations
- Workflow trigger (mentioned)

**BUS/Orchestration (4)**:
- BUS read/process
- Cloud Run google-workspace-api (all)

### NOT_AVAILABLE (15 capabilities)
**No infrastructure, needs Path A/B/C**

**Google (15)**:
- Gmail: Write (5 operations)
- Drive: Write (5 operations)
- Calendar: Write (3 operations)
- Sheets: ALL (4 operations) 
- Docs: ALL (3 operations)

---

## 🎯 STRATEGIC RECOMMENDATIONS

### Quick Wins (AVAILABLE_NOW)
1. **Use Google READ capabilities** - 9 tools ready
2. **Use GitHub full workflow** - 12 tools ready
3. **Use Sheets BUS append** - Working via Actions

### Medium-Term (INFRA_PRESENT)
1. **Investigate github-executor-api** - Check deployment
2. **Investigate google-workspace-api** - Check deployment
3. **Wire BUS queue** - If APIs exist

### Long-Term (NOT_AVAILABLE)
1. **Choose Path A/B/C** for Google WRITE
2. **Implement according to chosen path**
3. **Test and validate all operations**

---

## 📋 EVIDENCE QUALITY LEGEND

**Sources Used**:
- ✅ **MCP Testing** (2025-11-17): Direct verification
- ✅ **CAPABILITIES_MATRIX.md**: Documented capabilities
- ✅ **FULL_CAPABILITIES_REPORT**: Analysis and findings
- 🟡 **Repo Code Search**: Found cloudbuild.yaml
- ❌ **Cannot Verify**: Network restrictions

**"אין באפשרותי לאשר" means**:
- No direct evidence available
- Code may exist but not verified
- Deployment status unknown
- Needs further investigation (OS_SAFE only)

---

## 🔐 POLICY COMPLIANCE

**This Document**:
- ✅ OS_SAFE ONLY
- ✅ No CLOUD_OPS_HIGH operations
- ✅ No state changes
- ✅ Documentation and cataloging only
- ✅ Evidence-based claims only

**Or's Role**:
- Read this catalog
- Choose capabilities to activate
- Approve CLOUD_OPS_HIGH operations
- Zero manual execution required

---

**END OF CATALOG**

**Next**: Or decides which capabilities to activate and in what order.

**Document Status**: ✅ COMPLETE (OS_SAFE)  
**Last Updated**: 2025-11-17  
**Version**: 1.0
