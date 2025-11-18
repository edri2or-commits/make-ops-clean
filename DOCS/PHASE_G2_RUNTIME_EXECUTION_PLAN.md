# Phase G2 Runtime Execution Plan (G2.2-G2.5)

**Document Type**: Execution Planning (OS_SAFE design only)  
**Created**: 2025-11-17  
**Status**: 📝 EXECUTION_PLANNED  
**Purpose**: Define complete runtime execution workflow for all 4 pilots with Executor RACI

---

## 🎯 Purpose & Scope

### What This Document Provides

**Complete execution roadmap** for moving pilots from PILOT_DESIGNED → VERIFIED:

```
Current State:
- 4 pilots designed (Gmail Drafts, Gmail Send, Drive Doc, Calendar Focus)
- 87 evals designed (all scenarios documented)
- Template proven (universal across domains/risk levels)
- Everything OS_SAFE (documentation only)

This Plan:
- HOW to execute G2.2-G2.5 phases
- WHO executes (Executor RACI)
- WHAT gets run (OAuth, Evals, Evidence)
- WHERE results stored (OPS/EVALS/)
- WHEN MATRIX updates (after 100% pass)

Next State (after execution):
- Pilots VERIFIED (if evals pass 100%)
- Evidence committed (permanent audit trail)
- MATRIX updated (reflects operational reality)
- Ready for production use (with Or approval)
```

**Critical principle**: **No execution without this plan approved by Or**

---

## 📋 Universal Execution Flow

### Master Flow (applies to ALL phases)

```
START
  ↓
[Phase Prerequisites]
  - Playbook exists (PILOT_DESIGNED status)
  - Evals defined (AUTOMATION_EVALS_PLAN.md)
  - Executor identified and authorized
  - Or approves execution (GO signal)
  ↓
[Executor: OAuth Scope Expansion]
  - Update MCP config with new scopes
  - Generate OAuth consent URL
  - Or clicks URL (one-time consent)
  - Verify token works (test read operation)
  ↓
[Executor: Test Environment Setup]
  - Verify MCP server running
  - Verify OAuth token valid
  - Verify logs directory exists
  - Verify MATRIX is current
  ↓
[Executor: Run Evals]
  For each eval scenario (19-26 scenarios):
    1. Execute scenario (manual or automated)
    2. Capture evidence (API responses, logs, screenshots)
    3. Record result (PASS/FAIL + evidence)
    4. Log to results.json
  ↓
[Executor: Calculate Pass Rate]
  - Total scenarios: X
  - Passed: Y
  - Failed: Z
  - Pass rate: Y/X * 100%
  ↓
[Decision Gate: Pass Rate Check]
  If pass rate = 100%:
    → Executor: Collect evidence
    → Executor: Update CAPABILITIES_MATRIX
    → Executor: Commit to repo
    → Executor: Create PR
    → Executor: Request Or sign-off
    → Or: Reviews evidence
    → Or: Approves PR
    → Status: PILOT_DESIGNED → VERIFIED
  
  If pass rate < 100%:
    → Executor: Document failures
    → Executor: Update CAPABILITIES_MATRIX (BLOCKED)
    → Executor: Commit evidence
    → Executor: Report to Or (what failed, why)
    → Or: Decides: fix and retry OR block indefinitely
    → Status: PILOT_DESIGNED → BLOCKED
  ↓
[Executor: Report to Or]
  - Format: EXECUTOR→OR_REPORT (see template below)
  - Includes: Pass rate, evidence links, MATRIX update, next steps
  ↓
END
```

**Key insight**: Executor executes, Or approves - clear separation of responsibilities

---

## 👤 Executor RACI

### Who is Executor?

**Executor**: Technical operator authorized by Or to execute Runtime phases

**NOT Executor**:
- Or (strategic approver, not operator)
- Claude (planner, not operator)
- GPTs (assistants, not operators)

