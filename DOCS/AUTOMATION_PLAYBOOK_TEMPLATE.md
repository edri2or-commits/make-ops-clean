# Automation Playbook Template

**Document Type**: Universal Template (OS_SAFE)  
**Created**: 2025-11-17  
**Status**: 📋 TEMPLATE  
**Purpose**: Mandatory template for ALL automations in Claude-Ops system

---

## 🎯 Purpose

This template is the **required starting point** for every automation in the Claude-Ops system, regardless of domain (Google, GitHub, GCP, Local, or any other).

**Before creating ANY automation**:
1. Copy this template
2. Fill in all sections
3. Document in CAPABILITIES_MATRIX
4. Get Or's approval before CLOUD_OPS_HIGH execution

**Domains covered**: Gmail, Drive, Calendar, Sheets, GitHub, GCP, Local Filesystem, PowerShell, Make.com, any future integrations

---

## 1. Intent & Classification

### 1.1 Intent Statement

**Format**: One clear sentence describing what Or/Architect wants to achieve.

**Template**:
```
Intent: [Actor] wants [Claude/System] to [action] [target] [under conditions] [with outcome].
```

**Example (Gmail Drafts)**:
```
Intent: Or wants Claude to create contextual email drafts based on thread history, 
        documents, and meetings, without sending, so Or can review and send manually.
```

### 1.2 Classification - Purpose

**Choose one**:
- **Protection**: Prevents bad outcomes (security, backups, monitoring)
- **Control**: Enables Or to manage systems (dashboards, reports, approvals)
- **Expansion**: Adds new capabilities (integrations, workflows, features)

**Example (Gmail Drafts)**:
```
Classification: Expansion
Reason: Adds new capability (draft creation) to Claude's toolkit
```

### 1.3 Classification - Risk Level

**Choose one** (mandatory):

| Level | Definition | Examples | Approval Required |
|-------|-----------|----------|-------------------|
| **OS_SAFE** | No external impact, fully reversible, private | Read data, create drafts, local files, analysis | Content review only |
| **CLOUD_OPS_MEDIUM** | Reversible external changes, notifies others | Edit shared docs, create calendar events (with invites), label emails | Or notification + logging |
| **CLOUD_OPS_HIGH** | Irreversible or high-impact external changes | Send emails, share files externally, delete data, financial transactions | Explicit approval phrase (e.g., "מאשר שליחה") + TTL |

**Example (Gmail Drafts)**:
```
Risk Level: OS_SAFE
Reason: Drafts created but not sent, no recipients notified, fully reversible (Or can delete)
```

---

## 2. Actors & RACI

### 2.1 Actors Table

**List ALL actors involved** (even if minimal role):

| Actor | Role | Capabilities | Limitations |
|-------|------|--------------|-------------|
| **Or** | Strategic approver, Intent provider | Approve/reject, provide high-level goals | No manual technical execution |
| **Architect GPT** | Strategic planner, Task breakdown | Design workflows, suggest approaches | No direct system access |
| **Claude Desktop** | Primary executor (analysis, authoring) | Read/write/analyze, local integration, MCP tools | No GUI access, no UAC elevation |
| **GPTs GO** | Operational executor (structured, bulk) | High-volume operations, queue processing | Limited context window |
| **Executors** | Technical runners (CI/CD, Scripts) | Run workflows, deploy, configure | No strategic decisions |
| **External Systems** | Target systems (GitHub, GCP, Google, Make) | Provide APIs, execute operations | Rate limits, permissions |

**Example (Gmail Drafts)**:
```
| Actor | Role | This Automation |
|-------|------|----------------|
| Or | Approver | Reviews draft content, approves creation |
| Architect GPT | Planner | (optional) Suggests draft structure |
| Claude Desktop | Executor | Gathers context, drafts, creates via MCP |
| GPTs GO | Consulted | (optional) Template alternatives |
| External: Gmail API | Target | Stores draft in Or's account |
```

### 2.2 RACI Matrix

**For each major task in the automation**:

| Task | R (Responsible) | A (Accountable) | C (Consulted) | I (Informed) |
|------|----------------|-----------------|---------------|--------------|
| Define intent | Or | Or | Architect GPT | - |
| Design automation | Claude/GPTs GO | Or | RACI docs | - |
| Gather context | Claude | Or | External APIs | - |
| Execute operation | Claude/GPTs GO/Executor | Or | - | LOGS, MATRIX |
| Approve (if HIGH risk) | Or | Or | - | - |
| Log outcome | Claude/Executor | Or | - | STATE, MATRIX |

**Example (Gmail Drafts)**:
```
| Task | R | A | C | I |
|------|---|---|---|---|
| Request draft | Or | Or | - | - |
| Check MATRIX/RACI | Claude | Or | Docs | - |
| Gather context | Claude | Or | Gmail, Drive, Calendar | - |
| Draft content | Claude | Or | - | - |
| Review content | Or | Or | Claude (revisions) | - |
| Create draft via MCP | Claude | Or | Gmail API | LOGS |
| Log operation | Claude | Or | - | OPS/LOGS, MATRIX |
```

**Note**: **A (Accountable) is ALWAYS Or** - strategic approval authority

---

## 3. Plan - Logical Steps

### 3.1 Pre-Execution Checks (MANDATORY)

**Every automation MUST start with**:

```
1. Read CAPABILITIES_MATRIX.md
   - Check: Is this capability already documented?
   - Check: What's current status (Planned/Verified/Broken)?
   - Check: What safeguards are required?

2. Read relevant RACI document (if exists)
   - GOOGLE_AGENTS_RACI.md for Google operations
   - (future) GITHUB_AGENTS_RACI.md for GitHub operations
   - Check: Who is Responsible (R) for this operation?

3. Classify risk level
   - OS_SAFE: No approval needed (but log)
   - CLOUD_OPS_MEDIUM: Or notification + logging
   - CLOUD_OPS_HIGH: Explicit approval phrase + logging

4. Identify dependencies
   - What auth is needed? (OAuth, PAT, WIF, etc.)
   - What external systems? (APIs, databases, etc.)
   - What local resources? (files, configs, etc.)
```

### 3.2 Task Decomposition

**Break the automation into steps**, marking each:

