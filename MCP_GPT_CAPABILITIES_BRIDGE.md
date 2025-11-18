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

## 🆕 AUTOMATION_PLAYBOOK_TEMPLATE - Universal (2025-11-17)

**מה חדש**:

Claude יצר **template אוניברסלי** לכל האוטומציות במערכת:

### 📋 AUTOMATION_PLAYBOOK_TEMPLATE.md

**קישור**: [`DOCS/AUTOMATION_PLAYBOOK_TEMPLATE.md`](DOCS/AUTOMATION_PLAYBOOK_TEMPLATE.md) (43.7KB)

**מה זה**:
- Template חובה לכל automation במערכת (לא רק Google)
- כולל כל התחומים: Gmail, Drive, GitHub, GCP, Local, Make.com, עתידיים
- מבנה של 11 סעיפים מפורטים
- דוגמה ממולאת מלאה: Gmail Drafts (Section 8, 6.5KB)

**11 סעיפים**:
1. **Intent & Classification** - הצהרת intent + רמת סיכון
2. **Actors & RACI** - מי עושה מה (Or, Claude, GPTs GO, Executors)
3. **Plan** - צעדים לוגיים, risk לכל צעד
4. **Execution Skeleton** - trigger, flow, tools, approval gates
5. **Safeguards** - 5 שכבות חובה (approval, rate, log, scope, blocks)
6. **Observability** - logs, status files, success indicators
7. **CAPABILITIES_MATRIX Entry** - שורה מלאה עם כל safeguards
8. **Example** - Gmail Drafts מלא (worked example)
9. **Template Usage** - איך למלא, מתי להשתמש, checklist
10. **Integration** - קישור ל-MATRIX, RACI, BRIDGE
11. **Appendix** - quick reference (decision trees, templates)

**למה זה חשוב**:
- ✅ סטנדרט אחיד לכל האוטומציות
- ✅ מונע שכחת safeguards
- ✅ מבטיח CAPABILITIES_MATRIX עדכני
- ✅ מאלץ תיעוד לפני execution
- ✅ דוגמה מלאה (Gmail Drafts) להדרכה

---

## 🎯 MANDATORY: Template Before Automation

**חוק חדש** (החל מ-2025-11-17):

### כל automation חדשת חייבת playbook

**לפני יצירת automation**:
```
1. Copy AUTOMATION_PLAYBOOK_TEMPLATE.md
   → DOCS/[NAME]_PLAYBOOK.md

2. Fill ALL 9 sections
   - Use Gmail Drafts (Section 8) as guide
   - All 5 safeguards mandatory
   - Complete RACI matrix

3. Create CAPABILITIES_MATRIX entry
   - Row with all safeguards
   - Status: PILOT_DESIGNED (before execution)

4. Get Or's approval
   - Show complete playbook
   - Explain intent, risk, safeguards

5. ONLY THEN execute
   - If CLOUD_OPS_HIGH: Executor runs
   - Log to OPS/LOGS/
   - Update MATRIX status
```

**אין automation בלי playbook** = אין execution

---

## 📋 Template Checklist (חובה)

**לפני marking automation כ-"documented"**:

- [ ] כל 9 סעיפים מלאים
- [ ] RACI matrix מראה מי עושה מה
- [ ] רמת risk נקבעה + הצדקה
- [ ] כל 5 safeguards מתועדות
- [ ] פורמט logging מוגדר
- [ ] CAPABILITIES_MATRIX entry מוכן
- [ ] Or reviewed + approved (לפני CLOUD_OPS_HIGH)

**אם missing אפילו אחד** → Playbook לא complete

---

## 🔄 Gmail Drafts - הדוגמה הרשמית

**Gmail Drafts (Section 8 in template)**:
- ✅ Intent מלא + classification (Expansion, OS_SAFE)
- ✅ RACI matrix (10 tasks, roles clear)
- ✅ Plan (14 steps, risk per step)
- ✅ Execution flow (pseudo-schema מלא)
- ✅ All 5 safeguards documented
- ✅ Logging format (JSON example)
- ✅ CAPABILITIES_MATRIX row ready

**למה Gmail Drafts דוגמה טובה**:
- OS_SAFE (קל להבין)
- Complete flow (Intent עד Logs)
- כל הelement מתוך template
- שימושי (drafts = use case נפוץ)

**איך להשתמש**:
```
Creating new automation?
→ Open AUTOMATION_PLAYBOOK_TEMPLATE.md
→ Go to Section 8 (Gmail Drafts example)
→ Copy structure
→ Adjust: operation, scope, risk, safeguards
→ Your automation now has complete playbook
```

---

