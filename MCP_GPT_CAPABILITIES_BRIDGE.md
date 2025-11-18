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

## 🆕 Google MCP - Phase G2.1-Pilot Complete (2025-11-17)

**מה השתנה**:

Claude בנה **פיילוט מלא** ל-Gmail Drafts - template לכל היכולות הבאות:

### המסמכים המרכזיים:

1. **[`DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md`](DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md)** (28.7KB) - Phase G1
   - חזון, scopes, מודל autonomy

2. **[`DOCS/GOOGLE_AGENTS_RACI.md`](DOCS/GOOGLE_AGENTS_RACI.md)** (22.4KB) - Phase G1
   - חלוקת תפקידים Claude vs GPTs GO

3. **[`DOCS/GOOGLE_MCP_OAUTH_ARCH.md`](DOCS/GOOGLE_MCP_OAUTH_ARCH.md)** (52.6KB) - Phase G2.1
   - ארכיטקטורה טכנית מלאה

4. **[`DOCS/PILOT_GMAIL_DRAFTS_FLOW.md`](DOCS/PILOT_GMAIL_DRAFTS_FLOW.md)** (22.3KB) ⭐ **NEW - Phase G2.1-Pilot**
   - פיילוט מלא: Intent → Plan → Execution → Report → Logs
   - Template לכל היכולות הבאות

### Phase G2.1-Pilot Status (COMPLETE):
- ✅ Gmail Drafts flow - תכנון מלא (OS_SAFE)
- ✅ End-to-end playbook - Intent עד Logs
- ✅ RACI integration - Claude (R) for contextual drafts
- ✅ Safeguards defined - 5 layers
- ✅ CAPABILITIES_MATRIX updated - Gmail Drafts row added
- ✅ MCP_GPT_CAPABILITIES_BRIDGE updated (this file)
- ✅ Template established - copy for Gmail Send, Drive, Calendar, Sheets

---

## 🎯 Gmail Drafts Pilot - Use Case Recognition

**כשהמשתמש מבקש**: "Draft an email to X about Y"

**GPT צריך**:

### 1. זיהוי Use Case
```
Request matches Gmail Drafts pilot:
✅ "Draft email" / "Create draft" / "Write draft"
✅ Has recipient
✅ Has context/purpose
→ This is PILOT_GMAIL_DRAFTS_FLOW territory
```

### 2. בדיקת RACI
```
Check: GOOGLE_AGENTS_RACI.md Section 1.2
→ Contextual drafts = Claude (R)
→ Template-based drafts = GPTs GO (R)

If contextual/researched/unique:
→ Claude is Responsible
→ Proceed with Claude

If template/bulk/standard:
→ GPTs GO is Responsible
→ Delegate or consult
```

### 3. בדיקת MATRIX
```
Check: CAPABILITIES_MATRIX Section 3.1 Gmail
→ "Create drafts" capability
→ Status: PILOT_DESIGNED (or VERIFIED after G2.2)
→ Risk: OS_SAFE
→ Safeguards: Content approval, no send, logging
```

### 4. הפעלת Flow
```
If Status = VERIFIED (after G2.2):
→ Follow PILOT_GMAIL_DRAFTS_FLOW.md
→ Intent → Plan → Execution → Report → Logs

If Status = PILOT_DESIGNED (before G2.2):
→ Claude can draft text
→ Save to local file
→ Offer to proceed with G2.2 setup
```

---

## Pilot Flow Pattern (הנחיות ל-GPTs)

**כשרואים Use Case דומה לפיילוט**:

### Phase 1: Intent Recognition
```
User says:
"Draft an email to sarah@example.com about project delay"

GPT recognizes:
→ Use Case: Gmail Draft
→ Agent: Claude (contextual)
→ Phase: Check MATRIX status
```

### Phase 2: Route to Claude
```
GPT → Claude:
"User wants to draft email to sarah@example.com about project delay.

Per GOOGLE_AGENTS_RACI.md:
- This is contextual drafting
- Claude is Responsible (R)

Per CAPABILITIES_MATRIX:
- Gmail Drafts: PILOT_DESIGNED (or VERIFIED)
- Risk: OS_SAFE
- Playbook: PILOT_GMAIL_DRAFTS_FLOW.md

Please execute draft flow."
```

### Phase 3: Claude Executes
```
Claude follows PILOT_GMAIL_DRAFTS_FLOW.md:
1. Check MATRIX (capability status)
2. Check RACI (confirm responsibility)
3. Gather context (thread, docs, calendar, local, web)
4. Draft content
5. Present for Or's review
6. If approved:
   - Create draft via MCP (if G2.2 done)
   - Or save to file (if before G2.2)
7. Log operation
8. Report to Or
```

### Phase 4: GPT Tracks
```
GPT observes:
→ Claude created draft successfully
→ Logged to OPS/LOGS/google-operations.jsonl
→ Or received draft ID

GPT can now:
→ Offer next steps (edit, send, discard)
→ Track pattern (how often this use case happens)
→ Suggest automation (if repetitive)
```

---

## Pilot הוא Template - איך להעתיק

**כאשר Or מבקש יכולת חדשה** (למשל: Gmail Send):

### 1. GPT בודק אם יש Pilot
```
Request: "Send email to customer@example.com"

GPT checks:
→ Is there a PILOT for "Gmail Send"?
→ Check: DOCS/PILOT_GMAIL_SEND_FLOW.md exists?

If NO:
→ Suggest creating pilot using Gmail Drafts template
→ Ask Or: "Should Claude create PILOT_GMAIL_SEND_FLOW?"
```