| Step | Description | Actor | Risk | Output |
|------|-------------|-------|------|--------|
| 1 | ... | ... | OS_SAFE / MEDIUM / HIGH | File / API call / State change |
| 2 | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

**Example (Gmail Drafts)**:
```
| Step | Description | Actor | Risk | Output |
|------|-------------|-------|------|--------|
| 1 | User requests draft | Or | OS_SAFE | Intent captured |
| 2 | Check MATRIX/RACI | Claude | OS_SAFE | Capability confirmed |
| 3 | Search Gmail threads | Claude | OS_SAFE | Thread context |
| 4 | Search Drive docs | Claude | OS_SAFE | Document context |
| 5 | Search Calendar meetings | Claude | OS_SAFE | Meeting context |
| 6 | Draft email content | Claude | OS_SAFE | Draft text |
| 7 | Present to Or | Claude | OS_SAFE | Preview shown |
| 8 | Or approves content | Or | OS_SAFE | Approval given |
| 9 | Create draft via MCP | Claude | OS_SAFE | Draft in Gmail |
| 10 | Log operation | Claude | OS_SAFE | JSON in OPS/LOGS |
```

### 3.3 Specification Artifacts

**What documentation artifacts are created** (before any CLOUD_OPS_HIGH):

```
Artifacts:
- [ ] Playbook/Flow document (DOCS/[NAME]_FLOW.md)
- [ ] CAPABILITIES_MATRIX entry (row with safeguards)
- [ ] Workflow YAML (if GitHub Actions needed)
- [ ] Config template (if new service configuration)
- [ ] Test plan (verification steps after execution)
```

**Example (Gmail Drafts)**:
```
Artifacts created (G2.1-Pilot):
- [x] DOCS/PILOT_GMAIL_DRAFTS_FLOW.md (22.3KB playbook)
- [x] CAPABILITIES_MATRIX entry (Gmail Drafts row)
- [x] Test plan (5 test cases in playbook Section 7.3)
- [ ] Workflow YAML (deferred to G2.2)
- [ ] MCP config update (deferred to G2.2)
```

---

## 4. Execution Skeleton

### 4.1 Trigger

**How does the automation start?**

**Options**:
- **Chat request**: Or asks Claude directly
- **GPT delegation**: Architect GPT routes to Claude/GPTs GO
- **Schedule**: Cron/GitHub Actions on schedule
- **Event**: Webhook, email arrival, file change
- **Manual**: Executor runs workflow on demand

**Example (Gmail Drafts)**:
```
Trigger: Chat request
Flow: Or → Claude Desktop (via chat)
```

### 4.2 Execution Flow (Pseudo-Schema)

**Describe the flow** without actual code:

```
START
  ↓
[Trigger] → User request OR Schedule OR Event
  ↓
[Gate 1] → Check CAPABILITIES_MATRIX
  ├─ If Status != VERIFIED → Inform user, exit or offer G2.2 setup
  └─ If Status == VERIFIED → Continue
  ↓
[Gate 2] → Check RACI
  ├─ If Wrong Agent → Delegate to correct agent
  └─ If Correct Agent → Continue
  ↓
[Gather Context] → Read necessary data
  ├─ Local files (Filesystem)
  ├─ External APIs (Gmail, Drive, GitHub, etc.)
  └─ Previous state (STATE_FOR_GPT_SNAPSHOT)
  ↓
[Prepare Operation] → Build request payload
  ↓
[Risk Check]
  ├─ If OS_SAFE → Proceed
  ├─ If CLOUD_OPS_MEDIUM → Notify Or, log, proceed
  └─ If CLOUD_OPS_HIGH → Request explicit approval
      ├─ If Not Approved → Cancel, log
      └─ If Approved → Proceed (with TTL)
  ↓
[Execute] → Call tool/API/MCP
  ├─ Success → Log, update STATE, report to Or
  └─ Failure → Log error, report to Or, offer retry/alternatives
  ↓
[Update CAPABILITIES_MATRIX] → If first execution or status change
  ↓
END
```

### 4.3 Tool Usage

**Which tools/APIs are called**:

| Tool/API | Purpose | Auth Method | Who Executes | Risk |
|----------|---------|-------------|--------------|------|
| ... | ... | ... | Claude / GPTs GO / Executor | ... |

**Example (Gmail Drafts)**:
```
| Tool/API | Purpose | Auth Method | Who Executes | Risk |
|----------|---------|-------------|--------------|------|
| gmail.readonly | Read threads | OAuth (MCP) | Claude | OS_SAFE |
| drive.readonly | Read docs | OAuth (MCP) | Claude | OS_SAFE |
| calendar.readonly | Read meetings | OAuth (MCP) | Claude | OS_SAFE |
| gmail.compose | Create draft | OAuth (MCP) | Claude | OS_SAFE |
```

### 4.4 Approval Flow (if CLOUD_OPS_HIGH)

**Not applicable for OS_SAFE**, but include template:

```
IF Risk == CLOUD_OPS_HIGH:
  1. Claude presents:
     - Operation name
     - Target (who/what affected)
     - Preview (what will happen)
     - Reversibility (yes/no)
     - Approval phrase required (e.g., "מאשר שליחה")
     - TTL (e.g., 60 minutes)
  
  2. Or responds:
     - Exact approval phrase → Proceed
     - Different text → Request clarification
     - Timeout → Cancel operation
  
  3. Claude logs approval:
     - Timestamp
     - Operation
     - Approval phrase
     - Approved by (Or)
```

**Example (Gmail Drafts - N/A)**:
```
Risk: OS_SAFE
Approval: Content review only (not formal CLOUD_OPS_HIGH approval)
Process: Or reviews draft text, says "Create draft" or "Revise"
```

---

## 5. Safeguards

### 5.1 Mandatory Fields

**Every automation MUST document**:

```
Safeguards:
1. Approval Gate: [None / Or notification / Explicit approval phrase + TTL]
2. Rate Limiting: [None / X operations per Y time / By service]
3. Logging: [What is logged, where, format]
4. Policy Blocks: [What operations are forbidden, technical enforcement]
5. Rollback: [How to undo if things go wrong]
```

### 5.2 Approval Gate

