# MCP – GPT Side Bridge to CAPABILITIES_MATRIX

## הקשר

בפרויקט זה, Claude Desktop עובד עם MCP וכלי ענן עבור אור.  
הקובץ `CAPABILITIES_MATRIX.md` בריפו `edri2or-commits/make-ops-clean` הוא:

- מקור האמת (SSOT) למצב היכולות והחיבורים של Claude/MCP.
- מתוחזק על ידי Claude כחלק מהלולאות שלו.
- משקף את מצב החיבורים:
  - GitHub
  - Local (Filesystem / PowerShell / Scripts)
  - Google MCP (Gmail / Drive / Calendar / Sheets)
  - GCP דרך GitHub Actions (WIF / Secret Manager / APIs)
  - ועוד כלים (Canva, Web וכו’).

...

כאשר GPT מתכנן שכבות אוטונומיה/חיבורים/אוטומציות:

1. להניח ש:
   - CAPABILITIES_MATRIX הוא המאסטר למידע על יכולות Claude.
   - כל שינוי יכולת אמור להיסגר בלולאה שבה Claude מעדכן את הקובץ.

2. לעזור לאור:
   - לבחור "מנות" (חיבורים קטנים) לחיזוק יכולות,
   - לנסח לקלוד הוראות מדויקות שמבוססות על המטריצה,
   - להקפיד שכל משימה לקלוד כוללת:
     - תכנון → ביצוע → עדכון בקובץ `CAPABILITIES_MATRIX.md`.

3. לזכור:
   - המטרה הסופית היא 100% יכולת בכל כלי (Gmail, Drive, GitHub, GCP, Local וכו’),
   - תחת Approval Gate יחיד – אור.
