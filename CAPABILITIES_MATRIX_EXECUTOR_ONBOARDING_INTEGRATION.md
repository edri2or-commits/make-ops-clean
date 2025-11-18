# CAPABILITIES MATRIX - Executor Onboarding Integration

**Updated**: 2025-11-17  
**Addition**: Executor Onboarding Kit as mandatory prerequisite for Runtime execution

---

## 🎓 Four-Document Model (Complete Framework)

### Complete Documentation Before Runtime

**Every Runtime execution requires ALL four documents**:

```
Document 1: PLAYBOOK
→ What to do, how to do it, safeguards
→ Template: AUTOMATION_PLAYBOOK_TEMPLATE.md
→ Examples: 4 pilots (Gmail x2, Drive, Calendar)
→ Gate 1: Playbook exists

Document 2: EVALS
→ How to test, PASS/FAIL criteria, evidence
→ Reference: AUTOMATION_EVALS_PLAN.md
→ 87 scenarios across 4 pilots
→ Gate 2: Evals defined (100% pass required)

Document 3: EXECUTION PLAN
→ Who executes, step-by-step roadmap, reporting
→ Reference: PHASE_G2_RUNTIME_EXECUTION_PLAN.md
→ Includes: Executor RACI, OAuth, Evidence formats
→ Gate 3: Execution Plan approved by Or

Document 4: EXECUTOR ONBOARDING KIT ⭐ NEW
→ Practical onboarding for Executor
→ Reference: G2_EXECUTOR_ONBOARDING_KIT.md
→ Includes: Quickstart, Checklists, Templates, Guardrails
→ Prerequisite: Executor reads before starting

All four documents = Complete Runtime readiness
```

---

## 📚 Executor Onboarding Kit Summary

### What It Provides

**Complete practical guide** (34KB):

```
Section 1: Context & Overview
- What's already done (349.5KB framework)
- What G2.2-G2.5 means (Executor language)
- Three-gate model explained
- Key documents bookmarked

Section 2: Quickstart G2.2 (Gmail Drafts)
- BEFORE/DURING/AFTER checklists
- 9 steps detailed (OAuth → Report)
- Direct links to all relevant docs
- Step-by-step execution guide

Section 3: Patterns for G2.3-G2.5
- Universal 9-step model
- What stays same vs changes
- Phase-specific differences
- Time estimates per phase

Section 4: Communication & Reporting
- Complete EXECUTOR→OR_REPORT template
- Report checklist (must-have items)
- OPS/EVALS and OPS/LOGS usage
- Evidence documentation

Section 5: Guardrails & Boundaries
- ALLOWED operations (OAuth, evals, commits, PRs)
- FORBIDDEN operations (skip evals, bypass gates)
- Strategic responsibility (Or decides, Executor executes)
- Escalation paths (when to contact Or)
```

**Reference**: [`G2_EXECUTOR_ONBOARDING_KIT.md`](../DOCS/G2_EXECUTOR_ONBOARDING_KIT.md) (34KB)

---

## 👤 Executor Prerequisite Checklist

### Before ANY Phase Execution

**Executor must verify**:

```
□ Read: G2_EXECUTOR_ONBOARDING_KIT.md (complete)
□ Read: PILOT_[NAME]_FLOW.md (relevant playbook)
□ Read: AUTOMATION_EVALS_PLAN.md (eval scenarios)
□ Read: PHASE_G2_RUNTIME_EXECUTION_PLAN.md (execution roadmap)
□ Bookmarked: All 4 key documents
□ Understood: Three-gate model (Playbook + Evals + Execution Plan)
□ Understood: ALLOWED/FORBIDDEN boundaries
□ Understood: EXECUTOR→OR_REPORT format
□ Understood: 100% pass requirement (no exceptions)
□ Understood: Safeguard priority (CRITICAL)
□ Access verified: Claude Desktop, GitHub, Or communication
□ Or approval: Explicit GO signal received (chat/email)

If ANY item unchecked: STOP, complete before execution
```

---

## 🔗 Documentation Links (Executor Reference)

### All Four Documents

| # | Document | Purpose | Size | Link |
|---|----------|---------|------|------|
| 1 | **Playbooks** | What to do | 144KB | [PILOT_GMAIL_DRAFTS_FLOW.md](../DOCS/PILOT_GMAIL_DRAFTS_FLOW.md) etc. |
| 2 | **Evals** | How to test | 31.5KB | [AUTOMATION_EVALS_PLAN.md](../DOCS/AUTOMATION_EVALS_PLAN.md) |
| 3 | **Execution Plan** | How to execute | 26.5KB | [PHASE_G2_RUNTIME_EXECUTION_PLAN.md](../DOCS/PHASE_G2_RUNTIME_EXECUTION_PLAN.md) |
| 4 | **Onboarding Kit** | Practical guide | 34KB | [G2_EXECUTOR_ONBOARDING_KIT.md](../DOCS/G2_EXECUTOR_ONBOARDING_KIT.md) ⭐ |

**Total**: 236KB of Executor-facing documentation

---

## 📋 Updated Gate Model

### Four-Gate Model (with Onboarding)

**Old model** (3 gates):
```
Gate 1: Playbook
Gate 2: Evals
Gate 3: Execution Plan
→ Executor begins
```