**Requirements for Executor**:
- Access to Or's machine (physical or remote)
- Authorized to modify MCP configs
- Authorized to handle OAuth flows
- Authorized to commit to repo
- Authorized to create PRs
- Trusted by Or (security critical)

### Executor Responsibilities (R)

**ALLOWED operations**:

```
1. OAuth Management:
   ✅ Update MCP config with new scopes
   ✅ Generate OAuth consent URLs
   ✅ Verify tokens work
   ✅ Store tokens in Secret Manager (if using GCP)

2. Test Execution:
   ✅ Run eval scenarios (manual or automated)
   ✅ Capture evidence (logs, screenshots, API responses)
   ✅ Document results (results.json)
   ✅ Calculate pass rates

3. Repository Operations:
   ✅ Update CAPABILITIES_MATRIX (after eval completion)
   ✅ Commit evidence to OPS/EVALS/
   ✅ Create PRs for Or review
   ✅ Merge PRs after Or approval

4. Reporting:
   ✅ Report results to Or (EXECUTOR→OR_REPORT format)
   ✅ Explain failures clearly
   ✅ Suggest fixes if known

5. Environment Management:
   ✅ Verify MCP server health
   ✅ Check log directories exist
   ✅ Ensure prerequisites met
```

**FORBIDDEN operations**:

```
❌ Change playbooks without documentation
❌ Skip evals or eval scenarios
❌ Modify MATRIX without eval evidence
❌ Bypass approval gates
❌ Execute production operations (only test/verify)
❌ Commit without Or review (PRs required)
❌ Override 100% pass requirement
❌ Access Or's personal data beyond test scope
```

### Or Responsibilities (A - Accountable)

**Or's role**:
```
✅ Approves execution plan (this document)
✅ Approves OAuth consent (clicks URLs)
✅ Reviews evidence (eval results)
✅ Approves PRs (MATRIX updates)
✅ Signs off on VERIFIED status
✅ Blocks capabilities if evals fail
✅ Decides: retry or permanent block
```

**Or does NOT**:
```
❌ Run evals manually
❌ Update configs
❌ Handle OAuth tokens
❌ Execute technical operations
```

### RACI Matrix (Execution Phases)

| Task | R (Responsible) | A (Accountable) | C (Consulted) | I (Informed) |
|------|-----------------|-----------------|---------------|--------------|
| Approve execution plan | Or | Or | Claude (designer) | Executor |
| Update MCP config | **Executor** | Or | Claude (guidance) | - |
| Generate OAuth URL | **Executor** | Or | - | - |
| Click OAuth consent | **Or** | Or | - | Executor |
| Run eval scenarios | **Executor** | Or | - | - |
| Capture evidence | **Executor** | Or | - | - |
| Calculate pass rate | **Executor** | Or | - | - |
| Update MATRIX | **Executor** | Or | - | - |
| Commit evidence | **Executor** | Or | - | - |
| Create PR | **Executor** | Or | - | - |
| Review evidence | **Or** | Or | Executor (explains) | Claude |
| Approve PR | **Or** | Or | - | Executor |
| Sign off VERIFIED | **Or** | Or | - | All |

---

## 📅 Phase Execution Timeline

### Phase G2.2: Gmail Drafts (FIRST PILOT)

**Status**: Next to execute  
**Priority**: HIGH (proves execution model)  
**Risk**: OS_SAFE (drafts not sent, reversible)  
**Estimated time**: 2-4 hours (including OAuth + 19 evals)

### Phase G2.3: Gmail Send (CRITICAL)

**Status**: After G2.2 success  
**Priority**: CRITICAL (CLOUD_OPS_HIGH validation)  
**Risk**: CLOUD_OPS_HIGH (irreversible, external impact)  
**Estimated time**: 4-6 hours (26 evals + heavy validation)  
**Special**: BLOCKED for production even if evals pass

### Phase G2.4: Drive Create Doc

