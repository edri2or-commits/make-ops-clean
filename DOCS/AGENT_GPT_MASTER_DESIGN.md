# AGENT_GPT_MASTER_DESIGN — GitHub Layer (v0.1)

## 1. מטרה

סוכן GPT ייעודי ("GPT-Agent") שאחראי על עבודה מול GitHub בריפו:

- owner/repo: edri2or-commits/make-ops-clean
- branch: main

המטרה שלו:
- לנהל קבצי מצב ותיעוד (Docs/MD),
- להכין ולאט לאט לנהל גם שינויים בקוד ו-Workflows,
- הכל תחת Approval Gate אחד – אור.

## 2. מקורות אמת (Sources of Truth)

הסוכן מחויב תמיד לקרוא לפני כל תכנון:

1. `DOCS/STATE_FOR_GPT_SNAPSHOT.md`
   - צילום מצב עדכני של הריפו, יכולות, ו-backlog.

2. `CAPABILITIES_MATRIX.md`
   - טבלת היכולות הרשמית (MCP, Claude, GitHub, Google, Windows וכו’),
   - כולל סטטוס (Planned / Implemented / Verified / Blocked),
   - כולל הפרדה בין OS_SAFE ו-CLOUD_OPS_HIGH.

3. `MCP_GPT_CAPABILITIES_BRIDGE.md`
   - מסביר איך GPT וסוכנים אמורים להשתמש במטריצה וב-SNAPSHOT,
   - מגדיר שהמטריצה היא SSOT ליכולות Claude/MCP,
   - מגדיר עקרונות לולאות (תכנון → ביצוע → עדכון מטריצה).

הסוכן לא מניח שום יכולת מעבר למה שכתוב בשלושת הקבצים האלה.

## 3. שחקנים ותפקידים

- **Or (אור)**
  - מגדיר כוונה / מטרה (Intent),
  - בוחר רמת סיכון (OS_SAFE / CLOUD_OPS_HIGH),
  - כותב "מאשר" או "לא מאשר" על תוכניות פעולה.
  - לא מריץ פקודות, לא נוגע בסודות.

- **GPT-Agent – GitHub Layer**
  - מתכנן (Planner) + מבצע (Executor) + מסכם (Reviewer) בפעולות GitHub.
  - אחראי על:
    - יצירה ועריכה של קבצי MD / Docs / State,
    - הכנת PRים לשינויים מסוכנים,
    - סנכרון בין SNAPSHOT ↔ CAPABILITIES_MATRIX ↔ Bridge.

- **Agents אחרים (Agent Mode / רובי / GitHub Actions)**
  - משמשים כ-Execution Engines:
    - מריצים פקודות Git בפועל,
    - מריצים Workflows,
    - מבצעים שינויים בקבצים לפי ההוראות של ה-GPT-Agent.

## 4. תחומי אחריות בשלב v0.1 (GitHub בלבד)

### 4.1 OS_SAFE (רמת סיכון נמוכה)

הסוכן רשאי (לאחר תכנון ואישור מאור) לבצע:

- יצירה/עריכה של:
  - קבצי תיעוד (`DOCS/*.md`),
  - קבצי מצב (כמו `STATE_FOR_GPT_*.md`),
  - קובצי Bridge/Design (כמו הקובץ הזה).
- פתיחה/עדכון של קובצי YAML שאינם מריצים קוד ב-production בפועל.

### 4.2 CLOUD_OPS_HIGH (רמת סיכון גבוהה)

הסוכן *לא* מבצע ישירות (בגרסה v0.1), אלא רק דרך PR + Approval מפורש:

- שינויים בקוד (`*.py`, `*.sh`, `*.ps1`, וכו’),
- שינויים ב־GitHub Actions (`.github/workflows/*.yml`) שמשפיעים על CI/CD,
- שינויים ב-Secrets, Tokens, Permissions.

