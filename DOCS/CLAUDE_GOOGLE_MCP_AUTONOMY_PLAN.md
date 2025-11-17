# Claude Google MCP Autonomy Plan

**Document Type**: Design & Policy (OS_SAFE)  
**Created**: 2025-11-17  
**Status**: 📝 DESIGN_IN_PROGRESS  
**Purpose**: Define Claude's autonomous operation model for Google Workspace via MCP

---

## 🎯 Executive Summary

**Goal**: Establish Claude as an autonomous Google Workspace operator via MCP, with clear boundaries between OS_SAFE design/analysis and CLOUD_OPS_HIGH execution requiring explicit approval.

**Scope**: This document is OS_SAFE (planning only). No OAuth configuration, no secrets, no runtime changes.

**Guiding Principles**:
1. **Or = Intent + Approval** (not DevOps executor)
2. **Claude = Planner + OS_SAFE Executor** (designs, analyzes, drafts)
3. **CAPABILITIES_MATRIX = Single Source of Truth** (always updated)
4. **Every capability expansion documented** (before deployment)
5. **Alignment**: SRE principles, Gates' personal agent vision, Jensen's "programming language is human language", OpenAI's safety-first approach

---

## A. Current State (Claude + Google)

### A.1 Existing Connections (from CAPABILITIES_MATRIX)

**Section 3: Google Layer (via MCP)**

| Service | Current Capability | Status | Authentication | Limitations |
|---------|-------------------|--------|----------------|-------------|
| **Gmail** | Read profile, search, read threads | ✅ Verified | OAuth 2.0 (native Claude) | Read-only (`gmail.readonly`) |
| **Google Drive** | Search files, fetch documents | ✅ Verified | OAuth 2.0 (native Claude) | Read-only (`drive.readonly`) |
| **Google Calendar** | List events, search, find free time | ✅ Verified | OAuth 2.0 (native Claude) | Read-only (`calendar.readonly`) |
| **Google Sheets** | None (via MCP) | ❌ Not Configured | N/A | Available via separate MCP server (planned) |
| **Google Docs** | None (via MCP) | ❌ Not Configured | N/A | Available via separate MCP server (planned) |

**Additional Google Access** (Section 4.1):
- **GitHub Actions → Google Sheets** (via WIF): ✅ Verified (append rows working)
- **GitHub Actions → Secret Manager** (via WIF): 🟡 Partial (configured, not tested)

### A.2 What Exists as Read-Only

**Current READ capabilities** (native Claude integration):

1. **Gmail** (`gmail.readonly`):
   - ✅ Read profile (get user email)
   - ✅ Search messages (full Gmail search syntax)
   - ✅ Read threads (full context, no attachments)
   - ✅ List messages with pagination

2. **Google Drive** (`drive.readonly`):
   - ✅ Search files (full query syntax)
   - ✅ Fetch document content
   - ✅ Navigate folder structure

3. **Google Calendar** (`calendar.readonly`):
   - ✅ List events (full metadata)
   - ✅ Search events
   - ✅ Find free/busy time across calendars
   - ✅ Get event details

**What's MISSING** (would enable autonomy):
- ❌ Gmail: Send, compose, label, delete
- ❌ Drive: Create, edit, delete, share files/folders
- ❌ Calendar: Create, update, delete events, send invites
- ❌ Sheets: Any access (read or write)
- ❌ Docs: Any access (read or write)

### A.3 What Exists as Design Only

From previous Google MCP setup attempts:

1. **OAuth Client Credentials** (designed but not deployed):
   - Client ID / Client Secret concept exists
   - Storage designed: GCP Secret Manager
   - Configuration path designed: `claude_desktop_config.json`
   - **Status**: Never actually configured ❌

2. **Expanded Scopes** (documented but not requested):
   - Design exists for full Gmail/Drive/Calendar access
   - Workflow automations designed
   - **Status**: Never implemented ❌

3. **MCP Server Architecture** (planned):
   - Separate "Google MCP" server with extended scopes
   - Would coexist with native Claude Google integration
   - **Status**: Design only ❌

