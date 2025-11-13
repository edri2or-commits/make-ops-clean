# Bridge Proposal - L1 to L2 Transition

**Status**: ✅ APPROVED - Option A Primary Path  
**Target**: L2 (Controlled Execution Layer)  
**Last Updated**: 2025-11-13  
**Decision**: Option A (MCP-ify controllers) with Option B as quick win if needed

---

## ⚡ Quick Decision Summary

**APPROVED PATH**: **Option A - MCP-ify Local Controllers**

**Rationale**:
- ✅ Strategic and future-proof (L1→L5 progression)
- ✅ Full integration of metacontrol.py + local_controller.py
- ✅ Unified governance via policy_gate.yaml
- ✅ Foundation for L3+ (Desktop, OS management)

**Optional Quick Win**: **Option B - Enhanced ps_exec**
- Can be implemented first (1-2 days) for immediate script execution
- Then proceed with Option A (1-2 weeks) for full solution

**Next Steps Before L2 Implementation**:
1. 🔴 **CRITICAL**: Clean up secrets (see [SECURITY_FINDINGS_SECRETS.md](SECURITY_FINDINGS_SECRETS.md))
   - Delete `_audit/purged_2025-11-11/` directory
   - Move active credentials to vault
   - Review and rotate exposed keys
2. ✅ Complete L1 validation (done - see L1_INVENTORY_REPORT.md)
3. ✅ Create detailed L2 design (this document)

---

## 🎯 Executive Summary

**Goal**: Bridge the gap between Claude Desktop MCP and Local Python Controllers, enabling controlled execution while maintaining security and governance.

**Primary Approach (Option A)**: MCP-ify existing Python controllers  
**Secondary Approach (Option B)**: Enhance ps_exec for signed script execution  
**Fallback (Option C)**: Stay at L1 and defer L2

---

## 🔍 The Problem

### Current State (L1):
```
Claude Desktop (MCP Client)
  ├─ ps_exec → Read-only PowerShell (10 commands)
  ├─ Filesystem → Full R/W on files
  ├─ GitHub → Full repo operations
  └─ Google → Read-only services

         ↕ ❌ NO INTEGRATION ❌ ↕

Local Python Controllers (Independent)
  ├─ metacontrol.py → Telegram, GitHub, OpenAI, Make.com
  ├─ claude_auto_agent.py → File downloader
  └─ local_controller.py → Command executor
```

**Key Issues**:
1. Claude cannot trigger Python controllers directly
2. Controllers don't respect `policy_gate.yaml` constraints
3. No unified governance for local execution
4. ps_exec too limited (read-only)

---

## 🏗️ Option A: MCP-ify Local Controllers (✅ PRIMARY - APPROVED)

### Overview

Convert existing Python controllers into MCP servers that Claude Desktop can interact with directly, while enforcing governance policies.

### Architecture

```
┌──────────────────────────────────────────────────────┐
│  אור (Human Approval Gate)                          │
│  ↕ Telegram approvals via L1.2 flow                 │
└──────────────────────────────────────────────────────┘
         ↕
┌──────────────────────────────────────────────────────┐
│  GitHub: make-ops-clean (Control Plane)             │
│  • policy_gate.yaml (enforced by MCP servers)       │
│  • capability_registry.yaml (intent definitions)    │
│  • allowlist.json (approved scripts + hashes)       │
└──────────────────────────────────────────────────────┘
         ↕
┌──────────────────────────────────────────────────────┐
│  Claude Desktop (MCP Client)                         │
│  L1 Tools (existing):                                │
│  ├─ ps_exec (read-only)                             │
│  ├─ Filesystem (R/W)                                │
│  ├─ GitHub (R/W)                                    │
│  └─ Google (read-only)                              │
│                                                      │
│  L2 Tools (new - to be built):                      │
│  ├─ metacontrol_mcp                                 │
│  │   Tools: telegram_send, github_commit,          │
│  │          openai_chat, make_trigger              │
│  │   Policy: Check policy_gate.yaml before action  │
│  │   Secrets: From vault/env vars only             │
│  │                                                  │
│  └─ local_exec_mcp                                  │
│      Tools: write_local_file, run_signed_script,   │
│             delete_local_file                       │
│      Policy: ALWAYS requires approval               │
│      Verification: SHA256 hashes + allowlist        │
└──────────────────────────────────────────────────────┘
         ↕
┌──────────────────────────────────────────────────────┐
│  Python Controllers (wrapped by MCP)                 │
│  ├─ metacontrol.py (backend for metacontrol_mcp)   │
│  └─ local_controller.py (backend for local_exec)   │
└──────────────────────────────────────────────────────┘
```

