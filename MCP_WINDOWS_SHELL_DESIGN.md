# Windows Shell MCP - Design Document

**Version**: 1.0  
**Created**: 2025-11-15  
**Status**: DESIGN → IMPLEMENTATION → VERIFICATION

---

## 🎯 Purpose

Provide **policy-enforced Windows shell execution** for Claude-Ops automation.

**NOT**: A generic "run any command" tool  
**IS**: A JEA-style (Just Enough Administration) execution layer with:
- Explicit capability allowlist
- Policy-based command validation
- Full audit trail
- Risk categorization

---

## 🏛️ Architecture Principles

### 1. Least Privilege
**Every tool/capability is explicitly defined**
- No `run_arbitrary_command`
- No dynamic command construction
- No user-supplied command strings

### 2. JEA (Just Enough Administration)
**Two execution modes**:
1. **Named Tools**: Pre-defined operations with validated parameters
2. **Approved Scripts**: Whitelisted scripts by script_id from dedicated directory

### 3. Defense in Depth
**Multiple validation layers**:
1. MCP tool schema validation (JSON schema)
2. Policy file validation (WINDOWS_MCP_SAFETY_POLICY.md)
3. Runtime parameter validation
4. Audit logging (every execution)

### 4. Fail Secure
**Default behavior on error**: DENY
- Unknown tool → reject
- Invalid parameters → reject
- Policy violation → reject + log
- Missing approval → reject

---

## 📋 Capability Categories

### Category: OS_SAFE ✅ (No Approval)
**Purpose**: Read-only system information  
**Risk**: None

**Tools**:
- `check_gcloud_version` - Get gcloud CLI version
- `check_powershell_version` - Get PowerShell version
- `list_approved_scripts` - Show available scripts
- `get_execution_log` - Read audit log

**Example**:
```json
{
  "tool": "check_gcloud_version",
  "parameters": {}
}
```

---

### Category: CLOUD_OPS_SAFE ✅ (Approval Required)
**Purpose**: Enable Google APIs for MCP  
**Risk**: Low (Free Tier, reversible)

**Tools**:
- `enable_google_apis` - Enable 6 specific APIs in edri2or-mcp

**Parameters**:
```json
{
  "tool": "enable_google_apis",
  "parameters": {
    "apis": [  // Optional - defaults to all 6
      "gmail.googleapis.com",
      "drive.googleapis.com",
      "calendar-json.googleapis.com",
      "sheets.googleapis.com",
      "docs.googleapis.com",
      "iap.googleapis.com"
    ],
    "project": "edri2or-mcp"  // Hardcoded validation
  }
}
```

**Constraints**:
- ✅ Only these 6 APIs
- ✅ Only project: edri2or-mcp
- ❌ No other gcloud commands
- ❌ No IAM operations

**Approval Phrase**: "מאשר הפעלת Google APIs דרך Windows-MCP"

---

### Category: CLOUD_OPS_MODERATE ⚠️ (Review Required)
**Not Yet Implemented** - Future phases:
- OAuth client creation
- Secret Manager operations
- Cloud Shell execution

---

### Category: DANGEROUS ❌ (Forbidden)
**Never Allowed**:
- IAM operations
- Project deletion
- Billing changes
- System-level modifications

---

## 🛠️ Implementation Architecture

### Directory Structure
```
mcp-servers/windows-shell/
├── index.js                    # MCP server entry point
├── package.json               # Dependencies
├── lib/
│   ├── policy-validator.js    # Policy enforcement
│   ├── tool-handlers.js       # Named tool implementations
│   ├── script-executor.js     # Approved script runner
│   └── audit-logger.js        # Centralized logging
├── scripts/                   # Approved scripts directory
│   ├── enable_google_apis.ps1 # Already created
│   └── healthcheck.ps1        # System health verification
└── logs/
    └── execution.log          # Audit trail
```

### MCP Server Schema

**Server Name**: `windows-shell`  
**Protocol**: Model Context Protocol (MCP)  
**Transport**: stdio

**Tools Exposed**:

#### 1. `check_gcloud_version`
```json
{
  "name": "check_gcloud_version",
  "description": "Get gcloud CLI version information",
  "inputSchema": {
    "type": "object",
    "properties": {},
    "required": []
  }
}
```

#### 2. `enable_google_apis`
```json
{
  "name": "enable_google_apis",
  "description": "Enable Google APIs for MCP (CLOUD_OPS_SAFE)",
  "inputSchema": {
    "type": "object",
    "properties": {
      "project": {
        "type": "string",
        "enum": ["edri2or-mcp"],
        "description": "GCP project (must be edri2or-mcp)"
      },
      "apis": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": [
            "gmail.googleapis.com",
            "drive.googleapis.com",
            "calendar-json.googleapis.com",
            "sheets.googleapis.com",
            "docs.googleapis.com",
            "iap.googleapis.com"
          ]
        },
        "description": "APIs to enable (optional - defaults to all)"
      }
    },
    "required": ["project"]
  }
}
```

