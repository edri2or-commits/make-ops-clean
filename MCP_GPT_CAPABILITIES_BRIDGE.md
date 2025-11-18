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

## 🆕 Gmail Send - CLOUD_OPS_HIGH Pilot (2025-11-17)

**מה חדש**:

Claude בנה **פיילוט מלא** ל-Gmail Send - הדוגמה הראשונה ל-CLOUD_OPS_HIGH:

### 📧 PILOT_GMAIL_SEND_FLOW.md

**קישור**: [`DOCS/PILOT_GMAIL_SEND_FLOW.md`](DOCS/PILOT_GMAIL_SEND_FLOW.md) (46KB)

**מה זה**:
- Complete playbook לשליחת מיילים עם אישור מפורש
- **Risk: CLOUD_OPS_HIGH** (irreversible, external impact)
- כל 5 הsafeguards ב-full strength (heavy enforcement)
- 19 צעדים (כולל approval gate מלא)
- 8 test cases (כולל בדיקות safeguards)

**למה זה שונה מ-Gmail Drafts**:
- **Drafts = OS_SAFE** (no external impact, reversible)
- **Send = CLOUD_OPS_HIGH** (cannot unsend, recipient receives)
- Approval: "מאשר שליחה" (explicit phrase + 60min TTL)
- Rate limit: 10/hour (hard block, mandatory)
- Logging: Detailed (includes approval details + rate state)

---

## 🎯 Gmail Send - Use Case Recognition

**כשהמשתמש מבקש**: "Send email to X"

**GPT צריך**:

### 1. זיהוי Use Case + Risk Check
```
Request: "Send email to customer@example.com"

GPT recognizes:
→ Use Case: Gmail Send
→ Risk: CLOUD_OPS_HIGH (irreversible, external impact)
→ Agent: Claude (R) for single sends
→ Phase: Check MATRIX status
```

### 2. בדיקת MATRIX
```
Check: CAPABILITIES_MATRIX Section 3.1 Gmail
→ "Send email" capability
→ Status: PILOT_DESIGNED (before G2.3) or VERIFIED (after G2.3)
→ Risk: CLOUD_OPS_HIGH
→ Safeguards: ALL 5 layers (heavy)
```

### 3. בדיקת RACI
```
Check: GOOGLE_AGENTS_RACI.md Section 1.3
→ Single contextual send = Claude (R)
→ Bulk/campaign sends = GPTs GO (R)

If single/contextual:
→ Claude is Responsible
→ Proceed

If bulk (>10 emails):
→ GPTs GO is Responsible
→ Delegate or consult
```

### 4. הפעלת Flow
```
If Status = VERIFIED (after G2.3):
→ Follow PILOT_GMAIL_SEND_FLOW.md
→ Intent → Plan → Context → Draft → Preview
→ **Approval Gate** (CLOUD_OPS_HIGH):
    - Check rate limit (< 10/hour?)
    - Request: "מאשר שליחה"
    - Verify: exact phrase + within 60min TTL
    - Send → Log (detailed) → Report

If Status = PILOT_DESIGNED (before G2.3):
→ Claude: "Gmail Send is designed but not operational.
           Current status: PILOT_DESIGNED
           
           To make this work, need Phase G2.3:
           - Expand OAuth scope (add gmail.send)
           - Configure rate limiting
           - Test and verify
           
           For now, I can create a draft instead.
           Would you like to save as draft?"
→ Offer draft alternative (OS_SAFE)
```

---

## 🔐 CLOUD_OPS_HIGH - What It Means

**Definition**:
> Operations with **high external impact** and **irreversibility** - cannot be undone, affects others

**Examples**:
- ✅ Send email (Gmail Send) - recipient receives, cannot unsend
- ✅ Share file externally (Drive) - others gain access
- ✅ Delete event with attendees (Calendar) - notifies everyone
- ✅ Permanent delete (any service) - cannot recover

**Comparison with other risk levels**:

| Risk Level | External Impact | Reversibility | Approval | Rate Limit | Example |
|-----------|-----------------|---------------|----------|------------|---------|
| **OS_SAFE** | None | Full | Content review | Optional | Gmail Drafts |
| **CLOUD_OPS_MEDIUM** | Low-Medium | Partial (24h) | Or notification | Recommended | Edit shared doc |
| **CLOUD_OPS_HIGH** | High | None | Explicit phrase + TTL | Mandatory | Gmail Send |

