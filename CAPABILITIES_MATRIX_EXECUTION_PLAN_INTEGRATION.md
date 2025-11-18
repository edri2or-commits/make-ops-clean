# CAPABILITIES MATRIX - Execution Plan Integration (MANDATORY GATE)

**Updated**: 2025-11-17  
**Addition**: Runtime Execution Plan as mandatory gate before any execution

---

## 🚨 Three-Gate Model: Playbook → Evals → Execution Plan

### Complete Gate Sequence

**Every capability must pass ALL three gates before Runtime execution**:

```
Gate 1: PLAYBOOK EXISTS
→ Status: PILOT_DESIGNED
→ Requirement: Complete playbook (Intent, RACI, Plan, Execution, Safeguards, etc.)
→ Reference: AUTOMATION_PLAYBOOK_TEMPLATE.md
→ Examples: PILOT_GMAIL_DRAFTS_FLOW.md, PILOT_GMAIL_SEND_FLOW.md, etc.

Gate 2: EVALS DEFINED
→ Requirement: Complete eval scenarios (Happy Path, Safeguards, Edge Cases, Failure Modes, Observability)
→ Reference: AUTOMATION_EVALS_PLAN.md
→ Coverage: 87 scenarios across 4 pilots
→ Requirement: 100% pass for upgrade to VERIFIED

Gate 3: EXECUTION PLAN EXISTS ⭐ NEW
→ Requirement: Complete execution plan (OAuth, Evals, Evidence, MATRIX update, Reporting)
→ Reference: PHASE_G2_RUNTIME_EXECUTION_PLAN.md
→ Includes: Executor RACI, Evidence collection, Failure handling
→ Requirement: Or approves execution plan before Executor begins

Only after ALL three gates:
→ Executor can begin Runtime execution
→ Evals can be run
→ Status can upgrade to VERIFIED
```

---

## 📋 Execution Plan Requirements

### What Execution Plan Provides

**Complete operational roadmap**:

```
1. Master Flow:
   - Prerequisites check
   - OAuth scope expansion
   - Test environment setup
   - Eval execution (all scenarios)
   - Evidence collection
   - Pass rate calculation
   - MATRIX update
   - PR creation
   - Or sign-off

2. Executor RACI:
   - ALLOWED operations (OAuth, tests, commits, PRs)
   - FORBIDDEN operations (skip evals, bypass gates, modify without docs)
   - Reporting format (EXECUTOR→OR_REPORT)

3. Per-Pilot Details:
   - OAuth scopes required
   - Eval execution strategy
   - Evidence formats
   - Success criteria
   - Failure handling

4. First Pilot (G2.2):
   - Gmail Drafts as detailed example
   - Step-by-step execution
   - 19 eval scenarios mapped
   - Evidence collection detailed
   - results.json format specified
```

**Reference**: [`PHASE_G2_RUNTIME_EXECUTION_PLAN.md`](../DOCS/PHASE_G2_RUNTIME_EXECUTION_PLAN.md) (26.5KB)

---

## 👤 Executor Role & Boundaries

### Executor RACI Summary

**Executor = Technical operator** (NOT Or, NOT Claude, NOT GPTs)

**ALLOWED**:
- ✅ Update MCP configs (OAuth scopes)
- ✅ Generate OAuth consent URLs
- ✅ Run eval scenarios
- ✅ Capture evidence (logs, screenshots, API responses)
- ✅ Update CAPABILITIES_MATRIX (after evals)
- ✅ Commit evidence to repo
- ✅ Create PRs for Or review
- ✅ Merge PRs after Or approval
- ✅ Report to Or (EXECUTOR→OR_REPORT format)

**FORBIDDEN**:
- ❌ Skip evals or eval scenarios
- ❌ Modify playbooks without documentation
- ❌ Bypass approval gates
- ❌ Override 100% pass requirement
- ❌ Commit without Or review (PRs required)
- ❌ Execute production operations (only test/verify)

**Or = Accountable**:
- Reviews evidence
- Approves PRs
- Signs off on VERIFIED status
- Decides: retry or block on failures

---

## 📊 Updated Status Transition Rules

### With Execution Plan Gate

**Old model** (2 gates):
```
PILOT_DESIGNED → (Evals PASS 100%) → VERIFIED
```

**New model** (3 gates) ⭐:
```
PILOT_DESIGNED
  ↓
[Gate 1] Playbook exists? YES → Continue
  ↓
[Gate 2] Evals defined? YES → Continue
  ↓
[Gate 3] Execution Plan approved? YES → Executor can begin
  ↓
[Execution] Executor runs evals (per Execution Plan)
  ↓
[Results] Pass rate = 100%? 
  YES → VERIFIED
  NO → BLOCKED
```

**Key insight**: Execution Plan prevents ad-hoc execution (everything documented before Runtime)

---

## 🔧 Phase G2.2-G2.5: Execution Status

### Current Status (Before Execution)

| Phase | Pilot | Playbook | Evals | Execution Plan | Status | Ready? |
|-------|-------|----------|-------|----------------|--------|--------|
| **G2.2** | **Gmail Drafts** | ✅ | ✅ | ✅ | PILOT_DESIGNED | ⏳ Awaiting Or GO |
| **G2.3** | **Gmail Send** | ✅ | ✅ | ✅ | PILOT_DESIGNED | After G2.2 |
| **G2.4** | **Drive Create Doc** | ✅ | ✅ | ✅ | PILOT_DESIGNED | After G2.2 |
| **G2.5** | **Calendar Focus** | ✅ | ✅ | ✅ | PILOT_DESIGNED | After G2.2 |

