# make-ops-clean — Chat-Ops Proof Pack

## מה זה
מסלול Chat-Ops נקי: Telegram → Make (EU2) → GitHub Actions. המטרה: פקודה אחת בצ’אט → פעולה אחת עם ראיות בכל חוליה.

## ארכיטקטורה קצרה
- **Telegram Bot** → מקבל פקודות (`/ping`, `/make.scenarios`).
- **Make (EU2, scenario 7598259)** → מפעיל HTTP POST ל-GitHub.
- **GitHub Actions** (`.github/workflows/layer_c_chat_commands.yml`) → מאזין ל:
  - `repository_dispatch` עם `types: [chat.run]`
  - `workflow_dispatch` (fallback ידני)

---

## שימוש מהיר
- שלח בטלגרם: `/ping` → חוזר Pong + קישור לריצת Actions.
- שלח בטלגרם: `/make.scenarios` → מחזיר רשימת סצנריוז (ודוגמא להפעלה).

---

## Proof Fix (PFIX-001) — **עבר**
**תאריך:** 2025-10-19  
**מצב:** ✅ קצה-לקצה עובד.

**פרטי הוכחה (Update-Proof):**
- **Event:** `repository_dispatch`
- **action:** `chat.run`
- **client_payload.text:** `/ping`
- **Status code (Make → GitHub):** `204`
- **run_url:** **RUN_URL_HERE**

### Evidence (event.json excerpt)
```json
"action": "chat.run",
"client_payload": { "text": "/ping" }