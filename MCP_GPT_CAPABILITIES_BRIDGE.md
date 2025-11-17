# MCP – GPT Side Bridge to CAPABILITIES_MATRIX

## הקשר

בפרויקט זה, Claude Desktop עובד עם MCP וכלי ענן עבור אור.  
הקובץ `CAPABILITIES_MATRIX.md` בריפו `edri2or-commits/make-ops-clean` הוא:

- מקור האמת (SSOT) למצב היכולות והחיבורים של Claude/MCP.
- מתוחזק על ידי Claude כחלק מהלולאות שלו.
- משקף את מצב החיבורים:
  - GitHub
  - Local (Filesystem / PowerShell / Scripts)
  - **Google MCP** (Gmail / Drive / Calendar / Sheets / Docs) ⭐ **Phase G2.1 הושלם (2025-11-17)**
  - GCP דרך GitHub Actions (WIF / Secret Manager / APIs)
  - ועוד כלים (Canva, Web וכו').

---

## 🆕 Google MCP Autonomy Layer - Phase G2.1 Complete (2025-11-17)

**מה השתנה**:

Claude בנה ארכיטקטורה טכנית מלאה ל-OAuth + Google MCP:

### המסמכים המרכזיים:

1. **[`DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md`](DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md)** (28.7KB) - Phase G1
   - חזון, scopes, מודל autonomy

2. **[`DOCS/GOOGLE_AGENTS_RACI.md`](DOCS/GOOGLE_AGENTS_RACI.md)** (22.4KB) - Phase G1
   - חלוקת תפקידים Claude vs GPTs GO

3. **[`DOCS/GOOGLE_MCP_OAUTH_ARCH.md`](DOCS/GOOGLE_MCP_OAUTH_ARCH.md)** (52.6KB) ⭐ **NEW - Phase G2.1**
   - ארכיטקטורה טכנית מלאה
   - OAuth 2.0 + Service Account + WIF
   - 3 flows מפורטים
   - 4 workflow skeletons
   - Safeguards framework
   - Observability plan

### Phase G2.1 Status (COMPLETE):
- ✅ OAuth Architecture - תכנון מלא
- ✅ Authentication Pattern - OAuth + SA + WIF (keyless)
- ✅ Workflow Skeletons - 4 GitHub Actions workflows מעוצבים
- ✅ Safeguards Framework - 5 layers של הגנה
- ✅ Observability Plan - status files, health checks, audit trails
- ✅ CAPABILITIES_MATRIX Section 3 - עודכן עם Safeguards column
- ✅ MCP_GPT_CAPABILITIES_BRIDGE - עודכן (this file)

### Phase G2.2 (NEXT):
- Requires **Executor** (not Or, not Claude alone)
- Requires Or's **one-time OAuth consent click**
- All workflows ready to execute
- Technical setup automated except OAuth click

---

## כאשר GPT מתכנן שכבות אוטונומיה/חיבורים/אוטומציות

### 1. להניח ש:
- **CAPABILITIES_MATRIX** הוא המאסטר למידע על יכולות Claude
- כל שינוי יכולת אמור להיסגר בלולאה שבה Claude מעדכן את הקובץ
- **Google MCP** עכשיו ב-Phase G2.1 (OAuth Architecture Complete) - אין runtime access עדיין

### 2. לעזור לאור:
- לבחור "מנות" (חיבורים קטנים) לחיזוק יכולות
- לנסח לקלוד הוראות מדויקות שמבוססות על המטריצה
- להקפיד שכל משימה לקלוד כוללת:
  - תכנון → ביצוע → עדכון ב-`CAPABILITIES_MATRIX.md`

### 3. ספציפית ל-Google MCP (Phase G2.1+):
- **לא לבקש מאור** "תוסיף secret" או "תפתח console"
- **לא להניח** ש-Claude יכול לשלוח מיילים (עדיין read-only)
- **כן לתכנן** workflows שידרשו:
  - Executor עם גישה (לא אור)
  - אישור CLOUD_OPS_HIGH מאור (רק לפעולות משמעותיות)
  - עדכון CAPABILITIES_MATRIX אחרי כל שינוי
- **כן להסתכל** ב-GOOGLE_MCP_OAUTH_ARCH.md לפרטים טכניים מלאים
- **כן להשתמש** ב-GOOGLE_AGENTS_RACI.md לבחירת agent נכון

### 4. Safeguards = חובה (Phase G2.1 Decision):
- כל יכולת חדשה ב-CAPABILITIES_MATRIX **חייבת** לכלול עמודת "Safeguards"
- לא מספיק "יש יכולת" - צריך "יש יכולת + הגנות"
- 5 Layers של הגנה:
  1. Capability Tracking (MATRIX as guardrail)
  2. Approval Templates (structured, explicit)
  3. Rate Limiting (hard limits per service)
  4. Mandatory Logging (audit trail)
  5. Policy Blocks (technical enforcement)

### 5. לזכור:
- המטרה הסופית: 100% יכולת בכל כלי (Gmail, Drive, GitHub, GCP, Local וכו')
- תחת Approval Gate יחיד – אור
- אבל Or = Intent + Approval בלבד, לא DevOps executor
- **Preparedness Tracking**: Monthly reviews של autonomy metrics

---

## דוגמה: איך GPT צריך לעבוד עם Google MCP (עדכון Phase G2.1)

### ❌ לא טוב:
```
GPT: "אור, תוסיף את ה-GMAIL_TOKEN ל-Secret Manager ואז תעדכן את claude_desktop_config.json"
```

### ✅ טוב:
```
GPT: "אני רואה שClaude צריך יכולת לשלוח מיילים.
      
      לפי CAPABILITIES_MATRIX, Google MCP עכשיו ב-Phase G2.1 (OAuth Architecture Complete).
      
      Claude כבר בנה:
      1. תכנית מלאה (CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md)
      2. RACI matrix (GOOGLE_AGENTS_RACI.md)
      3. ארכיטקטורה טכנית מלאה (GOOGLE_MCP_OAUTH_ARCH.md)
      4. 4 GitHub Actions workflows מוכנים להרצה
      
      השלב הבא (G2.2 - Execution) דורש:
      1. Executor שיריץ workflows (לא אתה)
      2. אישור אסטרטגי ממך (כן/לא על התכנון)
      3. קליק OAuth אחד ממך (כשה-workflow יפיק URL)
      
      האם אתה מאשר את התכנון של G2.1 ורוצה שנתקדם ל-G2.2?"
```

### ✅ טוב יותר - עם Safeguards:
```
GPT: "Claude רוצה יכולת לשלוח מיילים.
      
      לפי GOOGLE_MCP_OAUTH_ARCH.md, היכולת הזו תבוא עם:
      
      Safeguards:
      1. CLOUD_OPS_HIGH approval (מאשר שליחה) - כל מייל
      2. Rate limit: 10 מיילים/שעה
      3. Logging חובה ל-OPS/LOGS/google-operations.jsonl
      4. Approval TTL: 60 דקות
      5. Policy block: לא ניתן ליצור forwarding rules
      
      Agent Routing (לפי RACI):
      - Claude: מיילים בודדים, הקשריים, חשובים
      - GPTs GO: bulk sends, קמפיינים, templated
      
      התכנון מלא. האם להתקדם ל-Execution (G2.2)?"
```

---

## Capability Update Protocol (Phase G2.1+)

**כאשר מוסיפים יכולת חדשה ב-Google**:

### 1. בדוק RACI קודם:
```
Is this Claude's responsibility or GPTs GO's?
→ Check GOOGLE_AGENTS_RACI.md
→ If Claude: Continue
→ If GPTs GO: Delegate or consult
```

### 2. בדוק Safeguards:
```
What's the risk level?
→ OS_SAFE: No safeguards needed
→ CLOUD_OPS_MEDIUM: Logging + notification
→ CLOUD_OPS_HIGH: All 5 layers

Document safeguards in CAPABILITIES_MATRIX (new row)
```

### 3. תכנן Observability:
```
How will we know it worked?
→ Status file path: OPS/STATUS/google-{operation}.json
→ Log entry format: OPS/LOGS/google-operations.jsonl
→ Health check: What API call verifies functionality?
```

### 4. עדכן MATRIX:
```
Add row with:
- Capability name
- Status (Design/Ready/Verified)
- Details
- Safeguards (ALL 5 if CLOUD_OPS_HIGH)
- Last Verified date
```

### 5. תעד ב-Phase Tracking:
```
Which phase adds this capability?
→ G2.2: OAuth + base access
→ G2.3: Advanced features
→ G3: Autonomy features
→ G4: Proactive features
```

---

## דוגמה: Gmail Send Capability Workflow

**User asks**: "Can Claude send emails?"

**GPT Response**:
```
Current status (per CAPABILITIES_MATRIX):
- Gmail send: 🔄 Phase G2.3 (Design Ready)
- Status: Not available yet (OAuth not configured)

What's ready:
✅ Full architecture (GOOGLE_MCP_OAUTH_ARCH.md)
✅ Safeguards defined (5 layers)
✅ Workflows designed (skeleton ready)
✅ RACI assignment (Claude responsible for single sends)

What's needed:
⏳ Phase G2.2: OAuth setup (Executor + Or consent)
⏳ Phase G2.3: Enable gmail.send scope + verify

Timeline:
- G2.2: ~30-60 min (mostly automated)
- G2.3: ~15 min (scope addition + test)

Once ready, sending email will require:
1. Claude drafts (OS_SAFE)
2. Or approves: "מאשר שליחה"
3. Claude sends via MCP
4. Logged to OPS/LOGS/

Rate limit: 10 emails/hour
Approval TTL: 60 minutes

Ready to proceed with G2.2?
```

---

## Phase Tracking Summary

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

### Phase G2.2 ⏳ (Next):
- Execute workflows
- OAuth consent (Or)
- Verify MCP server
- Status: Awaiting Executor

### Phase G3 ⏳ (Future):
- Controlled autonomy
- Approval gates operational
- Monthly Preparedness reviews
- Status: Planned

### Phase G4 ⏳ (Future):
- Advanced autonomy
- Proactive suggestions
- Cross-service orchestration
- Status: Planned

---

## Critical Reminders for GPTs

### 1. Never Assume Capabilities
```
❌ "Claude will send that email for you"
✅ "Claude can draft that email. Sending requires G2.3 (not yet available)"
```

### 2. Always Check MATRIX First
```
Before planning any Google operation:
1. Read CAPABILITIES_MATRIX Section 3
2. Check status (Verified/Design/Planned)
3. If Verified: Check safeguards
4. If not Verified: Don't promise capability
```

### 3. Respect RACI Boundaries
```
Before assigning work:
1. Read GOOGLE_AGENTS_RACI.md
2. Check who is Responsible (R)
3. If Claude: Proceed
4. If GPTs GO: Delegate appropriately
5. If conflict: Escalate to Or
```

### 4. Document Safeguards
```
When adding capability:
1. Define risk level (OS_SAFE/MEDIUM/HIGH)
2. List all safeguards (approval, rate, logging, etc.)
3. Update CAPABILITIES_MATRIX with Safeguards column
4. Never mark "Verified" without tested safeguards
```

### 5. Track Preparedness
```
Monthly review questions:
1. How many Google operations this month?
2. What % required CLOUD_OPS_HIGH approval?
3. Any safeguard triggers (rate limits, blocks)?
4. Emerging patterns or risks?
5. Should we adjust safeguards?
```

---

## עדכון אחרון

**2025-11-17 (Phase G2.1 Complete)**:
- ✅ Google MCP OAuth Architecture (52.6KB) created
- ✅ Safeguards framework (5 layers) defined
- ✅ Workflow skeletons (4 files) designed
- ✅ Observability plan complete
- ✅ CAPABILITIES_MATRIX Section 3 updated (Safeguards column added)
- ✅ This file updated with G2.1 guidance

**Next**: Or approves G2.1 → Executor runs G2.2 → Verify → Begin G3

---

**תחזוקה**: Claude (עם אישור אור)  
**עדכון אחרון**: 2025-11-17 (Phase G2.1 Complete)  
**גרסה**: 2.0 (major update with G2.1 architecture)
