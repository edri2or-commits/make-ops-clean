# Bridge Proposal - L1 to L2 Transition

**Status**: Planning Phase  
**Target**: L2 (Controlled Execution Layer)  
**Last Updated**: 2025-11-13

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

## 🏗️ Option A: MCP-ify Local Controllers (PRIMARY)

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
│  L2 Tools (new):                                    │
│  ├─ metacontrol_mcp                                 │
│  │   Tools: telegram_send, github_commit,          │
│  │          openai_chat, make_trigger              │
│  │   Policy: Check policy_gate.yaml before action  │
│  │                                                  │
│  └─ local_exec_mcp                                  │
│      Tools: write_local_file, run_signed_script,   │
│             delete_local_file                       │
│      Policy: ALWAYS requires approval               │
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

#### Phase 1: metacontrol_mcp

**Create**: `C:\...\Claude-Ops\mcp-servers\metacontrol_mcp\`

**Structure**:
```
metacontrol_mcp/
├── index.js              # MCP server (Node.js)
├── package.json
├── python_bridge.js      # Spawns metacontrol.py
├── policy_checker.js     # Validates against policy_gate.yaml
└── README.md
```

**MCP Tools Exposed**:
1. `telegram_send` 
   - Intent: `messaging.telegram.send`
   - Policy: Auto (if enabled in registry)
   - Action: Calls `metacontrol.py telegram_send(...)`

2. `github_commit`
   - Intent: `gh.commit.create`
   - Policy: Auto (already allowed in L1)
   - Action: Calls `metacontrol.py github_commit(...)`

3. `openai_chat`
   - Intent: `ai.openai.query`
   - Policy: Auto (non-destructive)
   - Action: Calls `metacontrol.py openai_chat(...)`

4. `make_trigger`
   - Intent: `automation.make.webhook`
   - Policy: Auto (L1.2 flow compatible)
   - Action: Calls `metacontrol.py make_trigger(...)`

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

---

#### Phase 2: local_exec_mcp

**Create**: `C:\...\Claude-Ops\mcp-servers\local_exec_mcp\`

**Structure**:
```
local_exec_mcp/
├── index.js
├── package.json
├── executor.js           # Spawns local_controller.py or scripts
├── signature_verify.js   # Validates script SHA256 hashes
├── allowlist.json        # Approved scripts with hashes
└── README.md
```

**MCP Tools Exposed**:
1. `run_signed_script`
   - Intent: `local.script.execute`
   - Policy: **ALWAYS requires_approval**
   - Validation: 
     - Must be in `allowlist.json` with matching SHA256
     - Must be located in approved directory
   - Action: Executes via PowerShell or Python subprocess

2. `write_local_file`
   - Intent: `local.file.write`
   - Policy: Auto (similar to Filesystem MCP)
   - Action: Calls `local_controller.py write_file(...)`

3. `delete_local_file`
   - Intent: `local.file.delete`
   - Policy: Requires approval for system/protected paths
   - Action: Calls `local_controller.py delete_file(...)`

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
      "path": "C:\\...\\Scripts\\cleanup.ps1",
      "sha256": "abc123...",
      "approved_by": "edri2or",
      "approved_at": "2025-11-13T10:00:00Z",
      "description": "Cleans temp files"
    }
  ],
  "directories": [
    "C:\\Users\\edri2\\Work\\AI-Projects\\Claude-Ops\\Scripts"
  ]
}
```

---

### Approval Flow (L2 Integration)

**For `local.install` or other approval-required intents**:

```
1. Claude calls local_exec_mcp.run_signed_script(script_path)
     ↓
2. MCP checks policy_gate.yaml → "requires_approval"
     ↓
3. MCP creates approval request:
   - Calls create-approval-request.sh (reuses L1.2 flow)
   - Provides: script path, hash, description
     ↓
4. L1.2 Telegram flow:
   - Make #1 → Telegram message with buttons
   - אור clicks ✅ or ❌
   - Make #2 → GitHub repository_dispatch
     ↓
5. GitHub Actions:
   - Verifies script hash
   - Adds script to allowlist.json (if approved)
   - Commits + pushes
   - Notifies Claude MCP
     ↓
6. Claude MCP re-attempts script execution
     ↓
7. Signature verification passes → Script runs
     ↓
8. Result logged to Evidence Index
```

