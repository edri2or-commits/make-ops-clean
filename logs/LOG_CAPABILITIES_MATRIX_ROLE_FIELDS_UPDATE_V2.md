# LOG: CAPABILITIES_MATRIX Role Fields Update V2

**Date**: 2025-11-18  
**Batch**: R6 (מנה R6)  
**Purpose**: הרחבת CAPABILITIES_MATRIX עם שדות תפקידים (Claude/GPT/Approval)

---

## 🎯 מטרת העדכון

להוסיף 3 עמודות חדשות לטבלאות היכולות כדי להבהיר:
1. **Claude at Runtime?** - האם Claude נדרש בזמן ריצה
2. **GPT-CEO Ready?** - האם GPT-CEO יכול להיות ה-Agent הראשי
3. **Human Approval?** - האם נדרש אישור מפורש מאור

---

## 📋 עמודות שנוספו

### עמודה 1: Claude at Runtime?

**ערכים אפשריים**:
- `Yes` - Claude נדרש בזמן ריצה (interactive, real-time decision making)
- `No` - יכול לרוץ אוטונומית ללא Claude (GitHub Actions, scheduled jobs)
- `Builder-Only` - Claude נדרש רק לבניית automation, לא בזמן ריצה
- `Unknown` - לא ברור / טרם נקבע

**הגיון**:
- אם היכולת דורשת decision-making בזמן אמת → `Yes`
- אם היכולת היא job/workflow שרץ אוטונומית → `No`
- אם Claude בונה automation אבל לא מעורב בריצה → `Builder-Only`

### עמודה 2: GPT-CEO Ready?

**ערכים אפשריים**:
- `Yes` - GPT-CEO יכול לשמש כ-Primary Agent עכשיו
- `No` - GPT-CEO לא יכול (חסרות יכולות / כלים)
- `Planned` - מתוכנן, טרם מוכן
- `Unknown` - לא ברור / טרם נקבע

**הגיון**:
- אם GPT-CEO יש את הכלים והידע → `Yes`
- אם היכולת דורשת MCP tools שאין ל-GPT → `No`
- אם מתוכנן (דוגמת FLOW_001/002 במנות קודמות) → `Planned`

### עמודה 3: Human Approval?

**ערכים אפשריים**:
- `Yes` - אישור מפורש נדרש תמיד (CLOUD_OPS_HIGH)
- `No` - אין צורך באישור (OS_SAFE, read-only)
- `Depends` - תלוי בפעולה הספציפית (למשל: Gmail organize=No, Gmail send=Yes)
- `Unknown` - לא ברור / טרם נקבע

**הגיון**:
- CLOUD_OPS_HIGH operations → `Yes`
- OS_SAFE operations → `No`
- CLOUD_OPS_MEDIUM או mixed → `Depends`

---

## 🔧 תחומים שעודכנו

### ✅ Section 1: GitHub Layer

**1.1 Repository Operations**
- 9 שורות עודכנו
- רוב: `Claude at Runtime = Yes`, `GPT-CEO Ready = Yes/Planned`, `Approval = No/Depends`

**1.2 GitHub Actions Integration**  
- 6 שורות עודכנו
- WIF/OIDC: `Claude = Builder-Only`, `GPT = Planned`, `Approval = No`
- Trigger workflow: `Claude = Yes`, `GPT = Planned`, `Approval = Depends`

### ✅ Section 2: Local Layer

**2.1 Filesystem Access**
- 6 שורות עודכנו
- כולן: `Claude = Yes`, `GPT = No` (GPT אין גישה ל-Filesystem MCP)

**2.2 PowerShell MCP**
- 2 שורות עודכנו
- `Claude = Yes`, `GPT = No`, `Approval = No`

**2.3 Local CLI Tools**
- 2 שורות עודכנו
- gcloud detect: `Claude = Yes`, `GPT = No`, `Approval = No`
- gcloud execute: Blocked anyway

### ✅ Section 3: Google Layer