**Based on risk level**:

| Risk Level | Approval Required | Format |
|-----------|-------------------|--------|
| OS_SAFE | Content/plan review | Conversational ("looks good", "proceed") |
| CLOUD_OPS_MEDIUM | Or notified before execution | Or acknowledges ("OK", "go ahead") |
| CLOUD_OPS_HIGH | Explicit approval phrase | Exact phrase (e.g., "מאשר שליחה"), TTL (60 min) |

**Example (Gmail Drafts)**:
```
Approval Gate: Content review (OS_SAFE)
Process: Or reviews draft text, approves creation
No formal approval phrase needed (drafts not sent)
```

### 5.3 Rate Limiting

**Prevent runaway automation**:

```
Rate Limits:
- [Service/Operation]: [X] per [time period]
- Alert at: [Y%] of limit
- Block at: [100%] of limit
- Override: [Or explicit approval for additional operations]
```

**Example (Gmail Drafts)**:
```
Rate Limits:
- Gmail draft creation: 50 per hour (optional, not enforced in pilot)
- Alert: Not implemented (OS_SAFE operation)
- Override: N/A
```

### 5.4 Mandatory Logging

**What gets logged**:

```
Log Entry Format (JSON):
{
  "timestamp": "ISO 8601 datetime",
  "operation": "tool.method or action name",
  "risk_level": "OS_SAFE | CLOUD_OPS_MEDIUM | CLOUD_OPS_HIGH",
  "status": "success | failure | cancelled",
  "actor": "Claude | GPTs GO | Executor",
  "details": {
    "target": "who/what affected",
    "params": "operation parameters (sanitized)",
    "result": "outcome summary"
  },
  "context": {
    "user_request": "original intent",
    "approval": "approval phrase if CLOUD_OPS_HIGH",
    "session_id": "tracking ID"
  },
  "metadata": {
    "pilot": "playbook name if pilot",
    "phase": "project phase",
    "logged_at": "when log was written"
  }
}
```

**Log Location**:
- Primary: `OPS/LOGS/[domain]-operations.jsonl` (append-only, committed to repo)
- Optional: External logging (Google Sheets, CloudWatch, etc.)
- State: `STATE_FOR_GPT_SNAPSHOT.md` updated with latest operation

**Privacy**: Log metadata and previews, NOT full content (email bodies, file contents, etc.)

**Example (Gmail Drafts)**:
```json
{
  "timestamp": "2025-11-17T20:55:00Z",
  "operation": "gmail.create_draft",
  "risk_level": "OS_SAFE",
  "status": "success",
  "actor": "Claude",
  "details": {
    "to": ["sarah@client.com"],
    "subject": "Apology for Q4 Report Delay + Next Steps",
    "body_preview": "Hi Sarah, I wanted to reach out... [50 chars]",
    "draft_id": "r-1234567890"
  },
  "context": {
    "user_request": "Draft apology for report delay",
    "gathered_context": ["email_thread", "calendar_recent_meetings"],
    "session_id": "session-456"
  },
  "metadata": {
    "pilot": "gmail_drafts_flow",
    "phase": "G2.1-Pilot",
    "logged_at": "2025-11-17T20:55:05Z"
  }
}
```

### 5.5 Policy Blocks

**Technical enforcement** (not just policy):

```
Forbidden Operations:
- [Operation name]: [Why forbidden]
- [Operation name]: [Why forbidden]

Enforcement Method:
- MCP server / API wrapper / Workflow validation
- Blocks even if prompt injection attempts
- Clear error message to user
```

**Example (Gmail Drafts)**:
```
Policy Blocks:
- gmail.send: Draft flow cannot send emails (requires separate flow with CLOUD_OPS_HIGH)
- gmail.settings.updateForwarding: No email forwarding (data exfiltration risk)

Enforcement: MCP server blocks these API calls
Error: "Operation blocked by policy. Use PILOT_GMAIL_SEND_FLOW for sending."
```

### 5.6 Rollback Plan

**If something goes wrong**:

```
Rollback Strategy:
- Operation type: [Create / Update / Delete]
- Reversibility: [Fully reversible / Partially / Irreversible]
- Rollback method: [Manual / Automated / Not possible]
- Recovery time: [Immediate / Within N hours / Permanent]
```

**Example (Gmail Drafts)**:
```
Rollback Strategy:
- Operation: Create draft
- Reversibility: Fully reversible
- Rollback method: Or deletes draft from Gmail manually
- Recovery time: Immediate (Or can delete anytime)
```

---

## 6. Observability & Logging

### 6.1 Log Destinations

**Where logs are stored**:

```
Primary Logging:
- Location: OPS/LOGS/[domain]-operations.jsonl
- Format: JSON Lines (one JSON object per line)
- Committed: Yes (permanent audit trail)
- Retention: Indefinite

Secondary Logging (optional):
- GitHub Actions logs (if workflows used)
- GCP Audit Logs (if GCP resources)
- External logging (Sheets, CloudWatch, etc.)
```

**Example (Gmail Drafts)**:
```
Primary: OPS/LOGS/google-operations.jsonl
Secondary: (none for pilot, future: Google Sheets tracking)
Committed: Yes (every log entry)
```

### 6.2 Status Files

**For async operations** (workflows, long-running tasks):

```
Status File Pattern:
- Location: OPS/STATUS/[operation]-status.json
- Purpose: Track operation progress
- Format:
  {
    "task": "operation name",
    "timestamp": "when started",
    "status": "pending | running | success | failed",
    "progress": "X of Y steps complete",
    "next_step": "human-readable next action",
    "workflow_run": "link to GitHub Actions run",
    "errors": []
  }
- Committed: Yes (Claude can read to verify)
```

**Example (Gmail Drafts)**:
```
Status Files: Not needed (synchronous operation via MCP)
Future (G2.2): OPS/STATUS/google-oauth-complete.json for OAuth setup
```

### 6.3 Success/Failure Indicators

**How does Claude know if automation worked?**:

```
Success Indicators:
- [ ] API returns 2xx status
- [ ] Expected output created (file, draft, resource)
- [ ] Log entry written successfully
- [ ] STATE_FOR_GPT_SNAPSHOT updated
- [ ] No errors in response

Failure Indicators:
- [ ] API returns 4xx/5xx status
- [ ] Timeout or network error
- [ ] Resource not created
- [ ] Partial completion
- [ ] Error logged
```