**Status**: After G2.2 or G2.3  
**Priority**: MEDIUM (proves template works for Drive)  
**Risk**: OS_SAFE (private docs, reversible)  
**Estimated time**: 3-5 hours (21 evals)

### Phase G2.5: Calendar Focus

**Status**: After G2.2 or G2.4  
**Priority**: MEDIUM (completes 3-domain proof)  
**Risk**: OS_SAFE (personal events, no attendees)  
**Estimated time**: 3-5 hours (21 evals)

**Recommended order**: G2.2 → G2.3 → G2.4 → G2.5 (validates template progression)

---

## 🔧 Phase G2.2: Gmail Drafts - DETAILED EXECUTION PLAN

### Overview

**Pilot**: Gmail Drafts  
**Playbook**: [`PILOT_GMAIL_DRAFTS_FLOW.md`](PILOT_GMAIL_DRAFTS_FLOW.md)  
**Evals**: 19 scenarios (5+3+4+4+3)  
**Risk**: OS_SAFE  
**Goal**: Prove execution model, validate template, establish VERIFIED baseline

### Prerequisites

```
Before G2.2 execution:

1. ✅ Or approves this execution plan
2. ✅ Executor identified and authorized
3. ✅ MCP server running (Claude Desktop active)
4. ✅ Current OAuth scopes: gmail.readonly
5. ✅ Repository current (no pending changes)
6. ✅ CAPABILITIES_MATRIX reflects PILOT_DESIGNED
7. ✅ Evals documented (AUTOMATION_EVALS_PLAN.md)
```

### Step 1: OAuth Scope Expansion

**Required scopes**:
```
Current: gmail.readonly
Add: gmail.compose

Final: gmail.readonly + gmail.compose
```

**Executor actions**:

```
1. Update MCP config:
   - File: ~/AppData/Roaming/Claude/claude_desktop_config.json (Windows)
   - Section: google-mcp server
   - Add scope: https://www.googleapis.com/auth/gmail.compose

2. Restart Claude Desktop (to load new config)

3. Generate OAuth consent URL:
   - MCP server generates URL
   - URL includes gmail.compose scope
   - Executor sends URL to Or

4. Or clicks URL:
   - Google OAuth consent screen
   - Shows: "Claude wants to compose drafts"
   - Or approves (one-time)
   - Token saved to Secret Manager (if using GCP) or local file

5. Verify token:
   - Test: List drafts (gmail.readonly)
   - Test: Create test draft (gmail.compose)
   - If both work → OAuth successful
   - If fail → Debug, retry
```

**Evidence**:
- Screenshot of OAuth consent screen
- Test draft created (proof of gmail.compose working)
- Log entry from successful test

### Step 2: Test Environment Setup

**Executor verifies**:

```
1. MCP server health:
   ✅ Claude Desktop running
   ✅ google-mcp server connected
   ✅ OAuth token valid (test read operation)

2. Directories exist:
   ✅ OPS/EVALS/ (for results)
   ✅ OPS/LOGS/ (for operation logs)

3. CAPABILITIES_MATRIX current:
   ✅ Gmail Drafts row: PILOT_DESIGNED
   ✅ Eval Coverage: 0/19 (0%)
   ✅ Last Eval: Not run

4. Tools available:
   ✅ GitHub access (for commits/PRs)
   ✅ Text editor (for results.json)
   ✅ Screenshot tool (if needed)
```

### Step 3: Run Evals (19 scenarios)

**Eval execution strategy**:

```
For each scenario:
1. Read scenario from AUTOMATION_EVALS_PLAN.md
2. Execute scenario (manual or via script/workflow)
3. Capture evidence (API response, log, screenshot)
4. Record result (PASS/FAIL)
5. Document in results.json

Scenarios run in order:
- Category 1: Happy Path (5 scenarios)
- Category 2: Safeguards (3 scenarios)
- Category 3: Edge Cases (4 scenarios)
- Category 4: Failure Modes (4 scenarios)
- Category 5: Observability (3 scenarios)
```

