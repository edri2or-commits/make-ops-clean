# Phase 2 Tools - Complete Definitions

**Status**: ✅ BUILT - Awaiting Execution Approval  
**Version**: Windows Shell MCP 1.1.0  
**Date**: 2025-11-15

---

## 🎯 Overview

**4 new tools added to Windows Shell MCP** for Phase 2 (OAuth credentials management):

1. **store_secret** (CLOUD_OPS_HIGH)
2. **read_secret** (OS_SAFE)
3. **backup_claude_config** (OS_SAFE)
4. **update_claude_config** (CLOUD_OPS_HIGH)

**Total Tools**: 8 (4 from Phase 1 + 4 from Phase 2)

---

## 📋 Tool Definitions

### 1. store_secret

**Category**: CLOUD_OPS_HIGH  
**Approval Required**: ✅ YES  
**Approval Phrase**: "מאשר אחסון credentials ב-Secret Manager"

**Purpose**: Store OAuth credentials in GCP Secret Manager

**Parameters**:
```javascript
{
  project: "edri2or-mcp", // hardcoded constraint
  secret_name: string,    // must start with "google-mcp-"
  secret_value: string    // the credential to store
}
```

**Constraints**:
- ✅ ONLY project: `edri2or-mcp`
- ✅ ONLY secret names starting with: `google-mcp-`
- ❌ NO other projects
- ❌ NO other secret name prefixes

**gcloud Commands**:
```bash
# Create new secret
echo $SECRET_VALUE | gcloud secrets create $SECRET_NAME \
  --data-file=- \
  --project=edri2or-mcp

# OR update existing
echo $SECRET_VALUE | gcloud secrets versions add $SECRET_NAME \
  --data-file=- \
  --project=edri2or-mcp
```

**Response**:
```json
{
  "success": true,
  "action": "created" | "updated",
  "secret_name": "google-mcp-client-id",
  "project": "edri2or-mcp",
  "output": "..."
}
```

**Audit**:
- Event logged in `mcp-servers/windows-shell/logs/execution.log`
- Secret value REDACTED in logs
- GCP Secret Manager audit logs

---

### 2. read_secret

**Category**: OS_SAFE  
**Approval Required**: ❌ NO (read-only)

**Purpose**: Read OAuth credentials from GCP Secret Manager

**Parameters**:
```javascript
{
  project: "edri2or-mcp", // hardcoded constraint
  secret_name: string     // secret to read
}
```

**Constraints**:
- ✅ ONLY project: `edri2or-mcp`
- Read-only operation

**gcloud Command**:
```bash
gcloud secrets versions access latest \
  --secret=$SECRET_NAME \
  --project=edri2or-mcp
```

**Response**:
```json
{
  "success": true,
  "secret_name": "google-mcp-client-id",
  "secret_value": "...",
  "project": "edri2or-mcp"
}
```

**Audit**:
- Event logged (secret value NOT logged)

---

### 3. backup_claude_config

**Category**: OS_SAFE  
**Approval Required**: ❌ NO (backup only)

**Purpose**: Create timestamped backup of Claude Desktop config

**Parameters**: None

**Actions**:
1. Read `C:\Users\edri2\AppData\Roaming\Claude\claude_desktop_config.json`
2. Write to `claude_desktop_config.backup.{timestamp}.json`

**Response**:
```json
{
  "success": true,
  "original_path": "C:\\Users\\edri2\\AppData\\Roaming\\Claude\\claude_desktop_config.json",
  "backup_path": "C:\\Users\\edri2\\AppData\\Roaming\\Claude\\claude_desktop_config.backup.2025-11-15T12-00-00-000Z.json",
  "timestamp": "2025-11-15T12:00:00.000Z"
}
```

**Audit**:
- Event logged with backup path

---

### 4. update_claude_config

**Category**: CLOUD_OPS_HIGH  
**Approval Required**: ✅ YES  
**Approval Phrase**: "מאשר עדכון Claude config עם Google MCP"

**Purpose**: Add Google MCP server to Claude Desktop config

**Parameters**:
```javascript
{
  client_id: string,      // OAuth client ID
  client_secret: string,  // OAuth client secret
  scopes: string          // Comma-separated scopes
}
```

**Constraints**:
- ✅ ONLY allowed scopes:
  - `https://www.googleapis.com/auth/gmail.modify`
  - `https://www.googleapis.com/auth/drive`
  - `https://www.googleapis.com/auth/calendar`
  - `https://www.googleapis.com/auth/spreadsheets`
  - `https://www.googleapis.com/auth/documents`
