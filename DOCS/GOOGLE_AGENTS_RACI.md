# Google Agents RACI - Claude vs GPTs GO

**Document Type**: Agent Routing & Responsibility Matrix (OS_SAFE)  
**Created**: 2025-11-17  
**Status**: 📝 DESIGN_COMPLETE  
**Purpose**: Define clear boundaries between Claude Desktop and GPTs GO for Google operations

---

## 🎯 Executive Summary

**Problem**: Two AI agents (Claude Desktop + GPTs GO) both have/will have access to Google Workspace. Without clear boundaries, they might:
- Duplicate work
- Conflict on operations
- Create confusion about "who does what"

**Solution**: RACI matrix defining Responsible agent for each Google use case

**Guiding Principle**: 
- **Claude Desktop** = Deep, contextual, analytical work with local integration
- **GPTs GO** = Operational, repetitive, high-volume tasks with structured data

---

## 📊 RACI Matrix Legend

- **R (Responsible)**: Primary agent executing the task
- **A (Accountable)**: Or (always - strategic approval)
- **C (Consulted)**: Secondary agent, provides input/context
- **I (Informed)**: CAPABILITIES_MATRIX, STATE docs (updated after action)

---

## 1️⃣ Gmail Operations

### 1.1 Email Triage & Analysis

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Email triage** | "Read recent emails and summarize" | R | C | A | I | LOW | OS_SAFE |
| **Pattern detection** | "Find all emails from X about Y" | R | C | A | I | LOW | OS_SAFE |
| **Thread analysis** | "What's the status of thread ABC?" | R | C | A | I | LOW | OS_SAFE |
| **Attachment extraction** | "List all PDFs from last week" | R | C | A | I | LOW | OS_SAFE |
| **Sentiment analysis** | "Analyze tone of customer emails" | R | C | A | I | LOW | OS_SAFE |

**Rationale**: Claude has superior context window and analysis capabilities. Read-only operations are OS_SAFE.

---

### 1.2 Email Drafting & Replies

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Contextual reply** | "Draft response to this email" | R | C | A | I | LOW | OS_SAFE (draft only) |
| **Multi-draft generation** | "Create 3 draft responses" | R | C | A | I | LOW | OS_SAFE |
| **Template-based reply** | "Use template X for email Y" | C | R | A | I | LOW | OS_SAFE (draft only) |
| **Deep research reply** | "Draft with local docs + web research" | R | C | A | I | LOW | OS_SAFE |
| **Quick acknowledgment** | "Send 'received, will review'" | C | R | A | I | MED | CLOUD_OPS_MEDIUM |

**Rationale**: 
- Claude = Deep, researched, contextual drafts (can access local files, web, Drive)
- GPTs GO = Template-based, quick operational responses
- **Both create drafts (OS_SAFE)**, sending requires approval

---

### 1.3 Email Sending Operations

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Send single email** | Or approves specific draft → send | R | C | A | I | HIGH | CLOUD_OPS_HIGH (each time) |
| **Bulk operational send** | Send standard email to list from Sheet | C | R | A | I | HIGH | CLOUD_OPS_HIGH (batch approval) |
| **Newsletter/broadcast** | Send update to customer list | C | R | A | I | HIGH | CLOUD_OPS_HIGH (campaign approval) |
| **Auto-responder** | Automated "OOO" style responses | C | R | A | I | MED | CLOUD_OPS_MEDIUM (one-time playbook) |
| **Urgent notification** | System alert to team | C | R | A | I | HIGH | CLOUD_OPS_HIGH (each time) |

**Rationale**:
- Claude = Single, important, unique emails (direct Or approval)
- GPTs GO = Bulk, structured, templated sends (batch approval efficient)
- **All sends require explicit Or approval**, but bulk can be batched

---

### 1.4 Email Organization

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Label/categorize** | "Label these as 'Customer/Lead/Urgent'" | R | C | A | I | LOW | OS_SAFE |
| **Archive old emails** | "Archive emails >6 months, not starred" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **Delete spam** | "Delete all in Spam folder" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **Create filter** | "Auto-label emails from domain X" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **Bulk unsubscribe** | "Unsubscribe from newsletters" | C | R | A | I | MED | CLOUD_OPS_MEDIUM |

**Rationale**: Claude handles ad-hoc organization; GPTs GO better for systematic bulk operations

---

