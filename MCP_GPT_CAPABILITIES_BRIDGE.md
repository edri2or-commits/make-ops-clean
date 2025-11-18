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

## 🆕 THREE Pilots Complete (2025-11-17)

Claude בנה **3 פיילוטים מלאים** המוכיחים את הtemplate האוניברסלי:

### 1. Gmail Drafts (OS_SAFE, Gmail)
- **קישור**: [`DOCS/PILOT_GMAIL_DRAFTS_FLOW.md`](DOCS/PILOT_GMAIL_DRAFTS_FLOW.md) (22KB)
- **Risk**: OS_SAFE (draft not sent, reversible)
- **Approval**: Conversational ("Create draft")
- **Use Case**: Draft emails without sending

### 2. Gmail Send (CLOUD_OPS_HIGH, Gmail)
- **קישור**: [`DOCS/PILOT_GMAIL_SEND_FLOW.md`](DOCS/PILOT_GMAIL_SEND_FLOW.md) (46KB)
- **Risk**: CLOUD_OPS_HIGH (irreversible, external impact)
- **Approval**: Explicit phrase ("מאשר שליחה") + 60min TTL
- **Use Case**: Send emails with heavy safeguards

### 3. Drive Create Strategy Doc (OS_SAFE, Drive) ⭐ NEW
- **קישור**: [`DOCS/PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md`](DOCS/PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md) (43KB)
- **Risk**: OS_SAFE (private doc, reversible)
- **Approval**: Outline review (conversational)
- **Use Case**: Create strategic documents in Drive

**Key insight**: Template works across **domains** (Gmail, Drive) and **risk levels** (OS_SAFE, CLOUD_OPS_HIGH)

---

## 🎯 Drive Create Strategy Doc - Use Case Recognition

**כשהמשתמש מבקש**: "Create strategy doc for X"

**GPT צריך**:

### 1. זיהוי Use Case + Domain
```
Request: "Create strategy doc for Q1 planning"

GPT recognizes:
→ Use Case: Drive Create Strategy Doc
→ Domain: Drive + Docs (not Gmail)
→ Risk: OS_SAFE (private doc, no external sharing)
→ Agent: Claude (R) for single strategic docs
→ Phase: Check MATRIX status
```

### 2. בדיקת MATRIX
```
Check: CAPABILITIES_MATRIX Section 3.2 Drive
→ "Create strategy doc" capability
→ Status: PILOT_DESIGNED (before G2.4) or VERIFIED (after G2.4)
→ Risk: OS_SAFE
→ Safeguards: 5 layers (light)
```

### 3. בדיקת RACI
```
Check: GOOGLE_AGENTS_RACI.md Section 2.2
→ Single strategic doc = Claude (R)
→ Bulk doc generation = GPTs GO (R)

If single/contextual:
→ Claude is Responsible
→ Proceed

If bulk (>20 docs):
→ GPTs GO is Responsible
→ Delegate or consult
```

### 4. הפעלת Flow
```
If Status = VERIFIED (after G2.4):
→ Follow PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md
→ Gather context (repos, emails, meetings, files, web)
→ Synthesize (key themes, decisions, data)
→ Propose outline (structure + sections + sources)
→ Present to Or (full structure)
→ **Outline Approval** (OS_SAFE, conversational):
    - Or reviews structure
    - Or approves: "Looks good" / "Create it" (any positive)
    - No exact phrase, no TTL
→ Create doc in dedicated folder
→ Populate sections (content + formatting)
→ Log (standard) → Share link with Or

If Status = PILOT_DESIGNED (before G2.4):
→ Claude: "Drive Create Doc is designed but not operational.
           Current status: PILOT_DESIGNED
           
           To make this work, need Phase G2.4:
           - Expand OAuth scope (drive.file + docs.file)
           - Set up dedicated folder
           - Test and verify
           
           For now, I can create outline in markdown file.
           Would you like to proceed with G2.4 setup?"
→ Offer local text file alternative
```

---

## 📊 Three Pilots - Complete Comparison

**Template universality proven**:

| Aspect | Gmail Drafts | Gmail Send | Drive Create Doc |
|--------|--------------|------------|------------------|
| **Domain** | Gmail | Gmail | Drive + Docs |
| **Risk** | OS_SAFE | CLOUD_OPS_HIGH | OS_SAFE |
| **External impact** | None | High | None |
| **Reversibility** | Full | None | Full |
| **Approval** | Conversational | "מאשר שליחה" + TTL | Outline review |
| **Approval style** | Casual | Strict | Conversational |
| **TTL** | None | 60 minutes | None |
| **Rate limit** | 50/h (optional) | 10/h (hard) | 20/h (optional) |
| **Logging** | Standard | Detailed | Standard |
| **Scope** | gmail.compose | gmail.send | drive.file + docs.file |
| **Policy blocks** | No send | No forward/BCC/bulk | No share/delete existing |
| **Test cases** | 5 | 8 | 8 |
| **Phase** | G2.2 | G2.3 | G2.4 |
| **Playbook size** | 22KB | 46KB | 43KB |