**All three gates passed** - ready for Executor + Or GO

---

## 📝 Example: Gmail Drafts (G2.2) - Complete Gates

### Gate 1: Playbook ✅
- File: [`PILOT_GMAIL_DRAFTS_FLOW.md`](../DOCS/PILOT_GMAIL_DRAFTS_FLOW.md) (22KB)
- Sections: Intent, RACI, Plan (14 steps), Execution Skeleton, 5 Safeguards, Observability
- Status: Complete

### Gate 2: Evals ✅
- File: [`AUTOMATION_EVALS_PLAN.md`](../DOCS/AUTOMATION_EVALS_PLAN.md) Section 1 (Gmail Drafts)
- Scenarios: 19 (5+3+4+4+3)
- Categories: Happy Path, Safeguards, Edge Cases, Failure Modes, Observability
- PASS/FAIL criteria: Clear for every scenario

### Gate 3: Execution Plan ✅
- File: [`PHASE_G2_RUNTIME_EXECUTION_PLAN.md`](../DOCS/PHASE_G2_RUNTIME_EXECUTION_PLAN.md) Section "Phase G2.2"
- OAuth scopes: gmail.readonly + gmail.compose
- Executor steps: 9 steps (OAuth → Setup → Run 19 evals → Evidence → MATRIX → PR → Report)
- Evidence format: results.json with all 19 scenarios
- Success criteria: 100% pass rate

### Next: Executor Execution
- Awaiting: Or approves Execution Plan
- Awaiting: Executor identified
- Awaiting: Or signals GO
- Then: Executor executes per plan
- Then: If 100% → VERIFIED

---

## 🔗 MATRIX Row Format (With All Gates)

### Complete Entry Format

```markdown
| From | To | Capability | Status | Playbook | Evals | Execution Plan | Eval Coverage | Last Eval | Results |
|------|----|-----------| -------|----------|-------|----------------|---------------|-----------|---------|
| Claude MCP | Gmail API | Create draft | PILOT_DESIGNED | ✅ [link] | ✅ 19 defined | ✅ [link] | 0/19 (0%) | Not run | Pending G2.2 |
```

**After G2.2 execution**:
```markdown
| From | To | Capability | Status | Playbook | Evals | Execution Plan | Eval Coverage | Last Eval | Results |
|------|----|-----------| -------|----------|-------|----------------|---------------|-----------|---------|
| Claude MCP | Gmail API | Create draft | ✅ VERIFIED | ✅ [link] | ✅ 19 defined | ✅ [link] | 19/19 (100%) | 2025-11-18 | [results.json] |
```

---

## 📋 Checklist: Before Runtime Execution

**Executor verifies ALL items before beginning**:

```
Prerequisites:
□ Playbook exists (Gate 1)
□ Evals defined (Gate 2)
□ Execution Plan exists (Gate 3)
□ Or approved Execution Plan
□ Executor identified and authorized
□ MCP server running
□ Current OAuth scopes documented
□ Repository current (no pending changes)
□ CAPABILITIES_MATRIX reflects PILOT_DESIGNED

Ready to Execute:
□ Or signals GO
□ Executor begins per Execution Plan
□ Evidence collected throughout
□ Results documented (results.json)
□ PR created for Or review
```

**If ANY item unchecked**: STOP, do not execute

---

## 🚨 Critical Reminders

### Three Gates = Three Documents

```
Every capability needs:
1. ✅ PLAYBOOK (what to do, how to do it, safeguards)
2. ✅ EVALS (how to test, pass/fail criteria, evidence)
3. ✅ EXECUTION PLAN (who executes, step-by-step, reporting)

No shortcuts. No ad-hoc execution.
Everything documented before Runtime.
```

### Executor ≠ Or

```
Executor: Technical operator (runs evals, collects evidence)
Or: Strategic approver (reviews evidence, signs off)

Clear separation of responsibilities.
Executor cannot override Or's decisions.
Or cannot execute technical operations (relies on Executor).
```

### 100% Pass Still Required

```
Execution Plan does NOT change eval requirements:
- Still need 100% pass rate
- Still need safeguards to pass
- Still need evidence collected
- Still need Or sign-off

Execution Plan just adds HOW to execute (not WHAT is required).
```

---

## 📊 Summary

**What Changed**:
- Added Gate 3: Execution Plan (mandatory before execution)
- Defined Executor RACI (clear boundaries)
- Detailed G2.2 execution (first pilot example)
- Added EXECUTOR→OR_REPORT format

**What Stayed the Same**:
- Playbook requirement (Gate 1)
- Evals requirement (Gate 2)
- 100% pass requirement
- Or approval requirement
- Evidence collection requirement

**Status**: All 4 pilots have passed all 3 gates, ready for Executor + Or GO

---

**Maintained by**: Claude  
**Last Updated**: 2025-11-17 (Execution Plan gate added)  
**Next Update**: After G2.2 execution (first pilot runtime)  
**Reference**: [`PHASE_G2_RUNTIME_EXECUTION_PLAN.md`](../DOCS/PHASE_G2_RUNTIME_EXECUTION_PLAN.md)
