# MCP – GPT Side Bridge to CAPABILITIES_MATRIX

## הקשר

בפרויקט זה, Claude Desktop עובד עם MCP וכלי ענן עבור אור.  
הקובץ `CAPABILITIES_MATRIX.md` בריפו `edri2or-commits/make-ops-clean` הוא:

- מקור האמת (SSOT) למצב היכולות והחיבורים של Claude/MCP.
- מתוחזק על ידי Claude כחלק מהלולאות שלו.
- משקף את מצב החיבורים:
  - GitHub
  - Local (Filesystem / PowerShell / Scripts)
  - **Google MCP** (Gmail / Drive / Calendar / Sheets / Docs) ⭐ **עכשיו בעיצוב (Phase G1)**
  - GCP דרך GitHub Actions (WIF / Secret Manager / APIs)
  - ועוד כלים (Canva, Web וכו').

---

## 🆕 Google MCP Autonomy Layer (2025-11-17)

**מה השתנה**:

Claude עכשיו בונה שכבת אוטונומיה על Google Workspace:

### המסמך המרכזי:
**[`DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md`](DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md)** (28.7KB)

### מה כולל:
1. **Current State** - מה Claude כבר יכול (read-only)
2. **Vision** - מה Claude רוצה להיות מסוגל (write, send, create)
3. **Scopes** - רשימת OAuth scopes מלאה + מטריצת סיכונים
4. **OS_SAFE vs CLOUD_OPS_HIGH** - גבולות ברורים לכל פעולה
5. **CAPABILITIES_MATRIX Integration** - איך Claude מעדכן את המטריצה
6. **Roadmap** - G1 (Design) → G2 (Bootstrap) → G3 (Autonomy) → G4 (Advanced)

### מודל הפעולה:
```
OS_SAFE (Claude alone):
- Read, analyze, search
- Create drafts (not sent)
- Propose actions
- Generate reports

CLOUD_OPS_MEDIUM (Or notified, reversible):
- Label/organize emails
- Create calendar events (invites sent automatically)
- Edit files (version history available)

CLOUD_OPS_HIGH (Or's explicit approval each time):
- Send emails
- Share files externally
- Delete events with attendees
- Permanent deletions
```

### Phase G1 Status (CURRENT):
- ✅ AUTONOMY_PLAN created (OS_SAFE document)
- ✅ CAPABILITIES_MATRIX Section 3 updated
- ⏳ MCP_GPT_CAPABILITIES_BRIDGE update (this file)

### Phase G2 (NEXT):
- Requires **Executor** (not Or, not Claude alone)
- Requires Or's **one-time OAuth consent click**
- Technical setup: APIs, credentials, MCP server config
- All automated except the OAuth click

---

## כאשר GPT מתכנן שכבות אוטונומיה/חיבורים/אוטומציות

### 1. להניח ש:
- **CAPABILITIES_MATRIX** הוא המאסטר למידע על יכולות Claude
- כל שינוי יכולת אמור להיסגר בלולאה שבה Claude מעדכן את הקובץ
- **Google MCP** עכשיו ב-Phase G1 (Design) - אין runtime access עדיין

### 2. לעזור לאור:
- לבחור "מנות" (חיבורים קטנים) לחיזוק יכולות
- לנסח לקלוד הוראות מדויקות שמבוססות על המטריצה
- להקפיד שכל משימה לקלוד כוללת:
  - תכנון → ביצוע → עדכון ב-`CAPABILITIES_MATRIX.md`

### 3. ספציפית ל-Google MCP:
- **לא לבקש מאור** "תוסיף secret" או "תפתח console"
- **לא להניח** ש-Claude יכול לשלוח מיילים (עדיין read-only)
- **כן לתכנן** workflows שידרשו:
  - Executor עם גישה (לא אור)
  - אישור CLOUD_OPS_HIGH מאור (רק לפעולות משמעותיות)
  - עדכון CAPABILITIES_MATRIX אחרי כל שינוי

### 4. לזכור:
- המטרה הסופית: 100% יכולת בכל כלי (Gmail, Drive, GitHub, GCP, Local וכו')
- תחת Approval Gate יחיד – אור
- אבל Or = Intent + Approval בלבד, לא DevOps executor

---

## דוגמה: איך GPT צריך לעבוד עם Google MCP

### ❌ לא טוב:
```
GPT: "אור, תוסיף את ה-GMAIL_TOKEN ל-Secret Manager ואז תעדכן את claude_desktop_config.json"
```

### ✅ טוב:
```
GPT: "אני רואה שClaude צריך יכולת לשלוח מיילים.
      
      לפי CAPABILITIES_MATRIX, Google MCP עכשיו ב-Phase G1 (Design).
      
      Claude כבר יצר תכנית מלאה ב-CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md.
      
      השלב הבא (G2) דורש:
      1. Executor שיריץ automation (לא אתה)
      2. אישור אסטרטגי ממך (כן/לא על הכיוון)
      3. קליק OAuth אחד ממך (כשה-provider יבקש)
      
      האם אתה רוצה שנתקדם ל-Phase G2?"
```

---

## עדכון אחרון

**2025-11-17**: נוספה שכבת Google MCP Autonomy (Phase G1)
- מסמך תכנון: `DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md`
- CAPABILITIES_MATRIX עודכן (Section 3)
- הקובץ הזה עודכן עם הנחיות Google MCP

---

**תחזוקה**: Claude (עם אישור אור)  
**עדכון אחרון**: 2025-11-17
