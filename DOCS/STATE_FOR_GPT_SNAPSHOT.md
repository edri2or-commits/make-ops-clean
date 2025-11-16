# STATE FOR GPT (Snapshot) – v2 (GitHub Layer + Agent DRY RUN)

## 1. Repo Overview

- owner/repo: **edri2or-commits/make-ops-clean**
- default_branch: **main**
- visibility: public
- purpose: תשתית MCP + GPT-Agent לאוטונומיה (GitHub + GCP + Google + Windows)

## 2. Key Files (GPT-facing)

- `CAPABILITIES_MATRIX.md`  
  מפת היכולות והרמות (OS_SAFE / CLOUD_OPS_HIGH) לכל שכבה (GitHub, Google, GCP, Windows/MCP וכו’).

- `MCP_GPT_CAPABILITIES_BRIDGE.md`  
  מדריך עבודה לסוכני GPT: איך לקרוא את המטריצה, איך לגזור ממנה החלטות, ואיך לעדכן אותה.

- `GPT_REPO_ACCESS_BRIDGE.md`  
  מידע על החיבור של GPT/Agents לריפו (`make-ops-clean`) – מה מותר לעשות, איך לגשת, ומה הנתיב המועדף.

- `DOCS/STATE_FOR_GPT_SNAPSHOT.md` (הקובץ הזה)  
  צילום מצב קנוני ל-GPT על הריפו, היכולות, וה-Backlog.

- `DOCS/AGENT_GPT_MASTER_DESIGN.md`  
  Design ראשי ל-GPT-Agent בשכבת GitHub:
  - תפקידים: Or / GPT-Agent / Claude / Agents אחרים
  - מקורות אמת: Snapshot, Matrix, Bridge
  - מודל תהליך: Intent → Plan → Approval → Execute → Reflect
  - הבחנה בין OS_SAFE (Docs/State) ל-CLOUD_OPS_HIGH (קוד/קונפיג).

- `DOCS/GPT_TASKS_SPEC.md`  
  פורמט משימות YAML ל-GPT Tasks Executor (עדיין ברמת Design; runtime בעייתי).

- `.github/workflows/gpt_tasks_executor.yml`  
  Workflow שמיועד להריץ משימות YAML מ-`.chatops/gpt_tasks/` – כרגע מעוצב אבל runtime בפועל לא יציב, לא נחשב אמין.

- `DOCS/GPT_EXECUTOR_TEST.md`  
  קובץ smoke-test שנוצר מ-flow קודם (commit `1c64fd5`) כדי לאמת כתיבה ישירה לריפו.

- `gpt_agent/github_agent.py`  
  סוכן GitHub Agent **DRY RUN**:
  - קורא את:
    - `DOCS/AGENT_GPT_MASTER_DESIGN.md`
    - `DOCS/STATE_FOR_GPT_SNAPSHOT.md`
    - `CAPABILITIES_MATRIX.md`
  - מקבל `--intent`
  - מחזיר Plan טקסטואלי בלבד (ללא כתיבה לקבצים).

- `.github/workflows/github_agent_dry_run.yml`  
  Workflow ל-GitHub Actions (כשיעבוד) שמריץ את `gpt_agent/github_agent.py` עם `workflow_dispatch` ו-input בשם `intent`.

## 3. Current Capabilities Status (High Level)

### GitHub – Direct Writes / Docs

- Direct writes (Docs/State) דרך GPT/Agents (כולל Agent Mode + הפעלה ידנית שלך) → ✅ **Verified (OS_SAFE)**
- ראיות:
  - `1c64fd5` – יצירת `DOCS/GPT_EXECUTOR_TEST.md`
  - `81cba22` – יצירת `DOCS/STATE_FOR_GPT_SNAPSHOT.md`
  - `52e5e39` – עדכון `STATE_FOR_GPT.md` להפניה לסנאפשוט
  - `92de8df` – יצירת `MCP_GPT_CAPABILITIES_BRIDGE.md` + עדכון במטריצה
  - `b10769b` – `DOCS/AGENT_GPT_MASTER_DESIGN.md`
  - `047eea8` – `gpt_agent/github_agent.py` + `.github/workflows/github_agent_dry_run.yml`