---

## 🛡️ CLOUD_OPS_HIGH Safeguards (Heavy)

**All 5 layers - MANDATORY and STRICT**:

### Layer 1: Approval Gate (STRICT)
```
Type: Explicit phrase + TTL
Phrase: "מאשר שליחה" (must be exact)
TTL: 60 minutes from preview
Process:
1. Claude shows FULL preview (every word)
2. Or reviews thoroughly
3. Or types exact phrase: "מאשר שליחה"
4. Claude verifies: phrase + TTL + rate limit
5. Claude sends immediately after verification

Why strict:
- Cannot unsend → Must prevent wrong sends
- Explicit phrase → No accidental approvals
- TTL → No stale approvals (context changes)
```

### Layer 2: Rate Limiting (HARD BLOCK)
```
Limit: 10 sends per 60-minute rolling window
Tracking: OPS/STATE/gmail-send-rate.json
Enforcement: Hard block at 10 (cannot send more)
Alert: Warning at 8 sends (80%)
Override: Separate approval phrase required

Why mandatory:
- Prevents runaway sending
- Protects reputation
- Forces deliberate pace
```

### Layer 3: Logging (DETAILED)
```
Location: OPS/LOGS/google-operations.jsonl
Format: JSON (~1000 bytes per send)
Content:
- Full metadata (timestamp, actor, status)
- Recipients (to, cc, bcc)
- Subject + body preview (100 chars)
- **Approval details** (phrase, who, when, TTL)
- **Rate limit state** (before/after counts)
- Context gathered (threads, docs, meetings)
- Delivery status

Why detailed:
- Forensics (if email causes issue)
- Compliance (audit trail)
- Anomaly detection (spot patterns)
- Learning (how capability used)
```

### Layer 4: Scope Limitation
```
Scope: gmail.send ONLY
Cannot:
- Modify settings (gmail.settings.*)
- Create filters/forwarding
- Access admin APIs

Why minimal:
- Least privilege principle
- Reduces attack surface
```

### Layer 5: Policy Blocks (TECHNICAL)
```
Blocked operations (cannot bypass):
1. Auto-forwarding rules (data exfiltration)
2. BCC hijacking (all BCC must be approved)
3. Bulk sending (>10/hour blocked)
4. Scheduled sends (separate automation)
5. Settings modification (use Gmail directly)
6. Sending without approval (mandatory gate)

Enforcement: MCP server + Claude logic + API scopes
Prompt injection proof: Technical blocks
```

---

## 📋 Comparison: Drafts vs Send (Critical Differences)

**For GPTs to understand the paradigm shift**:

| Aspect | Gmail Drafts (OS_SAFE) | Gmail Send (CLOUD_OPS_HIGH) |
|--------|------------------------|----------------------------|
| **Phase** | G2.2 (base OAuth) | G2.3 (scope expansion) |
| **Risk** | OS_SAFE | CLOUD_OPS_HIGH |
| **Scope** | gmail.compose | gmail.send |
| **External impact** | None (draft private) | High (recipient receives) |
| **Reversibility** | Full (delete draft) | None (cannot unsend) |
| **Approval** | "Create draft" (casual) | "מאשר שליחה" (formal + TTL) |
| **TTL** | None | 60 minutes |
| **Rate limit** | 50/hour (optional) | 10/hour (hard block) |
| **Rate enforcement** | Soft (warning) | Hard (blocks at 10) |
| **Logging** | Standard (~500 bytes) | Detailed (~1000 bytes) |
| **Policy blocks** | No send from draft | No forward/BCC/bulk/schedule |
| **Test cases** | 5 | 8 (includes safeguard tests) |
| **Steps** | 14 | 19 (+ approval gate) |

**Key insight**: This is NOT just "more safeguards" - it's a **completely different approval model**

---

## 🎯 Gmail Send Flow Pattern (הנחיות ל-GPTs)

**כשרואים request לשליחת מייל**:

### Phase 1: Intent Recognition + Risk Assessment
```
User says:
"Send email to sarah@example.com about project delay"

GPT recognizes:
→ Use Case: Gmail Send
→ Risk: CLOUD_OPS_HIGH (external impact, irreversible)
→ Agent: Claude (R) for single contextual send
→ Phase: Check MATRIX status
→ Safeguards: ALL 5 layers mandatory
```

### Phase 2: Route to Claude with Risk Warning
```
GPT → Claude:
"User wants to send email to sarah@example.com.

CRITICAL: This is CLOUD_OPS_HIGH operation.

Per CAPABILITIES_MATRIX:
- Gmail Send: PILOT_DESIGNED (or VERIFIED)
- Risk: CLOUD_OPS_HIGH (irreversible)
- Playbook: PILOT_GMAIL_SEND_FLOW.md

Per GOOGLE_AGENTS_RACI.md:
- Single contextual send: Claude (R)

Safeguards required:
1. Full preview (every word)
2. Explicit approval: 'מאשר שליחה'
3. Rate limit check (< 10/hour)
4. TTL: 60 minutes
5. Detailed logging

Please execute Gmail Send flow if operational,
or offer draft alternative if not ready."
```

### Phase 3: Claude Executes with Full Safeguards
```
Claude follows PILOT_GMAIL_SEND_FLOW.md:
1. Check MATRIX (status: PILOT_DESIGNED or VERIFIED)
2. If PILOT_DESIGNED:
   → Offer draft alternative (OS_SAFE)
   → Explain what's needed for G2.3
3. If VERIFIED:
   → Check RACI (confirm Claude R)
   → Gather context (threads, docs, calendar, local, web)
   → Draft email
   → Present FULL preview to Or
   → Check rate limit (< 10/hour?)
   → Request approval: "מאשר שליחה"
   → Or provides phrase
   → Verify: exact phrase + within TTL + rate OK
   → Send via MCP (gmail.send)
   → Log (detailed) to OPS/LOGS/
   → Report: "✅ Sent, Message ID: m-123"
```

### Phase 4: GPT Tracks Outcome
```
GPT observes:
→ Email sent successfully
→ Logged to OPS/LOGS/ (detailed)
→ Rate limit updated (X+1 of 10)
→ Or received confirmation

GPT can now:
→ Track pattern (how often this happens)
→ Suggest improvements (if repetitive)
→ Monitor rate limit usage
→ Alert if approaching limit (8-9 sends)
```

---

## ⚠️ Critical: Before Suggesting Gmail Send

**GPTs MUST check these before suggesting send**:

### 1. Is capability operational?
```
Check CAPABILITIES_MATRIX:
- Gmail Send status: PILOT_DESIGNED or VERIFIED?
- If PILOT_DESIGNED:
    → NOT operational yet
    → Suggest draft alternative
    → Explain G2.3 needed
- If VERIFIED:
    → Operational
    → Proceed with safeguards
```

### 2. Is this single or bulk?
```
Check RACI:
- Single send (1-3 recipients, contextual) → Claude (R)
- Bulk send (>10 recipients, templated) → GPTs GO (R)

If bulk:
→ Delegate to GPTs GO
→ DO NOT use Claude's Gmail Send (rate limit 10/hour)
```

### 3. Does Or understand risk?
```
Before suggesting send:
"⚠️ Gmail Send is CLOUD_OPS_HIGH:
- Email will be sent (cannot unsend)
- Requires explicit approval: 'מאשר שליחה'
- Rate limit: X of 10 used this hour
- Full logging to OPS/LOGS/

Ready to proceed?"
```

### 4. Is there a draft alternative?
```
Always offer draft option:
"Would you like to:
1. Send email now (CLOUD_OPS_HIGH, requires approval)
2. Create draft first (OS_SAFE, review before sending)

Recommendation: Draft first for review"
```

---

## 📐 Risk Decision Tree (Updated with Send)

**מהtemplate, מורחב עם Gmail Send**:

```
Gmail operation requested:

1. What's the operation?
   ├─ Read (search, list, get) → OS_SAFE
   ├─ Create draft → OS_SAFE
   ├─ Label/organize → CLOUD_OPS_MEDIUM
   └─ **Send email** → **CLOUD_OPS_HIGH** ← WE ARE HERE

2. If Send:
   - External impact? YES (recipient receives)
   - Reversible? NO (cannot unsend)
   - Affects others? YES (recipient, CC, BCC)
   → CLOUD_OPS_HIGH

3. CLOUD_OPS_HIGH requirements:
   ✓ Explicit approval phrase
   ✓ 60-minute TTL
   ✓ Hard rate limit (10/hour)
   ✓ Detailed logging
   ✓ Policy blocks enforced
   ✓ Full preview mandatory
   ✓ RACI check (single or bulk?)
```

---

## 🔄 Phase Tracking (עדכון)

### Phase G1 ✅ (Complete 2025-11-17):
- Autonomy model
- RACI matrix
- Scopes analysis

### Phase G2.1 ✅ (Complete 2025-11-17):
- OAuth architecture
- Safeguards framework
- Workflow skeletons

### Phase G2.1-Pilot ✅ (Complete 2025-11-17):
- **Gmail Drafts** (OS_SAFE) - complete
- **AUTOMATION_PLAYBOOK_TEMPLATE** - universal
- **Gmail Send** (CLOUD_OPS_HIGH) - complete ⭐ NEW

### Phase G2.2 ⏳ (Next):
- Execute base OAuth (gmail.compose)
- Test Gmail Drafts
- Status: PILOT_DESIGNED → VERIFIED

### Phase G2.3 ⏳ (Future):
- Expand OAuth (add gmail.send)
- Test Gmail Send (8 test cases)
- Status: PILOT_DESIGNED → VERIFIED

---

## Critical Reminders for GPTs (עדכון)

### 1. Gmail Send = CLOUD_OPS_HIGH
```
✅ "Gmail Send is CLOUD_OPS_HIGH - highest risk level"
✅ "Requires explicit approval phrase + TTL"
✅ "Rate limited to 10/hour (hard block)"
✅ "Cannot unsend - prevention critical"
```

### 2. Always Check Operational Status
```
Before suggesting send:
1. Check CAPABILITIES_MATRIX (PILOT_DESIGNED or VERIFIED?)
2. If PILOT_DESIGNED → Offer draft alternative
3. If VERIFIED → Proceed with full safeguards
4. Never promise send before checking status
```

### 3. Offer Draft Alternative
```
ALWAYS present draft option:
"Would you like to:
1. Send now (CLOUD_OPS_HIGH, explicit approval required)
2. Create draft (OS_SAFE, review before sending)

Draft recommended for non-urgent sends."
```

### 4. Check RACI Before Routing
```
Single contextual send → Claude (R)
Bulk/campaign send → GPTs GO (R)

If >10 recipients or templated:
→ DO NOT route to Claude (rate limit)
→ Route to GPTs GO instead
```

### 5. Warn About Rate Limit
```
Before suggesting send:
"Rate limit status: X of 10 sends used this hour"

If 8-9 sends:
"⚠️ Approaching rate limit (X of 10).
 Consider spacing out sends or using draft."

If 10 sends:
"❌ Rate limit reached (10/hour).
 Wait Y minutes or use draft instead."
```

---

## עדכון אחרון

**2025-11-17 (Gmail Send CLOUD_OPS_HIGH Pilot Complete)**:
- ✅ PILOT_GMAIL_SEND_FLOW.md created (46KB)
- ✅ Complete CLOUD_OPS_HIGH playbook
- ✅ All 5 safeguards (heavy enforcement)
- ✅ 19-step flow (includes approval gate)
- ✅ 8 test cases (safeguard validation)
- ✅ CAPABILITIES_MATRIX updated (Gmail Send row)
- ✅ MCP_GPT_CAPABILITIES_BRIDGE updated (this file)

**Total Documentation**:
- Google MCP Base: 126KB (G1 + G2.1 + Gmail Drafts)
- Gmail Send: 46KB (CLOUD_OPS_HIGH pilot)
- Universal Template: 43.7KB
- **Grand Total: 215.7KB** של תיעוד OS_SAFE

**Next**: Or approves Gmail Send design → G2.3 execution (future)

---

**תחזוקה**: Claude (עם אישור אור)  
**עדכון אחרון**: 2025-11-17 (Gmail Send CLOUD_OPS_HIGH added)  
**גרסה**: 2.3 (CLOUD_OPS_HIGH template added)
