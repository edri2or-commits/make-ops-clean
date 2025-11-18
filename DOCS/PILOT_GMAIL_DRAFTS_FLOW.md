# Pilot: Gmail Drafts Flow (Phase G2.1-Pilot)

**Document Type**: Pilot Specification (OS_SAFE)  
**Created**: 2025-11-17  
**Status**: 📝 PILOT_DESIGNED  
**Purpose**: End-to-end playbook for Gmail Drafts capability - template for all future capabilities

---

## 🎯 Purpose

This pilot establishes a **single, complete, end-to-end workflow** for one capability:

> **Claude creates Gmail Drafts (not sent) based on user intent**

**Why this pilot**:
- Proves the full flow (Intent → Plan → Execution → Report → Logs)
- Establishes patterns for all future capabilities
- Low risk (OS_SAFE - drafts never sent)
- High value (contextual email drafting)

**After this pilot works**, we can copy this playbook to:
- Gmail Send (with CLOUD_OPS_HIGH safeguards)
- Drive file creation
- Calendar event creation
- Sheets updates
- All other Google capabilities

---

## 1. Use Case Definition

### 1.1 Scope

**What's included**:
- ✅ Create new Gmail drafts in Or's personal inbox
- ✅ Draft based on user intent (context, tone, content requirements)
- ✅ Include threading (if replying to existing email)
- ✅ Support attachments references (will be added manually by Or)
- ✅ Preview draft before creating
- ✅ Log creation for audit trail