---

### Implementation Plan

#### Phase 1: metacontrol_mcp (Week 1)

**Create**: `C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\metacontrol_mcp\`

**Structure**:
```
metacontrol_mcp/
├── index.js              # MCP server (Node.js)
├── package.json
├── python_bridge.js      # Spawns metacontrol.py
├── policy_checker.js     # Validates against policy_gate.yaml
├── secrets_loader.js     # Loads secrets from env (not hardcoded!)
├── logger.js             # Scrubs secrets before logging
└── README.md
```

**MCP Tools Exposed**:

| Tool | Intent | Policy | Description |
|------|--------|--------|-------------|
| `telegram_send` | `messaging.telegram.send` | Auto (if enabled) | Send message to Telegram |
| `github_commit` | `gh.commit.create` | Auto | Commit file to GitHub repo |
| `openai_chat` | `ai.openai.query` | Auto | Query OpenAI API |
| `make_trigger` | `automation.make.webhook` | Auto | Trigger Make.com scenario |

**Tool Details**:

1. **`telegram_send(message, parse_mode='Markdown')`**
   - Calls: `metacontrol.py telegram_send(...)`
   - Secrets: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` from env
   - Logging: Message content logged (but not tokens)
   - Use case: Send notifications, approval requests

2. **`github_commit(file_path, commit_message)`**
   - Calls: `metacontrol.py github_commit(...)`
   - Secrets: `GITHUB_PAT` from env
   - Logging: File path + commit message (not PAT)
   - Use case: Auto-commit config changes, logs

3. **`openai_chat(prompt, model='gpt-4o-mini')`**
   - Calls: `metacontrol.py openai_chat(...)`
   - Secrets: `OPENAI_API_KEY` from env
   - Logging: Prompt + response (not API key)
   - Use case: AI-assisted analysis, planning

4. **`make_trigger(data)`**
   - Calls: `metacontrol.py make_trigger(...)`
   - Secrets: `MAKE_WEBHOOK_URL` from env
   - Logging: Data payload (not webhook URL)
   - Use case: Trigger Make scenarios for complex workflows

**Policy Enforcement**:
```javascript
// policy_checker.js
async function checkPolicy(intent, action) {
  const policyGate = await loadYAML('policy_gate.yaml');
  
  if (policyGate.blocked.includes(intent)) {
    throw new Error(`Intent '${intent}' is blocked`);
  }
  
  if (policyGate.requires_approval.includes(intent)) {
    // Trigger L1.2 approval flow
    return await requestApproval(intent, action);
  }
  
  if (policyGate.auto.includes(intent)) {
    return true; // Proceed
  }
  
  throw new Error(`Intent '${intent}' not defined in policy`);
}
```

**Secrets Management**:
```javascript
// secrets_loader.js
// ✅ GOOD - Load from environment
function loadSecrets() {
  return {
    telegramBotToken: process.env.TELEGRAM_BOT_TOKEN,
    telegramChatId: process.env.TELEGRAM_CHAT_ID,
    githubPat: process.env.GITHUB_PAT,
    openaiApiKey: process.env.OPENAI_API_KEY,
    makeWebhookUrl: process.env.MAKE_WEBHOOK_URL
  };
}

// ❌ BAD - Never hardcode
// const telegramBotToken = "123456:ABC-DEF..."; // DON'T DO THIS
```

**Logging with Secret Scrubbing**:
```javascript
// logger.js
function scrubSecrets(message) {
  return message
    // OpenAI API keys
    .replace(/sk-[a-zA-Z0-9]{48}/g, 'sk-***REDACTED***')
    // GitHub PATs
    .replace(/ghp_[a-zA-Z0-9]{36}/g, 'ghp_***REDACTED***')
    // Telegram bot tokens
    .replace(/\d{10}:[A-Za-z0-9_-]{35}/g, '***TELEGRAM_BOT_TOKEN***')
    // Make webhook URLs
    .replace(/https:\/\/hook\.(eu1|eu2|us1|us2)\.make\.com\/[a-zA-Z0-9]+/g, '***MAKE_WEBHOOK_URL***');
}
```