---

### Benefits of Option A

✅ **Strategic**:
- Future-proof: All controllers become MCP-native
- Unified governance: Single policy_gate.yaml for all tools
- Scalable: Easy to add new tools

✅ **Secure**:
- Policy enforcement at MCP layer
- Signature verification for scripts
- Full audit trail (GitHub commits + Evidence Index)

✅ **User-Friendly**:
- Claude has direct tool access
- No manual JSON file creation
- Familiar L1.2 approval flow

✅ **Maintainable**:
- Controllers remain as Python (existing logic)
- MCP layer is thin wrapper
- Clear separation of concerns

---

### Risks and Mitigations

#### Risk 1: Privilege Escalation

**Threat**: MCP server bypasses policy checks

**Mitigation**:
- Policy checker runs BEFORE Python subprocess spawn
- allowlist.json is append-only (via GitHub Actions)
- All executions logged with full context

#### Risk 2: Signature Bypass

**Threat**: Attacker modifies script after approval

**Mitigation**:
- SHA256 verification on every run (not just approval)
- Scripts stored in read-only location (or signed)
- File modification timestamps logged

#### Risk 3: Secrets Exposure

**Threat**: MCP logs contain sensitive data

**Mitigation**:
- No secrets in MCP tool parameters
- Secrets passed via environment variables only
- All logs scrubbed of `TELEGRAM_BOT_TOKEN`, `GITHUB_PAT`, etc.

#### Risk 4: Runaway Execution

**Threat**: Script loops or hangs

**Mitigation**:
- Timeout enforcement (default: 30 seconds, max: 5 minutes)
- Process kill switch via GitHub Actions
- Resource limits (CPU, memory)

---

### Implementation Effort

**Estimated Time**: 1-2 weeks

| Task | Effort | Priority |
|------|--------|----------|
| metacontrol_mcp scaffold | 4 hours | P0 |
| Policy checker integration | 3 hours | P0 |
| local_exec_mcp scaffold | 4 hours | P1 |
| Signature verification | 4 hours | P1 |
| allowlist.json management | 2 hours | P1 |
| L1.2 approval integration | 6 hours | P0 |
| Testing (unit + integration) | 8 hours | P0 |
| Documentation | 4 hours | P1 |
| **Total** | **35 hours** | - |

---

## 🔧 Option B: Enhanced ps_exec (SECONDARY)

### Overview

Extend ps_exec to execute signed scripts from approved directories, without full controller integration.

### Architecture

```
┌──────────────────────────────────────────────────────┐
│  Claude Desktop (MCP Client)                         │
│  ├─ ps_exec_enhanced                                │
│  │   • Read-only commands (existing 10)             │
│  │   • NEW: run_signed_script                       │
│  │   • Validates SHA256 hash                        │
│  │   • Only from C:\...\Scripts\                    │
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

**Modify**: `C:\...\mcp-servers\ps_exec\dispatcher.ps1`

**Add**:
```powershell
# allowlist_ps.json
{
  "scripts": [
    {
      "name": "cleanup_temp",
      "path": "C:\\...\\Scripts\\cleanup_temp.ps1",
      "sha256": "abc123...",
      "approved_by": "edri2or",
      "approved_at": "2025-11-13T10:00:00Z"
    }
  ]
}