**Example (Gmail Drafts)**:
```
Success:
- ✅ MCP returns draft_id
- ✅ Draft visible in Gmail (Or can verify)
- ✅ Log entry in OPS/LOGS/
- ✅ No errors

Failure:
- ❌ MCP returns error
- ❌ Invalid recipient email
- ❌ Rate limit exceeded
- ❌ Network timeout
→ Claude logs error, offers retry or alternatives
```

### 6.4 Health Checks

**Post-execution verification**:

```
Health Check (after first successful execution):
1. Verify resource created/modified
2. Check logs for completeness
3. Confirm CAPABILITIES_MATRIX updated
4. Test rollback procedure
5. Document any unexpected behavior
```

**Example (Gmail Drafts)**:
```
Health Check (after G2.2):
1. Create test draft → verify in Gmail
2. Check OPS/LOGS/ for entry
3. Confirm CAPABILITIES_MATRIX shows ✅ VERIFIED
4. Test: Or deletes draft (rollback works)
5. Document: Draft threading works, attachments referenced correctly
```

---

## 7. CAPABILITIES_MATRIX & STATE Updates

### 7.1 CAPABILITIES_MATRIX Entry (MANDATORY)

**Every automation MUST have a row in CAPABILITIES_MATRIX**:

```markdown
| From | To | Capability | Status | Details | Safeguards | Last Verified | Reference |
|------|----|-----------| -------|---------|------------|---------------|-----------|
| [Actor] | [System/API] | [Capability name] | [Status emoji + text] | [What it does] | [(1) Gate (2) Rate (3) Log (4) Scope (5) Blocks] | [Date or "Pending"] | [Link to playbook] |
```

**Status values**:
- 📋 **PLANNED**: Documented intent, no implementation yet
- 🔄 **PILOT_DESIGNED**: Playbook created, not executed (OS_SAFE design only)
- ⚙️ **IN_PROGRESS**: Execution started (CLOUD_OPS_HIGH in progress)
- ✅ **VERIFIED**: Operational, tested, documented
- ⚠️ **PARTIAL**: Works but with limitations
- ❌ **BROKEN**: Was working, now broken (needs fix)

**Safeguards** (all 5 required):
1. **Approval Gate**: None / Or notification / Explicit phrase + TTL
2. **Rate Limiting**: None / X per Y / Service-specific
3. **Logging**: Where logged, what's included
4. **Scope Limitation**: Which API scopes / permissions used
5. **Policy Blocks**: What's forbidden, enforcement method

**Example (Gmail Drafts)**:
```markdown
| Claude MCP | Gmail API | Create drafts | 🔄 PILOT_DESIGNED | Create new email drafts (not sent) | (1) Content approval (OS_SAFE) (2) Rate: 50/hour (optional) (3) Log: OPS/LOGS/google-operations.jsonl (4) Scope: gmail.compose only (5) Block: cannot call gmail.send | Pending G2.2 | [PILOT_GMAIL_DRAFTS_FLOW.md](DOCS/PILOT_GMAIL_DRAFTS_FLOW.md) |
```

### 7.2 STATE_FOR_GPT_SNAPSHOT Update

**After successful execution**, update STATE snapshot:

```
STATE_FOR_GPT_SNAPSHOT.md additions:

## [Domain] Operations

**[Capability Name]**:
- Status: [Verified / Partial / Broken]
- Last used: [Date and time]
- Last operation: [Brief description]
- Success rate: [X of Y successful]
- Known issues: [List any problems]
- Next review: [Date]

Example recent operation:
[Brief 1-2 sentence summary of last use]
```

**Example (Gmail Drafts after G2.2)**:
```markdown
## Google MCP Operations

**Gmail Drafts**:
- Status: Verified
- Last used: 2025-11-17 20:55 IST
- Last operation: Created draft to sarah@client.com (Q4 report apology)
- Success rate: 5 of 5 successful
- Known issues: None
- Next review: 2025-12-01

Example recent operation:
Created contextual draft for customer about project delay, gathered context 
from email thread + calendar meeting, draft stored in Gmail (not sent).
```

### 7.3 Evidence Collection

**Document proof that automation works**:

```
Evidence Required:
- [ ] Screenshot/log of successful execution
- [ ] Link to created resource (draft, file, PR, etc.)
- [ ] Git commit showing CAPABILITIES_MATRIX update
- [ ] Git commit showing log entry
- [ ] Link to GitHub Actions run (if applicable)
```

**Example (Gmail Drafts)**:
```
Evidence (after G2.2):
- [ ] MCP response with draft_id
- [ ] Screenshot of draft in Gmail
- [ ] Commit: [sha] updated CAPABILITIES_MATRIX (Gmail Drafts → VERIFIED)
- [ ] Commit: [sha] added log to OPS/LOGS/google-operations.jsonl
- [ ] Claude session showing successful draft creation
```

---

## 8. Example - Gmail Drafts Pilot (Filled Template)

**This section demonstrates a complete worked example using Gmail Drafts.**

---

### 8.1 Intent & Classification

**Intent Statement**:
```
Intent: Or wants Claude to create contextual email drafts based on thread history, 
        related documents, and recent meetings, without sending, so Or can review 
        and manually send when ready.
```

**Classification - Purpose**:
```
Classification: Expansion
Reason: Adds new capability (contextual draft creation) to Claude's toolkit, 
        enhancing email workflow efficiency
```

**Classification - Risk**:
```
Risk Level: OS_SAFE
Reason: 
- Drafts created but not sent (no recipients notified)
- No external impact (drafts remain in Or's Gmail account)
- Fully reversible (Or can delete or edit drafts anytime)
- Private (only Or sees drafts)
- No automation (each draft requires Or's content approval)
```

---

### 8.2 Actors & RACI

