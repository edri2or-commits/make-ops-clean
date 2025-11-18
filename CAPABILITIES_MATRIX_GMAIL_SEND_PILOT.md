# CAPABILITIES MATRIX - Gmail Send Entry (CLOUD_OPS_HIGH)

**Updated**: 2025-11-17  
**Addition**: Gmail Send capability (PILOT_DESIGNED)

---

## 3.1 Gmail - Updated with Send Capability

### Complete Gmail Capabilities Table

| From | To | Capability | Status | Details | Safeguards | Last Verified | Reference |
|------|----|-----------| -------|---------|------------|---------------|-----------|
| Claude MCP | Gmail API | Read profile | ✅ Verified | Get user email | None (OS_SAFE) | 2025-11-13 | Native integration |
| Claude MCP | Gmail API | Search messages | ✅ Verified | Full Gmail search syntax | None (OS_SAFE) | 2025-11-13 | Native integration |
| Claude MCP | Gmail API | Read threads | ✅ Verified | Full thread context | None (OS_SAFE) | 2025-11-13 | Native integration |
| Claude MCP | Gmail API | List messages | ✅ Verified | Pagination supported | None (OS_SAFE) | 2025-11-13 | Native integration |
| Claude MCP | Gmail API | **Create drafts** | **🔄 PILOT_DESIGNED** | **Create new email drafts (not sent)** | **(1) Content approval (2) OS_SAFE - no send (3) Log: OPS/LOGS/ (4) Scope: gmail.compose (5) Block: cannot gmail.send** | **Pending G2.2** | **[PILOT_GMAIL_DRAFTS_FLOW.md](DOCS/PILOT_GMAIL_DRAFTS_FLOW.md)** |
| Claude MCP | Gmail API | **Send email** | **🔄 PILOT_DESIGNED** | **Send individual emails with explicit approval** | **(1) CLOUD_OPS_HIGH approval ('מאשר שליחה') + 60min TTL (2) Rate: 10/hour (hard block) (3) Log: Detailed (approval + recipients + preview) (4) Scope: gmail.send only (5) Blocks: No forward/BCC/bulk/schedule** | **Pending G2.3** | **[PILOT_GMAIL_SEND_FLOW.md](DOCS/PILOT_GMAIL_SEND_FLOW.md)** |
| Claude MCP | Gmail API | Organize (labels) | 🔄 G2.2 | Requires `gmail.modify` scope | CLOUD_OPS_MEDIUM + logged | Pending G2.2 | AUTONOMY_PLAN |
| Claude MCP | Gmail API | Download attachments | 🔄 G2.2 | Requires expanded scopes | None (OS_SAFE - read-only) | Pending G2.2 | AUTONOMY_PLAN |

---

## Gmail Send - Detailed Entry

**Capability**: Send email via Gmail API  
**Status**: 🔄 PILOT_DESIGNED (Phase G2.1-Pilot)  
**Operational After**: G2.3 execution (OAuth scope expansion + testing)

### What it does

**Primary function**:
- Sends individual emails on Or's behalf
- Each send requires explicit approval
- Irreversible operation (cannot unsend)
- External impact (recipients receive email)

**Use cases**:
- Customer communication (apologies, updates, follow-ups)
- Team announcements (feature launches, changes)
- Partner correspondence (meeting confirmations, proposals)
- Individual replies (contextual responses to threads)

**Not supported** (different flows):
- Bulk sends (>10/hour) → GPTs GO territory per RACI
- Scheduled sends → Separate automation
- Auto-replies → Forbidden by policy
- Template campaigns → GPTs GO territory

### Risk Level: CLOUD_OPS_HIGH

**Why CLOUD_OPS_HIGH**:
1. **External impact**: Recipients receive email (not just Or)
2. **Irreversible**: Cannot unsend once delivered
3. **Reputation risk**: Email represents Or's identity
4. **Potential for misuse**: Wrong recipient, wrong content, wrong timing
5. **Scale risk**: Automation could send many if safeguards fail