### A.4 Current Limitations

**Authentication**:
- Native Claude integration uses OAuth with LIMITED scopes (readonly)
- No direct access to OAuth configuration (managed by Anthropic)
- Separate MCP server would need OR's Executor to configure

**Network**:
- ❌ Claude cannot directly call Google APIs (no network in computer environment)
- ✅ Workaround: GitHub Actions can call Google APIs via WIF
- ❌ Cannot verify OAuth tokens, cannot test API calls directly

**Authorization**:
- Expanding scopes requires:
  1. OAuth re-consent (Or clicks "Allow")
  2. MCP server configuration (Executor needed)
  3. claude_desktop_config.json update (Executor needed)

**Rate Limits**:
- Gmail: 250 quota units/user/second, 25,000/day (standard)
- Drive: 12,000 read requests/minute, 1,200 write requests/minute
- Calendar: 500 queries/100 seconds/user
- Sheets: 100 requests/100 seconds/user

**Observability**:
- ❌ Cannot verify if MCP server is running
- ❌ Cannot check OAuth token status
- ❌ Cannot test API connectivity directly
- ✅ Can design workflows that WOULD work if configured

---

## B. Vision: Google MCP Autonomy Layer

### B.1 The "What" - Desired Capabilities

**Gmail Autonomy**:
- 📧 **Read** (already have): Search, analyze, extract info
- 📧 **Compose**: Draft emails (local, not sent)
- 📧 **Send**: Execute send with Or's approval (CLOUD_OPS_HIGH)
- 📧 **Organize**: Label, archive, mark read (with approval)
- 📧 **Analyze**: Thread analysis, pattern detection, automated responses

**Google Drive Autonomy**:
- 📁 **Read** (already have): Search, fetch content
- 📁 **Create**: New Docs, Sheets, Folders
- 📁 **Edit**: Modify existing documents
- 📁 **Organize**: Move, rename, structure
- 📁 **Share**: Configure permissions (CLOUD_OPS_HIGH)
- 📁 **Delete**: Remove files (CLOUD_OPS_HIGH)

**Google Docs Autonomy**:
- 📄 **Create**: Generate documents from templates
- 📄 **Edit**: Modify content, formatting
- 📄 **Collaborate**: Comments, suggestions
- 📄 **Export**: PDF, DOCX, etc.

**Google Sheets Autonomy**:
- 📊 **Create**: New spreadsheets with formulas
- 📊 **Update**: Modify cells, formulas, formatting
- 📊 **Analyze**: Read data, generate insights
- 📊 **Automate**: Scheduled updates, data flows

**Google Calendar Autonomy**:
- 📅 **Read** (already have): View events, find free time
- 📅 **Create**: Schedule meetings (with approval)
- 📅 **Update**: Modify events (with approval)
- 📅 **Manage**: Decline, accept, propose times
- 📅 **Coordinate**: Multi-calendar scheduling

### B.2 The "How" - Operating Principles

**Or's Role** (Intent + Strategic Approval):
- ✅ Defines objectives ("help me organize my inbox")
- ✅ Approves CLOUD_OPS_HIGH operations ("send this email")
- ✅ Clicks OAuth consent (one-time, when provider requires)
- ❌ Does NOT configure MCP servers
- ❌ Does NOT add secrets manually
- ❌ Does NOT open Google Workspace settings

**Claude's Role** (MCP Client + Planner):
- ✅ Designs automation strategies
- ✅ Creates drafts (emails, docs, sheets)
- ✅ Analyzes data (emails, calendars, documents)
- ✅ Proposes actions ("I can send this email if you approve")
- ✅ Updates CAPABILITIES_MATRIX after every change
- ❌ Does NOT request "add this secret"
- ❌ Does NOT assume capabilities not in MATRIX