#### Scenario Examples (Detailed)

**Scenario 1.1: Basic draft creation**

```
Steps:
1. Executor (via Claude): "Create draft to test@example.com, subject: Test Draft, body: This is a test"
2. Claude gathers context (or uses simple request)
3. Claude creates draft via MCP (gmail.compose)
4. MCP calls Gmail API: drafts.create
5. Gmail API returns: {draft_id: "draft-123", ...}

Evidence:
- Gmail API response JSON (draft_id present)
- Log entry in OPS/LOGS/google-operations.jsonl
- Screenshot of draft in Gmail (optional)

Result: PASS (if draft created) or FAIL (if error)

Record in results.json:
{
  "id": "1.1",
  "category": "Happy Path",
  "name": "Basic draft creation",
  "result": "PASS",
  "evidence": {
    "gmail_api_response": {"draft_id": "draft-123", ...},
    "log_file": "OPS/LOGS/google-operations.jsonl",
    "log_entry_line": 42
  },
  "notes": "Draft created successfully, all fields correct",
  "executed_at": "2025-11-18T10:15:00Z"
}
```

**Scenario 2.1: Cannot send from draft (Safeguard)**

```
Steps:
1. Executor creates draft (scenario 1.1)
2. Executor (via Claude): "Send this draft"
3. Claude attempts to use gmail.send scope
4. MCP server checks available scopes
5. MCP server blocks (gmail.send not granted)

Evidence:
- MCP error response: "Scope not available: gmail.send"
- Draft still in draft status (not sent)
- Gmail API confirms: draft.message.labelIds = ["DRAFT"]

Result: PASS (if send blocked) or FAIL (if draft sent)

Record in results.json:
{
  "id": "2.1",
  "category": "Safeguards",
  "name": "Cannot send from draft",
  "result": "PASS",
  "evidence": {
    "mcp_error": "Scope not available: gmail.send",
    "draft_status": "DRAFT",
    "gmail_api_check": {"labelIds": ["DRAFT"]}
  },
  "notes": "Safeguard enforced, send operation blocked",
  "executed_at": "2025-11-18T10:20:00Z"
}
```

**Scenario 3.1: Very long subject (Edge Case)**

```
Steps:
1. Executor: Create draft with 998-character subject (Gmail limit)
2. Claude creates draft with long subject
3. Gmail API accepts (within limit)

Evidence:
- Gmail API response with 998-char subject
- Draft visible in Gmail with truncated display

Result: PASS (if accepted) or FAIL (if error)
```

**Scenario 4.1: Network timeout (Failure Mode)**

```
Steps:
1. Executor simulates network failure (disconnect network briefly)
2. Executor: Create draft
3. MCP attempts API call
4. Network timeout occurs
5. Claude handles error gracefully

Evidence:
- Error log: "Network timeout"
- Claude message: "Failed to create draft due to network error. Retry?"
- Draft NOT created (verified via Gmail)

Result: PASS (if error handled gracefully) or FAIL (if crash/data leak)
```

**Scenario 5.1: Log entry complete (Observability)**

```
Steps:
1. Executor creates draft (any scenario)
2. Executor checks: OPS/LOGS/google-operations.jsonl
3. Verify log entry has all required fields:
   - timestamp
   - operation
   - risk_level
   - status
   - actor
   - details (draft_id, subject, recipient)

Evidence:
- Log file excerpt showing complete entry
- JSON validation passes

Result: PASS (if all fields present) or FAIL (if missing fields)
```

#### Running All 19 Scenarios

**Estimated time**: 1-2 hours

**Automation options**:
- Manual execution (Executor runs each via Claude Desktop)
- Semi-automated (script triggers Claude, Executor validates)
- Fully automated (GitHub Actions + MCP) - future enhancement

**For G2.2 PILOT**: **Manual execution recommended** (establishes baseline, validates model)

### Step 4: Collect Evidence