- ❌ NO scope expansion beyond this list
- ❌ NO removal of existing MCP servers

**Actions**:
1. Read existing config
2. Add 'google-full' MCP server entry
3. Write updated config

**Config Entry Added**:
```json
{
  "mcpServers": {
    "google-full": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-workspace"],
      "env": {
        "GOOGLE_CLIENT_ID": "...",
        "GOOGLE_CLIENT_SECRET": "...",
        "GOOGLE_SCOPES": "..."
      }
    }
  }
}
```

**Response**:
```json
{
  "success": true,
  "config_path": "C:\\Users\\edri2\\AppData\\Roaming\\Claude\\claude_desktop_config.json",
  "mcp_server_added": "google-full",
  "scopes": ["gmail.modify", "drive", "calendar", "spreadsheets", "documents"]
}
```

**Audit**:
- Event logged (client_secret REDACTED)
- Backup created automatically

---

## 🔐 Security Model

### Defense in Depth (4 Layers)

**Layer 1: MCP Schema Validation**
- Tool name must exist
- Parameters must match schema
- Required fields present
- Enum constraints (project, etc.)

**Layer 2: Policy Validation** (`policy-validator.js`)
- Tool in allowed category?
- Parameters match constraints?
- Approval required?
- Secret name prefix check
- Scope whitelist check

**Layer 3: Runtime Validation** (`tool-handlers.js`)
- Hardcoded constraint checks
- `project === "edri2or-mcp"`
- `secret_name.startsWith("google-mcp-")`
- Scope in allowed list

**Layer 4: Audit Logging** (`audit-logger.js`)
- Log before execution
- Log after completion
- Log policy violations
- REDACT sensitive values

**Result**: Any validation failure → DENY + LOG

---

## 📊 Tool Categories Summary

### OS_SAFE (5 tools, no approval)
1. check_gcloud_version
2. check_powershell_version
3. get_execution_log
4. **read_secret** ⭐ NEW
5. **backup_claude_config** ⭐ NEW

### CLOUD_OPS_SAFE (1 tool, approval required)
1. enable_google_apis

### CLOUD_OPS_HIGH (2 tools, approval required)
1. **store_secret** ⭐ NEW
2. **update_claude_config** ⭐ NEW

**Total**: 8 tools

---

## ⚡ Usage Examples

### Example 1: Store OAuth Client ID

**Approval**: "מאשר אחסון credentials ב-Secret Manager"

**Tool Call**:
```javascript
windows-shell:store_secret({
  project: "edri2or-mcp",
  secret_name: "google-mcp-client-id",
  secret_value: "123456789-abc.apps.googleusercontent.com"
})
```

**Result**: Secret created in Secret Manager

---

### Example 2: Read OAuth Client ID

**No Approval Required** (OS_SAFE)

**Tool Call**:
```javascript
windows-shell:read_secret({
  project: "edri2or-mcp",
  secret_name: "google-mcp-client-id"
})
```

**Result**: Returns client ID value

---

### Example 3: Update Claude Config

**Approval**: "מאשר עדכון Claude config עם Google MCP"

**Tool Call**:
```javascript
windows-shell:update_claude_config({
  client_id: "...",
  client_secret: "...",
  scopes: "https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/spreadsheets,https://www.googleapis.com/auth/documents"
})
```

**Result**: Google MCP added to config, backup created

---

## 🧪 Testing Status

### Installation
- ✅ npm install completed (90 packages)
- ✅ Healthcheck passed (5/5 tests)
- ✅ MCP server loads successfully

### Runtime (Not Yet Executed)
- ⏸️ store_secret - Awaiting execution approval
- ⏸️ read_secret - Awaiting execution approval
- ⏸️ backup_claude_config - Awaiting execution approval
- ⏸️ update_claude_config - Awaiting execution approval

**Note**: Tools are built and policy-validated, but not yet executed with real credentials.

---

## 📝 Next Steps

### For Or to Review
1. Tool definitions (this document)
2. Policy updates (WINDOWS_MCP_SAFETY_POLICY.md)
3. Capabilities matrix updates (next)

### After Or's Approval
1. Create OAuth client in Console (manual)
2. Execute Phase 2 tools with approval
3. Verify all tools work
4. Document results

---

**Status**: Tools ready, awaiting execution approval