## 🎯 כאשר GPT מתכנן אוטומציה חדשה

### Protocol חובה:

**Step 1: בדיקת MATRIX**
```
User requests automation: "Send email to X"

GPT checks CAPABILITIES_MATRIX:
→ Does "Gmail Send" exist?
   - YES + VERIFIED → Use it
   - YES + BROKEN → Fix it
   - NO → Must create playbook first
```

**Step 2: אם לא קיים - יצירת Playbook**
```
Automation not in MATRIX:

GPT → Claude:
"User wants Gmail Send capability.

Per AUTOMATION_PLAYBOOK_TEMPLATE requirement:
1. Copy template: AUTOMATION_PLAYBOOK_TEMPLATE.md
2. Use Gmail Drafts (Section 8) as guide
3. Adjust for Gmail Send:
   - Risk: OS_SAFE → CLOUD_OPS_HIGH
   - Safeguards: Add approval phrase, rate limits, TTL
   - Scope: gmail.compose → gmail.send

4. Create CAPABILITIES_MATRIX entry
5. Get Or approval before execution

Please create playbook first, then we'll execute."
```

**Step 3: אישור Or**
```
Claude creates playbook:
→ DOCS/PILOT_GMAIL_SEND_FLOW.md

GPT → Or:
"Claude created complete playbook for Gmail Send.

Intent: Send emails via Claude with approval
Risk: CLOUD_OPS_HIGH
Safeguards:
1. Explicit approval: 'מאשר שליחה'
2. Rate limit: 10/hour
3. Logging: OPS/LOGS/
4. TTL: 60 minutes
5. Policy blocks: No forwarding rules

Playbook: [link to PILOT_GMAIL_SEND_FLOW.md]

Approve design before execution?"
```

**Step 4: רק אחרי אישור - Execution**
```
Or approves → Phase G2.2 execution
Or declines → Revise playbook
Or wants changes → Update playbook, re-approve
```

---

## 📊 Governance Documents Hierarchy

**מבנה התיעוד**:

```
CAPABILITIES_MATRIX.md (SSOT)
  ├─ MCP_GPT_CAPABILITIES_BRIDGE.md (this file)
  │
  ├─ AUTOMATION_PLAYBOOK_TEMPLATE.md (universal template)
  │   └─ Gmail Drafts (Section 8 - worked example)
  │
  ├─ Domain-specific docs:
  │   ├─ GOOGLE_AGENTS_RACI.md (Google operations)
  │   ├─ GOOGLE_MCP_OAUTH_ARCH.md (Google auth)
  │   └─ (future) GITHUB_AGENTS_RACI.md
  │
  └─ Capability playbooks:
      ├─ PILOT_GMAIL_DRAFTS_FLOW.md (complete)
      ├─ PILOT_GMAIL_SEND_FLOW.md (future)
      ├─ PILOT_DRIVE_CREATE_FLOW.md (future)
      └─ ... (all future automations)
```

**כל playbook חייב להישען על template**

---

## ⚠️ Enforcement: No Playbook = No Execution

**החל מעכשיו**:

### Rule 1: Claude checks template first
```
Before planning ANY automation:
1. Read CAPABILITIES_MATRIX
2. If capability missing → Check if playbook exists
3. If no playbook → Create using AUTOMATION_PLAYBOOK_TEMPLATE
4. Never execute CLOUD_OPS_HIGH without complete playbook
```

### Rule 2: GPTs enforce template
```
When GPT plans automation:
1. Check MATRIX (capability exists?)
2. Check playbook (DOCS/[NAME]_PLAYBOOK.md?)
3. If missing → Guide Claude to create from template
4. If exists but incomplete → Request completion
5. Only suggest execution after playbook approved
```

### Rule 3: Or's approval gate includes playbook
```
Or reviewing automation:
- "Does this have complete playbook?" ← mandatory question
- "Are all 5 safeguards documented?" ← mandatory check
- "Is MATRIX entry ready?" ← mandatory check

If any NO → Send back for playbook completion
```

---

## 📐 Risk Decision Tree (Quick Reference)

**איך לקבוע risk level**:

```
Does operation affect external parties/systems?
  ├─ NO → Can it be undone easily?
  │      ├─ YES → OS_SAFE
  │      └─ NO → CLOUD_OPS_MEDIUM
  └─ YES → Is it reversible within 24 hours?
         ├─ YES → CLOUD_OPS_MEDIUM
         └─ NO → CLOUD_OPS_HIGH

Examples:
- Create draft (not sent) → OS_SAFE
- Edit shared doc (version history) → CLOUD_OPS_MEDIUM
- Send email (irreversible) → CLOUD_OPS_HIGH
- Share file externally → CLOUD_OPS_HIGH
```