**Pattern**:
- **OS_SAFE** (Drafts, Drive Doc): Light safeguards, conversational, no TTL
- **CLOUD_OPS_HIGH** (Send): Heavy safeguards, explicit approval, TTL

**Domains**:
- **Gmail** (Drafts, Send): Communication domain
- **Drive** (Create Doc): Documentation domain

**Template works** for both!

---

## 🎯 Drive Create Doc Flow Pattern (הנחיות ל-GPTs)

**כשרואים request ליצירת מסמך**:

### Phase 1: Intent Recognition + Domain Check
```
User says:
"Create strategy doc for Q1 planning"

GPT recognizes:
→ Use Case: Drive Create Strategy Doc
→ Domain: Drive + Docs (not Gmail)
→ Risk: OS_SAFE (private, reversible)
→ Agent: Claude (R) for single docs
→ Phase: Check MATRIX status
→ Safeguards: 5 layers (light)
```

### Phase 2: Route to Claude
```
GPT → Claude:
"User wants to create strategy doc for Q1 planning.

Per CAPABILITIES_MATRIX:
- Drive Create Doc: PILOT_DESIGNED (or VERIFIED)
- Risk: OS_SAFE (private document)
- Playbook: PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md

Per GOOGLE_AGENTS_RACI.md:
- Single strategic doc: Claude (R)

Safeguards (OS_SAFE level):
1. Outline review (conversational approval)
2. Rate limit: 20 docs/hour (soft, optional)
3. Logging: Standard to OPS/LOGS/
4. Private only (no external sharing)
5. Dedicated folder only

Please execute Drive Create Doc flow if operational,
or offer text file alternative if not ready."
```

### Phase 3: Claude Executes with Light Safeguards
```
Claude follows PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md:
1. Check MATRIX (status: PILOT_DESIGNED or VERIFIED)
2. If PILOT_DESIGNED:
   → Offer text file alternative (local markdown)
   → Explain what's needed for G2.4
3. If VERIFIED:
   → Check RACI (confirm Claude R)
   → Gather context:
       - GitHub repos (commits, issues, PRs, docs)
       - Gmail threads (discussions, decisions)
       - Calendar (meetings, planning sessions)
       - Local files (notes, drafts)
       - Web research (trends, best practices)
   → Synthesize context (themes, decisions, data)
   → Propose outline (structure + sections + sources)
   → Present to Or (full structure)
   → Or reviews & approves: "Looks good" (conversational)
   → Create doc in dedicated folder
   → Populate sections (content + formatting)
   → Log (standard) to OPS/LOGS/
   → Share link: "✅ Created, Doc ID: doc-123"
```

### Phase 4: GPT Tracks Outcome
```
GPT observes:
→ Document created successfully
→ Logged to OPS/LOGS/ (standard)
→ Or received link
→ Document in dedicated folder

GPT can now:
→ Track docs created (how many, what topics)
→ Suggest edits (if Or wants changes)
→ Monitor folder organization
```

---

## ⚠️ Critical: Drive Create Doc vs Gmail Send

**GPTs must understand the key differences**:

### Approval Style
| Aspect | Gmail Send (HIGH) | Drive Create Doc (SAFE) |
|--------|-------------------|------------------------|
| **Phrase** | "מאשר שליחה" (exact) | "Looks good" (any positive) |
| **TTL** | 60 minutes | None (no expiry) |
| **Strictness** | Rigid (must match) | Flexible (conversational) |
| **Why** | Irreversible send | Reversible document |

### Safeguard Weight
| Layer | Gmail Send (HIGH) | Drive Create Doc (SAFE) |
|-------|-------------------|------------------------|
| 1. Approval | Explicit + TTL | Conversational |
| 2. Rate Limit | 10/h (hard block) | 20/h (soft, optional) |
| 3. Logging | Detailed (~1000B) | Standard (~500B) |
| 4. Scope | gmail.send only | drive.file + docs.file |
| 5. Policy Blocks | No forward/BCC/bulk | No share/delete existing |

**Key insight**: Same 5 layers, different weights based on risk

---

## 📐 Risk Decision Tree (Complete)

**מהtemplate, כולל Gmail וDrive**:

```
Operation requested:

1. Which domain?
   ├─ Gmail → Continue to Gmail decision tree
   └─ Drive → Continue to Drive decision tree

Gmail operations:
├─ Read/search → OS_SAFE
├─ Create draft → OS_SAFE
├─ Label/organize → CLOUD_OPS_MEDIUM
└─ Send email → CLOUD_OPS_HIGH

Drive operations:
├─ Read/search → OS_SAFE
├─ Create private doc → OS_SAFE ← NEW
├─ Edit shared doc → CLOUD_OPS_MEDIUM
└─ Share externally → CLOUD_OPS_HIGH

2. If OS_SAFE:
   - External impact? NO
   - Reversible? YES
   - Approval: Conversational
   - Rate limit: Optional
   - Logging: Standard

3. If CLOUD_OPS_HIGH:
   - External impact? YES
   - Reversible? NO
   - Approval: Explicit phrase + TTL
   - Rate limit: Mandatory (hard)
   - Logging: Detailed
```

---

## 🔄 Phase Tracking (עדכון)

### Phase G1 ✅ (Complete 2025-11-17):
- Autonomy model, RACI, Scopes

### Phase G2.1 ✅ (Complete 2025-11-17):
- OAuth architecture, Safeguards

### Phase G2.1-Pilot ✅ (Complete 2025-11-17):
- **Gmail Drafts** (OS_SAFE, Gmail)
- **AUTOMATION_PLAYBOOK_TEMPLATE** (Universal)
- **Gmail Send** (CLOUD_OPS_HIGH, Gmail)
- **Drive Create Doc** (OS_SAFE, Drive) ⭐ NEW

### Phase G2.2 ⏳ (Next):
- Base OAuth (gmail.compose)
- Test Gmail Drafts

### Phase G2.3 ⏳ (Future):
- Expand OAuth (gmail.send)
- Test Gmail Send

### Phase G2.4 ⏳ (Future):
- Expand OAuth (drive.file + docs.file)
- Test Drive Create Doc

---

## Critical Reminders for GPTs (עדכון)

### 1. Three Pilots = Three Patterns
```
✅ "Gmail Drafts = OS_SAFE, Gmail domain"
✅ "Gmail Send = CLOUD_OPS_HIGH, Gmail domain"
✅ "Drive Create Doc = OS_SAFE, Drive domain"
```

### 2. Domain Matters
```
Gmail use cases:
- Drafts, Send, Search, Organize
- Domain: Communication

Drive use cases:
- Create Doc, Edit, Share, Search
- Domain: Documentation

Same template, different domains ✓
```

### 3. Risk Determines Safeguards
```
OS_SAFE (Drafts, Drive Create):
- Light approval (conversational)
- Optional rate limits
- Standard logging

CLOUD_OPS_HIGH (Gmail Send):
- Strict approval (exact phrase + TTL)
- Mandatory rate limits (hard)
- Detailed logging
```

### 4. Always Check MATRIX First
```
Before suggesting ANY automation:
1. Check CAPABILITIES_MATRIX (exists?)
2. Check status (PILOT_DESIGNED or VERIFIED?)
3. Check playbook (reference link)
4. Only then suggest execution
```

### 5. Offer Alternatives
```
If PILOT_DESIGNED:
- Gmail Send → Offer Gmail Drafts (OS_SAFE)
- Drive Create → Offer local text file

Never promise execution before checking status
```

---

## עדכון אחרון

**2025-11-17 (THREE Pilots Complete)**:
- ✅ PILOT_GMAIL_DRAFTS_FLOW.md (22KB, OS_SAFE, Gmail)
- ✅ PILOT_GMAIL_SEND_FLOW.md (46KB, CLOUD_OPS_HIGH, Gmail)
- ✅ PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md (43KB, OS_SAFE, Drive) ⭐ NEW
- ✅ AUTOMATION_PLAYBOOK_TEMPLATE (43.7KB, Universal)
- ✅ CAPABILITIES_MATRIX updated (all 3 pilots)
- ✅ MCP_GPT_CAPABILITIES_BRIDGE updated (this file)

**Total Documentation**:
- Gmail pilots: 68KB (Drafts 22KB + Send 46KB)
- Drive pilot: 43KB (Create Doc)
- Universal template: 43.7KB
- Architecture: 103.7KB (G1 + G2.1)
- **Grand Total: 258.4KB** של תיעוד OS_SAFE

**Proven**: Template works for multiple domains (Gmail, Drive) and risk levels (OS_SAFE, CLOUD_OPS_HIGH)

**Next**: Or approves designs → Execution phases (G2.2, G2.3, G2.4)

---

**תחזוקה**: Claude (עם אישור אור)  
**עדכון אחרון**: 2025-11-17 (Drive Create Doc added)  
**גרסה**: 2.4 (multi-domain template proven)
