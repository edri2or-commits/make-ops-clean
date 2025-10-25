make-ops-clean — Chat-Ops Proof

PFIX-001 — ✅ עבר (2025-10-19). מטרה: להוכיח ש-Chat-Ops מגיב לאירוע repository_dispatch מסוג chat.run ומייצר ריצה. תוצאה: PASS — GitHub החזיר 204 ונוצרה ריצה.

נתונים:
- Event: repository_dispatch
- action: chat.run
- client_payload.text: /ping
- HTTP: 204
- Run URL: https://github.com/edri2or-commits/make-ops-clean/actions/runs/18630257494

DoD (met):
- בקשת API ל-/dispatches החזירה 204
- נוצרה ריצה עם קישור תקף (Run URL)
- ב-event.json נוכח client_payload.text="/ping"

Evidence (event.json excerpt):
"action": "chat.run",
"client_payload": { "text": "/ping" }

Repro (לשליחה ידנית):
POST https://api.github.com/repos/<owner>/<repo>/dispatches
Authorization: token <PAT or App installation token>
Accept: application/vnd.github+json
{
  "event_type": "chat.run",
  "client_payload": { "text": "/ping" }
}

Timeline:
2025-10-19 | PFIX-001: repository_dispatch (chat.run) "/ping" → 204 → run | https://github.com/edri2or-commits/make-ops-clean/actions/runs/18630257494

Decision: PFIX-001 מאמת את ערוץ ה-Chat-Ops; ניתן להשתמש בו לטריגרים נוספים (/gh.run, /gh.dispatch).
Guardrail: כתיבה ב-GitHub רק עם App Installation Token; GITHUB_TOKEN נשאר לקריאה.

Decision Log (index line):
PFIX-001 | repository_dispatch(chat.run) "/ping" | http:204 | run:18630257494 | status:PASS
