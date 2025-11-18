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

### 4 Pilots + Eval Framework

**Pilots בנוי**:
1. Gmail Drafts (OS_SAFE, 22KB)
2. Gmail Send (CLOUD_OPS_HIGH, 46KB)
3. Drive Create Doc (OS_SAFE, 43KB)
4. Calendar Focus (OS_SAFE, 33KB)

**Eval Framework** ⭐ NEW:
- [`AUTOMATION_EVALS_PLAN.md`](DOCS/AUTOMATION_EVALS_PLAN.md) (31.5KB)
- **87 total evals** across 4 pilots
- **100% pass required** for capability upgrade
- **No Evals = No Autonomy Upgrade**

**Total Documentation**: 323KB (pilots 144KB + template 43.7KB + evals 31.5KB + arch 103.7KB)

---

## 🚨 CRITICAL: No Evals = No Autonomy Upgrade

### Eval Gate (MANDATORY)

**Every capability MUST**:
```
1. ✅ Have evals defined (AUTOMATION_EVALS_PLAN.md)
2. ✅ Run evals (execution phase)
3. ✅ Pass 100% of evals (strict)
4. ✅ Document evidence (OPS/EVALS/)
5. ✅ Get Or's sign-off

No shortcuts. No exceptions.
```

**Status transitions**:
```
PILOT_DESIGNED → (No evals) → PILOT_DESIGNED (blocked)
PILOT_DESIGNED → (Evals PASS 100%) → VERIFIED
PILOT_DESIGNED → (Evals FAIL) → BLOCKED
```

---

## 📊 Eval Coverage (Current Status)

| Pilot | Evals Designed | Evals Run | Pass Rate | Status |
|-------|----------------|-----------|-----------|--------|
| Gmail Drafts | 19 ✅ | 0 | 0% | PILOT_DESIGNED |
| Gmail Send | 26 ✅ | 0 | 0% | PILOT_DESIGNED |
| Drive Create Doc | 21 ✅ | 0 | 0% | PILOT_DESIGNED |
| Calendar Focus | 21 ✅ | 0 | 0% | PILOT_DESIGNED |
| **TOTAL** | **87 ✅** | **0** | **0%** | **Pending G2.2-G2.5** |

**All evals designed, none executed** (awaiting Executor + Or approval)

---

## 🔍 Eval Categories (Universal)

**Every pilot has 5 categories**:

1. **Happy Path** (core functionality works)
2. **Safeguards** (all 5 layers enforced) ⭐ CRITICAL
3. **Edge Cases** (boundaries, special inputs)
4. **Failure Modes** (errors handled gracefully)
5. **Observability** (logs, state, MATRIX)

**Example breakdown**:
- Gmail Drafts: 5+3+4+4+3 = 19 scenarios
- Gmail Send: 4+**8**+5+5+4 = 26 scenarios (more safeguards for CLOUD_OPS_HIGH)
- Drive Create Doc: 5+5+4+4+3 = 21 scenarios
- Calendar Focus: 5+5+4+4+3 = 21 scenarios

---

## 🛡️ Safeguard Evals (NON-NEGOTIABLE)

**Total safeguard scenarios**: 21 across all pilots