---

#### Phase 2: local_exec_mcp (Week 2)

**Create**: `C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\local_exec_mcp\`

**Structure**:
```
local_exec_mcp/
├── index.js
├── package.json
├── executor.js           # Spawns local_controller.py or scripts
├── signature_verify.js   # Validates script SHA256 hashes
├── allowlist.json        # Approved scripts with hashes
├── logger.js             # Audit logging
└── README.md
```

**MCP Tools Exposed**:

| Tool | Intent | Policy | Description |
|------|--------|--------|-------------|
| `run_signed_script` | `local.script.execute` | **ALWAYS requires approval** | Execute signed PowerShell/Python script |
| `write_local_file` | `local.file.write` | Auto (similar to Filesystem) | Write file via local_controller |
| `delete_local_file` | `local.file.delete` | Approval for system paths | Delete file via local_controller |

**Tool Details**:

1. **`run_signed_script(script_path)`**
   - Validation:
     - Must exist in `allowlist.json` with matching SHA256
     - Must be in approved directory (e.g., `C:\...\Scripts\`)
     - Hash verified on EVERY execution (not just approval)
   - Execution:
     - Spawns subprocess (PowerShell or Python)
     - Timeout: 30s default, 5min max
     - Logs: Full output + stderr to Evidence Index
   - Policy: **ALWAYS requires L1.2 approval flow**

2. **`write_local_file(path, content)`**
   - Calls: `local_controller.py write_file(...)`
   - Validation: Path must be in allowed directories
   - Logging: Path + size (not full content if sensitive)

3. **`delete_local_file(path)`**
   - Calls: `local_controller.py delete_file(...)`
   - Validation: Path must be in allowed directories
   - Policy: Approval required for system/protected paths
   - Logging: Path + timestamp

**Signature Verification**:
```javascript
// signature_verify.js
async function verifyScript(scriptPath) {
  const allowlist = await loadJSON('allowlist.json');
  const actualHash = await computeSHA256(scriptPath);
  
  const entry = allowlist.scripts.find(s => s.path === scriptPath);
  
  if (!entry) {
    throw new Error(`Script not in allowlist: ${scriptPath}`);
  }
  
  if (entry.sha256 !== actualHash) {
    throw new Error(`Hash mismatch for ${scriptPath}. Expected: ${entry.sha256}, Got: ${actualHash}`);
  }
  
  return true;
}
```

**allowlist.json Example**:
```json
{
  "scripts": [
    {
      "name": "system_cleanup",
      "path": "C:\\Users\\edri2\\Work\\AI-Projects\\Claude-Ops\\Scripts\\cleanup.ps1",
      "sha256": "abc123def456...",
      "approved_by": "edri2or",
      "approved_at": "2025-11-13T10:00:00Z",
      "description": "Cleans temp files safely",
      "max_runtime_seconds": 60
    }
  ],
  "directories": [
    "C:\\Users\\edri2\\Work\\AI-Projects\\Claude-Ops\\Scripts"
  ]
}
```

---

### Approval Flow (L2 Integration with L1.2)

**For `local.install` or `local.script.execute`**:

```
1. Claude calls local_exec_mcp.run_signed_script(script_path)
     ↓
2. MCP checks policy_gate.yaml → "requires_approval"
     ↓
3. MCP creates approval request:
   - Calls create-approval-request.sh (reuses L1.2 flow)
   - Provides: script path, hash, description, estimated risk
     ↓
4. L1.2 Telegram flow:
   - Make #1 → Telegram message with buttons [✅ Execute] [❌ Cancel]
   - Includes: script name, hash, description
   - אור reviews and clicks ✅ or ❌
     ↓
5a. IF APPROVED:
   - Make #2 → GitHub repository_dispatch
   - GitHub Actions:
     * Verifies script exists
     * Computes SHA256
     * Adds to allowlist.json
     * Commits + pushes to main
     * Notifies Claude MCP (via webhook)
   - Claude MCP receives approval
   - Re-attempts script execution
   - Signature verification passes → Script runs
   - Result logged to Evidence Index + GitHub Issue
     ↓