**Actors Table**:
```
| Actor | Role | This Automation |
|-------|------|-----------------|
| Or | Strategic approver | Reviews draft content, approves creation |
| Architect GPT | Planner (optional) | May suggest draft structure or approach |
| Claude Desktop | Primary executor | Gathers context (threads, docs, meetings), drafts content, creates via MCP |
| GPTs GO | Consultant (optional) | May offer template-based alternatives |
| Gmail API | Target system | Stores draft in Or's Gmail account |
```

**RACI Matrix**:
```
| Task | R (Responsible) | A (Accountable) | C (Consulted) | I (Informed) |
|------|-----------------|-----------------|---------------|--------------|
| Request draft | Or | Or | - | - |
| Check MATRIX/RACI | Claude | Or | CAPABILITIES_MATRIX, GOOGLE_AGENTS_RACI | - |
| Search email threads | Claude | Or | Gmail API | - |
| Search related docs | Claude | Or | Drive API | - |
| Check recent meetings | Claude | Or | Calendar API | - |
| Draft content | Claude | Or | Local files, web search (if needed) | - |
| Present draft to Or | Claude | Or | - | - |
| Review content | Or | Or | Claude (for revisions) | - |
| Approve creation | Or | Or | - | - |
| Create draft via MCP | Claude | Or | Gmail API | - |
| Log operation | Claude | Or | - | OPS/LOGS/, CAPABILITIES_MATRIX |
```

**Per GOOGLE_AGENTS_RACI.md**:
- Claude (R) for contextual, researched, unique drafts
- GPTs GO (R) for template-based, bulk, standardized drafts
- This use case = contextual → Claude is Responsible

---

### 8.3 Plan - Logical Steps

**Pre-Execution Checks**:
```
1. ✅ Read CAPABILITIES_MATRIX Section 3.1 Gmail
   - Find: "Create drafts" capability
   - Status: PILOT_DESIGNED (will become VERIFIED after G2.2)
   - Risk: OS_SAFE

2. ✅ Read GOOGLE_AGENTS_RACI.md Section 1.2
   - Contextual drafts: Claude (R)
   - Confirm: This is Claude's responsibility

3. ✅ Classify risk: OS_SAFE
   - Drafts not sent, no external impact

4. ✅ Identify dependencies:
   - Auth: OAuth via Google MCP Server (gmail.compose scope)
   - External: Gmail API, Drive API, Calendar API
   - Local: Filesystem (for context)
```

**Task Decomposition**:
```
| Step | Description | Actor | Risk | Output |
|------|-------------|-------|------|--------|
| 1 | User requests draft | Or | OS_SAFE | Intent captured |
| 2 | Claude checks MATRIX | Claude | OS_SAFE | Capability confirmed |
| 3 | Claude checks RACI | Claude | OS_SAFE | Responsibility confirmed (Claude = R) |
| 4 | Search Gmail threads | Claude | OS_SAFE | Thread context (if reply) |
| 5 | Search Drive for docs | Claude | OS_SAFE | Relevant documents (project status, etc.) |
| 6 | Search Calendar | Claude | OS_SAFE | Recent meetings with recipient |
| 7 | Check local files | Claude | OS_SAFE | Any relevant context on Or's computer |
| 8 | Web search (if needed) | Claude | OS_SAFE | Company info, news, etc. |
| 9 | Draft email content | Claude | OS_SAFE | Draft text (subject + body) |
| 10 | Present to Or | Claude | OS_SAFE | Full preview shown |
| 11 | Or reviews & approves | Or | OS_SAFE | "Create draft" or "Revise" |
| 12 | Create draft via MCP | Claude | OS_SAFE | Draft in Gmail (draft_id returned) |
| 13 | Log operation | Claude | OS_SAFE | JSON entry in OPS/LOGS/ |
| 14 | Report to Or | Claude | OS_SAFE | Confirmation + draft ID |
```

**Specification Artifacts**:
```
Created (Phase G2.1-Pilot):
- [x] DOCS/PILOT_GMAIL_DRAFTS_FLOW.md (22.3KB complete playbook)
- [x] CAPABILITIES_MATRIX entry (Gmail Drafts row with all safeguards)
- [x] Test plan (5 test cases in playbook Section 7.3)
- [x] AUTOMATION_PLAYBOOK_TEMPLATE.md (this template, using Gmail Drafts as example)

Deferred to G2.2 (OAuth setup phase):
- [ ] GitHub Actions workflow (google-mcp-enable-apis.yml)
- [ ] MCP server configuration update
- [ ] OAuth client creation
```

---

### 8.4 Execution Skeleton

**Trigger**:
```
Type: Chat request
Flow: Or → Claude Desktop (direct conversation)
Example: "Draft an email to sarah@client.com apologizing for Q4 report delay"
```

**Execution Flow**:
```
START
  ↓
[Chat Request] User: "Draft email to X about Y"
  ↓
[Gate 1: Check MATRIX]
  - Read: CAPABILITIES_MATRIX Section 3.1
  - Find: Gmail Drafts capability
  - Status: PILOT_DESIGNED (before G2.2) or VERIFIED (after G2.2)
  - If NOT VERIFIED:
      Claude: "This capability is designed but not operational yet.
               Current status: PILOT_DESIGNED
               Need Phase G2.2: OAuth setup (Executor + your consent)
               
               For now, I can draft the text and save to local file.
               Would you like to proceed with G2.2 setup?"
      → Exit or offer alternatives
  - If VERIFIED: Continue
  ↓
[Gate 2: Check RACI]
  - Read: GOOGLE_AGENTS_RACI.md Section 1.2
  - Check: Contextual draft = Claude (R)
  - If GPTs GO better suited: Suggest delegation
  - If Claude responsible: Continue
  ↓
[Gather Context] (all OS_SAFE)
  - Search Gmail: gmail.readonly scope
    → Is this a reply? Get thread context
  - Search Drive: drive.readonly scope
    → Relevant docs (project status, etc.)
  - Search Calendar: calendar.readonly scope
    → Recent meetings with recipient
  - Local files: Filesystem tools
    → Any relevant context on Or's computer
  - Web search (optional): web_search tool
    → Company info, news, etc.
  ↓
[Draft Content]
  - Claude generates draft:
      - Subject line
      - Greeting
      - Body (based on gathered context)
      - Call to action
      - Signature
  ↓
[Present for Review]
  - Claude shows full draft to Or
  - Options: "Create draft" / "Revise" / "Cancel"
  ↓
[Risk Check]
  - Risk: OS_SAFE
  - No formal approval gate needed (not CLOUD_OPS_HIGH)
  - Or's "Create draft" confirmation is content approval
  ↓
[Execute via MCP]
  - Tool: google_workspace_extended (MCP server)
  - Method: gmail.create_draft
  - Params:
      {
        "to": ["recipient@example.com"],
        "subject": "...",
        "body": "...",
        "body_type": "html",
        "thread_id": null (or thread ID if reply)
      }
  - MCP Server:
      1. Reads OAuth refresh token (from Secret Manager)
      2. Gets fresh access token (from Google OAuth)
      3. Calls Gmail API: users.drafts.create
      4. Returns: { "draft_id": "r-123", "message_id": "m-456" }
  ↓
[Handle Response]
  - Success:
      → Log to OPS/LOGS/google-operations.jsonl
      → Report to Or: "✅ Draft created, ID: r-123"
  - Failure:
      → Log error
      → Report to Or: "❌ Failed: [reason]"
      → Offer retry or alternatives
  ↓
[Update STATE]
  - Add to STATE_FOR_GPT_SNAPSHOT:
      "Gmail Drafts: Last used [timestamp], created draft for [recipient]"
  ↓
END
```