## 2️⃣ Google Drive Operations

### 2.1 File Search & Reading

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Semantic search** | "Find docs about Q3 strategy" | R | C | A | I | LOW | OS_SAFE |
| **Read document** | "Summarize this Doc" | R | C | A | I | LOW | OS_SAFE |
| **Extract data** | "Get all numbers from Sheet X" | R | C | A | I | LOW | OS_SAFE |
| **Compare files** | "Diff these two Docs" | R | C | A | I | LOW | OS_SAFE |
| **Find shared files** | "List all files shared with team" | R | C | A | I | LOW | OS_SAFE |

**Rationale**: Claude excels at semantic understanding and analysis. All read operations are OS_SAFE.

---

### 2.2 Document Creation & Editing

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Create strategic doc** | "Write project plan Doc" | R | C | A | I | LOW | OS_SAFE (in Claude folder) |
| **Create report** | "Generate weekly report from data" | R | C | A | I | LOW | OS_SAFE |
| **Update tracking Sheet** | "Log this GitHub issue to Sheet" | C | R | A | I | LOW | OS_SAFE (designated Sheet) |
| **Edit shared Doc** | "Fix typos in team Doc" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **Create template** | "Make reusable template" | R | C | A | I | LOW | OS_SAFE |

**Rationale**:
- Claude = Authored content (plans, reports, strategy docs)
- GPTs GO = Structured data updates (Sheets, logs, tracking)
- Editing shared files = MEDIUM risk (version history provides safety)

---

### 2.3 File Sharing & Permissions

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Share with team** | "Share this Doc with team@" | R | C | A | I | HIGH | CLOUD_OPS_HIGH (each time) |
| **Share externally** | "Share with customer email" | R | C | A | I | HIGH | CLOUD_OPS_HIGH (each time) |
| **Publish link** | "Make this Doc public" | R | C | A | I | HIGH | CLOUD_OPS_HIGH (each time) |
| **Revoke access** | "Remove person X from Doc" | R | C | A | I | HIGH | CLOUD_OPS_HIGH |
| **Bulk share** | "Share folder with list from Sheet" | C | R | A | I | HIGH | CLOUD_OPS_HIGH (batch) |

**Rationale**: All sharing operations are HIGH risk. Claude handles individual, GPTs GO handles bulk.

---

### 2.4 File Management

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Create folder structure** | "Organize Drive by project" | R | C | A | I | LOW | OS_SAFE |
| **Move files** | "Move these to archive/" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **Rename files** | "Rename with date prefix" | R | C | A | I | LOW | OS_SAFE |
| **Delete files** | "Delete old drafts" | R | C | A | I | HIGH | CLOUD_OPS_HIGH |
| **Export files** | "Export Doc as PDF" | R | C | A | I | LOW | OS_SAFE |

**Rationale**: Organization is low-risk; deletion always requires approval

---

## 3️⃣ Google Sheets Operations

### 3.1 Data Reading & Analysis

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Read Sheet data** | "Get all rows from Sheet X" | R | C | A | I | LOW | OS_SAFE |
| **Analyze trends** | "Show me sales trends" | R | C | A | I | LOW | OS_SAFE |
| **Generate charts** | "Create visualization" | R | C | A | I | LOW | OS_SAFE |
| **Filter/query data** | "Find all entries where X>Y" | R | C | A | I | LOW | OS_SAFE |
| **Cross-reference** | "Match Sheet A with Sheet B" | R | C | A | I | LOW | OS_SAFE |

**Rationale**: Claude better for analytical queries and cross-referencing

---

### 3.2 Data Writing & Updates

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Append status log** | "Log this event to Sheet" | C | R | A | I | LOW | OS_SAFE (designated log Sheet) |
| **Update tracking** | "Mark task X as done" | C | R | A | I | LOW | OS_SAFE (operations Sheet) |
| **Manual data entry** | "Add these 3 rows" | R | C | A | I | LOW | OS_SAFE |
| **Bulk import** | "Import 100 rows from CSV" | C | R | A | I | MED | CLOUD_OPS_MEDIUM |
| **Formula updates** | "Fix these formulas" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |

**Rationale**:
- Claude = Ad-hoc, manual, thoughtful updates
- GPTs GO = High-frequency, structured, automated logs
- Both can append to designated Sheets (OS_SAFE), but editing shared Sheets requires care

---

