# INDEX FOR GPT-CEO

**Purpose**: Master index for GPT-CEO to quickly locate essential documentation  
**Created**: 2025-11-18  
**Version**: 1.0  
**Status**: ✅ Active

---

## 🎯 START HERE

**First-Time Setup**:
1. Read `CAPABILITIES_MATRIX.md` (v1.3.0) - Your single source of truth
2. Read `GPT_CEO_ROUTING_CHEAT_SHEET.md` - Quick decision guide
3. Read `FLOW_001_GPT_CEO_GITHUB_ROUTING.md` - GitHub operations
4. Read `FLOW_002_GPT_CEO_GOOGLE_ROUTING.md` - Google operations

**Daily Operations**:
- Check `CAPABILITIES_MATRIX.md` before ANY operation
- Use Cheat Sheet for routing decisions
- Reference FLOW docs for execution patterns

---

## 📚 Core Documentation (Priority Order)

### 1. **CAPABILITIES_MATRIX.md** ⭐ MOST IMPORTANT
- **Path**: `/CAPABILITIES_MATRIX.md`
- **Version**: 1.3.0
- **Purpose**: Single source of truth for all capabilities
- **When to Read**: Before EVERY operation involving tools/integrations
- **Key Sections**:
  - Section 1: GitHub (MCP + GitHub Actions)
  - Section 2: Cloud Run / API Services
  - Section 3: Google Workspace (MCP)
  - Section 4: Local Windows Operations
  - Section 5: Additional Tools

### 2. **GPT_CEO_ROUTING_CHEAT_SHEET.md** ⭐ QUICK REFERENCE
- **Path**: `/DOCS/GPT_CEO_ROUTING_CHEAT_SHEET.md`
- **Purpose**: Fast routing decisions for GPT-CEO
- **When to Read**: When unsure how to handle a request
- **Contains**:
  - Decision matrix
  - Approval requirements
  - Status indicators (Ready/Planned/Unavailable)

### 3. **FLOW_001_GPT_CEO_GITHUB_ROUTING.md**
- **Path**: `/DOCS/FLOW_001_GPT_CEO_GITHUB_ROUTING.md`
- **Purpose**: GitHub operations routing and patterns
- **When to Read**: For any GitHub-related request
- **Covers**:
  - Pattern A: Simple File Update (DOCS/STATE/logs)
  - Pattern B: Code Change via PR
  - Approval requirements
  - Execution examples

### 4. **FLOW_002_GPT_CEO_GOOGLE_ROUTING.md**
- **Path**: `/DOCS/FLOW_002_GPT_CEO_GOOGLE_ROUTING.md`
- **Purpose**: Google operations routing and patterns
- **When to Read**: For any Google Workspace request
- **Covers**:
  - Pattern A: Read Operation (Gmail/Drive/Calendar)
  - Pattern B: Write Operation Design (Awaiting OAuth)
  - Pilot templates for future expansion

---

## 📂 Supporting Documentation

### PILOT Templates (Future Operations)
- `DOCS/PILOT_GMAIL_SEND_FLOW.md` - Gmail send workflow design
- `DOCS/PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md` - Drive create workflow
- `DOCS/PILOT_CALENDAR_FOCUS_EVENT_FLOW.md` - Calendar event creation

### Logging & Evidence
- `logs/LOG_CAPABILITIES_MATRIX_ROLE_FIELDS_UPDATE_V2.md` - Role field definitions
- `logs/LOG_*.md` - Various operation logs

### System Understanding
- `MCP_CAPABILITIES_SSOT_FOR_CLAUDE.md` - MCP capabilities overview
- `QUICK_REFERENCE.md` - User profile and quick facts
- `SYSTEM_STATUS.md` - Current system status
- `DECISION_LOG.md` - Decision history

---

## 🔄 Decision Flow for GPT-CEO

```
User Request
     ↓
┌─────────────────────────┐
│ 1. Check Domain         │
│ (GitHub/Google/Local)   │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ 2. Read CAPS_MATRIX     │
│ Find exact capability   │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ 3. Check GPT Ready?     │
│ (from Cheat Sheet)      │
└───────────┬─────────────┘
            ↓
    ┌───────┴───────┐
    │               │
    ↓               ↓
✅ Ready        📋 Planned
    │               │
    ↓               ↓
Execute         Design Playbook
via Claude      + Present to Or
    │               │
    ↓               ↓
Report          Explain Timeline
```

---

## 🎓 Key Principles

### 1. Single Source of Truth
**CAPABILITIES_MATRIX.md is ALWAYS the truth**
- If memory conflicts with CAPS_MATRIX → CAPS_MATRIX wins
- Never guess capabilities → Check the matrix
- Update matrix when capabilities change

### 2. Role-Based Routing
**Check these fields in CAPABILITIES_MATRIX**:
- **Claude Ready?** - Can Claude execute now?
- **GPT-CEO Ready?** - Can GPT direct this operation?
- **Approval Required?** - Does Or need to approve?

### 3. Transparency Over Execution
**Better to be honest than to pretend**:
- ✅ "This is designed but awaiting OAuth" - GOOD
- ❌ "I'll do that" (when status is Planned) - BAD
- ✅ "I can design the playbook now" - GOOD