**Mandatory checks** (every pilot):
1. ✅ Approval gate enforced (can't bypass)
2. ✅ Rate limiting works (if applicable)
3. ✅ Logging captures all fields
4. ✅ Scope limitations enforced
5. ✅ Policy blocks prevent forbidden operations

**Safeguard failure = BLOCKED** (no exceptions)

**Example safeguard evals** (Gmail Send):
- "מאשר שליחה" required (exact phrase)
- Wrong phrase blocked
- TTL (60 min) enforced
- Rate limit blocks at 10/hour
- No auto-forwarding rules
- No BCC hijacking
- Detailed logging (approval details)
- Scope: gmail.send only

---

## 📋 Before Using ANY Capability

**GPTs MUST check**:

```
1. Check CAPABILITIES_MATRIX:
   - Capability exists?
   - Status: PILOT_DESIGNED or VERIFIED?
   - Eval coverage: X/Y (Z%)?

2. If Status = PILOT_DESIGNED:
   - Evals NOT run yet
   - Capability NOT operational
   - Offer alternative (text, local file, etc.)

3. If Status = VERIFIED:
   - Evals passed (100%)
   - Capability operational
   - Check eval freshness (< 90 days)
   - Proceed with flow

4. If Status = BLOCKED:
   - Evals failed
   - Capability NOT safe
   - DO NOT use
```

**Never assume capability works** - always check MATRIX first!

---

## 🎯 Execution Phases with Evals

### Phase G2.2 (Gmail Drafts):
```
1. Executor expands OAuth → gmail.compose
2. Run 19 evals → OPS/EVALS/gmail-drafts-results.json
3. Check pass rate:
   - 100% → MATRIX: PILOT_DESIGNED → VERIFIED
   - <100% → BLOCKED, fix, re-run
4. Or sign-off
```

### Phase G2.3 (Gmail Send):
```
1. Executor expands OAuth → gmail.send
2. Run 26 evals (CRITICAL - CLOUD_OPS_HIGH)
3. Check pass rate:
   - 100% → MATRIX: PILOT_DESIGNED → VERIFIED (BLOCKED for prod)
   - <100% → BLOCKED indefinitely
4. Or sign-off
```

### Phase G2.4 (Drive Create Doc):
```
1. Executor expands OAuth → drive.file + docs.file
2. Run 21 evals
3. Check pass rate:
   - 100% → MATRIX: PILOT_DESIGNED → VERIFIED
   - <100% → BLOCKED, fix, re-run
4. Or sign-off
```

### Phase G2.5 (Calendar Focus):
```
1. Executor expands OAuth → calendar.events
2. Run 21 evals
3. Check pass rate:
   - 100% → MATRIX: PILOT_DESIGNED → VERIFIED
   - <100% → BLOCKED, fix, re-run
4. Or sign-off
```

---

## 📊 MATRIX Integration

**New field**: Eval Coverage

**Example MATRIX entries**:

**Before evals** (G2.2 not run):
```
| Capability | Status | Eval Coverage | Last Eval | Results |
|-----------|--------|---------------|-----------|---------|
| Gmail Drafts | PILOT_DESIGNED | 0/19 (0%) | Not run | Pending |
```

**After evals pass**:
```
| Capability | Status | Eval Coverage | Last Eval | Results |
|-----------|--------|---------------|-----------|---------|
| Gmail Drafts | ✅ VERIFIED | 19/19 (100%) | 2025-11-18 | [json](../../OPS/EVALS/gmail-drafts-results.json) |
```

**After evals fail**:
```
| Capability | Status | Eval Coverage | Last Eval | Results |
|-----------|--------|---------------|-----------|---------|
| Gmail Drafts | ❌ BLOCKED | 15/19 (79%) | 2025-11-18 | [json](../../OPS/EVALS/gmail-drafts-results.json) |
```

---

## 🔄 Phase Tracking (Complete)

### Phase G2.1-Pilot ✅ (2025-11-17):
- ✅ 4 pilots complete (Gmail x2, Drive x1, Calendar x1)
- ✅ Universal template proven (3 domains, 2 risk levels)
- ✅ **Eval framework complete** (87 evals designed) ⭐ NEW
- ✅ **Eval integration** (MATRIX + BRIDGE updated)

**Status**: Ready for G2.2-G2.5 execution (with Executor)

### Future Phases:
- G2.2: Gmail Drafts + 19 evals
- G2.3: Gmail Send + 26 evals (CRITICAL)
- G2.4: Drive Create Doc + 21 evals
- G2.5: Calendar Focus + 21 evals

---

## Critical Reminders for GPTs (Final)

### 1. Evals are Mandatory
```
🚨 NO EVALS = NO AUTONOMY UPGRADE 🚨

Every capability needs:
- Evals designed ✅ (done)
- Evals executed ⏳ (pending)
- 100% pass rate ⏳ (required)
- Or sign-off ⏳ (required)
```

### 2. Check MATRIX Before Every Use
```
Before suggesting ANY automation:
1. Check CAPABILITIES_MATRIX
2. Check status (PILOT_DESIGNED vs VERIFIED)
3. Check eval coverage (X/Y pass rate)
4. Only proceed if VERIFIED with 100% pass
```

### 3. Safeguards are NON-NEGOTIABLE
```
Safeguard evals MUST pass 100%
- Approval gates
- Rate limits
- Logging
- Scope restrictions
- Policy blocks

Any safeguard failure = BLOCKED indefinitely
```

### 4. Evidence is Permanent
```
All eval runs logged to OPS/EVALS/
- JSON results files
- Screenshots (if needed)
- Test execution logs
- Committed to repo (audit trail)
```

---

## עדכון אחרון

**2025-11-17 (Eval Framework Complete)**:
- ✅ 4 pilots (144KB)
- ✅ Universal template (43.7KB)
- ✅ **Eval framework (31.5KB)** ⭐ NEW
- ✅ **87 evals designed**
- ✅ **MATRIX + BRIDGE updated**

**Total Documentation**: 323KB של תיעוד מלא

**Next**: G2.2-G2.5 execution (Executor + Or approval required)

---

**תחזוקה**: Claude (עם אישור אור)  
**עדכון אחרון**: 2025-11-17 (Eval framework added)  
**גרסה**: 2.6 (evals mandatory for all upgrades)