# New action in dispatcher.ps1
if ($action -eq "run_signed_script") {
    $scriptPath = $args.script_path
    $allowlist = Get-Content "allowlist_ps.json" | ConvertFrom-Json
    
    # Find in allowlist
    $entry = $allowlist.scripts | Where-Object { $_.path -eq $scriptPath }
    if (-not $entry) {
        throw "Script not in allowlist: $scriptPath"
    }
    
    # Verify hash
    $actualHash = (Get-FileHash $scriptPath -Algorithm SHA256).Hash
    if ($actualHash -ne $entry.sha256) {
        throw "Hash mismatch for $scriptPath"
    }
    
    # Execute
    & $scriptPath
}
```

---

### Benefits of Option B

✅ **Quick Win**:
- Faster implementation (~1-2 days)
- Minimal new infrastructure
- Reuses existing ps_exec

✅ **Simple**:
- One MCP server to modify
- No new Python wrappers
- Straightforward approval flow

---

### Limitations of Option B

❌ **Not Future-Proof**:
- Doesn't integrate metacontrol.py (Telegram, Make, etc.)
- Doesn't bridge local_controller.py
- PowerShell-only (no Python script support)

❌ **Limited Scope**:
- Only executes scripts, doesn't expose tools
- No direct Telegram/Make integration
- Harder to extend for L3+

---

### When to Use Option B

**Use Case**: Quick tactical solution while planning Option A
- ✅ Need script execution ASAP
- ✅ Don't need Telegram/Make integration yet
- ✅ PowerShell-centric workflows

**Timeline**: 
- Week 1: Option B (quick win)
- Week 2-3: Option A (strategic solution)

---

## 🚫 Option C: Stay at L1 (FALLBACK)

### Overview

Defer L2 implementation and remain at L1 (read-only + file ops only).

### When to Choose

**Valid Reasons**:
- L1 capabilities are sufficient for current needs
- L2 complexity/risk too high right now
- Need more time to plan governance carefully

**Process**:
1. Document L1 as "complete"
2. Create L2 backlog in GitHub Issues
3. Schedule L2 review in 1-3 months

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

---

## 🎯 Recommended Path

### Primary Strategy: Option A

**Rationale**:
- Most aligned with long-term vision (L1→L5 progression)
- Enables full controller integration
- Provides foundation for L3+ (Desktop automation, OS management)

**Phased Rollout**:
1. **Week 1**: metacontrol_mcp (Telegram, Make, OpenAI)
2. **Week 2**: local_exec_mcp (signed script execution)
3. **Week 3**: Testing + Documentation
4. **Week 4**: Production deployment with L1.2 approval flow

---

### Quick Win: Option B (Optional Bridge)

**If needed for immediate value**:
- **Days 1-2**: Implement enhanced ps_exec
- **Use for**: Quick cleanup scripts, diagnostics
- **Then**: Proceed with Option A as planned

---

### Fallback: Option C

**Only if**:
- Resources unavailable for L2
- Security concerns too high
- L1 proves sufficient for extended period

---

## 🔒 Security Principles for L2

### Defense in Depth

1. **Policy Layer**: `policy_gate.yaml` enforced by MCP
2. **Signature Layer**: SHA256 verification for all scripts
3. **Approval Layer**: Human-in-loop via L1.2 Telegram flow
4. **Audit Layer**: Full logging to Evidence Index
5. **Kill Switch**: Disable MCP server or remove from config

### Least Privilege

- MCP servers run with minimum Windows permissions
- Python subprocesses inherit only necessary env vars
- No persistent credentials in MCP code

### Monitoring

- All tool calls logged with:
  - Timestamp
  - Intent
  - User (if applicable)
  - Result (success/failure)
  - Duration

---

## 📋 Next Steps

1. **Decision**: Choose Option A (strategic) vs B (tactical) vs C (defer)
2. **Approval**: Get explicit אור approval for chosen path
3. **Implementation**: Follow phased rollout plan
4. **Testing**: Run L1 Inventory PoC to validate current L1 capabilities
5. **Documentation**: Update ADRs with L2 decision

---

**End of Bridge Proposal**

See also:
- `CURRENT_STATE.md` - Current infrastructure
- `L1_CAPABILITIES.md` - What's possible now
- `platform/manifest/policy_gate.yaml` - Governance rules
