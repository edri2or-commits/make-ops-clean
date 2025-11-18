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

### Complete Framework: 4 Documents

**Built** (383.5KB total):
1. **4 Pilots** (144KB)
   - Gmail Drafts, Gmail Send, Drive Create Doc, Calendar Focus
2. **Eval Framework** (31.5KB)
   - 87 scenarios, 100% pass required
3. **Execution Plan** (26.5KB)
   - G2.2-G2.5 roadmap, Executor RACI, Evidence formats
4. **Executor Onboarding Kit** (34KB) ⭐ NEW
   - Practical guide for Executor
   - Quickstart, Checklists, Templates, Guardrails

**Status**: Complete OS_SAFE framework, ready for Executor + Runtime

---

## 📚 Four-Document Model (MANDATORY)

### Complete Documentation Before Runtime

```
Document 1: PLAYBOOK
→ What to do, how to do it, safeguards
→ Gate 1: Playbook exists

Document 2: EVALS
→ How to test, PASS/FAIL criteria, evidence
→ Gate 2: Evals defined (100% pass required)

Document 3: EXECUTION PLAN
→ Who executes, step-by-step, reporting
→ Gate 3: Execution Plan approved by Or

Document 4: EXECUTOR ONBOARDING KIT ⭐ NEW
→ Practical onboarding for Executor
→ Prerequisite: Executor reads before starting
→ Reference: G2_EXECUTOR_ONBOARDING_KIT.md

All four documents = Complete Runtime readiness
```

---

## 🎓 Executor Onboarding Kit (NEW)

### What It Provides (34KB)

**Complete practical guide**:

```
Section 1: Context & Overview
- What's already done (383.5KB framework)
- What G2.2-G2.5 means (Executor language)
- Three-gate model explained

Section 2: Quickstart G2.2 (Gmail Drafts)
- BEFORE/DURING/AFTER checklists
- 9 steps detailed (OAuth → Report)
- Direct links to all docs

Section 3: Patterns for G2.3-G2.5
- Universal 9-step model
- Phase-specific differences

Section 4: Communication & Reporting
- EXECUTOR→OR_REPORT template (complete)
- Report checklist (must-have items)
- OPS/EVALS and OPS/LOGS usage

Section 5: Guardrails & Boundaries
- ALLOWED: OAuth, evals, commits, PRs
- FORBIDDEN: Skip evals, bypass gates
- Escalation paths (when to contact Or)
```

**Reference**: [`G2_EXECUTOR_ONBOARDING_KIT.md`](DOCS/G2_EXECUTOR_ONBOARDING_KIT.md)

---

## 🚨 Three-Gate Model + Executor Prerequisite

### Before Runtime Execution

**Three gates** (must pass):
```
Gate 1: PLAYBOOK EXISTS ✅
Gate 2: EVALS DEFINED ✅
Gate 3: EXECUTION PLAN APPROVED ✅
```

**Executor prerequisite** (before execution):
```
Prerequisite: EXECUTOR ONBOARDED ⭐
→ Executor reads G2_EXECUTOR_ONBOARDING_KIT.md
→ Executor verifies checklist (all items)
→ Executor confirms understanding
→ Or verifies Executor ready
→ Or signals GO

Only then: Executor begins Runtime execution
```

---

## 👤 Executor Role Summary

**Executor = Technical operator** (NOT Or, NOT Claude, NOT GPTs)

**ALLOWED**:
- ✅ OAuth management (configs, consent, tokens)
- ✅ Test execution (all evals, evidence, results)
- ✅ Repository operations (branches, MATRIX, commits, PRs)
- ✅ Reporting (EXECUTOR→OR_REPORT format)
- ✅ Environment management (verify health, directories)

**FORBIDDEN**:
- ❌ Skip evals/safeguards/gates
- ❌ Modify docs without approval
- ❌ Bypass 100% pass requirement
- ❌ Execute without Or GO
- ❌ Make strategic decisions

**Or = Accountable** (strategic approver):
- Reviews evidence
- Approves PRs
- Signs off on VERIFIED

---

## 🎯 Current Status (All 4 Pilots)