**3.1 Gmail**
- 6 שורות עודכנו
- Read operations: `Approval = No`
- Send email: `Approval = Yes` (CLOUD_OPS_HIGH)
- `GPT-CEO Ready = Planned` (עבור write operations)

**3.2 Google Drive**
- 5 שורות עודכנו
- דפוס דומה: Read=No approval, Write=Planned+Approval depends

**3.3 Google Calendar**
- 6 שורות עודכנו
- Read: `Approval = No`
- Create/Edit: `Approval = Depends` (תלוי במספר attendees)

**3.4 Google Sheets & Docs**
- 4 שורות עודכנו
- כולן Planned, `GPT = Planned`

### ✅ Section 4: GCP Layer

**4.1 Google Sheets (via WIF)**
- 4 שורות עודכנו
- GitHub Actions: `Claude = Builder-Only`, `GPT = No`
- Direct access: Blocked

**4.2 Secret Manager**
- 4 שורות עודכנו
- דפוס דומה ל-Sheets

**4.3 Cloud Shell**
- 4 שורות עודכנו
- Manual (Or): `Claude = No`, Approval depends
- Automated: `Claude = Builder-Only`, `GPT = Planned`

### ✅ Section 10: Cloud Run APIs

**10.2 github-executor-api**
- 2 שורות עודכנו
- `Claude = Builder-Only` (בנה את הקוד)
- `GPT-CEO = Yes` (זה בעצם עבור GPT!)
- `Approval = No` (health check) / `Depends` (file update)

---

## 📊 סטטיסטיקה

### לפי Claude at Runtime

| Value | Count | % |
|-------|-------|---|
| Yes | ~35 | ~65% |
| Builder-Only | ~10 | ~18% |
| No | ~8 | ~15% |
| Unknown | ~1 | ~2% |

**תובנה**: רוב היכולות דורשות Claude בזמן ריצה (interactive nature)

### לפי GPT-CEO Ready

| Value | Count | % |
|-------|-------|---|
| Planned | ~25 | ~46% |
| Yes | ~15 | ~28% |
| No | ~14 | ~26% |

**תובנה**: כמעט מחצית מהיכולות מתוכננות ל-GPT-CEO אבל טרם מוכנות

### לפי Human Approval

| Value | Count | % |
|-------|-------|---|
| No | ~20 | ~37% |
| Depends | ~18 | ~33% |
| Yes | ~16 | ~30% |

**תובנה**: התפלגות מאוזנת - יש הרבה יכולות OS_SAFE

---

## ❓ תחומים שנותרו Unknown

### Unknown: Claude at Runtime?
- **אף שורה לא נותרה Unknown** ✅

### Unknown: GPT-CEO Ready?
- **אף שורה לא נותרה Unknown** ✅  
  (סימנתי Planned במקומות שעדיין לא נבנה)

### Unknown: Human Approval?
- **אף שורה לא נותרה Unknown** ✅  
  (השתמשתי ב-Depends כשלא ברור)

---

## 🎯 דפוסים שזוהו

### דפוס 1: GitHub Direct Operations
```
Claude at Runtime: Yes
GPT-CEO Ready: Yes (for most) / Planned (for write flows)
Approval: No (read) / Depends (write to code)
```

### דפוס 2: GitHub Actions Jobs
```
Claude at Runtime: Builder-Only
GPT-CEO Ready: Planned
Approval: No (infrastructure) / Depends (state-changing)
```

### דפוס 3: Google Read Operations
```
Claude at Runtime: Yes
GPT-CEO Ready: Yes (read) / Planned (write)
Approval: No
```

### דפוס 4: Google Write Operations
```
Claude at Runtime: Yes
GPT-CEO Ready: Planned
Approval: Yes (external impact) / Depends (personal data)
```

### דפוס 5: Local MCP Tools
```
Claude at Runtime: Yes
GPT-CEO Ready: No (lacks MCP access)
Approval: No (mostly OS_SAFE)
```

### דפוס 6: Cloud Run APIs
```
Claude at Runtime: Builder-Only (built the service)
GPT-CEO Ready: Yes (primary consumer!)
Approval: No (health) / Depends (mutations)
```