**Tool Usage**:
```
| Tool/API | Purpose | Auth Method | Who Executes | Risk |
|----------|---------|-------------|--------------|------|
| gmail.readonly | Read email threads | OAuth (MCP) | Claude | OS_SAFE |
| drive.readonly | Read documents | OAuth (MCP) | Claude | OS_SAFE |
| calendar.readonly | Read meetings | OAuth (MCP) | Claude | OS_SAFE |
| filesystem (local) | Read local files | Native (Claude) | Claude | OS_SAFE |
| web_search | Research context | Brave API | Claude | OS_SAFE |
| gmail.compose | Create draft | OAuth (MCP) | Claude | OS_SAFE |
```

**Approval Flow**:
```
Risk: OS_SAFE
Approval Process:
  1. Claude presents full draft to Or
  2. Or reviews content
  3. Or says: "Create draft" (conversational, not formal approval phrase)
  4. Claude creates draft via MCP
  5. No TTL (OS_SAFE doesn't require time-bound approvals)

Not CLOUD_OPS_HIGH because:
  - Draft is not sent
  - No recipients notified
  - Fully reversible
```

---

### 8.5 Safeguards

**Mandatory Fields**:
```
Safeguards (Gmail Drafts):
1. Approval Gate: Content review (Or approves draft text before creation)
2. Rate Limiting: 50 drafts/hour (optional, not enforced in pilot)
3. Logging: Every draft creation logged to OPS/LOGS/google-operations.jsonl
4. Policy Blocks: Cannot call gmail.send (even if prompted)
5. Rollback: Or can delete draft from Gmail anytime (fully reversible)
```

**Approval Gate**:
```
Type: Content review (OS_SAFE)
Process:
  - Claude presents full draft
  - Or reviews subject + body
  - Or can request revisions
  - Or says "Create draft" to proceed
  - No formal approval phrase needed (not CLOUD_OPS_HIGH)
```

**Rate Limiting**:
```
Service: Gmail draft creation
Limit: 50 per hour (optional, not currently enforced)
Rationale: OS_SAFE operation, low abuse risk
Alert: Not implemented
Block: Not implemented
Override: N/A (no hard limit in pilot)
```

**Mandatory Logging**:
```json
{
  "timestamp": "2025-11-17T20:55:00Z",
  "operation": "gmail.create_draft",
  "risk_level": "OS_SAFE",
  "status": "success",
  "actor": "Claude",
  "details": {
    "to": ["sarah@client.com"],
    "subject": "Apology for Q4 Report Delay + Next Steps",
    "body_preview": "Hi Sarah, I wanted to reach out... [first 50 chars]",
    "draft_id": "r-1234567890",
    "thread_id": null
  },
  "context": {
    "user_request": "Draft apology for report delay",
    "gathered_context": ["email_thread", "calendar_recent_meetings", "drive_docs"],
    "session_id": "session-456"
  },
  "metadata": {
    "pilot": "gmail_drafts_flow",
    "phase": "G2.1-Pilot",
    "logged_at": "2025-11-17T20:55:05Z"
  }
}
```

**Log Location**: `OPS/LOGS/google-operations.jsonl` (committed to repo)

**Policy Blocks**:
```
Forbidden Operations:
  - gmail.send: Draft flow cannot send emails
    → Requires separate PILOT_GMAIL_SEND_FLOW with CLOUD_OPS_HIGH approval
  - gmail.settings.updateForwarding: No email forwarding
    → Data exfiltration risk
  - gmail.settings.updateAutoReply: No auto-responders without approval
    → Could send spam

Enforcement Method:
  - MCP server checks operation before API call
  - Blocks forbidden operations
  - Returns clear error: "Operation blocked by policy. Use [correct flow] instead."
  - Prompt injection cannot bypass (technical enforcement)
```

**Rollback Plan**:
```
Operation Type: Create (draft)
Reversibility: Fully reversible
Rollback Method: Manual (Or deletes draft from Gmail)
Recovery Time: Immediate (Or can delete anytime)
Steps:
  1. Or opens Gmail
  2. Navigates to Drafts folder
  3. Finds draft (by subject or recipient)
  4. Clicks Delete or Edit
→ No automation needed for rollback (OS_SAFE operation)
```

---

### 8.6 Observability & Logging

**Log Destinations**:
```
Primary: OPS/LOGS/google-operations.jsonl
  - Format: JSON Lines (one object per line)
  - Committed: Yes (permanent audit trail)
  - Retention: Indefinite

Secondary: (future) Google Sheets tracking
  - Not implemented in pilot
  - Could add: Spreadsheet logging for dashboard

GitHub Actions Logs: N/A
  - Pilot uses MCP (synchronous), not workflows

GCP Audit Logs: Yes (future)
  - Secret Manager access logged automatically
  - OAuth token refresh logged
```