**Comparison with Gmail Drafts**:
| Aspect | Drafts (OS_SAFE) | Send (CLOUD_OPS_HIGH) |
|--------|------------------|----------------------|
| External impact | None | High (recipient receives) |
| Reversibility | Full (delete draft) | None (cannot unsend) |
| Safeguards | 5 layers (light) | 5 layers (heavy) |
| Approval | Conversational | Explicit phrase + TTL |
| Rate limit | Optional | Mandatory (hard block) |

### Safeguards (ALL 5 LAYERS - MANDATORY)

**Layer 1: Approval Gate** (CLOUD_OPS_HIGH)
- **Type**: Explicit phrase + TTL
- **Phrase**: "מאשר שליחה" (Hebrew: "I approve sending")
- **TTL**: 60 minutes from preview to approval
- **Process**:
  1. Claude presents FULL email (every word)
  2. Or reviews thoroughly
  3. Or types exact phrase: "מאשר שליחה"
  4. Claude verifies: phrase correct + within TTL
  5. Claude sends immediately after verification
- **Why strict**: Cannot unsend, must prevent wrong sends
- **Alternatives**: "Draft" (save as draft), "Revise" (change content), "Cancel" (abort)

**Layer 2: Rate Limiting** (MANDATORY)
- **Limit**: 10 sends per 60-minute rolling window
- **Tracking**: OPS/STATE/gmail-send-rate.json
- **Enforcement**: Hard block at 10 (cannot send more)
- **Alert**: Warning at 8 sends (80%)
- **Override**: Separate approval phrase required ("מאשר חריגה מגבלת קצב")
- **Why**: Prevents runaway sending, spam, reputation damage
- **Example**: If 10 sends in last hour, must wait until oldest expires

**Layer 3: Mandatory Logging** (DETAILED)
- **Location**: OPS/LOGS/google-operations.jsonl
- **Format**: JSON (one per line, ~1000 bytes per send)
- **Content**:
  - Full metadata (timestamp, actor, status)
  - Recipients (to, cc, bcc)
  - Subject (full)
  - Body preview (first 100 chars)
  - **Approval details** (phrase, who, when, TTL status)
  - **Rate limit state** (before/after counts)
  - Context gathered (threads, docs, meetings)
  - Delivery status (sent, delivered, failed)
- **Retention**: Permanent (committed to repo)
- **Why**: Audit trail, forensics, compliance, learning

**Layer 4: Scope Limitation**
- **Scope**: `gmail.send` ONLY
- **Cannot**:
  - Modify settings (gmail.settings.*)
  - Create filters/forwarding (data exfiltration risk)
  - Access admin APIs
  - Modify labels/categories (gmail.modify)
- **Why**: Minimal access principle

**Layer 5: Policy Blocks** (TECHNICAL ENFORCEMENT)
- **Blocked operations** (cannot bypass):
  1. Auto-forwarding rules (data exfiltration risk)
  2. BCC hijacking (all BCC must be approved)
  3. Bulk sending (>10/hour blocked by rate limit)
  4. Scheduled sends (separate automation needed)
  5. Settings modification (use Gmail directly)
  6. Sending without approval (approval gate mandatory)
- **Enforcement**: MCP server + Claude logic + API scopes
- **Prompt injection proof**: Technical blocks (not just "Claude promises")

### Required Scope

**OAuth scope**: `gmail.send`
- **Purpose**: Send emails on user's behalf
- **Grants**: Ability to send email via Gmail API
- **Does NOT grant**: Settings access, filter creation, admin access
- **Requires**: Or's one-time OAuth consent (Phase G2.3)
- **Current status**: Not yet granted (pending G2.3)

### Agent Routing (per RACI)

**Per GOOGLE_AGENTS_RACI.md Section 1.3**:

| Use Case | Claude | GPTs GO | Why |
|----------|--------|---------|-----|
| Single, contextual send | **R** (Responsible) | C (Consulted) | Claude has deep context from threads/docs/meetings |
| Bulk sends (campaigns) | C (Consulted) | **R** (Responsible) | GPTs GO better for high-volume, templated sends |
| Emergency send (override) | **R** | I (Informed) | Claude can handle with override approval |
| Scheduled sends | - | **R** | Separate automation (not in this pilot) |

**This pilot**: Single contextual sends → Claude is Responsible

### Execution Flow Summary

