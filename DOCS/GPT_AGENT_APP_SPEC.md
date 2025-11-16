# GPT-Agent App – High-Level Spec (v0.1)

## 1. Goal

אפליקציית GPT-Agent (OpenAI GPT / Service חיצוני) שמנהלת עבודה אוטונומית על הריפו:

- owner/repo: edri2or-commits/make-ops-clean
- branch: main

המטרה:
- לקרוא תמיד את מצב הריפו (STATE_FOR_GPT_SNAPSHOT, CAPABILITIES_MATRIX, MCP_GPT_CAPABILITIES_BRIDGE),
- לקבל כוונות מ-Or (Intent),
- לתכנן צעדים (Plan),
- לבקש Approval,
- ולבצע פעולות מותרות (Execute) בצורה מבוקרת.

## 2. Sources of Truth (חייב לקרוא לפני כל תכנון)

1. `DOCS/STATE_FOR_GPT_SNAPSHOT.md`
   - צילום מצב קנוני של הריפו: מה יש, מה עובד, מה שבור, ומה ב-Backlog.

2. `CAPABILITIES_MATRIX.md`
   - מפת היכולות לפי שכבות:
     - GitHub
     - Google / GCP
     - Windows MCP
     - ועוד.
   - כולל OS_SAFE vs CLOUD_OPS_HIGH, ראיות, סטטוס (Planned / Implemented / Verified / Broken).

3. `MCP_GPT_CAPABILITIES_BRIDGE.md`
   - "ספר חוקים" לסוכני GPT:
     - איך לקרוא את המטריצה,
     - איך לתכנן שכבות/לולאות,
     - איך לסמן Backlog לקלוד או לשירותים אחרים.

4. `DOCS/AGENT_GPT_MASTER_DESIGN.md`
   - Design של סוכן GitHub (שכבת GitHub בלבד):
     - Or = Intent + Approval
     - GPT-Agent = Planner/Executor בתוך גבולות ה-Policy
     - Agents אחרים (Claude / MCP) = Builders / Tools.

## 3. Runtime Modes

האפליקציה תתמוך בשלושה מצבים:

1. **PLAN_ONLY (OS_SAFE)**
   - קוראת את 4 הקבצים לעיל.
   - מקבלת Intent מאור (טקסט חופשי).
   - מחזירה Plan טקסטואלי (DRY RUN), בדומה ל-`gpt_agent/github_agent.py` היום.
   - לא נוגעת בקבצים ולא מריצה ג'ובים.

2. **DOCS_UPDATE (OS_SAFE – Docs בלבד)**
   - אחרי ש-Or כותב "מאשר":
     - מותר לה:
       - לעדכן Doc/MD (למשל STATE_FOR_GPT_SNAPSHOT / Docs נוספים),
       - לעדכן CAPABILITIES_MATRIX באזורים שסומנו OS_SAFE.
   - כל שינוי:
       - עובר דרך Commit מוסבר (או PR),
       - מתועד ב-Snapshot ובמטריצה.

3. **OPS_HIGH (CLOUD_OPS_HIGH – בעתיד, Resricted)**
   - מצב עתידי בלבד.
   - מיועד לשינויים מסוכנים:
     - קוד,
     - Workflows,
     - חיבור לגוגל/GCP/Secrets.
   - חייב תמיד:
     - PR,
     - Review,
     - אישור מפורש של Or (בהודעה ספציפית).

## 4. Interface – איך משתמשים באפליקציה

### Input (מה Or נותן)

- טקסט Intent, למשל:
  - "תמפה את יכולות GitHub ותעדכן את STATE_FOR_GPT_SNAPSHOT בהתאם."
  - "תוסיף למטריצה שורה על חיבור Google MCP, בלי לגעת בקוד."

- לכל Intent:
  - הסוכן מסווג:
    - OS_SAFE → PLAN_ONLY / DOCS_UPDATE
    - CLOUD_OPS_HIGH → רק PLAN + הצעת PR, בלי ביצוע עד לשלב מתקדם יותר.

### Output

- PLAN טקסטואלי:
  - אילו קבצים לקרוא,
  - מה בדיוק לשנות,
  - איך זה מתועד במטריצה/סנאפשוט.

- ואם יש Approval:
  - רשימת Commits / PRs שנוצרו,
  - לינקים,
  - מה עוד נשאר כ-Backlog.

## 5. GitHub Integration (ברמת Spec)

- שימוש באחד מאלה (לא נקבע עכשיו, רק מתועד כאפשרויות):
  - GitHub App + Token (מועדף),
  - או GitHub Actions + GITHUB_TOKEN,
  - או Service חיצוני (Cloud Run) שמתחבר ל-GitHub API.

- דרישות:
  - לא לשמור Secrets בקוד.
  - להשתמש ב-Env / Secrets של GitHub / Cloud בלבד.
  - כל חיבור חדש → חייב לקבל שורה ב-CAPABILITIES_MATRIX עם:
    - סטטוס,
    - ראיות,
    - רמת סיכון.

## 6. Future Extension

- חיבור לשכבות נוספות (Google / GCP / Windows MCP) יתועדו כאן בהמשך כ-"Modules":
  - GitHub Module (קיים עכשיו).
  - Google/Gmail/Drive Module.
  - GCP Ops Module.
  - Windows MCP Module.

- כל מודול:
  - יקבל תת-Design,
  - יתועד ב-Snapshot ובמטריצה,
  - יישלט דרך אותו GPT-Agent App ודרך Approval אחד – Or.