**Status Files**:
```
Not needed for Gmail Drafts:
  - Synchronous operation via MCP
  - Immediate response (draft_id or error)

Future (G2.2 OAuth setup):
  - OPS/STATUS/google-oauth-complete.json
  - OPS/STATUS/google-mcp-ready.json
```

**Success/Failure Indicators**:
```
Success:
  - ✅ MCP returns draft_id (e.g., "r-1234567890")
  - ✅ Draft visible in Gmail Drafts folder
  - ✅ Log entry created in OPS/LOGS/
  - ✅ Claude reports: "✅ Draft created successfully"

Failure:
  - ❌ MCP returns error object
  - ❌ Possible errors:
      - Invalid recipient email
      - Rate limit exceeded (unlikely for OS_SAFE)
      - Network timeout
      - Invalid OAuth token
  - ❌ Claude logs error
  - ❌ Claude reports: "❌ Failed: [reason]"
  - ❌ Claude offers: Retry / Fix recipient / Report to Or
```

**Health Checks (after G2.2)**:
```
Post-Execution Verification:
  1. Create test draft to test@example.com
  2. Verify draft appears in Gmail
  3. Check OPS/LOGS/ for log entry
  4. Confirm CAPABILITIES_MATRIX updated to ✅ VERIFIED
  5. Test rollback: Or deletes test draft
  6. Verify threading: Create reply draft, check thread_id correct
  7. Document any unexpected behavior

Test Cases (from PILOT_GMAIL_DRAFTS_FLOW Section 7.3):
  1. Basic draft (simple recipient + subject)
  2. Contextual draft (reply to existing thread)
  3. Multi-draft (create 3 options)
  4. Error handling (invalid recipient)
  5. Rate limit (if implemented: test 51 drafts in 1 hour)
```

---

### 8.7 CAPABILITIES_MATRIX & STATE Updates

**CAPABILITIES_MATRIX Entry**:
```markdown
### 3.1 Gmail

| From | To | Capability | Status | Details | Safeguards | Last Verified | Reference |
|------|----|-----------| -------|---------|------------|---------------|-----------|
| Claude MCP | Gmail API | Create drafts | 🔄 PILOT_DESIGNED | Create new email drafts based on context (not sent) | (1) Content approval (Or reviews before creation) (2) Rate: 50/hour (optional) (3) Log: OPS/LOGS/google-operations.jsonl (4) Scope: gmail.compose only (5) Block: cannot call gmail.send | Pending G2.2 | [PILOT_GMAIL_DRAFTS_FLOW.md](DOCS/PILOT_GMAIL_DRAFTS_FLOW.md) |
```

**Status will update after G2.2**:
```
Before G2.2: 🔄 PILOT_DESIGNED
After G2.2 execution: ⚙️ IN_PROGRESS (during OAuth setup)
After G2.2 complete + test: ✅ VERIFIED
If issues found: ⚠️ PARTIAL (works with limitations)
If breaks later: ❌ BROKEN (was working, now broken)
```

**STATE_FOR_GPT_SNAPSHOT Update (after G2.2)**:
```markdown
## Google MCP Operations

**Gmail Drafts**:
- Status: Verified
- Last used: 2025-11-17 20:55 IST
- Last operation: Created draft to sarah@client.com re: Q4 report delay
- Success rate: 5 of 5 successful (100%)
- Known issues: None
- Next review: 2025-12-01

Recent operations:
1. 2025-11-17 20:55 - Draft to sarah@client.com (apology, report delay)
2. 2025-11-17 19:30 - Draft to team@company.com (feature launch announcement)
3. 2025-11-17 18:15 - Draft reply to john@partner.com (meeting follow-up)

Context gathering working well:
- Email threads: Successfully extracts thread context for replies
- Documents: Pulls relevant Drive docs (project status, reports)
- Calendar: References recent meetings in drafts
- Local files: Integrates content from Or's computer when relevant
```

**Evidence (after G2.2)**:
```
Evidence of successful Gmail Drafts capability:

1. MCP Response:
   {
     "draft_id": "r-1234567890",
     "message_id": "m-0987654321",
     "thread_id": null
   }

2. Screenshot: Gmail Drafts folder showing created draft

3. Git Commit:
   - Commit [abc123]: Updated CAPABILITIES_MATRIX (Gmail Drafts → VERIFIED)
   - Commit [def456]: Added log to OPS/LOGS/google-operations.jsonl

4. Claude Session: Transcript showing successful draft creation flow

5. Test Results: All 5 test cases passed (basic, contextual, multi-draft, error handling, rate limit)
```

---

### 8.8 Summary - Gmail Drafts Example

**What makes this a good automation**:
- ✅ Clear intent (draft emails without sending)
- ✅ Well-defined scope (new drafts only, not editing existing)
- ✅ Low risk (OS_SAFE - no external impact)
- ✅ Documented safeguards (5 layers, even for OS_SAFE)
- ✅ Comprehensive logging (every operation tracked)
- ✅ Clear RACI (Claude responsible for contextual drafts)
- ✅ Integration with existing architecture (OAuth, MCP, MATRIX)
- ✅ Template for future capabilities (copy pattern for Gmail Send, Drive, etc.)
- ✅ Tested verification plan (5 test cases ready)

**Phase G2.1-Pilot Achievement**:
- Complete playbook (PILOT_GMAIL_DRAFTS_FLOW.md - 22.3KB)
- CAPABILITIES_MATRIX entry (with all safeguards documented)
- Template established (this example serves as pattern)
- Ready for G2.2 execution (OAuth setup by Executor)

**Next Steps**:
1. Or approves pilot design (this example)
2. Phase G2.2: Executor runs OAuth workflows
3. Or clicks OAuth consent (one-time, grants gmail.compose)
4. Test Gmail Drafts capability
5. Update CAPABILITIES_MATRIX: PILOT_DESIGNED → VERIFIED
6. Copy template for next capability (Gmail Send, Drive Create, etc.)

---

## 9. Template Usage Instructions

### 9.1 When to Use This Template

**ALWAYS use this template when**:
- Creating a new automation (any domain)
- Expanding an existing capability
- Documenting an undocumented automation
- Planning a CLOUD_OPS_HIGH operation