5b. IF REJECTED:
   - Make #2 → Telegram edit message "❌ Canceled"
   - Claude MCP receives rejection
   - Execution aborted
   - Logged to Evidence Index
```

---

### Benefits of Option A

✅ **Strategic**:
- Future-proof: All controllers become MCP-native
- Unified governance: Single policy_gate.yaml for all tools
- Scalable: Easy to add new tools (e.g., Desktop automation in L3)

✅ **Secure**:
- Policy enforcement at MCP layer (before execution)
- Signature verification for all scripts (SHA256)
- Full audit trail (GitHub commits + Evidence Index)
- Secrets from vault/env only (never hardcoded)
- Secret scrubbing in logs

✅ **User-Friendly**:
- Claude has direct tool access (no manual JSON files)
- Familiar L1.2 approval flow (Telegram buttons)
- Clear feedback on approval/rejection

✅ **Maintainable**:
- Controllers remain as Python (existing logic preserved)
- MCP layer is thin wrapper (separation of concerns)
- Clear upgrade path to L3+ (add new MCP servers)

---

### Risks and Mitigations

#### Risk 1: Privilege Escalation

**Threat**: MCP server bypasses policy checks

**Mitigation**:
- Policy checker runs BEFORE Python subprocess spawn
- allowlist.json is append-only (via GitHub Actions only)
- All executions logged with full context (timestamp, user, intent, result)
- Regular audits of allowlist.json

#### Risk 2: Signature Bypass

**Threat**: Attacker modifies script after approval

**Mitigation**:
- SHA256 verification on EVERY run (not just at approval time)
- Scripts stored in controlled directory with file monitoring
- File modification timestamps logged
- GitHub tracks all allowlist.json changes

#### Risk 3: Secrets Exposure

**Threat**: MCP logs contain sensitive data (API keys, tokens)

**Mitigation**:
- No secrets in MCP tool parameters (only in env vars)
- All logs scrubbed via `scrubSecrets()` function
- Secrets loaded at runtime from vault or secure env
- Regular secret rotation (30-90 days)

#### Risk 4: Runaway Execution

**Threat**: Script loops, hangs, or consumes excessive resources

**Mitigation**:
- Timeout enforcement (30s default, 5min max, configurable per script)
- Process kill switch via GitHub Actions (emergency disable)
- Resource limits (CPU, memory) via subprocess spawn options
- Kill switch: Disable MCP server in Claude Desktop config

#### Risk 5: Malicious Script Addition

**Threat**: Unauthorized script added to allowlist.json

**Mitigation**:
- allowlist.json lives in GitHub (version controlled)
- Only GitHub Actions can modify (not manual edits)
- CODEOWNERS file requires אור approval for allowlist changes
- GitHub audit log tracks all changes

---

### Implementation Effort

**Estimated Time**: 1-2 weeks (35-40 hours)

| Task | Effort | Priority | Notes |
|------|--------|----------|-------|
| metacontrol_mcp scaffold | 4 hours | P0 | Node.js MCP server setup |
| Python bridge (spawn metacontrol.py) | 3 hours | P0 | Subprocess management |
| Policy checker integration | 3 hours | P0 | Load + validate policy_gate.yaml |
| Secrets loader (env vars) | 2 hours | P0 | No hardcoded secrets |
| Secret scrubbing in logs | 2 hours | P0 | Regex patterns for common secrets |
| local_exec_mcp scaffold | 4 hours | P1 | Node.js MCP server setup |
| Signature verification (SHA256) | 4 hours | P1 | Crypto module + allowlist validation |
| allowlist.json management | 2 hours | P1 | JSON schema + validation |
| L1.2 approval integration | 6 hours | P0 | Webhook to create-approval-request.sh |
| Testing (unit + integration) | 8 hours | P0 | Jest tests + manual E2E |
| Documentation | 4 hours | P1 | README per MCP + usage guide |
| **Total** | **42 hours** | - | ~1-2 weeks (full-time equivalent) |

---

## 🔧 Option B: Enhanced ps_exec (⚡ QUICK WIN - OPTIONAL)

### Overview

Extend ps_exec to execute signed scripts from approved directories, without full controller integration. This is a **tactical quick win** that can be implemented in 1-2 days while planning Option A.

### When to Use Option B

✅ **Use if**:
- Need script execution capability IMMEDIATELY (1-2 days)
- Don't need Telegram/Make/OpenAI integration yet
- PowerShell-centric workflows (no Python scripts)

⚠️ **Then proceed with Option A** for full solution

### Architecture

```
┌──────────────────────────────────────────────────────┐
│  Claude Desktop (MCP Client)                         │
│  ├─ ps_exec_enhanced                                │
│  │   • Read-only commands (existing 10)             │
│  │   • NEW: run_signed_script                       │
│  │   • Validates SHA256 hash                        │
│  │   • Only from approved directories               │
│  └─ (other MCPs unchanged)                          │
└──────────────────────────────────────────────────────┘
         ↕
