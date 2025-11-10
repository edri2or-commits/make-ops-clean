# Telegram Approval Gate — Production Wiring

## Overview

This document describes the **production flow** for Telegram-based approval of GitHub PRs using the Single Telegram Gate pattern.

**Flow**: Telegram Button Click → Make Webhook → GitHub `repository_dispatch` → Auto-Merge

---

## Architecture

```
┌─────────────┐
│  Telegram   │  User clicks ✅ button
│   Button    │  callback_data: {"action":"approve","pr":85,"approval_id":"tg:123456"}
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Make     │  Custom Webhook (protected with secret_token)
│  Scenario   │  Parse callback_query → Extract pr_number
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   GitHub    │  POST /repos/{owner}/{repo}/dispatches
│ repository_ │  event_type: merge_approved
│  dispatch   │  client_payload: {pr_number, approval_id}
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   GitHub    │  Workflow: execute-on-approval.yml
│   Actions   │  Auto-merge PR using GITHUB_TOKEN
└─────────────┘
```

---

## Telegram Button Configuration

### Callback Data Schema

When sending approval requests via Telegram, use inline keyboard buttons with `callback_data`:

```json
{
  "action": "approve",
  "pr": 85,
  "approval_id": "tg:${MESSAGE_ID}"
}
```

**Fields**:
- `action`: Always `"approve"` for approval actions
- `pr`: GitHub PR number to merge
- `approval_id`: Unique identifier for audit trail (format: `tg:${MESSAGE_ID}`)

### Example Telegram API Call

```bash
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "${TELEGRAM_CHAT_ID}",
    "text": "🔔 PR #85 ready for approval",
    "reply_markup": {
      "inline_keyboard": [[
        {
          "text": "✅ Approve & Merge",
          "callback_data": "{\"action\":\"approve\",\"pr\":85,\"approval_id\":\"tg:123456\"}"
        },
        {
          "text": "❌ Reject",
          "callback_data": "{\"action\":\"reject\",\"pr\":85}"
        }
      ]]
    }
  }'
```

---

## Make.com Integration

### Scenario Structure

1. **Trigger: Custom Webhook**
   - **URL**: Provided by Make.com after creation
   - **Method**: POST
   - **Security**: Validate `X-Telegram-Bot-Api-Secret-Token` header

2. **Module 1: Parse Callback Query**
   - **Input**: `$.callback_query.data` (JSON string)
   - **Parse**: Extract `pr`, `action`, `approval_id`
   - **Filter**: Only proceed if `action == "approve"`

3. **Module 2: HTTP Request to GitHub**
   - **URL**: `https://api.github.com/repos/edri2or-commits/make-ops-clean/dispatches`
   - **Method**: POST
   - **Headers**:
     - `Authorization: Bearer ${GITHUB_TOKEN}`
     - `Accept: application/vnd.github.v3+json`
     - `Content-Type: application/json`
   - **Body**:
     ```json
     {
       "event_type": "merge_approved",
       "client_payload": {
         "pr_number": {{pr}},
         "approval_id": "{{approval_id}}",
         "approved_by": "{{callback_query.from.username}}",
         "approved_at": "{{callback_query.message.date}}"
       }
     }
     ```

4. **Module 3: Acknowledge to Telegram**
   - **URL**: `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/answerCallbackQuery`
   - **Body**:
     ```json
     {
       "callback_query_id": "{{callback_query.id}}",
       "text": "✅ Approval sent to GitHub Actions"
     }
     ```

### Security: Webhook Secret Token

Telegram supports webhook protection using `secret_token`:

```bash
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "${MAKE_WEBHOOK_URL}",
    "secret_token": "${WEBHOOK_SECRET}"
  }'
```

**Validation in Make**:
- Check that incoming request header `X-Telegram-Bot-Api-Secret-Token` matches your stored `WEBHOOK_SECRET`
- Reject requests without valid token

---

## GitHub Integration

### repository_dispatch Event

**Endpoint**: `POST /repos/{owner}/{repo}/dispatches`

**Required Headers**:
- `Authorization: Bearer ${GITHUB_TOKEN}`
- `Accept: application/vnd.github.v3+json`

**Body Schema**:
```json
{
  "event_type": "merge_approved",
  "client_payload": {
    "pr_number": 85,
    "approval_id": "tg:123456",
    "approved_by": "or",
    "approved_at": "2025-11-10T12:00:00Z"
  }
}
```