| Phase | Playbook | Evals | Exec Plan | Onboarding | Status | Executor Ready? |
|-------|----------|-------|-----------|------------|--------|-----------------|
| **G2.2** | ✅ | ✅ | ✅ | ✅ | PILOT_DESIGNED | ⏳ Awaiting Executor + Or GO |
| **G2.3** | ✅ | ✅ | ✅ | ✅ | PILOT_DESIGNED | After G2.2 |
| **G2.4** | ✅ | ✅ | ✅ | ✅ | PILOT_DESIGNED | After G2.2 |
| **G2.5** | ✅ | ✅ | ✅ | ✅ | PILOT_DESIGNED | After G2.2 |

**All prerequisites met** - ready for Executor onboarding + execution

---

## 📊 Before Using ANY Capability

**GPTs MUST check**:

```
1. Three gates passed?
   - Playbook ✅
   - Evals ✅
   - Execution Plan ✅

2. Executor onboarded?
   - Read Onboarding Kit ✅
   - Verified checklist ✅
   - Or confirmed ready ✅

3. Status check:
   - PILOT_DESIGNED → NOT operational
   - VERIFIED → Operational (evals passed 100%)
   - BLOCKED → NOT safe to use

If NOT VERIFIED: Offer alternative (text, local, draft)
```

---

## 🔧 G2.2-G2.5: Universal Execution Flow

**All phases follow same 9 steps**:

```
1. OAuth: Executor expands scopes
2. Setup: Verify environment
3. Evals: Run all scenarios (19-26)
4. Evidence: Collect results.json + logs
5. Pass Rate: Calculate (must be 100%)
6. MATRIX: Update status
7. PR: Create for Or review
8. Sign-off: Or approves
9. Report: EXECUTOR→OR_REPORT

First pilot (G2.2) proves model.
Subsequent pilots (G2.3-G2.5) follow same pattern.
```

---

## 🔄 Phase Tracking (Final)

### Phase G2.1-Pilot ✅ (2025-11-17):
- ✅ 4 pilots (Gmail x2, Drive, Calendar)
- ✅ Universal template (3 domains, 2 risk levels)
- ✅ Eval framework (87 scenarios)
- ✅ Execution Plan (G2.2-G2.5 roadmap)
- ✅ **Executor Onboarding Kit** (practical guide) ⭐ NEW

**Total**: 383.5KB של framework מלא

### Future Phases (with Executor):
- G2.2: Gmail Drafts (19 evals, first pilot)
- G2.3: Gmail Send (26 evals, CRITICAL)
- G2.4: Drive Create Doc (21 evals)
- G2.5: Calendar Focus (21 evals)

---

## Critical Reminders for GPTs (Final)

### 1. Four Documents Required
```
Before Runtime:
1. ✅ Playbook exists
2. ✅ Evals defined
3. ✅ Execution Plan approved
4. ✅ Executor onboarded ⭐ NEW

All four = Ready for execution
```

### 2. Executor Must Read Onboarding Kit
```
No execution without:
- Executor reads G2_EXECUTOR_ONBOARDING_KIT.md (34KB)
- Executor verifies checklist
- Or confirms Executor ready
- Or signals GO
```

### 3. Status Determines Capability
```
PILOT_DESIGNED: NOT operational (evals not run)
VERIFIED: Operational (evals passed 100%)
BLOCKED: NOT safe (evals failed)

Always check MATRIX status before use.
```

### 4. Executor ≠ Or
```
Executor: Technical operator (executes)
Or: Strategic approver (reviews, approves)

Executor cannot:
- Skip evals
- Bypass gates
- Make strategic decisions
- Execute without Or GO
```

---

## עדכון אחרון

**2025-11-17 (Executor Onboarding Kit Complete)**:
- ✅ 4 pilots (144KB)
- ✅ Universal template (43.7KB)
- ✅ Eval framework (31.5KB)
- ✅ Execution Plan (26.5KB)
- ✅ **Executor Onboarding Kit (34KB)** ⭐ NEW

**Total Documentation**: 383.5KB של framework מלא

**Next**: Executor onboarding → G2.2 execution (Gmail Drafts, first pilot)

---

**תחזוקה**: Claude (עם אישור אור)  
**עדכון אחרון**: 2025-11-17 (Executor Onboarding Kit added)  
**גרסה**: 2.8 (four-document model complete)
