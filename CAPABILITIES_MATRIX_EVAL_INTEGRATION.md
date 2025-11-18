# CAPABILITIES MATRIX - Eval Integration (MANDATORY)

**Updated**: 2025-11-17  
**Addition**: Eval Coverage as mandatory gate for all capability upgrades

---

## 🚨 CRITICAL: No Evals = No Autonomy Upgrade

### Universal Eval Gate

**Every capability MUST**:
1. ✅ Have evals defined ([`AUTOMATION_EVALS_PLAN.md`](../DOCS/AUTOMATION_EVALS_PLAN.md))
2. ✅ Run evals during execution phase
3. ✅ Pass 100% of evals (strict requirement)
4. ✅ Document evidence in OPS/EVALS/
5. ✅ Get Or's sign-off

**Status transitions**:
```
PILOT_DESIGNED → (No evals) → PILOT_DESIGNED (blocked)
PILOT_DESIGNED → (Evals PASS 100%) → VERIFIED
PILOT_DESIGNED → (Evals FAIL) → BLOCKED
```

---

## Eval Coverage Field (NEW)

### Added to Every Capability Row

**Format**:
```markdown
| Capability | Status | **Eval Coverage** | **Last Eval** | **Eval Results** |
|-----------|--------|-------------------|---------------|------------------|
| Gmail Drafts | PILOT_DESIGNED | **0/19 (0%)** | **Not run** | **Pending G2.2** |
```

**After eval execution**:
```markdown
| Capability | Status | **Eval Coverage** | **Last Eval** | **Eval Results** |
|-----------|--------|-------------------|---------------|------------------|
| Gmail Drafts | **VERIFIED** | **19/19 (100%)** | **2025-11-18** | **[results.json](../../OPS/EVALS/gmail-drafts-results.json)** |
```

---

## Four Pilots - Eval Status

| Pilot | Domain | Status | Eval Coverage | Evals Designed | Total Scenarios |
|-------|--------|--------|---------------|----------------|-----------------|
| **Gmail Drafts** | Gmail | PILOT_DESIGNED | 0/19 (0%) | ✅ Yes | 19 |
| **Gmail Send** | Gmail | PILOT_DESIGNED | 0/26 (0%) | ✅ Yes | 26 |
| **Drive Create Doc** | Drive | PILOT_DESIGNED | 0/21 (0%) | ✅ Yes | 21 |
| **Calendar Focus** | Calendar | PILOT_DESIGNED | 0/21 (0%) | ✅ Yes | 21 |
| **TOTAL** | - | - | **0/87 (0%)** | ✅ Complete | **87** |

**Status**: All evals designed, none executed (pending G2.2-G2.5)

---

## Eval Categories (Per Pilot)

### Gmail Drafts (19 scenarios)
- ✅ Happy Path: 5 scenarios
- ✅ Safeguards: 3 scenarios
- ✅ Edge Cases: 4 scenarios
- ✅ Failure Modes: 4 scenarios
- ✅ Observability: 3 scenarios

### Gmail Send (26 scenarios) ⭐ Most Critical
- ✅ Happy Path: 4 scenarios
- ✅ Safeguards: **8 scenarios** (CLOUD_OPS_HIGH)
- ✅ Edge Cases: 5 scenarios
- ✅ Failure Modes: 5 scenarios
- ✅ Observability: 4 scenarios

### Drive Create Doc (21 scenarios)
- ✅ Happy Path: 5 scenarios
- ✅ Safeguards: 5 scenarios
- ✅ Edge Cases: 4 scenarios
- ✅ Failure Modes: 4 scenarios
- ✅ Observability: 3 scenarios

### Calendar Focus (21 scenarios)
- ✅ Happy Path: 5 scenarios
- ✅ Safeguards: 5 scenarios
- ✅ Edge Cases: 4 scenarios
- ✅ Failure Modes: 4 scenarios
- ✅ Observability: 3 scenarios

---

## Safeguard Evals (CRITICAL - 100% Pass Required)

**Total safeguard scenarios**: 21 across all pilots

**Mandatory checks** (every pilot):
1. ✅ Approval gate enforced
2. ✅ Rate limiting works (if applicable)
3. ✅ Logging captures all fields
4. ✅ Scope limitations enforced
5. ✅ Policy blocks prevent forbidden operations

**Failure = BLOCKED** (no exceptions for safeguard failures)

---

## Eval Execution Phases

