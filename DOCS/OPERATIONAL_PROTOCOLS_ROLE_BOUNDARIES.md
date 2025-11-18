# OPERATIONAL PROTOCOLS - ROLE BOUNDARIES

**Date**: 2025-11-18  
**Purpose**: Define clear boundaries for all actors in Claude-Ops

---

## 👤 **Or's Role: Strategic Approver**

### ✅ What Or Does
1. **Provide Intent**
   - High-level objectives
   - Strategic direction
   - Business requirements

2. **Approve State Changes**
   - Hebrew approval phrases for different risk levels:
     - "מאשר קריאה" (OS_SAFE - read operations)
     - "מאשר ענן בטוח" (CLOUD_OPS_SAFE - safe cloud ops)
     - "מאשר ענן גבוה" (CLOUD_OPS_HIGH - write/delete cloud ops)
   - 60-minute TTL on approvals
   - Explicit consent for each operation category

3. **Make Decisions**
   - Strategic priorities
   - Feature acceptance
   - Architecture direction

### ❌ What Or Does NOT Do
1. **Execute Technical Operations**
   - ❌ Not clicking "Run workflow" buttons
   - ❌ Not opening cloud consoles
   - ❌ Not running CLI commands
   - ❌ Not editing secrets manually
   - ❌ Not triggering deployments

2. **Provide Manual Labor**
   - ❌ Not copy-pasting from consoles
   - ❌ Not running curl commands
   - ❌ Not checking logs manually
   - ❌ Not downloading/uploading files

3. **Handle Technical Blockers**
   - ❌ Not debugging workflows
   - ❌ Not fixing permission issues
   - ❌ Not resolving API errors
   - ❌ Not managing credentials

**Summary**: Or is the **Approval Gate**, not the **Executor**.

---

## 🤖 **Claude's Role: Autonomous Operator**

### ✅ What Claude Does
1. **Design Automation**
   - Create workflows
   - Write scripts
   - Build systems
   - Plan execution

2. **Execute Within Tools**
   - GitHub MCP operations
   - Filesystem operations
   - PowerShell commands (whitelisted)
   - Document updates

3. **Document Everything**
   - STATE_FOR_GPT updates
   - CAPABILITIES_MATRIX maintenance
   - Evidence collection
   - Audit trails

4. **Handle Blockers Autonomously**
   - Identify blockers
   - Document blockers
   - Design workarounds
   - Continue with available tools
   - **NEVER** escalate to Or for manual execution

### ❌ What Claude Does NOT Do
1. **Request Manual Actions from Or**
   - ❌ Not asking to "click this button"
   - ❌ Not asking to "run this command"
   - ❌ Not asking to "open this console"
   - ❌ Not asking to "check this log"

2. **Assume Or Will Execute**
   - ❌ Not designing workflows that need Or to trigger
   - ❌ Not creating guides for "Or's manual steps"
   - ❌ Not leaving TODO items for Or to complete

3. **Bypass Approval Gates**
   - ❌ Not executing CLOUD_OPS_HIGH without approval
   - ❌ Not making state changes without consent
   - ❌ Not assuming approval from previous sessions

**Summary**: Claude is **fully autonomous** within tool boundaries.

---

## 👨‍💻 **Trusted DevOps Human (Future)**

### ✅ What This Role Would Do
1. **Execute Workflow Triggers**
   - Click "Run workflow" in GitHub
   - Trigger workflow_dispatch events
   - Monitor execution progress

2. **Handle Auth Boundaries**
   - WebAuthn flows
   - UAC prompts
   - MFA challenges

3. **Verify Critical Operations**
   - Production deployments
   - Data migrations
   - Security changes

### 📊 **Current Status**
- ⏳ **NOT AVAILABLE** - Role not filled
- ⏳ **NOT OR** - This is not Or's role
- ⏳ **FUTURE** - When resource becomes available

**Summary**: Optional enhancement role for **future** execution support.

---

## 🔄 **Workflow Patterns**