**Before writing ANY code or executing ANY workflow**:
1. Copy this template
2. Fill in ALL sections
3. Document in CAPABILITIES_MATRIX
4. Get Or's approval for design
5. Only then proceed to execution

### 9.2 How to Fill the Template

**Step-by-step**:
```
1. Copy template to new file:
   DOCS/[AUTOMATION_NAME]_PLAYBOOK.md

2. Fill Section 1: Intent & Classification
   - Write clear one-sentence intent
   - Choose: Protection / Control / Expansion
   - Determine risk: OS_SAFE / MEDIUM / HIGH

3. Fill Section 2: Actors & RACI
   - List all actors (Or, Claude, GPTs GO, Executors, External)
   - Create RACI matrix for each major task

4. Fill Section 3: Plan
   - Document pre-execution checks
   - Break down into logical steps
   - Mark each step with actor + risk level

5. Fill Section 4: Execution Skeleton
   - Describe trigger (chat, schedule, event, etc.)
   - Draw flow diagram (pseudo-schema)
   - List all tools/APIs used

6. Fill Section 5: Safeguards
   - Document ALL 5 layers (approval, rate, log, scope, blocks)
   - Even OS_SAFE needs safeguards (just lighter)

7. Fill Section 6: Observability
   - Define log locations and format
   - Status files (if async)
   - Success/failure indicators

8. Fill Section 7: MATRIX & STATE
   - Write complete CAPABILITIES_MATRIX row
   - Plan STATE_FOR_GPT_SNAPSHOT update
   - List evidence you'll collect

9. Add to CAPABILITIES_MATRIX:
   - Paste row from Section 7
   - Link to your playbook

10. Get Or's approval:
    - Present complete playbook
    - Explain intent, risk, safeguards
    - Only proceed after explicit approval
```

### 9.3 Customization by Risk Level

**OS_SAFE automations**:
- Lighter approval gate (content review)
- Optional rate limiting
- Logging still mandatory
- Policy blocks still needed
- Example: Gmail Drafts, Read operations, Local file creation

**CLOUD_OPS_MEDIUM automations**:
- Or notification before execution
- Rate limiting recommended
- Logging mandatory
- Reversibility via version history or manual undo
- Example: Edit shared docs, Label emails, Create calendar events with invites

**CLOUD_OPS_HIGH automations**:
- Explicit approval phrase required (e.g., "מאשר שליחה")
- 60-minute TTL on approval
- Rate limiting mandatory
- Logging mandatory (detailed)
- Policy blocks critical
- Example: Send emails, Share files externally, Delete data

### 9.4 Template Checklist

**Before considering automation "documented"**:

- [ ] All 9 sections filled completely
- [ ] RACI matrix shows who does what
- [ ] Risk level clearly determined and justified
- [ ] All 5 safeguards documented (even if "None" for some)
- [ ] Logging format specified
- [ ] CAPABILITIES_MATRIX entry ready
- [ ] Referenced from MCP_GPT_CAPABILITIES_BRIDGE (if needed)
- [ ] Or has reviewed and approved (before any CLOUD_OPS_HIGH)

---

## 10. Integration with Existing Framework

### 10.1 Relationship to Other Documents

**This template integrates with**:

| Document | Relationship |
|----------|-------------|
| **CAPABILITIES_MATRIX.md** | Every automation MUST have entry in MATRIX |
| **MCP_GPT_CAPABILITIES_BRIDGE.md** | GPTs check MATRIX, reference playbooks |
| **GOOGLE_AGENTS_RACI.md** | Specific RACI for Google operations |
| **GOOGLE_MCP_OAUTH_ARCH.md** | Authentication architecture for Google |
| **PILOT_GMAIL_DRAFTS_FLOW.md** | First complete playbook using this template |
| **STATE_FOR_GPT_SNAPSHOT.md** | Updated after each automation execution |
| **OPS/LOGS/** | All operations logged here |

### 10.2 Template Evolution

**As system grows**:
- This template may be extended (never reduced)
- New sections added based on lessons learned
- Examples updated with more diverse use cases
- Maintained as single source of truth for automation structure

**Version control**:
- Template updates committed to repo
- Version number in header (currently: 1.0)
- Major changes = new version
- All automations reference template version used

---

## 11. Appendix - Quick Reference

### Risk Level Decision Tree

```
Does operation affect external parties or systems?
  ├─ NO → Can it be undone easily?
  │      ├─ YES → OS_SAFE
  │      └─ NO → CLOUD_OPS_MEDIUM
  └─ YES → Is it reversible within 24 hours?
         ├─ YES → CLOUD_OPS_MEDIUM
         └─ NO → CLOUD_OPS_HIGH

Examples:
- Create draft (not sent) → OS_SAFE
- Edit shared doc (version history) → CLOUD_OPS_MEDIUM
- Send email (can't unsend) → CLOUD_OPS_HIGH
- Delete file (trash recovery <30 days) → CLOUD_OPS_MEDIUM
- Delete file (permanent) → CLOUD_OPS_HIGH
```

### Safeguards Quick Reference

```
Every automation needs:
1. Approval Gate:
   OS_SAFE: Content review
   CLOUD_OPS_MEDIUM: Or notification
   CLOUD_OPS_HIGH: Explicit phrase + TTL

2. Rate Limiting:
   Optional for OS_SAFE
   Recommended for MEDIUM
   Mandatory for HIGH

3. Logging:
   ALWAYS mandatory (all risk levels)
   Format: JSON to OPS/LOGS/
   Include: timestamp, operation, status, actor, details

4. Scope Limitation:
   Use minimal required scopes/permissions
   Document in CAPABILITIES_MATRIX

5. Policy Blocks:
   Technical enforcement of forbidden operations
   Cannot be bypassed by prompt injection
```

### CAPABILITIES_MATRIX Row Template

```markdown
| [From] | [To] | [Capability] | [Status] | [Details] | (1) [Approval] (2) [Rate] (3) [Log] (4) [Scope] (5) [Blocks] | [Date or Pending] | [Link to playbook] |
```

---

**Maintained by**: Claude  
**Created**: 2025-11-17  
**Version**: 1.0  
**Status**: TEMPLATE (mandatory for all automations)  
**Example**: Gmail Drafts (Section 8)