### 3.3 Sheet Creation & Structure

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Create new Sheet** | "Make tracking Sheet" | R | C | A | I | LOW | OS_SAFE |
| **Design structure** | "Plan columns/formulas" | R | C | A | I | LOW | OS_SAFE |
| **Create dashboard** | "Build KPI dashboard" | R | C | A | I | LOW | OS_SAFE |
| **Restructure existing** | "Redesign this Sheet" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **Duplicate Sheet** | "Copy as template" | R | C | A | I | LOW | OS_SAFE |

**Rationale**: Claude designs structure; GPTs GO consumes structure for ops

---

## 4️⃣ Google Calendar Operations

### 4.1 Calendar Reading

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **List events** | "Show my week" | R | C | A | I | LOW | OS_SAFE |
| **Find free time** | "When am I free Thursday?" | R | C | A | I | LOW | OS_SAFE |
| **Analyze schedule** | "How many meetings this month?" | R | C | A | I | LOW | OS_SAFE |
| **Check conflicts** | "Do these two events overlap?" | R | C | A | I | LOW | OS_SAFE |
| **Multi-calendar view** | "Show my + team calendar" | R | C | A | I | LOW | OS_SAFE |

**Rationale**: All calendar reading is OS_SAFE, Claude better for analysis

---

### 4.2 Event Creation & Management

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Create personal event** | "Block time for deep work" | R | C | A | I | LOW | OS_SAFE (no attendees) |
| **Schedule meeting** | "Schedule 1:1 with person X" | R | C | A | I | MED | CLOUD_OPS_MEDIUM (sends invite) |
| **Propose times** | "Suggest 3 meeting times" | R | C | A | I | LOW | OS_SAFE (suggestion only) |
| **Update event** | "Move meeting to 3pm" | R | C | A | I | MED | CLOUD_OPS_MEDIUM (notifies) |
| **Cancel meeting** | "Cancel tomorrow's call" | R | C | A | I | HIGH | CLOUD_OPS_HIGH (notifies all) |
| **Bulk scheduling** | "Schedule 10 interviews from Sheet" | C | R | A | I | MED | CLOUD_OPS_MEDIUM (batch) |

**Rationale**:
- Claude = Individual, contextual scheduling decisions
- GPTs GO = Bulk, structured scheduling from data
- Any event with attendees = at least MEDIUM (auto-sends invites)

---

### 4.3 Calendar Coordination

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Find group availability** | "When can these 5 people meet?" | R | C | A | I | LOW | OS_SAFE (check only) |
| **Send availability** | "Share my free slots" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **Accept/decline event** | "Accept this meeting" | R | C | A | I | MED | CLOUD_OPS_MEDIUM (binding) |
| **Request reschedule** | "Ask to move this meeting" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **Batch RSVP** | "Decline all meetings Friday" | C | R | A | I | HIGH | CLOUD_OPS_HIGH |

**Rationale**: Accepting/declining = binding commitment, requires care

---

## 5️⃣ Cross-System Workflows

### 5.1 Gmail → Other Systems

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Email → Sheet log** | "Log emails from X to tracking Sheet" | C | R | A | I | LOW | OS_SAFE |
| **Email → GitHub issue** | "Create issue from this email" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **Email → Calendar** | "Extract meeting details → event" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **Email → Local file** | "Save attachment locally" | R | C | A | I | LOW | OS_SAFE |
| **Email trigger → workflow** | "When email arrives, run workflow X" | C | R | A | I | MED | CLOUD_OPS_MEDIUM |

**Rationale**:
- Claude = Contextual extraction and transformation
- GPTs GO = Structured, rule-based routing

---

### 5.2 Drive/Sheets → Other Systems

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Sheet → GitHub** | "Create PRs from Sheet rows" | C | R | A | I | HIGH | CLOUD_OPS_HIGH |
| **Doc → Email** | "Send this Doc as email body" | R | C | A | I | HIGH | CLOUD_OPS_HIGH |
| **Sheet → Calendar** | "Schedule events from Sheet" | C | R | A | I | MED | CLOUD_OPS_MEDIUM |
| **Drive → Local** | "Sync these files locally" | R | C | A | I | LOW | OS_SAFE |
| **Sheet data → API** | "POST this data to webhook" | C | R | A | I | HIGH | CLOUD_OPS_HIGH |

**Rationale**: Structured data → external systems best handled by GPTs GO