**New model** (3 gates + 1 prerequisite) ⭐:
```
Gate 1: Playbook exists ✅
Gate 2: Evals defined ✅
Gate 3: Execution Plan approved ✅
  ↓
Prerequisite: Executor Onboarding ⭐ NEW
  - Executor reads G2_EXECUTOR_ONBOARDING_KIT.md
  - Executor verifies checklist
  - Executor confirms understanding
  - Or verifies Executor ready
  ↓
Runtime Execution Begins
  - Executor follows 9-step plan
  - Evidence collected
  - Report submitted
```

**Key change**: Onboarding Kit is prerequisite, not a gate (doesn't block documentation, blocks execution)

---

## 🎯 Governance Integration

### Executor Governance

**New section in CAPABILITIES_MATRIX**:

```
Executor Role:
- Technical operator (NOT Or, NOT Claude, NOT GPTs)
- Executes G2.2-G2.5 phases per documented plans
- Requirements: Read Onboarding Kit, verify checklist, get Or GO
- Boundaries: ALLOWED (OAuth, evals, commits, PRs) / FORBIDDEN (skip evals, bypass gates)
- Reporting: EXECUTOR→OR_REPORT format (mandatory)
- Accountability: Or approves (strategic), Executor executes (operational)

Onboarding Requirement:
- Document: G2_EXECUTOR_ONBOARDING_KIT.md (34KB)
- Mandatory: Read before any phase execution
- Verification: Executor confirms understanding, Or verifies readiness
- No execution without onboarding completion
```

---

## 📊 Current Status (All 4 Pilots)

| Phase | Pilot | Playbook | Evals | Exec Plan | Onboarding | Status | Executor Ready? |
|-------|-------|----------|-------|-----------|------------|--------|-----------------|
| **G2.2** | **Gmail Drafts** | ✅ | ✅ | ✅ | ✅ | PILOT_DESIGNED | ⏳ Awaiting Executor + Or GO |
| **G2.3** | **Gmail Send** | ✅ | ✅ | ✅ | ✅ | PILOT_DESIGNED | After G2.2 |
| **G2.4** | **Drive Doc** | ✅ | ✅ | ✅ | ✅ | PILOT_DESIGNED | After G2.2 |
| **G2.5** | **Calendar** | ✅ | ✅ | ✅ | ✅ | PILOT_DESIGNED | After G2.2 |

**All prerequisites met** - ready for Executor onboarding + execution

---

## 🚀 Next Steps (Executor Path)

### Path to G2.2 Execution

```
Current State:
✅ 4 documents complete (Playbooks, Evals, Execution Plan, Onboarding Kit)
✅ 3 gates passed (for all 4 pilots)
✅ Onboarding Kit created (practical guide ready)

Next Steps:
1. Or identifies Executor (person/agent authorized)
2. Executor reads G2_EXECUTOR_ONBOARDING_KIT.md (34KB)
3. Executor verifies prerequisite checklist
4. Executor confirms understanding (to Or)
5. Or verifies Executor readiness
6. Or signals GO for G2.2 (explicit approval)
7. Executor begins G2.2 (follows 9-step plan)
8. Executor reports results (EXECUTOR→OR_REPORT)
9. Or reviews evidence, approves PR
10. Gmail Drafts → VERIFIED (if 100% pass)

First pilot (G2.2) proves execution model.
Subsequent pilots (G2.3-G2.5) follow same pattern.
```

---

## 🔐 Security & Safety (Executor Focus)

### Executor Guardrails (from Onboarding Kit)

**ALLOWED**:
```
✅ OAuth: Update configs, generate consent URLs, verify tokens
✅ Tests: Run all evals, capture evidence, document results
✅ Repository: Create branches, update MATRIX (after 100%), commit evidence, create PRs, merge (after Or approval)
✅ Reporting: Send EXECUTOR→OR_REPORT, explain failures, suggest fixes
✅ Environment: Verify MCP health, check directories, ensure prerequisites
```

**FORBIDDEN**:
```
❌ Skip: Evals, safeguards, gates, 100% requirement, Or approval, evidence collection
❌ Modify: Playbooks (without PR), evals (without docs), MATRIX (without evidence), policy, logs
❌ Execute: Without Or GO, without OR review, production ops, beyond test scope
❌ Falsify: Results, failures, evidence, safeguard outcomes, blockers
❌ Decide: Strategic decisions, permanent blocks, architecture changes, policy changes
```

**Escalation**:
```
IMMEDIATE (don't wait):
🚨 Safeguard failure
🚨 Security concern
🚨 Data leak/privacy violation
🚨 Scope escalation
🚨 MCP/OAuth malfunction
🚨 Unclear instructions

ROUTINE (in report):
- Eval failures (<100%)
- Blocker issues
- Documentation gaps
- Questions about next steps
```

---

## 📋 Summary

**What Changed**:
- Added Document 4: Executor Onboarding Kit (34KB)
- Added Executor prerequisite checklist
- Added onboarding requirement before execution
- Added governance section (Executor role)

**What Stayed the Same**:
- Three-gate model (Playbook + Evals + Execution Plan)
- 100% pass requirement
- Or approval requirement
- Evidence collection requirement

**Status**: Complete framework (4 documents, 383.5KB total), ready for Executor onboarding + Runtime execution

---

**Maintained by**: Claude  
**Last Updated**: 2025-11-17 (Executor Onboarding Kit added)  
**Next Update**: After G2.2 execution (first pilot Runtime)  
**Reference**: [`G2_EXECUTOR_ONBOARDING_KIT.md`](../DOCS/G2_EXECUTOR_ONBOARDING_KIT.md)