**After all 19 scenarios run**:

```
Executor creates: OPS/EVALS/gmail-drafts-results.json

Format:
{
  "eval_id": "gmail-drafts-2025-11-18-001",
  "pilot": "Gmail Drafts",
  "phase": "G2.2",
  "playbook": "DOCS/PILOT_GMAIL_DRAFTS_FLOW.md",
  "executed_by": "Executor Name",
  "executed_at": "2025-11-18T10:00:00Z",
  "duration_minutes": 90,
  "environment": "Claude Desktop + MCP + OAuth",
  
  "summary": {
    "total_scenarios": 19,
    "passed": 19,
    "failed": 0,
    "skipped": 0,
    "pass_rate": "100%"
  },
  
  "category_breakdown": {
    "happy_path": "5/5 (100%)",
    "safeguards": "3/3 (100%)",
    "edge_cases": "4/4 (100%)",
    "failure_modes": "4/4 (100%)",
    "observability": "3/3 (100%)"
  },
  
  "scenarios": [
    {
      "id": "1.1",
      "category": "Happy Path",
      "name": "Basic draft creation",
      "result": "PASS",
      "evidence": {...},
      "notes": "...",
      "executed_at": "2025-11-18T10:15:00Z"
    },
    // ... all 19 scenarios
  ],
  
  "recommendation": "VERIFIED - All evals passed (100%)",
  "blockers": [],
  "notes": "First pilot execution, manual testing, all safeguards verified",
  "next_steps": [
    "Update CAPABILITIES_MATRIX: PILOT_DESIGNED → VERIFIED",
    "Commit evidence to repo",
    "Create PR for Or review",
    "Get Or sign-off"
  ]
}
```

**Additional evidence**:
- Screenshots (if needed for visual confirmation)
- Log files (OPS/LOGS/google-operations.jsonl entries)
- OAuth consent screenshot
- Test drafts in Gmail (can be deleted after verification)

### Step 5: Calculate Pass Rate

```
Total scenarios: 19
Passed: 19
Failed: 0
Pass rate: 19/19 = 100%

Decision: VERIFIED (100% pass rate achieved)
```

**If <100%**: Document failures, update MATRIX to BLOCKED, report to Or

### Step 6: Update CAPABILITIES_MATRIX

**Executor updates**:

```markdown
Before (PILOT_DESIGNED):
| From | To | Capability | Status | Eval Coverage | Last Eval | Eval Results |
|------|----|-----------| -------|---------------|-----------|--------------|
| Claude MCP | Gmail API | Create draft | PILOT_DESIGNED | 0/19 (0%) | Not run | Pending G2.2 |

After (VERIFIED):
| From | To | Capability | Status | Eval Coverage | Last Eval | Eval Results |
|------|----|-----------| -------|---------------|-----------|--------------|
| Claude MCP | Gmail API | Create draft | ✅ VERIFIED | 19/19 (100%) | 2025-11-18 | [results.json](../../OPS/EVALS/gmail-drafts-results.json) |
```

**File to update**: `CAPABILITIES_MATRIX.md` (or relevant section file)

### Step 7: Commit Evidence

**Executor commits**:

```
Files to commit:
1. OPS/EVALS/gmail-drafts-results.json (evidence)
2. CAPABILITIES_MATRIX.md (updated row)
3. OPS/LOGS/google-operations.jsonl (if new entries)
4. Screenshots/ (if any visual evidence)

Commit message:
"Phase G2.2 Complete: Gmail Drafts VERIFIED (19/19 evals passed)"

Branch: feature/g2.2-gmail-drafts-verified
Create PR for Or review
```

### Step 8: Create PR & Request Or Sign-Off

**Executor creates PR**:

```
Title: Phase G2.2 Complete: Gmail Drafts VERIFIED

Description:
## Summary
Gmail Drafts pilot has been executed and verified.

## Results
- **Pass Rate**: 19/19 (100%)
- **Status Update**: PILOT_DESIGNED → VERIFIED
- **Evidence**: [gmail-drafts-results.json](../OPS/EVALS/gmail-drafts-results.json)

## Category Breakdown
- Happy Path: 5/5 ✅
- Safeguards: 3/3 ✅
- Edge Cases: 4/4 ✅
- Failure Modes: 4/4 ✅
- Observability: 3/3 ✅

## Files Changed
- CAPABILITIES_MATRIX.md (status update)
- OPS/EVALS/gmail-drafts-results.json (evidence)

## Next Steps
- Or reviews evidence
- Or approves PR
- Gmail Drafts capability operational

## Executor Sign-Off
Executed by: [Executor Name]
Date: 2025-11-18
All evals passed, safeguards verified, capability ready.
```

**Or reviews**:
1. Checks evidence (results.json)
2. Verifies 100% pass rate
3. Reviews safeguard scenarios (critical)
4. Approves PR
5. Merges to main

**Status**: Gmail Drafts now VERIFIED and operational ✅

### Step 9: Report to Or

**Format**: EXECUTOR→OR_REPORT

```
To: Or
From: Executor
Subject: Phase G2.2 Complete - Gmail Drafts VERIFIED
Date: 2025-11-18

## Executive Summary
Gmail Drafts pilot successfully verified.
- Pass Rate: 19/19 (100%)
- Status: PILOT_DESIGNED → VERIFIED
- Timeline: 2 hours (OAuth + evals + evidence)

## What Was Done
1. ✅ Expanded OAuth (gmail.compose added)
2. ✅ Ran 19 eval scenarios (manual execution)
3. ✅ Collected evidence (results.json + logs)
4. ✅ Updated CAPABILITIES_MATRIX
5. ✅ Created PR (awaiting your approval)

## Key Findings
- All safeguards enforced correctly
- Scope limitation verified (cannot send drafts)
- Logging complete and accurate
- Error handling graceful (network timeout tested)

## Evidence
- [PR #XXX](link)
- [results.json](../OPS/EVALS/gmail-drafts-results.json)
- OAuth consent: Approved by Or
- Test drafts: Created and verified

## Recommendation
Approve PR and mark Gmail Drafts as operational.

## Next Steps
- G2.3 (Gmail Send) - CRITICAL, requires heavy validation
- Or: When ready, signal GO for G2.3

## Notes
First pilot execution successful.
Execution model validated.
Template works as designed.

Executor: [Name]
Signed: 2025-11-18T12:00:00Z
```

---

## 🔄 Phases G2.3-G2.5: Execution Summary

### Phase G2.3: Gmail Send (CLOUD_OPS_HIGH)

**Same flow as G2.2, with differences**:

```
1. OAuth: Add gmail.send scope
2. Evals: 26 scenarios (more safeguards)
3. Critical: Safeguards MUST pass 100%
   - Approval phrase ("מאשר שליחה")
   - TTL (60 min)
   - Rate limit (10/hour hard block)
   - No forwarding/BCC hijacking
   - Detailed logging
4. Evidence: More detailed (~1000 bytes per scenario)
5. Status: VERIFIED but BLOCKED for production
6. Special: Even if 100% pass, capability stays BLOCKED
```

**Why BLOCKED**: Gmail Send = CLOUD_OPS_HIGH (irreversible, external impact). Needs separate production approval gate beyond evals.

### Phase G2.4: Drive Create Doc (OS_SAFE)

```
1. OAuth: Add drive.file + docs.file scopes
2. Evals: 21 scenarios
3. Special: Dedicated folder setup ("Claude Strategy Docs")
4. Safeguards: No external sharing, no delete existing
5. Status: VERIFIED (if 100% pass)
```

### Phase G2.5: Calendar Focus (OS_SAFE)

```
1. OAuth: Add calendar.events scope
2. Evals: 21 scenarios
3. Special: No attendees allowed (personal events only)
4. Safeguards: No attendees, no share calendar, no edit existing
5. Status: VERIFIED (if 100% pass)
```

