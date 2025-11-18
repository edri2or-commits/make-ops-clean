# FLOW_002 – GPT-CEO Google Routing Flow

**Flow ID**: FLOW_002  
**Created**: 2025-11-18  
**Owner**: GPT-CEO  
**Executor**: Claude Desktop  
**Version**: 1.0  
**Status**: 📋 Design Only (All write operations = Planned)

---

## 🎯 Purpose

This flow defines **how GPT-CEO orchestrates Google Workspace operations** (Gmail, Drive, Calendar, Sheets, Docs) based on CAPABILITIES_MATRIX v1.3.0.

**Critical Note**: Currently, **ALL Google write operations are `GPT-CEO Ready = Planned`**, meaning this flow is primarily for:
1. **Design and Playbook creation**
2. **Read-only operations** (search, analyze, extract)
3. **Preparation for future write capabilities** (when OAuth expansion complete)

---

## 📍 When to Use This Flow

GPT-CEO should invoke FLOW_002 when Or requests Google Workspace operations:

### ✅ Available Now (Read-Only)
- **Gmail**: Search emails, read threads, analyze inbox patterns
- **Drive**: Search files, fetch document content, navigate folders
- **Calendar**: List events, find free time, analyze schedule
- **Sheets/Docs**: Not available yet (even read-only)

### 📋 Design Phase (Write Operations - Planned)
- **Gmail**: Send emails, create drafts, organize with labels
- **Drive**: Create documents, edit files, share folders
- **Calendar**: Create events, schedule meetings, send invites
- **Sheets**: Create spreadsheets, update cells, generate reports
- **Docs**: Create documents, edit content, collaborate

### 🚫 Not Available
- **Gmail/Drive/Calendar write** without OAuth expansion
- **Sheets/Docs** (any operation - MCP server not configured)
- **Direct API calls** (Claude has network restrictions)

---

## 🔀 Routing Rules

### Rule 1: Check Readiness in CAPABILITIES_MATRIX

**ALWAYS** reference CAPABILITIES_MATRIX.md Section 3 (Google Layer):

```
1. Find capability in Section 3.1-3.4
2. Check "GPT-CEO Ready?" column
3. Route:
   - Yes (read ops) → Execute via Claude MCP
   - Planned (write ops) → Create Playbook/Design
   - No → Cannot perform
```

### Rule 2: Read Operations (GPT-CEO Ready = Yes)

**Pattern**:
```
Or → GPT-CEO: "Find all emails from X in last month"
     ↓
GPT-CEO → Claude: [Search query with Gmail MCP]
     ↓
Claude → Gmail API: [Executes search]
     ↓
Claude → GPT-CEO: [Returns results]
     ↓
GPT-CEO → Or: [Analyzes and presents findings]
```

**Available Operations**:
- Gmail: `search_gmail_messages`, `read_gmail_thread`, `read_gmail_profile`
- Drive: `google_drive_search`, `google_drive_fetch`
- Calendar: `list_gcal_events`, `find_free_time`

**Approval**: `No` (read-only, OS_SAFE)

### Rule 3: Write Operations (GPT-CEO Ready = Planned)

**Pattern**:
```
Or → GPT-CEO: "Send email to team about project update"
     ↓
GPT-CEO: [Checks CAPABILITIES_MATRIX → Planned]
     ↓
GPT-CEO → Claude: "Create DOCS/PLAYBOOKS/GMAIL_SEND_PLAYBOOK.md"
     ↓
Claude: [Creates design document with:]
        - Email content (draft)
        - Recipients list
        - Approval gate
        - Execution steps (when ready)
     ↓
GPT-CEO → Or: "I've drafted the email in a playbook.
               When Google MCP write access is ready, I can execute.
               Would you like me to create a manual send instruction?"
```

**Output**: Design document in `DOCS/PLAYBOOKS/`

**Existing Designs** (reference these):
- `DOCS/PILOT_GMAIL_SEND_FLOW.md`
- `DOCS/PILOT_GMAIL_DRAFTS_FLOW.md`
- `DOCS/PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md`
- `DOCS/PILOT_CALENDAR_FOCUS_EVENT_FLOW.md`

### Rule 4: Not Available → Explain Limitation

**Pattern**:
```
Or → GPT-CEO: "Create a new Google Sheet with data"
     ↓
GPT-CEO → Or: "Google Sheets access is not yet configured.
               Current status: Planned (CAPABILITIES_MATRIX 3.4)
               
               What I can do:
               - Create design for the sheet structure
               - Prepare data in CSV/markdown format
               - Document automation steps for future
               
               Alternative: Use GitHub Actions → Sheets (via WIF)
               for automated appends (already working)"
```