```
User: "Send email to X about Y"
  ↓
Claude checks MATRIX → Status: PILOT_DESIGNED (before G2.3) or VERIFIED (after G2.3)
  ↓
Claude checks RACI → Single send = Claude (R)
  ↓
Claude gathers context (threads, docs, calendar, local, web)
  ↓
Claude drafts email
  ↓
Claude presents FULL preview to Or
  ↓
Claude checks rate limit (< 10 sends/hour?)
  ↓
Claude requests approval: "Type: מאשר שליחה"
  ↓
Or provides: "מאשר שליחה"
  ↓
Claude verifies: phrase correct + within 60min TTL + rate limit OK
  ↓
Claude sends via MCP (gmail.send)
  ↓
Claude logs (detailed) to OPS/LOGS/
  ↓
Claude reports: "✅ Sent, Message ID: m-123"
```

### Test Plan (8 Test Cases)

**After G2.3 execution**:
1. Basic send → Success
2. Send with context (reply) → Success
3. Wrong approval phrase → Blocked
4. TTL expired (>60min) → Blocked
5. Rate limit hit (11th send) → Blocked
6. Override rate limit (emergency) → Logged + Sent
7. Invalid recipient email → Error handled
8. Network failure → Retry offered

**Success criteria**:
- All 8 tests pass
- Safeguards work as designed
- Logging complete
- Rate limiting enforced
- Or can review/approve/cancel easily

### Comparison: Drafts vs Send

| Aspect | Gmail Drafts | Gmail Send |
|--------|--------------|------------|
| **Phase** | G2.2 | G2.3 |
| **Risk** | OS_SAFE | CLOUD_OPS_HIGH |
| **Scope** | gmail.compose | gmail.send |
| **Approval** | "Create draft" | "מאשר שליחה" + TTL |
| **Rate limit** | 50/hour (optional) | 10/hour (mandatory, hard) |
| **Logging** | Standard (~500 bytes) | Detailed (~1000 bytes) |
| **Reversibility** | Full (delete draft) | None (cannot unsend) |
| **External impact** | None | High (recipient receives) |
| **Policy blocks** | No send from draft | No forward/BCC/bulk/schedule |
| **Test cases** | 5 | 8 (includes safeguard tests) |

**Key difference**: OS_SAFE → CLOUD_OPS_HIGH is paradigm shift, not just "more safeguards"

### Complete Playbook

**Reference**: [`DOCS/PILOT_GMAIL_SEND_FLOW.md`](DOCS/PILOT_GMAIL_SEND_FLOW.md) (46KB)

**Contents**:
- Section 1: Intent & Classification (CLOUD_OPS_HIGH)
- Section 2: Actors & RACI (Claude R for single sends)
- Section 3: Plan (19 steps including approval gate)
- Section 4: Execution Skeleton (detailed flow with all gates)
- Section 5: Safeguards (ALL 5 layers, heavy enforcement)
- Section 6: Observability (detailed logging, rate tracking)
- Section 7: CAPABILITIES_MATRIX entry (this row)
- Section 8: Phase tracking & comparison with Drafts
- Section 9: Summary & next steps

### Phase Tracking

**Phase G2.1-Pilot** ✅ (Complete):
- Gmail Send playbook created
- All safeguards documented
- Test plan defined
- CAPABILITIES_MATRIX entry prepared
- Status: PILOT_DESIGNED (OS_SAFE design only)

**Phase G2.3** ⏳ (Next - Requires Executor + Or):
- Expand OAuth scope (add gmail.send)
- Or clicks consent URL (one-time)
- Create rate limit tracking file
- Test all 8 test cases
- Update MATRIX: PILOT_DESIGNED → VERIFIED

**Critical**: No execution until G2.3 (requires Executor + Or's GO)

---

**Maintained by**: Claude  
**Last Updated**: 2025-11-17 (Phase G2.1-Pilot)  
**Next Update**: After G2.3 execution  
**Template**: [AUTOMATION_PLAYBOOK_TEMPLATE.md](DOCS/AUTOMATION_PLAYBOOK_TEMPLATE.md)  
**Comparison**: [PILOT_GMAIL_DRAFTS_FLOW.md](DOCS/PILOT_GMAIL_DRAFTS_FLOW.md) (OS_SAFE)