---

### 5.3 Calendar → Other Systems

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Calendar → Sheet** | "Log meetings to tracking Sheet" | C | R | A | I | LOW | OS_SAFE |
| **Calendar → Email** | "Send summary of week's meetings" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **Calendar → GitHub** | "Create issue for missed deadline" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **Calendar sync** | "Keep local calendar in sync" | R | C | A | I | LOW | OS_SAFE (read) |

**Rationale**: Calendar as data source → structured ops → GPTs GO

---

### 5.4 GitHub → Google

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Issue → Email** | "Email team about critical issue" | R | C | A | I | MED | CLOUD_OPS_MEDIUM |
| **PR → Sheet** | "Log PR metrics to dashboard" | C | R | A | I | LOW | OS_SAFE |
| **Commit → Doc** | "Update changelog Doc" | R | C | A | I | LOW | OS_SAFE |
| **Workflow → Calendar** | "Create event for deployment" | C | R | A | I | MED | CLOUD_OPS_MEDIUM |

**Rationale**: GitHub events → structured logging (GPTs GO); GitHub → human communication (Claude)

---

## 6️⃣ Special Cases: BUS & Task Queues

### 6.1 Task Queue Operations

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Add task to queue** | "Queue this email task" | C | R | A | I | LOW | OS_SAFE |
| **Process queue** | "Execute next 10 queued tasks" | C | R | A | I | MED-HIGH | Varies (batch approval) |
| **Monitor queue** | "Show queue status" | R | C | A | I | LOW | OS_SAFE |
| **Clear queue** | "Delete failed tasks" | C | R | A | I | MED | CLOUD_OPS_MEDIUM |
| **Reschedule tasks** | "Move tasks to tomorrow" | C | R | A | I | LOW | OS_SAFE |

**Rationale**: GPTs GO designed for queue processing; Claude for queue strategy/monitoring

---

### 6.2 Batch Operations

| Use Case | Description | Claude | GPTs GO | Or | Docs | Risk | Approval |
|----------|-------------|--------|---------|----|----- |------|----------|
| **Design batch job** | "Plan bulk email campaign" | R | C | A | I | LOW | OS_SAFE (planning) |
| **Execute batch** | "Send 100 emails from template" | C | R | A | I | HIGH | CLOUD_OPS_HIGH (batch) |
| **Monitor batch** | "Track batch progress" | C | R | A | I | LOW | OS_SAFE |
| **Rollback batch** | "Undo last batch operation" | C | R | A | I | HIGH | CLOUD_OPS_HIGH |
| **Batch reporting** | "Summarize batch results" | R | C | A | I | LOW | OS_SAFE |

**Rationale**: Claude plans and analyzes; GPTs GO executes and monitors

---

## 7️⃣ Agent Handoff Protocols

### 7.1 When Claude Delegates to GPTs GO

**Scenarios**:
1. Task requires bulk/structured operations (>10 items)
2. Task needs queue-based execution
3. Task is repetitive with clear template
4. Task benefits from persistent monitoring

**Protocol**:
```
Claude: "This task requires bulk operations.
        I'm preparing the spec/template.
        GPTs GO will execute with your approval."
        
↓

Claude creates:
- Task specification (Sheet/Doc)
- Batch approval request for Or
- Handoff note in STATE docs

↓

Or approves batch

↓

GPTs GO executes batch

↓

Both agents update CAPABILITIES_MATRIX
```

---

### 7.2 When GPTs GO Delegates to Claude

**Scenarios**:
1. Task requires deep context (local files, complex analysis)
2. Task needs original authoring (not template-based)
3. Task benefits from Claude's analytical capabilities
4. Task involves sensitive/unique communication

**Protocol**:
```
GPTs GO: "This task requires deep analysis/authoring.
          Delegating to Claude Desktop for execution."

↓

GPTs GO creates handoff note with:
- Context from Gmail/Drive/Sheets
- Specific question/task for Claude
- Expected output format

↓

Claude executes with full context

↓

Claude returns result to GPTs GO OR directly to Or

↓

Both agents update CAPABILITIES_MATRIX
```

---

### 7.3 Conflict Resolution

**If both agents could handle a task**:

1. **Check RACI table first** (this document)
2. **If still unclear**:
   - Default: Claude for **ad-hoc/unique**, GPTs GO for **structured/repeated**