### 2. יצירת Pilot חדש (Copy Pattern)
```
GPT → Claude:
"Create new pilot: Gmail Send

Template: PILOT_GMAIL_DRAFTS_FLOW.md
Changes:
- Section 1: Scope = send emails (not just drafts)
- Section 2.3: operation = gmail.send
- Section 3: Risk = CLOUD_OPS_HIGH (was OS_SAFE)
- Section 5: Add 5 safeguards:
  1. CLOUD_OPS_HIGH approval ('מאשר שליחה')
  2. Rate limit: 10 emails/hour
  3. Logging enabled
  4. Approval TTL: 60 minutes
  5. Policy block: no forwarding rules

Output: PILOT_GMAIL_SEND_FLOW.md"
```

### 3. עדכון MATRIX + BRIDGE
```
After pilot created:
1. Add row to CAPABILITIES_MATRIX:
   - Gmail Send capability
   - Status: PILOT_DESIGNED
   - Risk: CLOUD_OPS_HIGH
   - All 5 safeguards documented

2. Update this BRIDGE file:
   - Add Gmail Send use case recognition
   - Add RACI routing (Claude for single, GPTs GO for bulk)
```

---

## דוגמה: Gmail Send Capability (עתידי)

**User asks**: "Send this email draft to customer"

**GPT Response** (after Gmail Send pilot exists):
```
Current status (per CAPABILITIES_MATRIX):
- Gmail Send: PILOT_DESIGNED (or VERIFIED)
- Playbook: PILOT_GMAIL_SEND_FLOW.md
- Risk: CLOUD_OPS_HIGH

This requires:
1. Claude presents draft for final review
2. Or approves with: "מאשר שליחה"
3. Approval valid for 60 minutes
4. Claude sends via MCP
5. Logged to OPS/LOGS/
6. Rate limit: 10 sends/hour

Ready to proceed?
```

---

## Phase Tracking Summary (עדכון)

### Phase G1 ✅ (Complete 2025-11-17):
- Autonomy model
- Scopes analysis
- RACI matrix
- Status: DESIGN_COMPLETE

### Phase G2.1 ✅ (Complete 2025-11-17):
- OAuth architecture
- Authentication pattern
- Workflow skeletons
- Safeguards framework
- Observability plan
- Status: DESIGN_READY

### Phase G2.1-Pilot ✅ (Complete 2025-11-17):
- **Gmail Drafts pilot** - complete end-to-end flow
- **Template established** - copy for all future capabilities
- **CAPABILITIES_MATRIX** - Gmail Drafts row added
- **MCP_GPT_CAPABILITIES_BRIDGE** - pilot guidance added
- Status: PILOT_DESIGNED

### Phase G2.2 ⏳ (Next):
- Execute OAuth workflows (Executor)
- Or's one-time consent (includes gmail.compose)
- Test Gmail Drafts pilot
- Status: PILOT_DESIGNED → VERIFIED
- Status: Awaiting Executor

### Phase G2.3 ⏳ (Future):
- Copy pilot template for Gmail Send
- Copy pilot template for Drive operations
- Copy pilot template for Calendar
- Status: Planned

---

## Critical Reminders for GPTs (עדכון)

### 1. Gmail Drafts is the Template
```
✅ "Use PILOT_GMAIL_DRAFTS_FLOW as template for all Google capabilities"
✅ "Copy structure: Intent → Plan → Execution → Report → Logs"
✅ "Adjust only: operation, scope, risk, safeguards"
```

### 2. Always Check Pilot Status
```
Before routing to Claude:
1. Check if pilot exists (DOCS/PILOT_[CAPABILITY]_FLOW.md)
2. Check CAPABILITIES_MATRIX (status: PILOT_DESIGNED or VERIFIED)
3. Check RACI (who's responsible)
4. If no pilot: Suggest creating from template
```

### 3. Gmail Drafts is OS_SAFE
```
✅ "Draft creation requires no CLOUD_OPS_HIGH approval"
✅ "Drafts never sent automatically"
✅ "Or reviews content, then approves creation"
✅ "Fully reversible (Or can delete/edit)"
```

### 4. Pilot ≠ Operational
```
PILOT_DESIGNED status means:
- Flow is designed
- Safeguards defined
- Playbook ready
- BUT: Not operational yet (OAuth not configured)

VERIFIED status means:
- OAuth configured (G2.2 executed)
- MCP server running
- Tested successfully
- Operational ✅
```

### 5. Route Smart
```
Contextual draft → Claude (R)
Template draft → GPTs GO (R)
Bulk drafts → GPTs GO (R)
Single draft with research → Claude (R)
```

---

## עדכון אחרון

**2025-11-17 (Phase G2.1-Pilot Complete)**:
- ✅ PILOT_GMAIL_DRAFTS_FLOW.md created (22.3KB)
- ✅ Complete end-to-end playbook (Intent → Logs)
- ✅ CAPABILITIES_MATRIX updated (Gmail Drafts row)
- ✅ MCP_GPT_CAPABILITIES_BRIDGE updated (this file)
- ✅ Template established for future capabilities

**Total Google MCP Documentation**: 126KB (G1 + G2.1 + G2.1-Pilot)

**Next**: Or approves pilot → G2.2 execution → Gmail Drafts operational

---

**תחזוקה**: Claude (עם אישור אור)  
**עדכון אחרון**: 2025-11-17 (Phase G2.1-Pilot Complete)  
**גרסה**: 2.1 (pilot template added)