### 4. Design Over Wait
**If Planned status**:
1. Create playbook immediately
2. Present to Or with timeline
3. Offer alternatives if available
4. Reference existing PILOT templates

---

## 🚦 Quick Status Reference

### GitHub Operations
- ✅ **Ready Now**: All read/write via Claude MCP
- 📋 **Design Phase**: Workflow orchestration patterns
- 🚫 **Not Available**: None

### Google Operations
- ✅ **Ready Now**: Read-only (Gmail/Drive/Calendar)
- 📋 **Design Phase**: Write operations (awaiting OAuth)
- 🚫 **Not Available**: Direct API calls, Sheets/Docs MCP

### Local Desktop
- ⚠️ **Via Claude**: GPT can request, Claude executes
- 🚫 **Not Available**: Direct GPT access (architectural limit)

### Cloud Run / API
- ⚠️ **Unverified**: Code exists, deployment untested
- 🚫 **Do Not Use**: Use direct GitHub MCP instead

---

## 📊 Capability Coverage Matrix

| Domain | Read | Write | GPT Direct? | Notes |
|--------|------|-------|-------------|-------|
| **GitHub** | ✅ | ✅ | Yes | Via Claude MCP |
| **Gmail** | ✅ | 📋 | Yes | Write awaits OAuth |
| **Drive** | ✅ | 📋 | Yes | Write awaits OAuth |
| **Calendar** | ✅ | 📋 | Yes | Write awaits OAuth |
| **Local Files** | ✅ | ✅ | No* | Via Claude proxy |
| **PowerShell** | ✅ | ⚠️ | No* | Via Claude proxy |
| **Sheets** | ❌ | ❌ | No | MCP not configured |
| **Docs** | ❌ | ❌ | No | MCP not configured |

*GPT can request, Claude executes and reports back

---

## 🔍 Finding Specific Information

### "How do I handle a request to update GitHub?"
→ Read `FLOW_001_GPT_CEO_GITHUB_ROUTING.md`

### "Can I send an email via Gmail?"
→ Check `CAPABILITIES_MATRIX.md` Section 3 → Status: Planned
→ Read `DOCS/PILOT_GMAIL_SEND_FLOW.md` for design template

### "User wants me to read a local file"
→ Check `CAPABILITIES_MATRIX.md` Section 4
→ Request Claude to read via Filesystem MCP
→ Claude reports back to GPT

### "What approval do I need for X?"
→ Read `GPT_CEO_ROUTING_CHEAT_SHEET.md` → Approval Reference

### "Is Cloud Run API ready?"
→ Check `CAPABILITIES_MATRIX.md` Section 2 → Status: 🔍 Unverified
→ Recommendation: DO NOT USE, use GitHub MCP instead

---

## 🛠️ Common Operations Quick Links

### GitHub Operations
- **Simple file update**: FLOW_001 → Pattern A
- **Code change**: FLOW_001 → Pattern B
- **Create issue**: Direct via Claude MCP
- **Search repos**: Direct via Claude MCP

### Google Operations
- **Search Gmail**: Direct via Claude MCP (read-only)
- **Read Drive doc**: Direct via Claude MCP (read-only)
- **Send email**: PILOT_GMAIL_SEND_FLOW (design only)
- **Create event**: PILOT_CALENDAR_FOCUS_EVENT_FLOW (design only)

### Local Operations
- **Read file**: Request Claude → Claude uses Filesystem MCP
- **Run PowerShell**: Request Claude → Claude uses ps_exec MCP
- **Take screenshot**: Request Claude → Claude uses ps_exec screenshot

---

## 📝 Update Procedure

When capabilities change:
1. Update `CAPABILITIES_MATRIX.md` first
2. Update relevant FLOW docs
3. Update `GPT_CEO_ROUTING_CHEAT_SHEET.md`
4. Update this INDEX if structure changes
5. Create log entry in `logs/`

---

## ⚠️ Critical Reminders

1. **NEVER guess capabilities** - Always check CAPS_MATRIX
2. **NEVER just acknowledge** - Either execute or design
3. **ALWAYS verify status** before promising execution
4. **ALWAYS check GPT-CEO Ready column** in matrix
5. **NEVER use unverified services** (e.g., Cloud Run API)
6. **ALWAYS be transparent** about limitations

---

## 🔗 External References

- **GitHub Repo**: edri2or-commits/make-ops-clean
- **GCP Project**: edri2or-mcp
- **User**: edri2or@gmail.com
- **Location**: Tel Aviv, Israel
- **Timezone**: Asia/Jerusalem (IST)

---

## 📞 Escalation Path

When stuck:
1. Check CAPABILITIES_MATRIX.md
2. Check GPT_CEO_ROUTING_CHEAT_SHEET.md
3. Check relevant FLOW doc
4. If still unclear → Ask Or for clarification
5. Never proceed with uncertain operations

---

**Remember**: This index is your roadmap. The CAPABILITIES_MATRIX is your compass. Together they ensure accurate, transparent, and effective operations.

**Last Updated**: 2025-11-18  
**Maintained By**: Claude (on behalf of GPT-CEO operational needs)  
**Next Review**: When CAPABILITIES_MATRIX updates
