# Windows Shell MCP - Healthcheck & Verification

**Version**: 1.0  
**Created**: 2025-11-15  
**Purpose**: Define verification procedures for Windows Shell MCP

---

## 🎯 Purpose

This document defines how to verify that the Windows Shell MCP server is:
1. **Installed correctly** - All files present, dependencies installed
2. **Configured properly** - Claude Desktop knows about it
3. **Functioning correctly** - Tools execute as expected
4. **Secure** - Policy enforcement working

---

## 🛠️ Installation Verification

### Step 1: File Structure Check

**Expected Structure**:
```
C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\windows-shell\
├── index.js
├── package.json
├── install.ps1
├── README.md
├── lib\
│   ├── audit-logger.js
│   ├── policy-validator.js
│   └── tool-handlers.js
├── scripts\
│   └── healthcheck.ps1
└── logs\
    └── (auto-created)
```

**Verification Command**:
```powershell
Test-Path C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\windows-shell\index.js
```

**Expected**: `True`

---

### Step 2: Dependencies Check

**Run Installation**:
```powershell
cd C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\windows-shell
.\install.ps1
```

**Verification**:
```powershell
Test-Path .\node_modules\@modelcontextprotocol\sdk
```

**Expected**: `True`

---

### Step 3: Automated Healthcheck

**Run Healthcheck Script**:
```powershell
cd C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\windows-shell
.\scripts\healthcheck.ps1
```

**Expected Output**:
```
✅ HEALTHY: All tests passed (5/5)
```

**Healthcheck Tests**:
1. Server files exist
2. Node.js version ≥ 18.0.0
3. npm dependencies installed
4. gcloud CLI present
5. PowerShell version ≥ 5.1

**Log Location**: `logs\healthcheck.log`

---

## 🔧 Configuration Verification

### Step 1: Check Claude Desktop Config

**Config File**: `C:\Users\edri2\AppData\Roaming\Claude\claude_desktop_config.json`

**Expected Content**:
```json
{
  "mcpServers": {
    "windows-shell": {
      "command": "node",
      "args": [
        "C:\\Users\\edri2\\Work\\AI-Projects\\Claude-Ops\\mcp-servers\\windows-shell\\index.js"
      ]
    }
  }
}
```

**Verification**:
```powershell
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json | Select-Object -ExpandProperty mcpServers | Select-Object -ExpandProperty windows-shell
```

**Expected**: Command and args present

---

### Step 2: Restart Claude Desktop

**CRITICAL**: Changes to `claude_desktop_config.json` require full restart.

**Steps**:
1. Close Claude Desktop completely
2. Wait 5 seconds
3. Reopen Claude Desktop
4. MCP servers load automatically on startup

---

## ✅ Functional Verification

### Test 1: OS_SAFE Tool (No Approval)

**Claude Command**:
```
Can you check the gcloud version using the windows-shell MCP?
```

**Expected Tool Call**:
```json
{
  "tool": "check_gcloud_version",
  "parameters": {}
}
```

**Expected Response**:
```json
{
  "success": true,
  "version": "547.0.0",
  "full_output": {...}
}
```

**Status**: ✅ PASS if version returned

---

### Test 2: Audit Log Verification

**Claude Command**:
```
Get the execution log from windows-shell MCP (last 10 entries)
```

**Expected Tool Call**:
```json
{
  "tool": "get_execution_log",
  "parameters": { "tail": 10 }
}
```

**Expected Response**:
- Array of log entries
- Contains previous `check_gcloud_version` execution
- Timestamps in ISO format

**Status**: ✅ PASS if log entries returned

---

### Test 3: Policy Violation (Negative Test)

**Claude Command**:
```
Try calling a tool that doesn't exist: "dangerous_operation"
```

**Expected Response**:
```
POLICY VIOLATION: Tool 'dangerous_operation' is not defined in any policy category

Tool 'dangerous_operation' execution denied.
```

**Status**: ✅ PASS if execution denied

---

### Test 4: CLOUD_OPS_SAFE Tool (Approval Required)

**NOTE**: Do NOT execute until ready for Phase 1

**Setup**:
1. Or provides approval: "מאשר הפעלת Google APIs דרך Windows-MCP"
2. Claude calls tool

**Claude Tool Call**:
```json
{
  "tool": "enable_google_apis",
  "parameters": {
    "project": "edri2or-mcp"
  }
}
```

**Expected**:
- gcloud commands execute
- APIs get enabled
- Log file created: `logs/google_apis_enable.log`
- Audit entry in `logs/execution.log`

**Status**: ✅ PASS if 6/6 APIs verified enabled

---

## 🔒 Security Verification

### Test 1: Project Constraint Enforcement

**Claude Command** (DO NOT EXECUTE - test only):
```json
{
  "tool": "enable_google_apis",
  "parameters": {
    "project": "wrong-project"
  }
}
```

**Expected**:
```
ERROR: Project must be 'edri2or-mcp', got 'wrong-project'
```

**Status**: ✅ PASS if execution blocked

---

### Test 2: API Constraint Enforcement

**Claude Command** (DO NOT EXECUTE - test only):
```json
{
  "tool": "enable_google_apis",
  "parameters": {
    "project": "edri2or-mcp",
    "apis": ["compute.googleapis.com"]
  }
}
```

**Expected**:
```
ERROR: API 'compute.googleapis.com' not in allowed list
```

**Status**: ✅ PASS if execution blocked

---

### Test 3: Audit Trail Verification

**Check Audit Log**:
```powershell
Get-Content C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\windows-shell\logs\execution.log -Tail 5
```

**Expected**:
- JSON lines
- Each with: timestamp, tool, category, status
- Recent entries from tests above

**Status**: ✅ PASS if all executions logged

---

## 📊 Success Criteria (DoD)

### Installation Phase
- [x] All files created
- [ ] Dependencies installed (`npm install`)
- [ ] Healthcheck passes 5/5 tests

### Configuration Phase
- [ ] Claude Desktop config updated
- [ ] Claude Desktop restarted
- [ ] MCP server shows as available

### Functional Phase
- [ ] `check_gcloud_version` works
- [ ] `get_execution_log` works
- [ ] Policy violations are blocked
- [ ] Audit logging works

### Security Phase
- [ ] Project constraint enforced
- [ ] API constraint enforced
- [ ] All executions logged
- [ ] Emergency stop protocol tested

### Ready for Phase 1
- [ ] All above DoD items complete
- [ ] `enable_google_apis` tool validated (dry-run)
- [ ] Approval process documented
- [ ] Rollback plan defined

---

## 🔄 Rollback Plan

If Windows Shell MCP fails:

1. **Remove from Claude Desktop**:
   - Edit `claude_desktop_config.json`
   - Remove `windows-shell` entry
   - Restart Claude Desktop

2. **Document Failure**:
   - Save `logs/execution.log`
   - Save `logs/healthcheck.log`
   - Create incident report

3. **Revert to Previous State**:
   - Phase 1 remains BLOCKED
   - Document lessons learned
   - Plan fixes

---

## 📝 Next Steps

After ALL verifications pass:

1. **Update CAPABILITIES_MATRIX.md**:
   - Windows Shell MCP: ACTIVE
   - Tools: 4 (3 OS_SAFE + 1 CLOUD_OPS_SAFE)
   - Status: VERIFIED

2. **Update L2_PHASE1_BLOCKED.md**:
   - Add "Unblocking Path: Windows Shell MCP"
   - Link to this document

3. **Ready for Phase 1 Execution**:
   - Or provides approval
   - Claude calls `enable_google_apis`
   - Document results
   - Move to Phase 2

---

**Status**: Waiting for installation + verification
