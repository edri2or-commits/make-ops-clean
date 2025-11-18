# MCP – GPT Side Bridge to CAPABILITIES_MATRIX

## הקשר

בפרויקט זה, Claude Desktop עובד עם MCP וכלי ענן עבור אור.  
הקובץ `CAPABILITIES_MATRIX.md` בריפו `edri2or-commits/make-ops-clean` הוא:

- מקור האמת (SSOT) למצב היכולות והחיבורים של Claude/MCP.
- מתוחזק על ידי Claude כחלק מהלולאות שלו.
- משקף את מצב החיבורים:
  - GitHub
  - Local (Filesystem / PowerShell / Scripts)
  - **Google MCP** (Gmail / Drive / Calendar / Sheets / Docs) ⭐ **Phase G2.1-Pilot Complete (2025-11-17)**
  - GCP דרך GitHub Actions (WIF / Secret Manager / APIs)
  - ועוד כלים (Canva, Web וכו').

---

## 🆕 Phase G2.1-Pilot Complete (2025-11-17)

### Complete Framework: Pilots + Evals + Execution Plan

**Built**:
1. **4 Pilots** (144KB)
   - Gmail Drafts, Gmail Send, Drive Create Doc, Calendar Focus
2. **Eval Framework** (31.5KB)
   - 87 scenarios, 100% pass required
3. **Execution Plan** (26.5KB) ⭐ NEW
   - G2.2-G2.5 roadmap, Executor RACI, Evidence formats

**Total Documentation**: 349.5KB (complete OS_SAFE framework)

---

## 🚨 THREE-GATE MODEL (Complete)

### Mandatory Gates Before Runtime

**Every capability must pass ALL three gates**:

```
Gate 1: PLAYBOOK EXISTS
→ Requirement: Complete playbook (Intent, RACI, Plan, Safeguards, etc.)
→ Reference: AUTOMATION_PLAYBOOK_TEMPLATE.md
→ Status: PILOT_DESIGNED

Gate 2: EVALS DEFINED
→ Requirement: Complete eval scenarios (87 total)
→ Reference: AUTOMATION_EVALS_PLAN.md
→ Requirement: 100% pass for upgrade

Gate 3: EXECUTION PLAN EXISTS ⭐ NEW
→ Requirement: Complete execution roadmap
→ Reference: PHASE_G2_RUNTIME_EXECUTION_PLAN.md
→ Includes: Executor RACI, OAuth steps, Evidence formats
→ Requirement: Or approves before execution begins

Only after ALL three gates:
→ Executor can begin Runtime execution
→ Status can upgrade to VERIFIED (if evals pass 100%)
```

---

## 📋 Execution Plan Summary

### What's New (Gate 3)

**Complete operational roadmap**:
- Master flow (9 steps: OAuth → Evals → Evidence → MATRIX → PR)
- **Executor RACI** (who does what, allowed/forbidden operations)
- G2.2 detailed plan (Gmail Drafts as first pilot example)
- Evidence formats (results.json structure)
- Failure handling (what if evals fail)
- Reporting template (EXECUTOR→OR_REPORT)

**Key insight**: No ad-hoc execution - everything documented before Runtime

---

## 👤 Executor Role (NEW)

### Who Executes Runtime Phases

**Executor = Technical operator** (NOT Or, NOT Claude, NOT GPTs)

**ALLOWED**:
- ✅ Update MCP configs (OAuth scopes)
- ✅ Run eval scenarios
- ✅ Collect evidence
- ✅ Update CAPABILITIES_MATRIX (after evals)
- ✅ Create PRs for Or review
- ✅ Report results to Or

**FORBIDDEN**:
- ❌ Skip evals
- ❌ Bypass gates
- ❌ Override 100% pass requirement
- ❌ Commit without Or review

**Or = Accountable**:
- Reviews evidence
- Approves PRs
- Signs off on VERIFIED

---

## 🎯 Current Status (All 4 Pilots)

| Phase | Pilot | Playbook | Evals | Exec Plan | Status | Ready? |
|-------|-------|----------|-------|-----------|--------|--------|
| **G2.2** | **Gmail Drafts** | ✅ | ✅ | ✅ | PILOT_DESIGNED | ⏳ Awaiting Or GO |
| **G2.3** | **Gmail Send** | ✅ | ✅ | ✅ | PILOT_DESIGNED | After G2.2 |
| **G2.4** | **Drive Doc** | ✅ | ✅ | ✅ | PILOT_DESIGNED | After G2.2 |
| **G2.5** | **Calendar** | ✅ | ✅ | ✅ | PILOT_DESIGNED | After G2.2 |

**All three gates passed** - ready for Executor + Or GO signal

---

## 📊 Before Using ANY Capability

**GPTs MUST check ALL three gates**:

```
1. Check MATRIX:
   - Playbook exists? (Gate 1)
   - Evals defined? (Gate 2)
   - Execution Plan exists? (Gate 3)
   - Status: PILOT_DESIGNED or VERIFIED?

2. If PILOT_DESIGNED:
   - NOT operational yet
   - Evals not run OR not passed
   - Offer alternative (text, local file, draft)

3. If VERIFIED:
   - All gates passed ✓
   - Evals passed 100% ✓
   - Capability operational ✓
   - Check freshness (< 90 days)
   - Proceed with flow

4. If BLOCKED:
   - Evals failed
   - NOT safe to use
   - DO NOT proceed
```

---

## 🔧 G2.2-G2.5 Execution Phases

### All follow same master flow:

```
1. OAuth: Executor expands scopes
2. Setup: Verify environment
3. Evals: Run all scenarios (manual or automated)
4. Evidence: Collect results.json + logs
5. Pass Rate: Calculate (must be 100%)
6. MATRIX: Update status (VERIFIED or BLOCKED)
7. PR: Create for Or review
8. Sign-off: Or approves
9. Report: EXECUTOR→OR_REPORT
```

**First pilot**: G2.2 (Gmail Drafts) - proves execution model

---

## 📝 Example: G2.2 Gmail Drafts (Complete)

### All Three Gates ✅

**Gate 1 - Playbook**:
- File: PILOT_GMAIL_DRAFTS_FLOW.md (22KB)
- Complete: Intent, RACI, 14 steps, 5 safeguards

**Gate 2 - Evals**:
- File: AUTOMATION_EVALS_PLAN.md Section 1
- Scenarios: 19 (5+3+4+4+3)
- PASS/FAIL criteria: Clear

**Gate 3 - Execution Plan**:
- File: PHASE_G2_RUNTIME_EXECUTION_PLAN.md Section "G2.2"
- OAuth: gmail.readonly + gmail.compose
- Steps: 9 (detailed)
- Evidence: results.json format specified

### Next: Runtime Execution

- Awaiting: Or approves Execution Plan
- Awaiting: Executor identified
- Awaiting: Or signals GO
- Then: Executor executes (per plan)
- Then: If 100% → VERIFIED

---

## 🔄 Phase Tracking (Final)

### Phase G2.1-Pilot ✅ (2025-11-17):
- ✅ 4 pilots (Gmail x2, Drive x1, Calendar x1)
- ✅ Universal template (proven across 3 domains, 2 risk levels)
- ✅ Eval framework (87 scenarios)
- ✅ **Execution Plan** (G2.2-G2.5 roadmap) ⭐ NEW
- ✅ **Executor RACI** (clear boundaries) ⭐ NEW

**Status**: Complete OS_SAFE framework, ready for Runtime

### Future Phases (with Executor):
- G2.2: Gmail Drafts (19 evals, first pilot)
- G2.3: Gmail Send (26 evals, CRITICAL)
- G2.4: Drive Create Doc (21 evals)
- G2.5: Calendar Focus (21 evals)

---

## Critical Reminders for GPTs (Complete)

### 1. Three Gates = Three Checks
```
Before suggesting ANY automation:
1. ✅ Playbook exists?
2. ✅ Evals defined?
3. ✅ Execution Plan exists?
4. ✅ Status = VERIFIED?

If any NO → Capability NOT operational
```

### 2. Executor ≠ Or
```
Executor: Executes (runs evals, collects evidence)
Or: Approves (reviews evidence, signs off)

Clear separation of responsibilities.
```

### 3. 100% Pass Still Required
```
Execution Plan does NOT change:
- 100% pass rate required
- Safeguards MUST pass
- Evidence MUST be collected
- Or sign-off required

Execution Plan just adds HOW (not WHAT).
```

### 4. No Ad-Hoc Execution
```
Everything documented before Runtime:
- Playbook (what)
- Evals (how to test)
- Execution Plan (who executes, step-by-step)

No improvisation during execution.
```

---

## עדכון אחרון

**2025-11-17 (Execution Plan Complete)**:
- ✅ 4 pilots (144KB)
- ✅ Universal template (43.7KB)
- ✅ Eval framework (31.5KB)
- ✅ **Execution Plan (26.5KB)** ⭐ NEW

**Total Documentation**: 349.5KB של framework מלא

**Next**: G2.2 execution (Gmail Drafts, first pilot) - awaiting Or GO

---

**תחזוקה**: Claude (עם אישור אור)  
**עדכון אחרון**: 2025-11-17 (Execution Plan added)  
**גרסה**: 2.7 (three-gate model complete)