### Phase G2.2 (Gmail Drafts):
```
1. Executor expands OAuth → gmail.compose
2. Run 19 evals
3. Collect evidence → OPS/EVALS/gmail-drafts-results.json
4. Pass rate check:
   - 100% → Update MATRIX: PILOT_DESIGNED → VERIFIED
   - <100% → BLOCKED, fix issues, re-run
5. Or sign-off
```

### Phase G2.3 (Gmail Send):
```
1. Executor expands OAuth → gmail.send
2. Run 26 evals (CRITICAL - CLOUD_OPS_HIGH)
3. Collect evidence → OPS/EVALS/gmail-send-results.json
4. Pass rate check:
   - 100% → Update MATRIX: PILOT_DESIGNED → VERIFIED (BLOCKED)
   - <100% → BLOCKED indefinitely
5. Or sign-off
```

### Phase G2.4 (Drive Create Doc):
```
1. Executor expands OAuth → drive.file + docs.file
2. Run 21 evals
3. Collect evidence → OPS/EVALS/drive-create-doc-results.json
4. Pass rate check:
   - 100% → Update MATRIX: PILOT_DESIGNED → VERIFIED
   - <100% → BLOCKED, fix issues, re-run
5. Or sign-off
```

### Phase G2.5 (Calendar Focus):
```
1. Executor expands OAuth → calendar.events
2. Run 21 evals
3. Collect evidence → OPS/EVALS/calendar-focus-results.json
4. Pass rate check:
   - 100% → Update MATRIX: PILOT_DESIGNED → VERIFIED
   - <100% → BLOCKED, fix issues, re-run
5. Or sign-off
```

---

## Eval Evidence Storage

```
Location: OPS/EVALS/

Files:
- gmail-drafts-results.json (19 scenarios)
- gmail-send-results.json (26 scenarios)
- drive-create-doc-results.json (21 scenarios)
- calendar-focus-results.json (21 scenarios)
- screenshots/ (visual evidence if needed)
- logs/ (test execution logs)

All committed to repo (permanent audit trail)
```

---

## Example MATRIX Entry with Evals

**Before G2.2** (evals not run):
```markdown
| From | To | Capability | Status | Eval Coverage | Last Eval | Eval Results |
|------|----|-----------| -------|---------------|-----------|--------------|
| Claude MCP | Gmail API | Create draft | **PILOT_DESIGNED** | **0/19 (0%)** | **Not run** | **Pending G2.2** |
```

**After G2.2** (evals passed):
```markdown
| From | To | Capability | Status | Eval Coverage | Last Eval | Eval Results |
|------|----|-----------| -------|---------------|-----------|--------------|
| Claude MCP | Gmail API | Create draft | **✅ VERIFIED** | **19/19 (100%)** | **2025-11-18** | **[results](../../OPS/EVALS/gmail-drafts-results.json)** |
```

**If evals failed**:
```markdown
| From | To | Capability | Status | Eval Coverage | Last Eval | Eval Results |
|------|----|-----------| -------|---------------|-----------|--------------|
| Claude MCP | Gmail API | Create draft | **❌ BLOCKED** | **15/19 (79%)** | **2025-11-18** | **[results](../../OPS/EVALS/gmail-drafts-results.json)** |
```

---

## Critical Reminders

### 100% Pass Rate Required
```
🚨 NO EXCEPTIONS 🚨

Safeguard evals: 100% pass (mandatory)
Happy path evals: 100% pass (mandatory)
Edge case evals: 100% pass (mandatory)
Failure mode evals: 100% pass (mandatory)
Observability evals: 100% pass (mandatory)

Any failure = BLOCKED until fixed
```

### Eval Freshness
```
Evals older than 90 days = stale
Stale evals require re-run before production use
```

### Safeguard Priority
```
Safeguard evals are NON-NEGOTIABLE
If safeguards fail, capability is BLOCKED indefinitely
Security > Functionality
```

---

## Summary

**Total evals designed**: 87 scenarios  
**Evals executed**: 0 (pending G2.2-G2.5)  
**Pass rate required**: 100% (strict)  
**Evidence storage**: OPS/EVALS/  
**Reference**: [`AUTOMATION_EVALS_PLAN.md`](../DOCS/AUTOMATION_EVALS_PLAN.md)

**Gate enforcement**: Every capability status upgrade blocked until evals pass

---

**Maintained by**: Claude  
**Last Updated**: 2025-11-17 (Eval framework complete)  
**Next Update**: After first eval execution (G2.2)
