# CAPABILITIES MATRIX - Automation Template Entry

**Updated**: 2025-11-17  
**Addition**: Universal Automation Template

---

## New Section: Governance & Autonomy Layer

**Purpose**: This section tracks governance documents, templates, and autonomy frameworks that guide ALL automations in Claude-Ops.

### Governance Documents

| Document | Type | Purpose | Status | Mandatory For | Last Updated | Reference |
|----------|------|---------|--------|---------------|--------------|-----------|
| **AUTOMATION_PLAYBOOK_TEMPLATE** | Template | Universal template for ALL automations (any domain) | ✅ ACTIVE | Every new automation | 2025-11-17 | [AUTOMATION_PLAYBOOK_TEMPLATE.md](DOCS/AUTOMATION_PLAYBOOK_TEMPLATE.md) |
| CAPABILITIES_MATRIX | Registry | Single source of truth for all capabilities | ✅ ACTIVE | All operations | Continuous | CAPABILITIES_MATRIX.md |
| MCP_GPT_CAPABILITIES_BRIDGE | Bridge | Guidance for GPTs on using MATRIX | ✅ ACTIVE | GPT planning | Continuous | MCP_GPT_CAPABILITIES_BRIDGE.md |
| GOOGLE_AGENTS_RACI | RACI | Claude vs GPTs GO responsibilities (Google) | ✅ ACTIVE | Google operations | 2025-11-17 | [GOOGLE_AGENTS_RACI.md](DOCS/GOOGLE_AGENTS_RACI.md) |
| GOOGLE_MCP_OAUTH_ARCH | Architecture | OAuth + WIF + Safeguards for Google | ✅ ACTIVE | Google MCP setup | 2025-11-17 | [GOOGLE_MCP_OAUTH_ARCH.md](DOCS/GOOGLE_MCP_OAUTH_ARCH.md) |
| STATE_FOR_GPT_SNAPSHOT | State | Current system state snapshot | ✅ ACTIVE | All GPT interactions | Continuous | STATE_FOR_GPT_SNAPSHOT.md |

---

## AUTOMATION_PLAYBOOK_TEMPLATE - Details

**What it is**:
- Universal template for documenting ANY automation in Claude-Ops
- Covers all domains: Google, GitHub, GCP, Local, Make.com, future integrations
- Mandatory starting point before creating ANY automation
- 43.7KB comprehensive template with worked example

**Structure** (11 sections):
1. **Intent & Classification** - Clear intent statement + risk level (OS_SAFE/MEDIUM/HIGH)
2. **Actors & RACI** - Who does what (Or, Claude, GPTs GO, Executors, External)
3. **Plan** - Logical steps, risk per step, artifacts created
4. **Execution Skeleton** - Trigger, flow, tools, approval gates
5. **Safeguards** - 5 mandatory layers (approval, rate, log, scope, blocks)
6. **Observability** - Logs, status files, success/failure indicators
7. **CAPABILITIES_MATRIX Entry** - Complete row with all safeguards
8. **Example** - Gmail Drafts fully worked (Section 8, 6.5KB)
9. **Template Usage** - How to fill, when to use, checklist
10. **Integration** - How it connects to MATRIX, RACI, BRIDGE
11. **Appendix** - Quick reference (risk decision tree, safeguards, row template)

**Worked Example**: Gmail Drafts (Section 8)
- Complete Intent & Classification
- Full RACI matrix
- 14-step plan
- Execution flow with all tools
- All 5 safeguards documented
- Logging format with real JSON
- CAPABILITIES_MATRIX row ready
- Serves as pattern for all future automations

**Mandatory For**:
- ✅ Every new automation (any domain)
- ✅ Before any CLOUD_OPS_HIGH execution
- ✅ When documenting undocumented automation
- ✅ When expanding existing capability

**Key Principles**:
1. **Copy Before Create** - Copy template, fill all sections, get approval, THEN execute
2. **All 5 Safeguards** - Even OS_SAFE needs safeguards documented (just lighter)
3. **MATRIX Integration** - Every automation MUST have CAPABILITIES_MATRIX entry
4. **Risk-Based** - Different requirements for OS_SAFE vs CLOUD_OPS_HIGH
5. **Worked Example** - Gmail Drafts shows exactly how to fill template

**Template Checklist** (from Section 9.4):
- [ ] All 9 sections filled completely
- [ ] RACI matrix shows who does what
- [ ] Risk level clearly determined and justified
- [ ] All 5 safeguards documented
- [ ] Logging format specified
- [ ] CAPABILITIES_MATRIX entry ready
- [ ] Or reviewed and approved (before CLOUD_OPS_HIGH)

---

## Impact on Existing Capabilities

**Going forward**:
- All NEW capabilities MUST use AUTOMATION_PLAYBOOK_TEMPLATE
- Existing capabilities: Gradually document using template (priority: CLOUD_OPS_HIGH first)
- CAPABILITIES_MATRIX entries: Must reference playbook document
- No automation is "complete" without playbook

**Current Status**:
- Gmail Drafts: ✅ Has playbook (PILOT_GMAIL_DRAFTS_FLOW.md) - follows template structure
- Gmail Send: ⏳ Will use template (copy Gmail Drafts, adjust for CLOUD_OPS_HIGH)
- Drive operations: ⏳ Will use template
- Calendar operations: ⏳ Will use template
- All future: 📋 MUST use template

**Enforcement**:
- Claude checks CAPABILITIES_MATRIX before planning automation
- If no playbook referenced → Create using template first
- GPTs consult BRIDGE → BRIDGE references template requirement
- Or's approval gate includes "Does this have playbook?" check

---

## Template Evolution

**Version**: 1.0 (2025-11-17)

**Future updates**:
- Template may be extended (sections added) based on lessons learned
- Never reduced (safeguards only increase, never decrease)
- Version number in template header
- All automations reference template version used

**Feedback loop**:
- As automations are built, lessons learned → template updates
- Template becomes more comprehensive over time
- Examples added (currently: Gmail Drafts, future: CLOUD_OPS_HIGH examples)

---

## Quick Reference for GPTs

**When planning automation**:
```
1. Check: Does automation exist in CAPABILITIES_MATRIX?
   - YES → Check status (Verified/Broken?)
   - NO → Must create using AUTOMATION_PLAYBOOK_TEMPLATE

2. Copy template:
   DOCS/AUTOMATION_PLAYBOOK_TEMPLATE.md
   → DOCS/[AUTOMATION_NAME]_PLAYBOOK.md

3. Fill all 9 sections (use Gmail Drafts Section 8 as guide)

4. Create CAPABILITIES_MATRIX entry (Section 7 format)

5. Get Or's approval (show complete playbook)

6. Only then: Execute (if CLOUD_OPS_HIGH)

7. After execution: Update MATRIX status, log to OPS/LOGS/
```

**Decision tree**:
```
User requests automation
  ↓
Check CAPABILITIES_MATRIX
  ├─ Exists + VERIFIED → Use it
  ├─ Exists + BROKEN → Fix, update playbook
  └─ Not exists → Create playbook using template
      ↓
      Copy AUTOMATION_PLAYBOOK_TEMPLATE.md
      ↓
      Fill all sections
      ↓
      Add to CAPABILITIES_MATRIX
      ↓
      Get Or approval
      ↓
      Execute (if approved + CLOUD_OPS_HIGH)
```

---

**Maintained by**: Claude  
**Last Updated**: 2025-11-17  
**Template**: [AUTOMATION_PLAYBOOK_TEMPLATE.md](DOCS/AUTOMATION_PLAYBOOK_TEMPLATE.md)  
**Example**: Gmail Drafts (Section 8 in template)