┌──────────────────────────────────────────────────────┐
│  ps_exec Dispatcher (dispatcher.ps1)                 │
│  • Checks allowlist_ps.json                         │
│  • Verifies hash before execution                   │
│  • Logs to Evidence Index                           │
└──────────────────────────────────────────────────────┘
```

---

### Implementation

**Modify**: `C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\ps_exec\dispatcher.ps1`

**Add new action**:
```powershell
# allowlist_ps.json (new file)
{
  "scripts": [
    {
      "name": "cleanup_temp",
      "path": "C:\\Users\\edri2\\Work\\AI-Projects\\Claude-Ops\\Scripts\\cleanup_temp.ps1",
      "sha256": "abc123def456...",
      "approved_by": "edri2or",
      "approved_at": "2025-11-13T10:00:00Z",
      "max_runtime_seconds": 60
    }
  ]
}

# New action in dispatcher.ps1
if ($action -eq "run_signed_script") {
    $scriptPath = $args.script_path
    $allowlistPath = Join-Path $PSScriptRoot "allowlist_ps.json"
    $allowlist = Get-Content $allowlistPath | ConvertFrom-Json
    
    # Find in allowlist
    $entry = $allowlist.scripts | Where-Object { $_.path -eq $scriptPath }
    if (-not $entry) {
        throw "Script not in allowlist: $scriptPath"
    }
    
    # Verify hash
    $actualHash = (Get-FileHash $scriptPath -Algorithm SHA256).Hash
    if ($actualHash -ne $entry.sha256) {
        throw "Hash mismatch for $scriptPath. Expected: $($entry.sha256), Got: $actualHash"
    }
    
    # Log execution start
    Write-Host "Executing approved script: $scriptPath"
    
    # Execute with timeout
    $job = Start-Job -ScriptBlock { & $using:scriptPath }
    $timeout = $entry.max_runtime_seconds
    if (-not $timeout) { $timeout = 30 }
    
    Wait-Job $job -Timeout $timeout
    if ($job.State -eq 'Running') {
        Stop-Job $job
        throw "Script exceeded timeout of ${timeout}s"
    }
    
    $output = Receive-Job $job
    Remove-Job $job
    
    Write-Host "Script completed successfully"
    return $output
}
```

**Update index.js** to expose new tool:
```javascript
// Add to tools array
{
  name: "run_signed_script",
  description: "Execute a pre-approved PowerShell script with signature verification",
  inputSchema: {
    type: "object",
    properties: {
      script_path: {
        type: "string",
        description: "Full path to the approved script"
      }
    },
    required: ["script_path"]
  }
}
```

---

### Benefits of Option B

✅ **Quick Win**:
- Faster implementation (~1-2 days vs 1-2 weeks)
- Minimal new infrastructure (reuses ps_exec)
- Can be deployed while planning Option A

✅ **Simple**:
- One MCP server to modify
- No new Python wrappers needed
- Straightforward approval flow (same L1.2)

---

### Limitations of Option B

❌ **Not Future-Proof**:
- Doesn't integrate metacontrol.py (no Telegram/Make/OpenAI)
- Doesn't bridge local_controller.py
- PowerShell-only (no Python script support)

❌ **Limited Scope**:
- Only executes scripts (doesn't expose tools like `telegram_send`)
- No direct Telegram/Make integration
- Harder to extend for L3+ capabilities

---

### Recommended Timeline for Option B

**Day 1**:
- Modify dispatcher.ps1 (add run_signed_script action)
- Create allowlist_ps.json schema
- Update index.js to expose tool

**Day 2**:
- Test with sample script
- Add to Claude Desktop config
- Create first approved script (e.g., cleanup_temp.ps1)
- Document usage

**Then**: Proceed with Option A for full solution (metacontrol_mcp + local_exec_mcp)

---

## 🚫 Option C: Stay at L1 (FALLBACK ONLY)

### Overview

Defer L2 implementation and remain at L1 (read-only + file ops only).

### When to Choose

**Valid Reasons**:
- L1 capabilities are sufficient for current needs
- L2 complexity/risk too high right now
- Need more time to plan governance carefully
- Secrets cleanup proves too complex

**Process**:
1. Document L1 as "complete for now"
2. Create L2 backlog in GitHub Issues
3. Schedule L2 review in 1-3 months
4. Focus on other priorities

---

## 📊 Comparison Matrix

| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|
| **Time to Implement** | 1-2 weeks | 1-2 days | 0 (no change) |
| **Future-Proof** | ✅ High | ⚠️ Low | ❌ N/A |
| **Security** | ✅ Robust | ✅ Good | ✅ Maximum (no execution) |
| **Complexity** | ⚠️ High | ✅ Low | ✅ None |
| **Telegram Integration** | ✅ Yes | ❌ No | ❌ No |
| **Make Integration** | ✅ Yes | ❌ No | ❌ No |
| **Python Support** | ✅ Yes | ❌ No | ❌ No |
| **PowerShell Support** | ✅ Yes | ✅ Yes | ❌ Read-only |
| **Scalability (L3+)** | ✅ Easy | ⚠️ Hard | ❌ Blocked |
| **Effort** | 35-42 hours | 8-12 hours | 0 hours |

---

## 🎯 Approved Implementation Plan

### Phase 0: Prerequisites (BEFORE L2)

**Status**: ⏸️ BLOCKING

**Must Complete**:
1. 🔴 **CRITICAL**: Secrets cleanup (see [SECURITY_FINDINGS_SECRETS.md](SECURITY_FINDINGS_SECRETS.md))
   - [ ] Delete `_audit/purged_2025-11-11/` directory
   - [ ] Delete backup files: `CLAUDE_TOK.txt.backup`, `Github_key.pem.backup`
   - [ ] Move to vault: 4 OAuth2 secrets + 3 private keys
   - [ ] Review: `טוקנים/claude_bootstrap.env` for active tokens
   - [ ] Rotate any exposed credentials
2. ✅ L1 validation complete (L1_INVENTORY_REPORT.md)
3. ✅ Architecture designed (this document)

**Timeline**: 1-2 days (manual work by אור)

---

### Phase 1: metacontrol_mcp (Week 1)

**Goal**: Integrate Telegram, GitHub, OpenAI, Make

**Tasks**:
1. Create MCP server scaffold (Node.js)
2. Implement Python bridge (spawn metacontrol.py)
3. Add policy checker (policy_gate.yaml validation)
4. Implement secrets loader (env vars only)
5. Add secret scrubbing to logs
6. Expose 4 tools: telegram_send, github_commit, openai_chat, make_trigger
7. Test with sample calls
8. Update Claude Desktop config
9. Document usage

**Deliverables**:
- `mcp-servers/metacontrol_mcp/` (complete Node.js project)
- Updated `claude_desktop_config.json`
- README with usage examples
- Unit tests (Jest)

---

### Phase 2: local_exec_mcp (Week 2)

**Goal**: Enable controlled script execution

**Tasks**:
1. Create MCP server scaffold (Node.js)
2. Implement executor (spawn scripts with timeout)
3. Add signature verification (SHA256)
4. Create allowlist.json schema
5. Integrate L1.2 approval flow
6. Expose 3 tools: run_signed_script, write_local_file, delete_local_file
7. Test with sample approved script
8. Update Claude Desktop config
9. Document usage

**Deliverables**:
- `mcp-servers/local_exec_mcp/` (complete Node.js project)
- `allowlist.json` (with schema validation)
- Updated `claude_desktop_config.json`
- README with usage examples
- Unit tests (Jest)

---

### Phase 3: Integration & Testing (Week 3)

**Goal**: Validate end-to-end flows

**Tasks**:
1. E2E test: Claude → metacontrol_mcp → Telegram
2. E2E test: Claude → local_exec_mcp → Script execution (with approval)
3. Security audit: Verify no secrets in logs
4. Performance test: Measure tool call latency
5. Documentation: Update all guides
6. ADR: Document L2 decision

**Deliverables**:
- E2E test results
- Security audit report
- Performance metrics
- Updated documentation
- ADR-0002-l2-mcp-integration.md

---

### Phase 4: Production Deployment (Week 4)

**Goal**: Go live with L2

**Tasks**:
1. Deploy metacontrol_mcp to production
2. Deploy local_exec_mcp to production
3. Create first approved script (e.g., system_info.ps1)
4. Monitor logs for issues
5. Gather user feedback
6. Plan L3 capabilities

**Deliverables**:
- Production-ready L2 environment
- First approved script in allowlist.json
- Monitoring dashboard (logs + Evidence Index)
- L3 planning document

---

## 🔒 Security Principles for L2

### Defense in Depth (5 Layers)

1. **Policy Layer**: `policy_gate.yaml` enforced by MCP before execution
2. **Signature Layer**: SHA256 verification for all scripts (on every run)
3. **Approval Layer**: Human-in-loop via L1.2 Telegram flow
4. **Audit Layer**: Full logging to Evidence Index + GitHub
5. **Kill Switch**: Disable MCP server in config or via GitHub Actions

### Least Privilege

- MCP servers run with minimum Windows permissions
- Python subprocesses inherit only necessary env vars
- No persistent credentials in MCP code
- Each tool gets only the secrets it needs

### Secrets Management

**✅ DO**:
- Load secrets from env vars: `process.env.TELEGRAM_BOT_TOKEN`
- Store secrets in vault (1Password/Azure Key Vault/AWS Secrets Manager)
- Rotate secrets regularly (30-90 days)
- Scrub secrets from logs before writing

**❌ DON'T**:
- Hardcode secrets in code
- Store secrets in Git (even in private repos)
- Log secrets (even partially)
- Pass secrets as command-line arguments

### Monitoring & Alerting

**All tool calls logged with**:
- Timestamp (ISO 8601)
- Intent (e.g., `local.script.execute`)
- User (if applicable)
- Result (success/failure + error details)
- Duration (milliseconds)
- Secrets scrubbed before writing

**Log to**:
- Console (real-time monitoring)
- GitHub (Evidence Index via issue/commit)
- Local file (for debugging)

**Alert on**:
- Script execution failures (repeated)
- Policy violations (blocked intents attempted)
- Signature verification failures
- Timeout exceeded
- Secrets detected in logs (should never happen!)

---

## 📋 Next Steps

**Immediate** (This Week):
1. ✅ L1 Inventory complete
2. ✅ Security findings documented
3. ✅ Bridge proposal approved (this document)
4. ⏳ **אור performs secrets cleanup** (manual - see SECURITY_FINDINGS_SECRETS.md)

**After Secrets Cleanup** (Next 1-2 Weeks):
1. 🔨 Build metacontrol_mcp (Week 1)
2. 🔨 Build local_exec_mcp (Week 2)
3. 🧪 Integration testing (Week 3)
4. 🚀 Production deployment (Week 4)

**Optional Quick Win**:
- If needed urgently: Build Option B (enhanced ps_exec) in 1-2 days
- Then proceed with Option A as planned

---

## 📚 Related Documents

- [CURRENT_STATE.md](CURRENT_STATE.md) - Current infrastructure (L1)
- [L1_CAPABILITIES.md](L1_CAPABILITIES.md) - What Claude can do now
- [L1_INVENTORY_REPORT.md](L1_INVENTORY_REPORT.md) - System baseline scan
- [SECURITY_FINDINGS_SECRETS.md](SECURITY_FINDINGS_SECRETS.md) - Secrets audit (**CRITICAL - Must fix before L2**)
- `platform/manifest/policy_gate.yaml` - Governance rules
- `platform/manifest/capability_registry.yaml` - Intent definitions

---

**End of Bridge Proposal**

**Status**: ✅ APPROVED - Option A Primary  
**Next Action**: אור completes secrets cleanup → L2 implementation begins  
**Timeline**: 1-2 weeks (after secrets cleanup)