**What's excluded** (future phases):
- ❌ Sending emails (requires `gmail.send` + CLOUD_OPS_HIGH)
- ❌ Editing existing drafts (pilot creates new only)
- ❌ Scheduling drafts to send later
- ❌ Bulk draft creation (pilot: one at a time)
- ❌ Cross-account drafts (Or's account only)

### 1.2 Request Sources

**Who can trigger**:
1. **Or directly** → Claude Desktop chat
2. **Architect GPT** → Via structured input to Claude
3. **GPTs GO** → Delegation (per RACI, if contextual drafting needed)

**Request format** (examples):
```
"Draft an email to customer@example.com about project delay"

"Create a response to this email [thread] with apologetic tone"

"Write a draft to the team announcing the new feature launch"

"Draft a follow-up to John about the meeting we had yesterday"
```

### 1.3 RACI Assignment

Per [`GOOGLE_AGENTS_RACI.md`](GOOGLE_AGENTS_RACI.md) Section 1.2:

| Role | Agent | Responsibility |
|------|-------|---------------|
| **R (Responsible)** | Claude Desktop | Contextual, researched, unique drafts |
| **A (Accountable)** | Or | Approves content before creation |
| **C (Consulted)** | GPTs GO | Template-based alternatives (if applicable) |
| **I (Informed)** | CAPABILITIES_MATRIX | Updated after successful pilot |

**Why Claude (not GPTs GO)**:
- Drafts require deep context (email thread, local files, web research)
- Drafts require original authoring (not template-based)
- Fits Claude's strength in contextual, analytical work

---

## 2. Complete Flow: Intent → Plan → Execution → Report → Logs

### 2.1 Intent Phase

**User provides**:
- **What**: Draft request (new email or reply)
- **Who**: Recipient(s)
- **Why**: Context/purpose of email
- **How**: Tone, style, special requirements (optional)

**Example**:
```
User: "Draft an email to sarah@client.com apologizing for the delay 
       in delivering the Q4 report. Mention we'll have it ready by 
       Friday and offer a quick call to discuss. Professional but warm."
```

---

### 2.2 Plan Phase

**Claude executes**:

#### Step 1: Check Capabilities
```
1. Read: CAPABILITIES_MATRIX.md Section 3.1 (Gmail)
2. Find: "Gmail Drafts via MCP" capability
3. Check Status: PILOT_DESIGNED (or VERIFIED after G2.2)
4. Confirm: OS_SAFE (no send)
```

#### Step 2: Check RACI
```
1. Read: GOOGLE_AGENTS_RACI.md Section 1.2
2. Confirm: Claude is Responsible (R) for contextual drafts
3. If template-based: Consider GPTs GO consultation
```

#### Step 3: Gather Context
```
1. Search Gmail: Is this a reply? (thread context)
2. Search Drive: Relevant documents? (e.g., project status)
3. Search Calendar: Recent meetings with recipient?
4. Local files: Any relevant context on Or's computer?
5. Web search: If needed (e.g., company information)
```

#### Step 4: Draft Content
```
1. Compose email based on:
   - User intent
   - Gathered context
   - Appropriate tone/style
   - Professional best practices

2. Include:
   - Clear subject line
   - Greeting
   - Body (structured, clear)
   - Call to action (if applicable)
   - Signature (Or's standard signature)
```

#### Step 5: Present for Review
```
Claude: "I've drafted this email for sarah@client.com:

Subject: Apology for Q4 Report Delay + Next Steps

---

Hi Sarah,

I wanted to reach out personally to apologize for the delay in 
delivering our Q4 report. I know you were expecting it last week, 
and I take full responsibility for the timeline slip.

The good news: we'll have the complete report ready for you by 
this Friday, November 20th. To ensure we're aligned on the 
findings, I'd love to schedule a quick 15-minute call next week 
to walk through the key insights together.

Would Monday or Tuesday afternoon work for you?

Thank you for your patience and understanding.

Best regards,
Or
---

This is an OS_SAFE operation (draft only, not sent).

Options:
1. Create draft as-is
2. Revise (tell me what to change)
3. Cancel

What would you like?"
```

---

### 2.3 Execution Phase (Design for Future G2.2+)

**Prerequisite check**:
```
IF CAPABILITIES_MATRIX shows Status != "VERIFIED":
  Claude: "This capability is designed but not yet operational.
           Current status: PILOT_DESIGNED
           
           To make this work, we need Phase G2.2:
           - Enable Google APIs
           - Configure OAuth (your one-time consent)
           - Update MCP server
           
           For now, I can save the draft text to a local file,
           or we can proceed with G2.2 setup if you're ready."
  
  [Exit or offer alternatives]
```

**If operational** (after G2.2):

#### Step 1: MCP Call Preparation
```python
# Pseudo-code for Claude's internal logic
operation = {
    "tool": "google_workspace_extended",  # MCP server name
    "method": "gmail.create_draft",
    "params": {
        "to": ["sarah@client.com"],
        "subject": "Apology for Q4 Report Delay + Next Steps",
        "body": "[full draft text]",
        "body_type": "html",  # or "plain"
        "thread_id": null,  # if reply, include thread ID
        "in_reply_to": null  # if reply, include message ID
    },
    "required_scope": "gmail.compose",
    "risk_level": "OS_SAFE"
}
```

#### Step 2: Execute via MCP
```
1. MCP Server:
   - Reads: OAuth refresh token (from Secret Manager)
   - Gets: Fresh access token (from Google OAuth)
   - Calls: Gmail API - users.drafts.create
   - Returns: Draft ID + success confirmation

2. Claude receives:
   {
     "draft_id": "r-1234567890",
     "message_id": "m-0987654321",
     "thread_id": "t-1122334455",
     "created_at": "2025-11-17T20:55:00Z"
   }
```

#### Step 3: Error Handling
```
IF error occurs:
  - Rate limit exceeded:
    Claude: "Gmail draft creation rate limit reached (OS_SAFE).
             Wait 10 minutes or upgrade quota."
  
  - Invalid scope:
    Claude: "Missing gmail.compose scope.
             Need to update OAuth configuration (Phase G2.2)."
  
  - Network error:
    Claude: "Temporary connection issue with Gmail API.
             Retry in a moment?"
  
  - Authentication error:
    Claude: "OAuth token expired or invalid.
             Need to refresh credentials (technical issue)."

  [Log error, do not retry automatically]
```

---

### 2.4 Report Phase

**Success response**:
```
Claude: "✅ Draft created successfully

Subject: Apology for Q4 Report Delay + Next Steps
To: sarah@client.com
Status: Draft (not sent)

You can find it in Gmail → Drafts:
- Edit if needed
- Send when ready
- Or discard if plans change

Draft ID: r-1234567890
Created: 2025-11-17 20:55 IST

Logged to: OPS/LOGS/google-operations.jsonl"
```

**Alternative response** (if not operational yet):
```
Claude: "📝 Draft prepared (not created in Gmail yet)

Subject: Apology for Q4 Report Delay + Next Steps
To: sarah@client.com

The draft text has been saved to:
OPS/DRAFTS/gmail-draft-2025-11-17-sarah.md

To create this draft in Gmail, we need Phase G2.2 setup.
Would you like to proceed with OAuth configuration?"
```

---

### 2.5 Logs Phase

**Log entry** (OS_SAFE, minimal):
```json
{
  "timestamp": "2025-11-17T20:55:00Z",
  "operation": "gmail.create_draft",
  "risk_level": "OS_SAFE",
  "status": "success",
  "details": {
    "to": ["sarah@client.com"],
    "subject": "Apology for Q4 Report Delay + Next Steps",
    "body_preview": "Hi Sarah, I wanted to reach out... [50 chars]",
    "draft_id": "r-1234567890",
    "thread_id": null
  },
  "context": {
    "user_request": "Draft apology for report delay",
    "gathered_context": ["email_thread", "calendar_recent_meetings"],
    "claude_session": "session-456"
  },
  "metadata": {
    "pilot": "gmail_drafts_flow",
    "phase": "G2.1-Pilot",
    "logged_at": "2025-11-17T20:55:05Z"
  }
}
```

**Log location**:
- Primary: `OPS/LOGS/google-operations.jsonl` (append-only, committed to repo)
- Optional: Google Sheet (if tracking spreadsheet configured)
- State: Update `STATE_FOR_GPT_SNAPSHOT.md` with latest operation

**What's logged**:
- ✅ Operation metadata (what, when, who)
- ✅ Subject and preview (first 50 chars of body)
- ✅ Draft ID (for tracking)
- ✅ Context used (email thread, documents, etc.)

**What's NOT logged** (privacy):
- ❌ Full email body (too much, privacy concern)
- ❌ Recipient's personal details
- ❌ Attachments content

---

## 3. Risk Boundaries for This Pilot

### 3.1 Why This Pilot is OS_SAFE

**Definition of OS_SAFE**:
> Operations with **no external impact** - nothing leaves Claude's control, nothing affects others

**Gmail Drafts qualify because**:
1. **Not sent**: Drafts remain in Or's Gmail account, unsent
2. **No recipients notified**: No one receives anything
3. **Fully reversible**: Or can delete, edit, or discard
4. **Private**: Only Or can see the draft
5. **No automation**: Draft creation requires Or's explicit approval of content

**Comparison**:
| Operation | Risk Level | Why |
|-----------|-----------|-----|
| Read Gmail | OS_SAFE | No changes to any data |
| Create Draft | OS_SAFE | No external impact (not sent) |
| Send Email | CLOUD_OPS_HIGH | External impact (recipient receives) |
| Share Drive File | CLOUD_OPS_HIGH | External impact (others gain access) |

### 3.2 Scope Limitations

**This pilot uses ONLY**:
- `gmail.readonly` (already available) - to read threads for context
- `gmail.compose` (after G2.2) - to create drafts

**This pilot does NOT use**:
- ❌ `gmail.send` - sending emails (requires CLOUD_OPS_HIGH approval)
- ❌ `gmail.modify` - changing labels or categories
- ❌ `gmail.settings` - modifying Gmail settings

**Technical safeguard**:
- MCP server will block any attempt to call `gmail.send` without approval
- Even if prompt injection tries to send, policy block prevents it

### 3.3 OAuth/Secrets Note

**Current state** (Phase G2.1-Pilot):
- OAuth configuration: Not done yet (design only)
- Secrets: Not created yet (design only)
- MCP server: Not configured yet (design only)

**This pilot document**:
- ✅ Designs the flow
- ✅ Documents expectations
- ✅ Prepares CAPABILITIES_MATRIX
- ❌ Does NOT execute OAuth setup
- ❌ Does NOT touch secrets
- ❌ Does NOT modify MCP config

**OAuth/Secrets live in Phase G2.2** (future):
- Executor runs workflows
- Or clicks OAuth consent once
- Tokens stored in Secret Manager
- MCP server configured
- Then this pilot becomes operational

---

## 4. Connection to RACI & G2.1 Architecture

### 4.1 RACI Integration

**From [`GOOGLE_AGENTS_RACI.md`](GOOGLE_AGENTS_RACI.md) Section 1.2**:

| Use Case | Claude | GPTs GO | Or | Details |
|----------|--------|---------|----|----- ---|
| Contextual reply draft | **R** | C | A | Claude handles research-backed, contextual drafts |
| Multi-draft generation | **R** | C | A | Claude creates multiple options for Or to choose |
| Template-based reply | C | **R** | A | GPTs GO better for standardized templates |

**This pilot follows RACI**:
- Claude is Responsible (R) for execution
- Or is Accountable (A) for content approval
- GPTs GO are Consulted (C) if template alternative exists
- CAPABILITIES_MATRIX is Informed (I) after completion

**Handoff scenario**:
```
If user asks: "Send 100 similar emails to list"
→ Claude checks RACI
→ Bulk operation = GPTs GO territory
→ Claude: "This is a bulk operation (100 emails).
           Per RACI, GPTs GO is better suited for this.
           Would you like me to hand this off?"
```

### 4.2 G2.1 Architecture Integration

**From [`GOOGLE_MCP_OAUTH_ARCH.md`](GOOGLE_MCP_OAUTH_ARCH.md)**:

**Authentication flow** (once G2.2 executes):
```
Claude → MCP Server → OAuth Refresh Token (from Secret Manager)
                   → Google OAuth (get fresh access token)
                   → Gmail API (create draft)
                   → Return draft ID
```

**This pilot assumes**:
- OAuth Client created (G2.2 workflow)
- Refresh token stored in Secret Manager (G2.2 workflow)
- MCP server configured with credentials (G2.2 workflow)
- `gmail.compose` scope granted (Or's one-time consent)

**Workflow used** (from G2.1):
- `google-mcp-enable-apis.yml` - enables Gmail API
- `google-mcp-create-oauth-client.yml` - creates OAuth client
- `google-mcp-complete-oauth.yml` - exchanges code for tokens
- MCP config updated by Executor

**This pilot is the first consumer** of that architecture.

### 4.3 Safeguards from G2.1

**This pilot implements** (from [`GOOGLE_MCP_OAUTH_ARCH.md`](GOOGLE_MCP_OAUTH_ARCH.md) Section E):

**Layer 1: Capability Tracking**
- ✅ CAPABILITIES_MATRIX entry created
- ✅ Safeguards documented
- ✅ Status tracked (PILOT_DESIGNED → VERIFIED)

**Layer 2: Approval Templates**
- ✅ Or approves content before creation
- ✅ Clear prompt showing full draft
- ✅ Options to revise/cancel

**Layer 3: Rate Limiting**
- Not needed (OS_SAFE operation, no abuse potential)
- Future: If implemented, limit = 50 drafts/hour

**Layer 4: Mandatory Logging**
- ✅ Every draft creation logged
- ✅ Log includes metadata, not full content
- ✅ Committed to repo (audit trail)

**Layer 5: Policy Blocks**
- ✅ Cannot call `gmail.send` from draft flow
- ✅ MCP server enforces scope boundaries
- ✅ Even prompt injection can't bypass

---

## 5. CAPABILITIES_MATRIX Entry

**Section**: 3.1 Gmail

**New row**:
```markdown
| Claude MCP | Gmail API | Create drafts | 🔄 PILOT_DESIGNED | Create new email drafts (not sent) | Safeguards: (1) Content approval required (2) OS_SAFE - no send (3) Logging enabled (4) Scope: gmail.compose only (5) Cannot call gmail.send | Phase: G2.1-Pilot |
```

**Full entry details**:
- **From**: Claude MCP
- **To**: Gmail API
- **Capability**: Create drafts
- **Status**: 🔄 PILOT_DESIGNED (after G2.2 execution: ✅ VERIFIED)
- **Details**: Create new email drafts based on context (not sent)
- **Safeguards**:
  1. Content approval required (Or reviews before creation)
  2. OS_SAFE - drafts not sent, no external impact
  3. Logging enabled (OPS/LOGS/google-operations.jsonl)
  4. Scope: `gmail.compose` only (cannot send)
  5. Policy block: Cannot call `gmail.send` even if prompted
- **Last Verified**: Pending G2.2 execution
- **Reference**: [`PILOT_GMAIL_DRAFTS_FLOW.md`](PILOT_GMAIL_DRAFTS_FLOW.md)

**Phase tracking**:
- G2.1-Pilot: PILOT_DESIGNED (design complete)
- G2.2: Execute OAuth setup
- G2.3: Test and verify → Status becomes VERIFIED

---

## 6. Pilot as Template for Future Capabilities

### 6.1 What Stays the Same

**Universal structure** (copy to all capabilities):

1. **Intent Phase**:
   - User provides: What, Who, Why, How
   - Claude confirms understanding

2. **Plan Phase**:
   - Check CAPABILITIES_MATRIX (status, safeguards)
   - Check RACI (who's responsible)
   - Gather context (email/Drive/Calendar/local/web)
   - Prepare operation
   - Present for review

3. **Execution Phase**:
   - Prerequisite check (is capability operational?)
   - MCP call preparation
   - Execute via MCP
   - Error handling

4. **Report Phase**:
   - Success: Clear confirmation + IDs/links
   - Failure: Clear error + suggested next steps

5. **Logs Phase**:
   - JSON entry to OPS/LOGS/
   - Update STATE_FOR_GPT_SNAPSHOT.md
   - Commit to repo

### 6.2 What Changes Per Capability

**Variables by capability**:

| Capability | Operation | Scope | Risk Level | Safeguards | Rate Limit |
|-----------|-----------|-------|-----------|------------|-----------|
| **Gmail Drafts** | `gmail.create_draft` | `gmail.compose` | OS_SAFE | Approval, no send, logging | 50/hour (optional) |
| **Gmail Send** | `gmail.send` | `gmail.send` | CLOUD_OPS_HIGH | Approval ("מאשר שליחה"), rate (10/h), logging, TTL (60m), no forwarding | 10/hour |
| **Drive Create** | `drive.files.create` | `drive.file` | OS_SAFE | Create in Claude folder only | 100/hour |
| **Drive Share** | `drive.permissions.create` | `drive` | CLOUD_OPS_HIGH | Approval, rate (3/day), logging, no public write | 3/day |
| **Calendar Create** | `calendar.events.create` | `calendar.events` | OS_SAFE (personal) or CLOUD_OPS_MEDIUM (with invites) | Approval if invites, logging | 10/hour |
| **Sheets Update** | `sheets.spreadsheets.values.update` | `spreadsheets` | OS_SAFE (new file) or CLOUD_OPS_MEDIUM (shared) | Version history, logging | 50/hour |

**Template format** (copy and customize):
```markdown
# Pilot: [Capability Name] Flow

## 1. Use Case Definition
- Scope: [what's included/excluded]
- Request sources: [who can trigger]
- RACI: [who's responsible]

## 2. Complete Flow
- Intent: [user request format]
- Plan: [5 steps - same structure]
- Execution: [MCP call, error handling]
- Report: [success/failure responses]
- Logs: [what's logged, where]

## 3. Risk Boundaries
- Why [OS_SAFE / CLOUD_OPS_MEDIUM / CLOUD_OPS_HIGH]
- Scope limitations
- What this pilot does NOT do

## 4. Connection to RACI & Architecture
- RACI integration
- Authentication flow
- Safeguards applied

## 5. CAPABILITIES_MATRIX Entry
- [Full row with all details]

## 6. Testing Plan (after G2.2)
- [How to verify capability works]
```

### 6.3 Copy Checklist

**To create a new capability pilot** (from Gmail Drafts template):

1. [ ] Copy `PILOT_GMAIL_DRAFTS_FLOW.md` → `PILOT_[CAPABILITY]_FLOW.md`
2. [ ] Update Section 1: Use Case (scope, RACI)
3. [ ] Update Section 2.3: Execution (operation, scope, params)
4. [ ] Update Section 3: Risk level + safeguards
5. [ ] Update Section 5: CAPABILITIES_MATRIX row
6. [ ] Add to CAPABILITIES_MATRIX (new row)
7. [ ] Update MCP_GPT_CAPABILITIES_BRIDGE (reference new pilot)
8. [ ] Test after G2.2 (verify works as designed)

**Example**: Gmail Send
```bash
# 1. Copy file
cp PILOT_GMAIL_DRAFTS_FLOW.md PILOT_GMAIL_SEND_FLOW.md

# 2. Edit:
- Section 1: Scope = send emails (with approval)
- Section 2.3: operation = gmail.send, scope = gmail.send
- Section 3: Risk = CLOUD_OPS_HIGH
- Section 5: Add 5 safeguards (approval, rate, logging, TTL, no forwarding)

# 3. Update MATRIX:
- Add row: Gmail Send capability with all safeguards
```

---

## 7. Next Steps

### 7.1 Current State (G2.1-Pilot Complete)

**What we have now**:
- ✅ Complete flow documented (this file)
- ✅ RACI integration confirmed
- ✅ G2.1 architecture referenced
- ✅ Safeguards defined
- ✅ Logging plan ready
- ✅ Template for future capabilities

**What we don't have yet**:
- ❌ OAuth client configured
- ❌ MCP server updated
- ❌ Capability operational

**Status**: PILOT_DESIGNED

### 7.2 Path to Operational (G2.2)

**Prerequisites**:
- [ ] Or approves this pilot design
- [ ] Executor identified and authorized
- [ ] Or ready for one-time OAuth consent

**Execution tasks** (CLOUD_OPS_HIGH):
1. Run `google-mcp-enable-apis.yml` (enable Gmail API)
2. Run `google-mcp-create-oauth-client.yml` (create OAuth client with `gmail.compose` scope)
3. Or clicks consent URL (approves `gmail.compose` access)
4. Run `google-mcp-complete-oauth.yml` (exchange code for tokens)
5. Executor updates Claude Desktop config (MCP server credentials)
6. Claude restarts, reads OPS/STATUS/google-mcp-ready.json
7. Claude tests: Create a test draft
8. Claude updates CAPABILITIES_MATRIX: Status → VERIFIED
9. Pilot becomes operational ✅

**Estimated time**: 30-60 minutes

### 7.3 Testing Plan (After G2.2)

**Test cases**:

1. **Basic draft**:
   - Request: "Draft email to test@example.com with subject 'Test Draft'"
   - Expected: Draft created, visible in Gmail
   - Verify: Draft ID returned, logged to OPS/LOGS/

2. **Contextual draft**:
   - Request: "Draft reply to latest email from [person]"
   - Expected: Claude reads thread, creates contextual reply
   - Verify: Thread ID correct, draft appears in thread

3. **Multi-draft**:
   - Request: "Create 3 draft options for email to customer about delay"
   - Expected: 3 separate drafts created
   - Verify: All 3 logged, Or can choose best one

4. **Error handling**:
   - Test: Invalid recipient email
   - Expected: Clear error message, no draft created
   - Test: Network interruption
   - Expected: Retry prompt or graceful failure

5. **Rate limit** (if implemented):
   - Test: Create 51 drafts in 1 hour
   - Expected: 50 succeed, 51st blocked with clear message

**Success criteria**:
- [ ] All test cases pass
- [ ] Drafts appear in Gmail correctly
- [ ] Logging works (all operations in OPS/LOGS/)
- [ ] No send operations occur (safety check)
- [ ] Or can edit/send/discard drafts normally

---

## 8. Summary

**This pilot establishes**:
- ✅ Complete end-to-end flow for one capability
- ✅ Integration with RACI (Claude responsible)
- ✅ Integration with G2.1 architecture (OAuth + WIF + Secrets)
- ✅ Safeguards implementation (5 layers)
- ✅ Logging and audit trail
- ✅ Template for all future capabilities

**Risk**: OS_SAFE (drafts not sent, no external impact)

**Status**: PILOT_DESIGNED (ready for G2.2 execution)

**Next**: Or approves → G2.2 execution → Test → Operational

**Then**: Copy this template to Gmail Send, Drive, Calendar, Sheets, etc.

---

**Maintained by**: Claude  
**Created**: 2025-11-17  
**Phase**: G2.1-Pilot  
**Status**: PILOT_DESIGNED  
**Reference**: [`GOOGLE_MCP_OAUTH_ARCH.md`](GOOGLE_MCP_OAUTH_ARCH.md), [`GOOGLE_AGENTS_RACI.md`](GOOGLE_AGENTS_RACI.md)
