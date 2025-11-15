STATE FOR GPT (Snapshot)

1. Repo Overview
owner/repo: edri2or-commits/make-ops-clean
default_branch: main
visibility: public

2. Key Files
CAPABILITIES_MATRIX.md : קיים, מסלול מלא: /CAPABILITIES_MATRIX.md
MCP_GPT_CAPABILITIES_BRIDGE.md : קיים, מסלול מלא: /MCP_GPT_CAPABILITIES_BRIDGE.md, נדרש ליצור
GPT_REPO_ACCESS_BRIDGE.md : קיים, מסלול מלא: /GPT_REPO_ACCESS_BRIDGE.md
.github/workflows/ :
  - codeql.yml
  - python-app.yml
  - release.yml

3. Current Capabilities Status
GitHub Actions: ✅ פעיל – טסטים, release, כתיבת תוצאות לקבצים; ❌ אין גישה ל-API
GCP/Gmail/Drive/Sheets: 🟡 חלקי – גישה פעילה דרך WIF; Drive/Secrets לא מאומתים end-to-end
Windows/Local MCP: ❌ אין תיעוד/תמיכה ברורה, כנראה לא פעיל

4. Open TODOs / Backlog
- יישור מלא בין CAPABILITIES_MATRIX לבין STATE_FOR_GPT (כולל סטטוס לכל חיבור)
- מיפוי workflows מול מטריצה
- סנכרון matrix.json אם מתוכנן שימוש
- בדיקת permissions של Secrets
- בדיקת תמיכה מלאה מול GCP (WIF)