**All phases follow same master flow** - proven by G2.2 pilot

---

## 📊 Evidence Storage Structure

### Directory Layout

```
OPS/
├── EVALS/
│   ├── gmail-drafts-results.json (G2.2 evidence)
│   ├── gmail-send-results.json (G2.3 evidence)
│   ├── drive-create-doc-results.json (G2.4 evidence)
│   ├── calendar-focus-results.json (G2.5 evidence)
│   ├── screenshots/ (visual evidence if needed)
│   │   ├── g2.2-oauth-consent.png
│   │   ├── g2.2-draft-created.png
│   │   └── ...
│   └── logs/ (test execution logs)
│       ├── g2.2-execution-2025-11-18.log
│       └── ...
└── LOGS/
    └── google-operations.jsonl (runtime operation logs)
```

**All committed to repo** (permanent audit trail)

---

## 🚨 Failure Handling

### If Evals Fail (<100% pass rate)

```
Executor actions:
1. Stop execution (don't proceed to MATRIX update)
2. Document failures:
   - Which scenarios failed
   - Why they failed (root cause)
   - Evidence of failures
3. Create results.json with failure details
4. Update CAPABILITIES_MATRIX:
   - Status: PILOT_DESIGNED → BLOCKED
   - Eval Coverage: X/Y (Z%)
   - Note: "Evals failed, see results.json"
5. Commit evidence
6. Report to Or (EXECUTOR→OR_REPORT with failure analysis)

Or decides:
- Option A: Fix issues, retry evals
- Option B: Block capability indefinitely
- Option C: Adjust playbook/evals, then retry

No capability upgrade until 100% pass achieved.
```

### Example: Safeguard Failure (CRITICAL)

```
Scenario 2.1: Cannot send from draft - FAILED

Evidence:
- Draft was sent (should have been blocked)
- Log shows: gmail.send operation succeeded
- Gmail API confirms: message sent to recipient

Root cause:
- Scope limitation not enforced
- MCP server allowed gmail.send despite lacking scope

Impact:
- CRITICAL security violation
- Safeguard bypassed
- Capability BLOCKED indefinitely

Next steps:
- Fix MCP server scope enforcement
- Re-run ALL evals (not just failed one)
- Do NOT upgrade to VERIFIED until fixed
```

**Safeguard failures = immediate BLOCK** (no exceptions)

---

## 📋 EXECUTOR→OR_REPORT Template

### Standard Report Format

```
To: Or
From: Executor
Subject: Phase [G2.X] [Status] - [Pilot Name]
Date: [ISO timestamp]

## Executive Summary
[One paragraph: what was done, pass rate, status change]

## What Was Done
1. [OAuth expansion]
2. [Evals run]
3. [Evidence collected]
4. [MATRIX updated]
5. [PR created]

## Results
- Pass Rate: X/Y (Z%)
- Status: [OLD] → [NEW]
- Evidence: [link to results.json]

## Category Breakdown
- Happy Path: X/Y
- Safeguards: X/Y
- Edge Cases: X/Y
- Failure Modes: X/Y
- Observability: X/Y

## Key Findings
[Notable observations, issues, surprises]

## Evidence
- [PR link]
- [results.json link]
- [Other artifacts]

## Recommendation
[Approve PR / Fix issues / Block indefinitely]

## Next Steps
[What happens next]

## Notes
[Any additional context]

Executor: [Name]
Signed: [ISO timestamp]
```

---

## 🎯 Success Criteria (Per Phase)

### Phase Completion Checklist

```
For VERIFIED status:
✅ OAuth scopes expanded
✅ All evals run (100% of scenarios)
✅ Pass rate = 100%
✅ Evidence collected (results.json + logs)
✅ CAPABILITIES_MATRIX updated
✅ Evidence committed to repo
✅ PR created and reviewed
✅ Or approves PR
✅ Or signs off on VERIFIED status

For BLOCKED status:
✅ Failures documented
✅ Root causes identified
✅ CAPABILITIES_MATRIX updated (BLOCKED)
✅ Evidence committed
✅ Or notified
✅ Fix plan proposed OR indefinite block confirmed
```