#### 3. `run_approved_script`
```json
{
  "name": "run_approved_script",
  "description": "Execute an approved PowerShell script by ID",
  "inputSchema": {
    "type": "object",
    "properties": {
      "script_id": {
        "type": "string",
        "enum": ["enable_google_apis", "healthcheck"],
        "description": "ID of approved script"
      },
      "parameters": {
        "type": "object",
        "description": "Script-specific parameters"
      }
    },
    "required": ["script_id"]
  }
}
```

#### 4. `get_execution_log`
```json
{
  "name": "get_execution_log",
  "description": "Read audit log entries",
  "inputSchema": {
    "type": "object",
    "properties": {
      "tail": {
        "type": "number",
        "description": "Number of recent entries (default: 50)"
      }
    },
    "required": []
  }
}
```

---

## 🔐 Policy Validation Flow

```
┌─────────────────────────────────────────────┐
│  1. MCP Tool Call                           │
│     {tool: "enable_google_apis", ...}       │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  2. Schema Validation (MCP)                 │
│     - Valid tool name?                      │
│     - Valid parameters?                     │
│     - Required fields present?              │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  3. Policy Validation (policy-validator.js) │
│     - Check WINDOWS_MCP_SAFETY_POLICY.md    │
│     - Tool in allowed category?             │
│     - Parameters match constraints?         │
│     - Approval required?                    │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  4. Runtime Validation (tool-handlers.js)   │
│     - Hardcoded constraint checks           │
│     - project === "edri2or-mcp"?            │
│     - APIs in allowed list?                 │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  5. Audit Log (audit-logger.js)             │
│     - Log before execution                  │
│     - Timestamp, tool, parameters           │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  6. Execute                                 │
│     - Run PowerShell script OR              │
│     - Execute gcloud command                │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  7. Audit Result                            │
│     - Log success/failure                   │
│     - Capture output                        │
│     - Update status files                   │
└─────────────────────────────────────────────┘
```

**On ANY validation failure**: Stop + log + return error

---

## 📊 Audit Trail

### Log File Location
`C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\windows-shell\logs\execution.log`

### Log Entry Format
```json
{
  "timestamp": "2025-11-15T02:30:00Z",
  "tool": "enable_google_apis",
  "category": "CLOUD_OPS_SAFE",
  "parameters": {
    "project": "edri2or-mcp",
    "apis": ["gmail.googleapis.com", "..."]
  },
  "approval": "מאשר הפעלת Google APIs דרך Windows-MCP",
  "execution_time_ms": 3420,
  "status": "success",
  "output_summary": "6/6 APIs enabled",
  "error": null
}
```

### Status Files
- `logs/google_apis_enable.log` - Detailed gcloud output
- `.ops/results/windows_shell_execution.json` - Latest result
- Commit to Git for permanent audit trail

---

## 🚨 Error Handling

### Error Categories

1. **Schema Validation Error**
   - Invalid tool name
   - Missing required parameters
   - Type mismatch
   - **Action**: Return error to Claude immediately

2. **Policy Violation**
   - Tool not in allowed category
   - Parameters violate constraints
   - Missing approval
   - **Action**: Log + return error + alert

3. **Runtime Error**
   - gcloud not found
   - Permission denied
   - Network failure
   - **Action**: Log + return detailed error + STOP

4. **Execution Failure**
   - Script exits non-zero
   - API enablement fails
   - Partial success
   - **Action**: Log + return partial results + flag for review

### Emergency Stop Protocol

**If encountered**:
- Unexpected IAM errors
- Wrong project accessed
- Security violation detected

**Actions**:
1. STOP all execution
2. Log full context
3. Create incident report
4. Notify Or with details
5. Wait for explicit guidance

---

## 📈 Success Criteria

### Definition of Done (DoD)

**MCP Server**:
- [ ] Server starts successfully
- [ ] Tools schema validates
- [ ] Policy validator works
- [ ] Audit logging functional
- [ ] Error handling tested

**Healthcheck**:
- [ ] `check_gcloud_version` returns version
- [ ] `get_execution_log` reads logs
- [ ] Policy violations are rejected
- [ ] Audit log entries created

**Phase 1 Ready**:
- [ ] `enable_google_apis` tool works
- [ ] 6 APIs can be enabled
- [ ] Project constraint enforced
- [ ] Full audit trail captured
- [ ] Results documented

---

## 🔄 Upgrade Path

### Future Capabilities (Separate Approvals)

**Phase 2**: OAuth Operations
- `create_oauth_client`
- Category: CLOUD_OPS_MODERATE

**Phase 3**: Secret Manager
- `store_secret`
- `read_secret`
- Category: CLOUD_OPS_MODERATE

**Phase 4**: Cloud Shell
- `run_cloud_shell_command`
- Category: CLOUD_OPS_MODERATE

**Each requires**:
- Updated policy document
- Risk assessment
- Explicit approval
- Dedicated testing

---

## 📝 Related Documents

- `WINDOWS_MCP_SAFETY_POLICY.md` - Policy definitions
- `MCP_WINDOWS_SHELL_HEALTHCHECK.md` - Verification procedures
- `CAPABILITIES_MATRIX.md` - Overall system capabilities
- `L2_PHASE1_BLOCKED.md` - Why we need this

---

**Status**: Design Complete → Ready for Implementation
