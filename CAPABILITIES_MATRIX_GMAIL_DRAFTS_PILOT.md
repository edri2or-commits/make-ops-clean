# CAPABILITIES MATRIX - Gmail Drafts Pilot Entry (G2.1-Pilot)

**Updated**: 2025-11-17  
**Phase**: G2.1-Pilot Complete

---

## Gmail Section Update - New Row

### 3.1 Gmail (with Pilot entry)

| From | To | Capability | Status | Details | Safeguards | Last Verified | Reference |
|------|----|-----------| -------|---------|------------|---------------|-----------|
| Claude MCP | Gmail API | Read profile | ✅ Verified | Get user email | None (OS_SAFE) | 2025-11-13 | Native integration |
| Claude MCP | Gmail API | Search messages | ✅ Verified | Full Gmail search syntax | None (OS_SAFE) | 2025-11-13 | Native integration |
| Claude MCP | Gmail API | Read threads | ✅ Verified | Full thread context | None (OS_SAFE) | 2025-11-13 | Native integration |
| Claude MCP | Gmail API | List messages | ✅ Verified | Pagination supported | None (OS_SAFE) | 2025-11-13 | Native integration |
| **Claude MCP** | **Gmail API** | **Create drafts** | **🔄 PILOT_DESIGNED** | **Create new email drafts (not sent)** | **(1) Content approval required (2) OS_SAFE - no send (3) Logging enabled (4) Scope: gmail.compose only (5) Policy block: cannot call gmail.send** | **Pending G2.2** | **[`PILOT_GMAIL_DRAFTS_FLOW.md`](DOCS/PILOT_GMAIL_DRAFTS_FLOW.md)** |
| Claude MCP | Gmail API | Organize (labels) | 🔄 G2.2 | Requires `gmail.modify` scope | CLOUD_OPS_MEDIUM + logged | Pending G2.2 | AUTONOMY_PLAN |
| Claude MCP | Gmail API | Send email | 🔄 G2.3 | Requires `gmail.send` | (1) CLOUD_OPS_HIGH approval (2) Rate: 10/hour (3) Logged (4) TTL: 60min (5) No forwarding rules | Pending G2.3 | OAUTH_ARCH |
| Claude MCP | Gmail API | Download attachments | 🔄 G2.2 | Requires expanded scopes | None (OS_SAFE - read-only) | Pending G2.2 | AUTONOMY_PLAN |

---

## Detailed Pilot Entry Breakdown

**Capability**: Create Gmail Drafts  
**Status**: 🔄 PILOT_DESIGNED (Phase G2.1-Pilot)  
**Operational After**: G2.2 execution (OAuth + MCP config)

**What it does**:
- Creates new email drafts in Or's Gmail account
- Based on contextual understanding (thread, documents, meetings)
- Supports reply-to (threading) and new emails
- Requires Or's approval of content before creation
- Drafts remain unsent (Or sends manually when ready)

**Risk Level**: OS_SAFE
- No external impact (drafts not sent)
- No recipients notified
- Fully reversible (Or can delete/edit)
- Private (only Or sees drafts)

**Required Scope**: `gmail.compose`
- Allows draft creation only
- Does NOT allow sending
- Does NOT allow label modification
- Does NOT allow settings changes

**Safeguards** (5 layers):

1. **Content Approval Required**:
   - Claude presents full draft for Or's review
   - Or can revise, approve, or cancel
   - Draft not created without explicit approval

2. **OS_SAFE - No Send**:
   - Drafts never sent automatically
   - Scope limited to `gmail.compose`
   - Cannot transition to send without CLOUD_OPS_HIGH approval

3. **Logging Enabled**:
   - Every draft creation logged to `OPS/LOGS/google-operations.jsonl`
   - Includes: timestamp, subject, recipient, draft ID
   - Audit trail committed to repo

4. **Scope Limitation**:
   - Uses `gmail.compose` ONLY
   - Does not include `gmail.send`, `gmail.modify`, or `gmail.settings`
   - Minimal access principle

5. **Policy Block**:
   - MCP server blocks `gmail.send` calls
   - Even if prompt injection attempts to send
   - Technical enforcement (not just policy)

**Agent Routing** (per RACI):
- **Claude (R)**: Contextual, researched, unique drafts
- **GPTs GO (C)**: Template-based alternatives (if consulted)
- **Or (A)**: Approves content before creation

**Complete Flow**: [`DOCS/PILOT_GMAIL_DRAFTS_FLOW.md`](DOCS/PILOT_GMAIL_DRAFTS_FLOW.md)

**Template Status**: This pilot serves as template for all future Google capabilities

---

## Phase Tracking

### ✅ Phase G2.1-Pilot (Complete):
- Gmail Drafts flow documented
- End-to-end playbook created
- CAPABILITIES_MATRIX updated (this entry)
- MCP_GPT_CAPABILITIES_BRIDGE updated
- Template established for future capabilities

### ⏳ Phase G2.2 (Next - Execution):
- Execute OAuth workflows (Executor)
- Or's one-time OAuth consent (includes `gmail.compose`)
- MCP server configuration
- Test draft creation
- Update Status: PILOT_DESIGNED → VERIFIED

### ⏳ Phase G2.3+ (Future):
- Gmail Send (copy pilot template)
- Drive operations (copy pilot template)
- Calendar operations (copy pilot template)
- Sheets/Docs (copy pilot template)

---

**Note**: This entry will update to ✅ VERIFIED after G2.2 execution and successful testing.

**Maintained by**: Claude  
**Last Updated**: 2025-11-17 (Phase G2.1-Pilot)  
**Next Update**: After G2.2 execution