**Fields**:
- `event_type`: Must be `"merge_approved"` to trigger the workflow
- `client_payload.pr_number`: **(Required)** PR number to merge
- `client_payload.approval_id`: **(Optional)** Audit trail identifier
- `client_payload.approved_by`: **(Optional)** Username who approved
- `client_payload.approved_at`: **(Optional)** ISO 8601 timestamp

### Workflow Trigger

The `execute-on-approval.yml` workflow listens for `repository_dispatch` events:

```yaml
on:
  repository_dispatch:
    types: [merge_approved]
```

The workflow extracts `pr_number` from `client_payload`:

```yaml
PR_NUMBER="${{ github.event.client_payload.pr_number }}"
```

---

## Permissions & Security

### GitHub Token Permissions

The workflow uses `GITHUB_TOKEN` with the following permissions:

```yaml
permissions:
  contents: write        # Required for merging PRs
  pull-requests: write   # Required for PR operations
```

**No PAT required** — `GITHUB_TOKEN` is automatically provided by GitHub Actions.

### Kill Switch

The workflow includes a kill-switch mechanism using the `EXEC_ENABLED` repository variable:

```bash
# To disable all executions:
gh variable set EXEC_ENABLED --body "false"

# To re-enable:
gh variable set EXEC_ENABLED --body "true"
```

**Default**: If `EXEC_ENABLED` is not set, execution is **enabled** (default: `true`).

### Secrets Required

The following secrets must be configured in GitHub repository settings:

1. `TELEGRAM_BOT_TOKEN` — Telegram bot API token
2. `TELEGRAM_CHAT_ID` — Telegram chat ID for notifications
3. `MAKE_WEBHOOK_URL` — Make.com webhook URL (for bootstrap/testing)

---

## Testing

### Manual Test via cURL

Simulate a Telegram callback by sending a `repository_dispatch` directly:

```bash
curl -X POST \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  https://api.github.com/repos/edri2or-commits/make-ops-clean/dispatches \
  -d '{
    "event_type": "merge_approved",
    "client_payload": {
      "pr_number": 85,
      "approval_id": "test:manual",
      "approved_by": "test-user",
      "approved_at": "2025-11-10T12:00:00Z"
    }
  }'
```

### Expected Behavior

1. Workflow `execute-on-approval.yml` is triggered
2. PR #85 is validated (exists, open state)
3. Pre-merge validation runs (if script exists)
4. PR is merged using `gh pr merge --squash --delete-branch`
5. Telegram notification sent with merge status

---

## Official Documentation

- **GitHub repository_dispatch**: https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event
- **GitHub workflow_dispatch**: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_dispatch
- **GitHub GITHUB_TOKEN permissions**: https://docs.github.com/en/actions/security-guides/automatic-token-authentication
- **Telegram setWebhook with secret_token**: https://core.telegram.org/bots/api#setwebhook
- **Telegram CallbackQuery**: https://core.telegram.org/bots/api#callbackquery
- **Make.com Webhooks**: https://www.make.com/en/help/tools/webhooks

---

## Audit Trail

The `approval_id` field enables end-to-end traceability:

1. Telegram message ID → `approval_id: "tg:${MESSAGE_ID}"`
2. Make.com logs → correlation with webhook request
3. GitHub Actions logs → `APPROVAL_ID` printed in workflow
4. Post-merge notification → confirmation back to Telegram

**Example Log Output**:
```
📌 Using repository_dispatch payload: PR #85
🔍 APPROVAL_ID=tg:123456
✅ Resolved PR Number: 85
```

---

## Troubleshooting

### Workflow Not Triggering

1. Verify `event_type` is exactly `"merge_approved"`
2. Check GitHub token has `repo` scope
3. Ensure webhook is calling correct repository URL

### Merge Failing

1. Check PR state is `OPEN`
2. Verify no merge conflicts exist
3. Review pre-merge validation logs

### Telegram Notification Not Sent

1. Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` secrets
2. Check workflow logs for curl errors
3. Test token manually: `curl https://api.telegram.org/bot${TOKEN}/getMe`

---

## Next Steps

1. ✅ Configure Telegram webhook with `secret_token`
2. ✅ Create Make.com scenario using blueprint
3. ✅ Test with PR #85 (E2E test)
4. ✅ Monitor GitHub Actions logs for first approval
5. ✅ Verify Telegram post-merge notification