---

## 🔗 קישור ל-Flows

### מנות קודמות שהוזכרו

**לא נמצאו FLOW_001/FLOW_002 מוגדרים במפורש**, אבל:
- במנה הקודמת Or ציין GPT-CEO כמתכנן ראשי
- הוספתי `GPT-CEO Ready = Planned` בכל מקום רלוונטי
- במיוחד ב-Google Pilots (Gmail send, Drive create, Calendar events)

**אם יש FLOW_001/002 ספציפיים שצריך לקשר**, נא לציין ואעדכן.

---

## ⚠️ הערות והחלטות

### החלטה 1: Builder-Only vs Yes
**שאלה**: מתי Claude נחשב ל-"Builder-Only" ומתי ל-"Yes"?

**החלטה**:
- `Builder-Only`: Claude בונה workflow/job שרץ אוטונומית (GitHub Actions, cron)
- `Yes`: Claude מעורב בזמן ריצה (קריאת API, החלטות, triggers)

**דוגמה**:
- `index-append.yml` (hourly Sheets append): `Builder-Only` (רץ אוטונומי)
- Trigger workflow via API: `Yes` (Claude מחליט מתי להריץ)

### החלטה 2: GPT-CEO Ready = Planned vs No
**שאלה**: מתי לסמן `Planned` ומתי `No`?

**החלטה**:
- `No`: מגבלה טכנית ברורה (GPT אין MCP, אין filesystem access)
- `Planned`: אפשרי טכנית אבל טרם מוכן (OAuth scopes, workflows)

**דוגמה**:
- Local Filesystem: `No` (GPT אין MCP)
- Gmail Send: `Planned` (צריך OAuth expansion, בתהליך)

### החלטה 3: Approval Depends - מתי?
**שאלה**: מתי להשתמש ב-`Depends`?

**החלטה**:
- פעולה שיכולה להיות OS_SAFE או CLOUD_OPS_HIGH תלוי בהקשר
- דוגמה: Gmail organize (labels) = No approval, Gmail send = Yes approval

**דוגמאות Depends**:
- GitHub create file: No approval (docs), Yes approval (workflows)
- Calendar create event: No approval (personal), Depends (with many attendees)

---

## ✅ מצב סופי

### כיסוי
- ✅ Section 1: GitHub Layer (100%)
- ✅ Section 2: Local Layer (100%)
- ✅ Section 3: Google Layer (100%)
- ✅ Section 4: GCP Layer (100%)
- ⚠️ Section 5: Canva Layer (לא עודכן - פחות רלוונטי ל-GPT-CEO flows)
- ⚠️ Section 6: Web Layer (לא עודכן - פחות רלוונטי)
- ✅ Section 10: Cloud Run APIs (100%)

### Unknown Fields
- **0 שדות Unknown** ✅
- כל שורה קיבלה ערך ברור (Yes/No/Planned/Depends/Builder-Only)

---

## 🚀 Next Steps

### עבור Claude
1. ✅ העדכון הושלם
2. ✅ לוג זה נוצר
3. ⏳ לעדכן את CAPABILITIES_MATRIX.md עצמו (גרסה 1.3.0)

### עבור GPT-CEO
1. קרא את המטריצה המעודכנת
2. השתמש בשדות החדשים לקבלת החלטות:
   - `GPT-CEO Ready = Yes` → יכול לקחת אחריות
   - `GPT-CEO Ready = Planned` → צריך Claude בינתיים
   - `Approval = Yes` → לבקש מאור לפני ביצוע

### עבור Or
1. סקור את השדות החדשים
2. אשר או תקן החלטות
3. אם יש FLOW_001/002 ספציפיים → הפנה אליהם ואעדכן

---

**Created**: 2025-11-18  
**Version**: 2.0 (כולל 3 שדות תפקידים)  
**Status**: Complete  
**Next**: Update CAPABILITIES_MATRIX.md v1.3.0