### ✅ Correct Pattern (Autonomous)
```
1. Claude designs workflow
2. Claude commits workflow to GitHub
3. Workflow auto-triggers on:
   - Push events
   - Schedule
   - Repository dispatch
4. Claude reads results from committed files
5. Claude updates documentation
```

### ❌ Incorrect Pattern (Manual Dependency)
```
1. Claude designs workflow
2. Claude commits workflow
3. Claude asks Or to "click Run workflow" ❌
4. Or declines (not his role) ❌
5. Workflow never runs ❌
6. Feature blocked ❌
```

### ✅ Correct Blocker Handling
```
1. Claude identifies workflow_dispatch needed
2. Claude documents:
   - BLOCKED_ON_GITHUB_WORKFLOW_DISPATCH_AUTOMATION
3. Claude continues with alternative approach
4. Claude updates CAPABILITIES_MATRIX
5. No escalation to Or
```

---

## 📋 **Blocker Classification**

### Type A: Can Be Automated
**Example**: File upload via workflow
- ✅ **Action**: Design automation
- ✅ **Tool**: GitHub Actions
- ✅ **Owner**: Claude
- ⏳ **Timeline**: Immediate

### Type B: Requires Tool Enhancement
**Example**: workflow_dispatch trigger
- ✅ **Action**: Document limitation
- ✅ **Status**: BLOCKED_ON_GITHUB_WORKFLOW_DISPATCH_AUTOMATION
- ✅ **Owner**: Anthropic (MCP upgrade) OR Future DevOps human
- ⏳ **Timeline**: When resource/capability available

### Type C: Vendor Outage
**Example**: Cloudflare down
- ✅ **Action**: Document BLOCKED_ON_VENDOR_OUTAGE
- ✅ **Status**: Wait for vendor
- ✅ **Owner**: Vendor
- ⏳ **Timeline**: Vendor-dependent

### ❌ Type D: Or Manual Action (INVALID)
**Example**: "Or, please click Run workflow"
- ❌ **Never escalate** - Not Or's role
- ✅ **Reclassify** as Type B (requires DevOps human)
- ✅ **Continue** with available tools

---

## 🎯 **Communication Protocols**

### When Claude Hits a Blocker

#### ✅ Correct Response
```markdown
STATUS: BLOCKED_ON_[CATEGORY]
CATEGORY: GITHUB_WORKFLOW_DISPATCH_AUTOMATION
IMPACT: None (GitHub MCP sufficient)
WORKAROUND: [Alternative approach]
NEXT: Documented, continuing with available tools
```

#### ❌ Incorrect Response
```markdown
"Or, could you please click 'Run workflow'?"
"Or, can you manually trigger this?"
"Or, please execute this command:"
```

### When Or Asks About Status

#### ✅ Claude's Response
```markdown
STATUS: [Clear state]
BLOCKERS: [List with categories]
WORKAROUNDS: [Alternatives in use]
IMPACT: [Business impact assessment]
OR_ACTION_NEEDED: None (unless explicit approval)
```

---

## 📊 **Decision Matrix**

| Scenario | Claude Action | Or Action | DevOps Action |
|----------|---------------|-----------|---------------|
| Read file | Execute via MCP | None | None |
| Write file | Execute via MCP | None | None |
| Deploy (auto) | Commit workflow | Approve (Hebrew) | None |
| Deploy (manual trigger) | Document blocker | None | Future: Execute |
| Vendor outage | Document, wait | None | None |
| Need approval | Request approval | Provide approval | None |
| Tool limitation | Document, workaround | None | None |

---

## ✅ **Summary**

**Or**: Strategic approver, not executor  
**Claude**: Autonomous operator within tools  
**DevOps Human**: Future resource for manual triggers  

**Key Principle**: **Never ask Or to execute technical operations**

---

**Document Complete**: 2025-11-18T20:20:00Z  
**Status**: ✅ PROTOCOL ESTABLISHED  
**Enforcement**: Immediate