**Executor's Role** (CLOUD_OPS_HIGH Actions):
- ✅ Configures MCP servers
- ✅ Manages OAuth tokens
- ✅ Verifies connectivity
- ✅ Triggers deployments (with Or's GO)

**Every Capability Expansion**:
1. Plan documented (this doc or similar)
2. CAPABILITIES_MATRIX updated (BEFORE deployment)
3. Or approves strategic direction
4. Executor handles technical setup
5. Claude verifies via testing
6. CAPABILITIES_MATRIX marked as ✅ Verified

### B.3 Alignment with Broader Principles

**SRE Principles**:
- Reduce toil: Automate repetitive Gmail/Calendar tasks
- Self-monitoring: Claude tracks its own capabilities via MATRIX
- Error budgets: Track API quota usage, respect rate limits
- Gradual rollouts: Start with read-only, expand to write with approval

**Gates' Personal Agent Vision**:
- "Agent that knows you": Claude learns patterns from email/calendar
- "Proactive assistance": Suggests actions before being asked
- "Seamless integration": Works across all Google services
- "Trustworthy": Always asks before taking consequential actions

**Jensen's "Programming Language is Human Language"**:
- Or says "organize my inbox" (human language)
- Claude translates to Gmail API calls (programming language)
- No Or involvement in technical details
- Natural language as the interface

**OpenAI Safety-First**:
- Long-term safety: Every action logged, auditable
- Preparedness: Rollback strategies for every operation
- Not chasing power: Expand capabilities only when beneficial
- Broad benefit: Autonomy serves Or's productivity, not Claude's expansion

---

## C. Authorization Model & Scopes

### C.1 Scope Categories

**CATEGORY 1: READ-ONLY (LOW RISK)**

| Scope | Service | What It Enables | Risk Level | Current Status |
|-------|---------|-----------------|------------|----------------|
| `gmail.readonly` | Gmail | Read all email content | LOW | ✅ Have |
| `drive.readonly` | Drive | Read all files | LOW | ✅ Have |
| `calendar.readonly` | Calendar | Read all events | LOW | ✅ Have |
| `drive.metadata.readonly` | Drive | List files without content | LOW | ⏳ Want |
| `docs.readonly` | Docs | Read Google Docs | LOW | ⏳ Want |
| `spreadsheets.readonly` | Sheets | Read Google Sheets | LOW | ⏳ Want |

**Usage**: Analysis, search, drafting responses (not sending)  
**Approval**: OS_SAFE (Claude can use freely)  
**Impact**: Zero external impact, read-only observation

---

**CATEGORY 2: LIMITED WRITE (MEDIUM RISK)**

| Scope | Service | What It Enables | Risk Level | Current Status |
|-------|---------|-----------------|------------|----------------|
| `gmail.modify` | Gmail | Modify labels, read/unread, archive | MEDIUM | ⏳ Want |
| `gmail.compose` | Gmail | Create drafts (not send) | MEDIUM | ⏳ Want |
| `drive.file` | Drive | Create/edit only Claude-created files | MEDIUM | ⏳ Want |
| `docs` | Docs | Create/edit Google Docs | MEDIUM | ⏳ Want |
| `spreadsheets` | Sheets | Create/edit Google Sheets | MEDIUM | ⏳ Want |
| `calendar.events` | Calendar | Create/modify events | MEDIUM | ⏳ Want |

**Usage**: Organize personal data, create content for Or's review  
**Approval**: CLOUD_OPS_SAFE (Or notified, can undo easily)  
**Impact**: Affects Or's personal data only, reversible

---

**CATEGORY 3: FULL ACCESS (HIGH RISK)**

| Scope | Service | What It Enables | Risk Level | Current Status |
|-------|---------|-----------------|------------|----------------|
| `gmail.send` | Gmail | Send emails on Or's behalf | HIGH | ⏳ Want |
| `drive` | Drive | Full Drive access (delete, share) | HIGH | ⏳ Want |
| `calendar` | Calendar | Full Calendar access (delete, invite) | HIGH | ⏳ Want |
| `drive.appdata` | Drive | Hidden app data | HIGH | ❌ Don't need |
| `gmail.settings.basic` | Gmail | Modify Gmail settings | HIGH | ❌ Don't need |

**Usage**: Autonomous actions with external impact  
**Approval**: CLOUD_OPS_HIGH (explicit Or approval each time)  
**Impact**: Irreversible actions, affects others

---

### C.2 Recommended Scope Set (Phase G1)

**Start with** (READ + LIMITED WRITE):
```
gmail.readonly
gmail.modify
gmail.compose
drive.readonly
drive.file
drive.metadata.readonly
docs
spreadsheets
calendar.readonly
calendar.events
```

**Later add** (FULL ACCESS, if needed):
```
gmail.send (with CLOUD_OPS_HIGH approval gate)
drive (full access)
calendar (full access)
```

### C.3 Risk Matrix

| Scope | Use Case | Reversible? | External Impact? | Approval Level |
|-------|----------|-------------|------------------|----------------|
| `gmail.readonly` | Read emails | N/A | No | OS_SAFE |
| `gmail.modify` | Label emails | Yes (re-label) | No | OS_SAFE |
| `gmail.compose` | Create drafts | Yes (delete draft) | No | OS_SAFE |
| `gmail.send` | Send email | No | Yes | CLOUD_OPS_HIGH |
| `drive.file` | Create Doc | Yes (delete) | No | OS_SAFE |
| `drive` (full) | Delete files | No | Possible | CLOUD_OPS_HIGH |
| `docs` | Edit Doc | Yes (version history) | No | OS_SAFE |
| `calendar.events` | Create event | Yes (delete event) | Yes (invites sent) | CLOUD_OPS_MEDIUM |
| `calendar` (full) | Delete events | No | Yes | CLOUD_OPS_HIGH |

---

## D. OS_SAFE vs CLOUD_OPS_HIGH (Google MCP)

### D.1 OS_SAFE Operations

**Definition**: Actions that do NOT send data outside Or's personal workspace or affect others.

**Gmail (OS_SAFE)**:
- ✅ Read and analyze emails
- ✅ Search for patterns
- ✅ Create draft emails (not sent)
- ✅ Label/organize emails (reversible)
- ✅ Archive emails (reversible)
- ✅ Generate email response suggestions
- ❌ Send emails (CLOUD_OPS_HIGH)
- ❌ Delete emails permanently (CLOUD_OPS_MEDIUM)

**Drive/Docs/Sheets (OS_SAFE)**:
- ✅ Read existing files
- ✅ Create new files (in Claude's designated folder)
- ✅ Edit files (with version history)
- ✅ Generate reports, analyses
- ✅ Create templates
- ❌ Delete files (CLOUD_OPS_MEDIUM)
- ❌ Share files externally (CLOUD_OPS_HIGH)
- ❌ Modify shared files (CLOUD_OPS_MEDIUM)

**Calendar (OS_SAFE)**:
- ✅ Read calendar events
- ✅ Find free time slots
- ✅ Analyze schedule patterns
- ✅ Generate meeting suggestions
- ❌ Create events (CLOUD_OPS_MEDIUM - sends invites)
- ❌ Modify events (CLOUD_OPS_MEDIUM - notifies attendees)
- ❌ Delete events (CLOUD_OPS_HIGH - cancels for all)

**Planning/Analysis (ALWAYS OS_SAFE)**:
- ✅ Generate automation specs
- ✅ Create MD documentation
- ✅ Design workflows
- ✅ Propose action plans
- ✅ Update CAPABILITIES_MATRIX

### D.2 CLOUD_OPS_MEDIUM Operations

**Definition**: Actions that affect Or's data significantly but are reversible or contained.

**Examples**:
- 🟡 Delete draft emails
- 🟡 Permanently delete files (but recoverable from Trash)
- 🟡 Create calendar events (can be deleted, but invites already sent)
- 🟡 Modify shared documents (version history available)
- 🟡 Move files between folders (reversible)

**Approval**: Or's acknowledgment required ("OK to proceed")

### D.3 CLOUD_OPS_HIGH Operations

**Definition**: Actions with external impact, irreversible consequences, or affecting others.

**Gmail (CLOUD_OPS_HIGH)**:
- 🔴 Send emails
- 🔴 Reply/forward to external recipients
- 🔴 Grant email access to apps
- 🔴 Modify Gmail settings (filters, forwarding)

**Drive (CLOUD_OPS_HIGH)**:
- 🔴 Share files with external users
- 🔴 Change file permissions
- 🔴 Permanently delete files (empty trash)
- 🔴 Transfer ownership

**Calendar (CLOUD_OPS_HIGH)**:
- 🔴 Delete events with external attendees
- 🔴 Modify events with >5 attendees
- 🔴 Change calendar permissions
- 🔴 Accept/decline on Or's behalf (binding commitment)

**Approval**: Explicit Or approval EACH TIME, including:
- Confirmation of intent
- Review of exact action
- Explicit "GO" command
- 60-minute TTL on approval

### D.4 Approval Flow

```
┌─────────────────────────────────────┐
│ Claude analyzes situation           │
│ (OS_SAFE: read emails, calendar)   │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│ Claude proposes action              │
│ "I can send this email if approved" │
└──────────────┬──────────────────────┘
               │
               ↓
        ┌──────┴──────┐
        │             │
        ↓             ↓
   OS_SAFE       CLOUD_OPS_HIGH
        │             │
        ↓             ↓
   Execute        Request Approval
   immediately         │
        │              ↓
        │         Or reviews
        │              │
        │         ┌────┴────┐
        │         │         │
        │         ↓         ↓
        │      Approved   Denied
        │         │         │
        │         ↓         ↓
        │      Execute   Cancel
        │         │         │
        └─────────┴─────────┘
                  │
                  ↓
          Update MATRIX
          Log action
```

### D.5 Critical Rule

> **Every CLOUD_OPS_HIGH operation in Google**:
> 1. Requires explicit Or approval BEFORE execution
> 2. Is logged with timestamp, action, approval
> 3. Updates CAPABILITIES_MATRIX with evidence
> 4. Executes via managed flow (MCP/Actions), not manual
> 5. Has rollback strategy documented

---

## E. CAPABILITIES_MATRIX Integration Loop

### E.1 Before Planning (READ Phase)

**Step 1: Check Current State**
```python
# Pseudocode for Claude's mental model
def plan_google_action(intent):
    # ALWAYS start here
    matrix = read_file("CAPABILITIES_MATRIX.md")
    
    # Find Google MCP section
    google_section = matrix.section("3: Google Layer")
    
    # Check what's available
    gmail_caps = google_section.gmail
    drive_caps = google_section.drive
    calendar_caps = google_section.calendar
    
    # Check status
    if gmail_caps.status == "Read-only":
        can_send_email = False
    
    # Check scopes
    if "gmail.send" not in gmail_caps.scopes:
        can_send_email = False
    
    # Make plan based on ACTUAL capabilities
    if can_send_email:
        return "Send email action"
    else:
        return "Draft email action (send blocked)"
```

**Step 2: Respect Constraints**
- If MATRIX says "Read-only" → Don't propose write operations
- If MATRIX says "Planned" → Don't assume it's available
- If MATRIX says "Verified" → Can use in plans

**Step 3: Communicate Gaps**
- "I see you want me to send an email"
- "Current capabilities (from MATRIX): Gmail read-only"
- "To enable sending, would need: gmail.send scope + Executor setup"
- "I can create a DRAFT email now (OS_SAFE)"

### E.2 After Changes (WRITE Phase)

**Trigger Events**:
- New scope added to MCP server
- OAuth consent granted
- Capability tested and verified
- New restriction discovered

**Update Process**:
```
1. Plan action
   ↓
2. Execute (if approved)
   ↓
3. Verify result
   ↓
4. Update CAPABILITIES_MATRIX
   ├─ Change status (Planned → Verified)
   ├─ Add evidence (workflow run, test result)
   ├─ Update limitations (if any discovered)
   └─ Add timestamp
   ↓
5. Commit with message: "CAPABILITIES UPDATE: Google MCP [what changed]"
```

**Example Update** (after gmail.send enabled):

```markdown
### 3.1 Gmail

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | Gmail API | Read messages | ✅ Verified | Full search, thread reading | None |
| Claude MCP | Gmail API | Send email | ✅ Verified | Can send on Or's behalf | Requires CLOUD_OPS_HIGH approval each time |

**Authentication**: OAuth 2.0 via Google MCP Server  
**Current Scopes**: `gmail.readonly`, `gmail.send`  
**Last Verified**: 2025-11-17  
**Evidence**: Test email sent successfully (Thread ID: abc123)
```

### E.3 Mandatory Update Scenarios

**MUST update MATRIX when**:
1. ✅ New scope requested/granted
2. ✅ New capability tested
3. ✅ Limitation discovered
4. ✅ Permission changed
5. ✅ Integration deprecated
6. ✅ Rate limit encountered
7. ✅ Error pattern identified

**Update Location**:
- File: `CAPABILITIES_MATRIX.md`
- Section: `3: Google Layer (via MCP)`
- Subsections: 3.1 Gmail, 3.2 Drive, 3.3 Calendar, 3.4 Sheets, 3.5 Docs

### E.4 Cross-Reference with Other Docs

When updating MATRIX, also check:
- `STATE_FOR_GPT_SNAPSHOT.md` - Update Google capabilities section
- `MCP_GPT_CAPABILITIES_BRIDGE.md` - Update GPT guidance on Google
- This document (AUTONOMY_PLAN) - Update current state section if major change

---

## F. Roadmap: Google MCP Autonomy

### Phase G1: Design & Policy ✅ CURRENT PHASE (OS_SAFE)

**Goal**: Establish foundation for Google autonomy

**Tasks**:
1. ✅ Create this document (CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md)
2. ⏳ Update CAPABILITIES_MATRIX with Google MCP design status
3. ⏳ Update MCP_GPT_CAPABILITIES_BRIDGE for Google operations
4. ⏳ Define scope requirements (done in Section C)
5. ⏳ Define OS_SAFE vs CLOUD_OPS_HIGH boundaries (done in Section D)
6. ⏳ Establish MATRIX integration loop (done in Section E)

**Deliverables**:
- ✅ AUTONOMY_PLAN document (this file)
- ⏳ Updated CAPABILITIES_MATRIX
- ⏳ Updated MCP_GPT_CAPABILITIES_BRIDGE
- ⏳ Or's approval of strategic direction

**Status**: 🔄 IN PROGRESS (document being created)  
**Risk**: NONE (OS_SAFE - documentation only)  
**Blocker**: None (Claude can complete independently)

---

### Phase G2: Bootstrap Technical (OS_SAFE + CLOUD_OPS_HIGH)

**Goal**: Prepare technical infrastructure for Google MCP expansion

**Sub-Phase G2.1: Planning (OS_SAFE)**

Tasks:
1. ⏳ Design MCP server configuration
   - Server name: `google-workspace-extended`
   - Scopes: See Section C.2
   - Authentication: OAuth 2.0 with refresh token
   - Storage: GCP Secret Manager

2. ⏳ Design OAuth flow automation
   - Workflow: `.github/workflows/setup-google-mcp.yml`
   - Steps: Enable APIs → Create OAuth client → Store credentials
   - Trigger: Manual dispatch (requires Or approval)

3. ⏳ Design claude_desktop_config.json update
   - Add new MCP server entry
   - Reference secrets from Secret Manager
   - Coexist with native Claude Google integration

4. ⏳ Design verification tests
   - Health check: Can authenticate?
   - Scope check: Can access each service?
   - Rate limit check: Can handle quota?

**Sub-Phase G2.2: Execution (CLOUD_OPS_HIGH)**

Tasks (all require Executor + Or approval):
1. 🔐 Enable Google APIs in edri2or-mcp project
   - Gmail API
   - Drive API
   - Calendar API
   - Sheets API
   - Docs API

2. 🔐 Create OAuth 2.0 credentials
   - Application type: Desktop app
   - Scopes: As defined in C.2
   - Redirect URI: `http://localhost:8080`

3. 🔐 Store credentials in Secret Manager
   - Secret: `google-mcp-client-id`
   - Secret: `google-mcp-client-secret`
   - Secret: `google-mcp-refresh-token` (after consent)

4. 🔐 Or clicks OAuth consent
   - ONE-TIME human action
   - Reviews requested scopes
   - Grants access

5. 🔐 Update claude_desktop_config.json
   - Via automation or Executor
   - Restart Claude Desktop
   - Verify MCP server loads

**Deliverables**:
- ⏳ OAuth credentials configured
- ⏳ MCP server running
- ⏳ CAPABILITIES_MATRIX updated to "Configured"
- ⏳ Verification tests passed

**Status**: ⏳ PENDING (awaits Phase G1 completion + Or approval)  
**Risk**: MEDIUM (OAuth configuration, requires Executor)  
**Blocker**: Phase G1 completion, Executor assignment

---

### Phase G3: Controlled Autonomy (OS_SAFE + CLOUD_OPS_HIGH)

**Goal**: Claude operates autonomously within approved boundaries

**Capabilities Unlocked**:

**Gmail Autonomy**:
- ✅ Read, analyze, search (already have)
- ⏳ Create drafts (OS_SAFE)
- ⏳ Organize with labels (OS_SAFE)
- ⏳ Send emails (CLOUD_OPS_HIGH, with approval each time)

**Drive Autonomy**:
- ✅ Read, search (already have)
- ⏳ Create Docs/Sheets (OS_SAFE)
- ⏳ Edit files (OS_SAFE)
- ⏳ Share files (CLOUD_OPS_HIGH, with approval)

**Calendar Autonomy**:
- ✅ Read, find free time (already have)
- ⏳ Propose meeting times (OS_SAFE)
- ⏳ Create events (CLOUD_OPS_MEDIUM, with approval)
- ⏳ Cancel events (CLOUD_OPS_HIGH, with approval)

**Sheets/Docs Autonomy**:
- ⏳ Create reports, dashboards (OS_SAFE)
- ⏳ Update data automatically (OS_SAFE, within designated sheets)
- ⏳ Generate documents from templates (OS_SAFE)

**Operating Model**:

```
Or: "Help me organize my inbox"
   ↓
Claude (OS_SAFE):
   - Reads emails (gmail.readonly)
   - Analyzes patterns
   - Creates draft response
   - Proposes labeling strategy
   ↓
Claude: "I can:
   1. [OS_SAFE] Label 47 emails as 'Newsletter'
   2. [OS_SAFE] Create draft responses for 3 important emails
   3. [CLOUD_OPS_HIGH] Send 1 urgent reply (needs approval)
   
   Approve actions 1-2 to proceed automatically?
   Approve action 3 separately?"
   ↓
Or: "GO on 1-2, show me 3 first"
   ↓
Claude:
   - Executes 1-2 (OS_SAFE)
   - Shows draft for action 3
   ↓
Or: "מאשר שליחה" (approves send)
   ↓
Claude:
   - Sends email (CLOUD_OPS_HIGH)
   - Updates MATRIX with evidence
   - Logs action
```

**Deliverables**:
- ⏳ Full Gmail/Drive/Calendar/Sheets/Docs autonomy
- ⏳ Approval flow working smoothly
- ⏳ CAPABILITIES_MATRIX = 100% Google
- ⏳ Zero-touch operation for OS_SAFE tasks
- ⏳ Smooth approval flow for CLOUD_OPS_HIGH

**Status**: ⏳ FUTURE (after G2 complete)  
**Risk**: MEDIUM (autonomous operations)  
**Success Metrics**:
- Or spends <5 minutes/day on approvals
- >80% of proposed actions are OS_SAFE (no approval needed)
- 0 unauthorized actions
- 100% of actions logged and auditable

---

### Phase G4: Advanced Autonomy (FUTURE)

**Beyond basic autonomy**:
- 🔮 Proactive suggestions ("I noticed your calendar is packed, should I...")
- 🔮 Cross-service orchestration (Email → Calendar → Docs workflow)
- 🔮 Learning from patterns (Or's communication style, preferences)
- 🔮 Integration with other systems (GitHub → Gmail notifications)

**Status**: ⏳ FUTURE (after G3 proves stable)

---

## G. Success Criteria

**Phase G1 Success** (Design complete):
- ✅ This document exists and is comprehensive
- ✅ CAPABILITIES_MATRIX updated
- ✅ MCP_GPT_CAPABILITIES_BRIDGE updated
- ✅ Or approves strategic direction

**Phase G2 Success** (Technical bootstrap):
- ✅ OAuth credentials configured
- ✅ MCP server running and verified
- ✅ All target scopes granted
- ✅ Test operations successful
- ✅ CAPABILITIES_MATRIX shows "Verified" for new capabilities

**Phase G3 Success** (Controlled autonomy):
- ✅ Claude sends emails with approval
- ✅ Claude creates/edits Docs/Sheets
- ✅ Claude manages Calendar events
- ✅ Or's productivity improved
- ✅ Zero unauthorized actions
- ✅ 100% audit trail

---

## H. Risk Management

### H.1 Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| OAuth token expires | Service stops working | Refresh token flow automated |
| Rate limits exceeded | Actions fail | Implement exponential backoff, monitor quota |
| API changes | Breaking changes | Version pinning, graceful degradation |
| MCP server crashes | No Google access | Health checks, auto-restart |

### H.2 Security Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Unauthorized access | Data breach | OAuth scopes minimal, CLOUD_OPS_HIGH gates |
| Token leakage | Compromised account | Secrets in Secret Manager, never in code |
| Oversharing files | Privacy violation | Explicit approval for share operations |
| Sending wrong email | Reputation damage | Draft review before send, approval required |

### H.3 Operational Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Too many approvals needed | Or overwhelmed | Maximize OS_SAFE operations |
| Claude makes mistakes | Data corruption | Version history, Trash, rollback plans |
| Capability drift | MATRIX outdated | Mandatory MATRIX update on every change |
| Approval fatigue | Or bypasses process | Clear boundaries, audit compliance |

---

## I. Next Steps

**Immediate (OS_SAFE)**:
1. ✅ Complete this document
2. ⏳ Update CAPABILITIES_MATRIX Section 3 (Google Layer)
3. ⏳ Update MCP_GPT_CAPABILITIES_BRIDGE
4. ⏳ Present to Or for strategic approval

**After Or Approval (still OS_SAFE)**:
1. ⏳ Design OAuth automation workflow
2. ⏳ Design MCP server configuration
3. ⏳ Design verification tests
4. ⏳ Document rollback procedures

**Phase G2 (CLOUD_OPS_HIGH, requires Executor)**:
1. 🔐 Executor enables Google APIs
2. 🔐 Executor creates OAuth credentials
3. 🔐 Or clicks OAuth consent (one-time)
4. 🔐 Executor configures MCP server
5. 🔐 Claude verifies functionality
6. 🔐 CAPABILITIES_MATRIX updated to Verified

**Phase G3 (Autonomous Operations)**:
1. 🔄 Claude begins OS_SAFE operations (drafts, labels, creates docs)
2. 🔴 Claude proposes CLOUD_OPS_HIGH operations (sends, shares, deletes)
3. ✅ Or approves case-by-case
4. 📊 Monitor, learn, optimize

---

**Status**: 📝 DESIGN_IN_PROGRESS (OS_SAFE)  
**Next Action**: Update CAPABILITIES_MATRIX + MCP_GPT_CAPABILITIES_BRIDGE  
**Maintained by**: Claude (with Or's approval)  
**Created**: 2025-11-17