**Template has full decision tree** (Section 11)

---

## 🔄 Phase Tracking Summary (עדכון)

### Phase G1 ✅ (Complete 2025-11-17):
- Autonomy model
- Scopes analysis
- RACI matrix

### Phase G2.1 ✅ (Complete 2025-11-17):
- OAuth architecture
- Safeguards framework
- Workflow skeletons

### Phase G2.1-Pilot ✅ (Complete 2025-11-17):
- **Gmail Drafts pilot** - complete playbook
- **AUTOMATION_PLAYBOOK_TEMPLATE** - universal template ⭐ NEW
- **Template established** - all future automations use this

### Phase G2.2 ⏳ (Next):
- Execute OAuth workflows (Executor)
- Or's consent (gmail.compose)
- Test Gmail Drafts
- Status: PILOT_DESIGNED → VERIFIED

---

## ✅ Template Benefits

**מה הTemplate נותן**:

1. **Consistency** - כל automation נראית אותו דבר
2. **Completeness** - אי אפשר לשכוח safeguards
3. **Traceability** - CAPABILITIES_MATRIX always updated
4. **Approval clarity** - Or knows exactly what reviewing
5. **Copy-paste ready** - Gmail Drafts example = template
6. **Risk management** - explicit risk level per automation
7. **Audit trail** - logging mandatory in template
8. **Documentation** - playbook = permanent record

**ללא template**:
- ❌ Inconsistent documentation
- ❌ Missing safeguards
- ❌ MATRIX outdated
- ❌ Unclear approvals
- ❌ Weak audit trail

**עם template**:
- ✅ Every automation documented same way
- ✅ All safeguards explicit
- ✅ MATRIX always reflects reality
- ✅ Clear approval gates
- ✅ Complete audit trail

---

## 📝 Template Evolution

**Version**: 1.0 (2025-11-17)

**Future**:
- Template may be extended (sections added)
- Never reduced (safeguards only increase)
- Version in template header
- All automations reference version used

**Feedback loop**:
- As automations built → lessons learned
- Lessons → template updates
- Template becomes more comprehensive
- Examples added (currently: Gmail Drafts, future: CLOUD_OPS_HIGH examples)

---

## Critical Reminders for GPTs (עדכון)

### 1. Template is Mandatory
```
✅ "Every automation needs playbook using AUTOMATION_PLAYBOOK_TEMPLATE"
✅ "No exceptions - OS_SAFE through CLOUD_OPS_HIGH all need playbooks"
✅ "Gmail Drafts (Section 8) shows exactly how to fill template"
```

### 2. Check Template Before Planning
```
Before suggesting ANY automation:
1. Check: CAPABILITIES_MATRIX (exists?)
2. Check: Playbook exists? (DOCS/[NAME]_PLAYBOOK.md)
3. If no playbook → Claude must create from template first
4. Only then: Suggest execution
```

### 3. Template Checklist
```
Playbook complete when:
- [ ] All 9 sections filled
- [ ] RACI matrix complete
- [ ] Risk level + justification
- [ ] All 5 safeguards documented
- [ ] Logging format defined
- [ ] CAPABILITIES_MATRIX entry ready
- [ ] Or reviewed + approved
```

### 4. No Playbook = No Execution
```
❌ "Let's execute this automation"
✅ "Let's create playbook first using AUTOMATION_PLAYBOOK_TEMPLATE, 
    then get Or's approval, then execute"
```

### 5. Gmail Drafts = Reference
```
When creating new playbook:
"Use Gmail Drafts (Section 8 in template) as guide:
- Copy structure
- Adjust: operation, scope, risk, safeguards
- Keep format consistent"
```

---

## עדכון אחרון

**2025-11-17 (AUTOMATION_PLAYBOOK_TEMPLATE Created)**:
- ✅ AUTOMATION_PLAYBOOK_TEMPLATE.md created (43.7KB)
- ✅ Universal template for ALL automations
- ✅ Gmail Drafts worked example (Section 8)
- ✅ CAPABILITIES_MATRIX governance layer updated
- ✅ MCP_GPT_CAPABILITIES_BRIDGE updated (this file)

**Total Documentation**:
- Google MCP: 126KB (G1 + G2.1 + G2.1-Pilot)
- Universal Template: 43.7KB
- **Total System Documentation: 169.7KB**

**Next**: Or uses template for next automation (any domain)

---

**תחזוקה**: Claude (עם אישור אור)  
**עדכון אחרון**: 2025-11-17 (AUTOMATION_PLAYBOOK_TEMPLATE added)  
**גרסה**: 2.2 (universal template added)