3. **If conflict occurs** (both claim responsibility):
   - **Or decides** (Accountable in RACI)
   - Update this RACI document with learned case

---

## 8️⃣ OS_SAFE vs CLOUD_OPS_HIGH Summary

### OS_SAFE Operations (No approval needed)

**Claude can do independently**:
- ✅ Read all Google data (Gmail, Drive, Calendar, Sheets)
- ✅ Analyze, search, summarize
- ✅ Create drafts (emails not sent)
- ✅ Create new files in Claude's designated folders
- ✅ Generate reports, proposals, plans
- ✅ Update designated tracking Sheets (append-only)

**GPTs GO can do independently**:
- ✅ Read all Google data
- ✅ Log structured data to tracking Sheets
- ✅ Monitor queues and batch jobs
- ✅ Create drafts from templates
- ✅ Generate reports from structured data

---

### CLOUD_OPS_MEDIUM (Or notified, reversible)

**Operations**:
- 🟡 Label/organize emails (reversible)
- 🟡 Create calendar events (can be deleted, but invites already sent)
- 🟡 Edit shared documents (version history available)
- 🟡 Move files (reversible)

**Approval**: Or acknowledgment ("OK to proceed")

---

### CLOUD_OPS_HIGH (Explicit approval each time)

**Operations**:
- 🔴 Send emails
- 🔴 Share files externally
- 🔴 Delete files/emails permanently
- 🔴 Cancel events with external attendees
- 🔴 Batch operations (>10 items)
- 🔴 Any operation affecting others

**Approval**: Or's explicit "מאשר שליחה" or similar for EACH operation

---

## 9️⃣ Integration with CAPABILITIES_MATRIX

### How to Use This RACI

**Before planning any Google operation**:

1. **Check this RACI** → Who is Responsible (R)?
2. **Check CAPABILITIES_MATRIX** → Is capability available?
3. **Check risk level** → What approval needed?
4. **Execute or request approval** → Based on risk
5. **Update MATRIX** → After operation completes

**Example Flow**:
```
User: "Send this email to customer"

↓

Agent checks RACI:
→ "Send single email" = Claude (R), HIGH risk

↓

Agent checks MATRIX:
→ gmail.send = Phase G3 (not available yet)

↓

Agent responds:
"I can create a draft now (OS_SAFE).
 Sending requires:
 1. Phase G2 OAuth setup (needs Executor)
 2. Your explicit approval for send (CLOUD_OPS_HIGH)
 
 Would you like me to create the draft?"
```

---

## 🔄 RACI Update Protocol

**When to update this document**:
1. New use case discovered
2. Agent handoff fails/conflicts
3. Risk level changes
4. Or provides clarification on responsibility

**Update process**:
1. Claude identifies gap/conflict
2. Claude proposes RACI update
3. Or approves strategic direction
4. Document updated
5. CAPABILITIES_MATRIX + BRIDGE updated accordingly

---

## 📊 Summary: Claude vs GPTs GO

### Claude Desktop Strengths
- 📖 Deep contextual understanding
- 🔍 Complex analysis and research
- ✍️ Original authoring (not templates)
- 🔗 Integration with local files
- 🧠 Strategic planning and design
- 💬 Sensitive/unique communications

**Primary Google Roles**:
- Email triage and analysis
- Contextual email replies
- Strategic document creation
- Sheet analysis and reporting
- Calendar analysis
- Cross-system contextual flows

---

### GPTs GO Strengths
- ⚡ High-volume operations
- 📊 Structured data processing
- 🔁 Repetitive tasks
- 📋 Template-based operations
- 🚦 Queue and batch management
- 🔄 Monitoring and logging

**Primary Google Roles**:
- Bulk email operations
- Structured Sheet updates
- Queue processing
- Batch scheduling
- Systematic logging
- Cross-system data flows

---

## ✅ Next Steps

1. ⏳ Update CAPABILITIES_MATRIX Section 3 with agent routing notes
2. ⏳ Update MCP_GPT_CAPABILITIES_BRIDGE with RACI reference
3. ⏳ Or reviews and approves this RACI
4. ⏳ Proceed to Phase G2.1 (Technical Planning)

---

**Status**: 📝 DESIGN_COMPLETE (OS_SAFE)  
**Maintained by**: Claude (with Or's approval)  
**Created**: 2025-11-17  
**Next Review**: After first agent conflict or Phase G3 launch