---

## 🔐 Approval Gates

### No Approval (Read Operations)
```
Operations:
- Search emails/files/events
- Read message content
- Fetch documents
- List folders/calendars
- Find free time slots

Execute: Immediately via Claude MCP
```

### High Approval (Write Operations - When Ready)
```
Operations:
- Send emails (external impact)
- Share files externally
- Delete any content
- Calendar invites to >5 people

Require: Explicit Or approval ("מאשר שליחה")
```

### Context-Dependent (Write Operations - When Ready)
```
Operations:
- Create personal files (No approval)
- Organize with labels (No approval)
- Create personal calendar events (No approval)
- Edit shared documents (Depends on scope)

Decision Tree:
1. Personal/reversible? → No approval
2. Shared/external? → Yes approval
3. Unclear? → Ask Or
```

---

## 📋 Execution Patterns

### Pattern A: Read Operation (Available Now)

**Use Case**: Search Gmail for specific emails

**GPT-CEO Message to Claude**:
```
[MESSAGE TO CLAUDE DESKTOP]

Task: Search Gmail for emails from john@example.com in last 30 days

Tool: search_gmail_messages
Query: from:john@example.com after:2025-10-18

Expected Response:
- Number of emails found
- Subject lines
- Dates
- Thread IDs (for follow-up if needed)

Approval: None (read-only per CAPABILITIES_MATRIX 3.1)
```

**Claude Response**:
```
✅ Gmail Search Results:
Found: 12 emails from john@example.com
Period: 2025-10-18 to 2025-11-18

Top 5 by date:
1. "Project Update Q4" (2025-11-15)
2. "Meeting Notes - Strategy" (2025-11-10)
[...]

Thread IDs available for detailed read if needed.
```

### Pattern B: Write Operation Design (Planned)

**Use Case**: Send email about project completion

**GPT-CEO Approach**:
```
1. Check CAPABILITIES_MATRIX → "Send email" = Planned
2. Create playbook document
3. Present to Or with:
   - Draft email content
   - Recipients
   - Timeline estimate (when capability available)
   - Manual alternative (Or sends via Gmail)
```

**Playbook Location**: `DOCS/PLAYBOOKS/EMAIL_PROJECT_COMPLETION.md`

**Content**:
```markdown
# Email Playbook: Project Completion Notification

## Status
- GPT-CEO Ready: Planned (CAPABILITIES_MATRIX 3.1)
- Awaiting: OAuth scope expansion (gmail.send)
- Alternative: Or sends manually via Gmail

## Draft Email
To: team@company.com
Subject: Project X Completion - Phase 1 Done

Body:
[Email content drafted by GPT-CEO]

## Approval Gate
- Requires: Explicit Or approval (CLOUD_OPS_HIGH)
- Phrase: "מאשר שליחה"

## When Ready
1. OAuth expanded
2. Or approves content
3. Claude sends via Gmail MCP
4. Confirmation to Or
```

### Pattern C: Complex Workflow (Future)

**Use Case**: Weekly report automation
- Search Gmail for week's updates
- Extract key points
- Create Google Doc with summary
- Share with team
- Add calendar reminder

**Current Status**: Each step marked `Planned`

**Approach**:
1. Create `DOCS/PLAYBOOKS/WEEKLY_REPORT_AUTOMATION.md`
2. Design each step with approval gates
3. Mark dependencies (OAuth, MCP config)
4. Present to Or: "This will be possible when all Google write access is ready"

---

## 🚦 Decision Tree

```
┌──────────────────────────────────┐
│ Or requests Google operation     │
└────────────┬─────────────────────┘
             ↓
┌──────────────────────────────────┐
│ GPT-CEO: Check CAPABILITIES      │
│ MATRIX Section 3 (Google Layer)  │
└────────────┬─────────────────────┘
             ↓
        ┌────┴────┐
        │         │
        ↓         ↓
    Read Op   Write Op
        │         │
        ↓         ↓
    Ready?    Planned?
        │         │
    ┌───┴───┐     │
    │       │     │
    ↓       ↓     ↓
  Yes      No   Design
    │       │   Playbook
    ↓       │     │
 Execute    │     │
    │       │     │
    │   Explain   │
    │   Gap       │
    └───────┴─────┘
             ↓
┌──────────────────────────────────┐
│ Claude executes or creates doc   │
└──────────────────────────────────┘
```