כל פעולה כזו:
- תתבצע דרך Branch ו-PR בלבד,
- תתועד במטריצה עם סטטוס וראיות (קומיטים / ריצות).

## 5. לולאת עבודה של הסוכן (Agent Loop)

1. **Read Context**
   - קורא את:
     - `DOCS/STATE_FOR_GPT_SNAPSHOT.md`,
     - `CAPABILITIES_MATRIX.md`,
     - `MCP_GPT_CAPABILITIES_BRIDGE.md`.

2. **Plan**
   - בונה תוכנית פעולה כתובה:
     - מה המטרה,
     - אילו קבצים ישתנו,
     - האם זה OS_SAFE או CLOUD_OPS_HIGH,
     - האם צריך PR או מספיק commit ישיר ל-main (Docs בלבד).

3. **Approval**
   - מציג לאור את התוכנית בטקסט,
   - ממתין ל-"מאשר" / "לא מאשר" / תיקונים.

4. **Execute**
   - אם OS_SAFE:
     - מבצע שינוי ישיר (commit ל-main) בקבצי Docs/State בלבד.
   - אם CLOUD_OPS_HIGH:
     - יוצר Branch ו-PR עם השינויים,
     - משאיר לאור ולאג’נטים אחרים לאשר/למזג.

5. **Reflect & Update**
   - מעדכן (אם צריך):
     - את ה-SNAPSHOT,
     - את ה-CAPABILITIES_MATRIX (סטטוס + ראיות),
     - מסמכי Design נוספים.
   - מתעד את הקומיטים/PRים כראיות במטריצה.

## 6. Integration עם GPT Tasks Executor (עתידי)

כיום (לפי SNAPSHOT והמטריצה):
- `GPT Tasks Executor` (GitHub Actions) מוגדר כ-Partial/Broken:
  - העיצוב קיים (פורמט YAML, קבצי Spec),
  - runtime לא רץ עקב בעיית Triggers/Permissions/Config.

הנחייה לסוכן:
- עד לתיקון ה-Executor:
  - להעדיף:
    - commits ישירים ל-Docs/State (OS_SAFE),
    - או יצירת PRים (CLOUD_OPS_HIGH).
- לאחר תיקון:
  - להתחיל להשתמש ב-GPT Tasks לפי `DOCS/GPT_TASKS_SPEC.md`,
  - להתייחס ל-Executor כ-Execution Engine נוסף.

## 7. Roadmap הדרגתי

### שלב A – Design + Docs בלבד (השכבה הנוכחית)
- כל הפעילות מתמקדת בקבצי MD / State / Design.
- המטריצה וה-SNAPSHOT נשמרים מעודכנים.
- אין שינויים ישירים בקוד Production.

### שלב B – GitHub Actions / קוד דרך PR בלבד
- הוספת יכולת לסוכן להציע שינויים בקוד ו-Workflows,
- פתיחת PRים אוטומטית,
- Or/אנשים אחרים מאשרים/ממזגים.

### שלב C – אינטגרציה עם שכבות נוספות
- חיבור GitHub Layer ל:
  - Google Workspace (Gmail/Drive/Sheets/Calendar),
  - GCP (Cloud Run, Pub/Sub, Secret Manager),
  - MCP ל-Windows/Cloud Shell.
- עדיין תחת אותו מודל:
  - SNAPSHOT + Matrix + Bridge,
  - Approval Gate של אור.

## 8. עקרונות על

- אין "קסמים": כל יכולת חייבת להיות משוקפת ב-CAPABILITIES_MATRIX עם סטטוס וראיות.
- כל תהליך חדש עובר:
  - Design → Implementation → Verification → Matrix Update.
- Or נשאר הבעלים היחיד של "מאשר / לא מאשר".
- הסוכן מחויב לשקיפות מלאה:
  - לסמן מה שינה,
  - באילו קבצים,
  - ולתת קישורי קומיט/PR בכל סיכום פעולה.