---

## 📊 Phase Progress Tracking

### Current Status (Before Execution)

| Phase | Pilot | Status | Evals | Pass Rate | Next Action |
|-------|-------|--------|-------|-----------|-------------|
| G2.2 | Gmail Drafts | PILOT_DESIGNED | 19 | 0% | Awaiting Executor + Or GO |
| G2.3 | Gmail Send | PILOT_DESIGNED | 26 | 0% | After G2.2 |
| G2.4 | Drive Create Doc | PILOT_DESIGNED | 21 | 0% | After G2.2 |
| G2.5 | Calendar Focus | PILOT_DESIGNED | 21 | 0% | After G2.2 |

### After G2.2 Execution (Example)

| Phase | Pilot | Status | Evals | Pass Rate | Executed |
|-------|-------|--------|-------|-----------|----------|
| **G2.2** | **Gmail Drafts** | **✅ VERIFIED** | **19** | **100%** | **2025-11-18** |
| G2.3 | Gmail Send | PILOT_DESIGNED | 26 | 0% | Awaiting GO |
| G2.4 | Drive Create Doc | PILOT_DESIGNED | 21 | 0% | Awaiting GO |
| G2.5 | Calendar Focus | PILOT_DESIGNED | 21 | 0% | Awaiting GO |

---

## 🔐 Security & Safety

### Critical Safety Measures

```
1. OAuth Security:
   ✅ Scopes granted = scopes documented
   ✅ Tokens stored securely (Secret Manager or encrypted)
   ✅ No scope escalation without Or approval

2. Test Isolation:
   ✅ Test operations clearly marked
   ✅ Test data disposable (can be deleted after)
   ✅ No production impact

3. Evidence Integrity:
   ✅ All evidence committed to repo (permanent)
   ✅ Results.json signed by Executor
   ✅ Or reviews before approval

4. Safeguard Enforcement:
   ✅ 100% pass required (no exceptions)
   ✅ Safeguard failures = immediate BLOCK
   ✅ Security over convenience

5. Executor Boundaries:
   ✅ Clear ALLOWED/FORBIDDEN lists
   ✅ Executor cannot bypass evals
   ✅ Executor cannot override 100% requirement
```

---

## 📋 Summary & Next Steps

### What This Plan Provides

- ✅ **Complete execution workflow** (master flow + per-phase details)
- ✅ **Executor RACI** (clear responsibilities and boundaries)
- ✅ **G2.2 detailed plan** (Gmail Drafts as first pilot)
- ✅ **Evidence collection** (formats and storage)
- ✅ **Failure handling** (what to do if evals fail)
- ✅ **Reporting template** (EXECUTOR→OR_REPORT)
- ✅ **Success criteria** (checklists per phase)

### Ready for Execution

**Prerequisites met**:
- ✅ 4 pilots designed (playbooks complete)
- ✅ 87 evals designed (scenarios documented)
- ✅ Execution plan designed (this document)
- ✅ Executor RACI defined (clear roles)

**Awaiting**:
- ⏳ Or approves this execution plan
- ⏳ Executor identified and authorized
- ⏳ Or signals GO for G2.2

**After Or approval**:
1. Executor executes G2.2 (Gmail Drafts)
2. Evidence collected and reviewed
3. If 100% pass → VERIFIED
4. Repeat for G2.3-G2.5

---

**Maintained by**: Claude  
**Created**: 2025-11-17  
**Phase**: G2.1-Pilot  
**Status**: EXECUTION_PLANNED (awaiting Or approval)  
**First Pilot**: G2.2 (Gmail Drafts)  
**Template**: Universal (applies to all future pilots)