---

## 📊 Google Capabilities Matrix Summary

### ✅ Ready Now (Read-Only)

| Service | Operations | GPT-CEO Ready? | Approval? |
|---------|-----------|----------------|-----------|
| Gmail | Search, Read, List | Yes | No |
| Drive | Search, Fetch, Navigate | Yes | No |
| Calendar | List, Search, Free Time | Yes | No |

### 📋 Planned (Write Operations)

| Service | Operations | GPT-CEO Ready? | Approval? | Blocker |
|---------|-----------|----------------|-----------|---------|
| Gmail | Send, Draft, Labels | Planned | Yes/Depends | OAuth expansion |
| Drive | Create, Edit, Share | Planned | Depends | OAuth expansion |
| Calendar | Create, Edit Events | Planned | Depends | OAuth expansion |
| Sheets | All ops | Planned | Depends | MCP not configured |
| Docs | All ops | Planned | Depends | MCP not configured |

### 🚫 Not Available

- Direct API calls (Claude network restrictions)
- Operations requiring OAuth consent before expansion

---

## ⚠️ Important Constraints

### Constraint 1: OAuth Expansion Required
```
Current Scopes:
- gmail.readonly ✅
- drive.readonly ✅
- calendar.readonly ✅

Required for Write:
- gmail.send ⏳
- gmail.modify ⏳
- drive.file ⏳
- calendar.events ⏳

Status: CAPABILITIES_MATRIX Priority 0 (Google MCP Full Setup)
See: DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md
```

### Constraint 2: MCP Server Configuration
```
Sheets/Docs Access:
- Status: Not configured
- Workaround: GitHub Actions → WIF → Sheets API
  (Available for automated appends only)
  
Action Required:
- Configure separate Google MCP server
- Add Sheets/Docs scopes
- Update claude_desktop_config.json
```

### Constraint 3: Approval Protocol
```
When write access becomes available:

CLOUD_OPS_HIGH (Yes approval):
- Send emails (external recipients)
- Share files externally
- Delete any content
- Calendar invites (>5 attendees)

OS_SAFE (No approval):
- Personal file creation
- Personal calendar events
- Label organization
- Drafts (not sent)

CLOUD_OPS_MEDIUM (Depends):
- Edit shared documents
- Internal file sharing
- Small meeting invites
```

---

## 🔄 Flow Evolution

### Current (v1.0) - Design Phase
- ✅ Read operations working
- 📋 Playbook creation for write ops
- 📋 Reference PILOT flows
- ⏳ Awaiting OAuth expansion

### Next (v1.1) - Partial Write
- 🔄 OAuth scopes expanded
- 🔄 Gmail send enabled
- 🔄 Drive create enabled
- 🔄 Calendar events enabled
- 🔄 Approval gates tested

### Future (v2.0) - Full Autonomy
- 🚀 Sheets/Docs MCP configured
- 🚀 Complex workflows automated
- 🚀 Multi-service orchestrations
- 🚀 Proactive suggestions

---

## 📚 References

**MUST READ**:
- `CAPABILITIES_MATRIX.md` (Section 3: Google Layer)
- `DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md` - Full strategy

**Existing Designs** (use as templates):
- `DOCS/PILOT_GMAIL_SEND_FLOW.md`
- `DOCS/PILOT_GMAIL_DRAFTS_FLOW.md`
- `DOCS/PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md`
- `DOCS/PILOT_CALENDAR_FOCUS_EVENT_FLOW.md`

**Related**:
- `FLOW_001_GPT_CEO_GITHUB_ROUTING.md` - GitHub operations
- `DOCS/GOOGLE_AGENTS_RACI.md` - Roles and responsibilities

---

## 🎓 For GPT-CEO: Key Takeaways

1. **Read operations work NOW** - use them freely
2. **Write operations are DESIGNED** - create playbooks
3. **Reference PILOT flows** - don't reinvent patterns
4. **Always check MATRIX** - single source of truth
5. **Be transparent with Or** - explain what's possible vs. planned
6. **Design > Wait** - create playbooks while waiting for OAuth

---

**Created**: 2025-11-18  
**By**: Claude (via GPT-CEO instructions)  
**Status**: 📋 Design Phase (awaiting OAuth expansion)  
**Next Review**: When Google MCP write access enabled