### GitHub – GPT GitHub Agent DRY RUN

- קיים Agent בסיסי ב-Python:
  - קובץ: `gpt_agent/github_agent.py`
  - מצב: ✅ **Implemented (OS_SAFE, DRY RUN בלבד)**
  - מריץ Plan על בסיס Snapshot + Matrix + Design.
  - נוסה לוקלית בפקודה:

    ```bash
    python gpt_agent/github_agent.py \
      --intent "Map current GitHub capabilities and propose next OS_SAFE documentation updates only."
    ```

- אין כתיבה אוטומטית לקבצים, אין commits, אין שינוי Workflows → רק Plan בטקסט.

### GitHub – GPT Tasks Executor (YAML דרך Actions)

- Design קיים (`DOCS/GPT_TASKS_SPEC.md` + `.github/workflows/gpt_tasks_executor.yml`)
- Runtime: 🟡 **Partial/Broken**
  - הפעלה דרך UI/CLI נותנת "successfully requested" אבל ריצות לא מופיעות בפועל.
  - לא להסתמך כרגע על `.chatops/gpt_tasks/*.yml` כערוץ ביצוע אמין.
- עד להודעה חדשה:
  - **Direct writes (Docs/State) + Git Bash + Agents** = נתיב עיקרי.
  - GPT Tasks Executor נשאר Backlog לתיקון ודיבאג.

### Google / GCP / Windows MCP (תמציתי בלבד)

- קיים תיעוד ו-Design ב-`CAPABILITIES_MATRIX.md` ו-`MCP_GPT_CAPABILITIES_BRIDGE.md`.
- מצב בפועל:
  - חיבורים קיימים/קיימו ברמת Claude + MCP + GCP (WIF, Secret Manager, APIs) – אבל ה-runtime לא מנוהל דרך הריפו הזה.
- עבור GPT-Agent:
  - הריפו משמש כ-Design + Docs + חלק GitHub בלבד.
  - חיבור מלא ל-Google/GCP/Windows MCP יגיע בשכבות הבאות.

## 4. Open TODOs / Backlog (GitHub-oriented)

- לתקן/להחליף את GPT Tasks Executor (YAML via Actions) כך שיהיה:
  - either: מתוקן ועובד,  
  - or: מוחלף במנגנון אחר (שירות חיצוני / Agent Service).
- לחבר את `gpt_agent/github_agent.py` ל-GPT אמיתי (LLM) במקום Planner סטטי.
- להרחיב את ה-Agent:
  - ליצירת PRים במקום commits ישירים לשינויים מסוכנים (CLOUD_OPS_HIGH).
  - ליכולת עדכון חכם של Docs/Matrix בהתאם לפעולות שבוצעו.
- לסנכרן תמיד:
  - `STATE_FOR_GPT_SNAPSHOT.md`
  - `CAPABILITIES_MATRIX.md`
  - `MCP_GPT_CAPABILITIES_BRIDGE.md`
  עם כל שינוי משמעותי.

## 5. GPT GitHub Agent – DRY RUN (Current Contract)

- תפקיד:
  - לקרוא Design + Snapshot + Matrix.
  - לבנות Plan טקסטואלי ברוח החוקה (AGENT_GPT_MASTER_DESIGN).
- מגבלות:
  - לא כותב קבצים.
  - לא יוצר commits.
  - לא מפעיל Workflows נוספים.
- שימוש:
  - לניתוח מצבים ו-What-If לפני שנכנסים לשינוי אמיתי.
  - להפקת תוכניות פעולה ש-Or יכול לאשר, ולאחר מכן Agent אחר יבצע (או אותו Agent בגרסה מתקדמת).

