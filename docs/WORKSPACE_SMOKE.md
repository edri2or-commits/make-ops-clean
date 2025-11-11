# Workspace Smoke Test — E2E Coverage

## Overview

Comprehensive smoke test covering all Google Workspace APIs with hybrid authentication support:
- **Drive**: WIF+SA (always available)
- **Gmail**: User OAuth (optional, graceful skip)
- **Calendar**: User OAuth (optional, graceful skip)

## Authentication Strategy

### Primary: WIF+SA (Drive)
- Uses Workload Identity Federation with Service Account
- No user interaction required
- Suitable for read/write operations on SA-owned resources

### Secondary: User OAuth (Gmail/Calendar)
- Uses OAuth 2.0 refresh token flow
- Only activated if secrets present:
  - `GOOGLE_OAUTH_CLIENT_ID`
  - `GOOGLE_OAUTH_CLIENT_SECRET`
  - `GOOGLE_OAUTH_REFRESH_TOKEN`
- Gracefully skips if secrets missing (logs "skipped" in ledger)

## Test Operations

### Drive: Create Empty Text File
```bash
POST https://www.googleapis.com/drive/v3/files
Body: {"name": "smoke-test-<timestamp>.txt", "mimeType": "text/plain"}
Result: File ID logged to ledger
```

### Gmail: Send Test Email
```bash
POST https://gmail.googleapis.com/gmail/v1/users/me/messages/send
Body: {"raw": "<base64-encoded-rfc2822-message>"}
Recipient: TEST_EMAIL_RECIPIENT or self
Result: Message ID + Thread ID logged to ledger
```

### Calendar: Create 15-Minute Event
```bash
POST https://www.googleapis.com/calendar/v3/calendars/primary/events
Body: {
  "summary": "Workspace Smoke Test",
  "start": {"dateTime": "<now+1h>"},
  "end": {"dateTime": "<now+1h15m>"}
}
Result: Event ID + HTML link logged to ledger
```

## Ledger Entries

### Drive (Always)
```json
{
  "id": "uuid",
  "type": "drive.create",
  "timestamp": "2025-01-15T15:30:00Z",
  "status": "success",
  "actor": "github-actions",
  "input": {
    "name": "smoke-test-1736952600.txt",
    "mimeType": "text/plain"
  },
  "output": {
    "fileId": "1abc...",
    "fileName": "smoke-test-1736952600.txt"
  },
  "commitSha": "abc123..."
}
```

### Gmail (If OAuth Available)
```json
{
  "id": "uuid",
  "type": "gmail.send",
  "timestamp": "2025-01-15T15:30:05Z",
  "status": "success",
  "actor": "github-actions",
  "input": {
    "subject": "Workspace Smoke Test",
    "recipientCount": 1
  },
  "output": {
    "messageId": "18d1234...",
    "threadId": "18d1234..."
  },
  "commitSha": "abc123..."
}
```

### Gmail (If OAuth Missing)
```json
{
  "id": "uuid",
  "type": "gmail.send",
  "timestamp": "2025-01-15T15:30:05Z",
  "status": "skipped",
  "actor": "github-actions",
  "input": {
    "reason": "user_oauth_not_available"
  },
  "output": {},
  "commitSha": "abc123..."
}
```

### Calendar (If OAuth Available)
```json
{
  "id": "uuid",
  "type": "calendar.create",
  "timestamp": "2025-01-15T15:30:10Z",
  "status": "success",
  "actor": "github-actions",
  "input": {
    "summary": "Workspace Smoke Test",
    "duration": "15min"
  },
  "output": {
    "eventId": "abc123_20250115T163000Z",
    "eventLink": "https://www.google.com/calendar/event?eid=..."
  },
  "commitSha": "abc123..."
}
```

### Calendar (If OAuth Missing)
```json
{
  "id": "uuid",
  "type": "calendar.create",
  "timestamp": "2025-01-15T15:30:10Z",
  "status": "skipped",
  "actor": "github-actions",
  "input": {
    "reason": "user_oauth_not_available"
  },
  "output": {},
  "commitSha": "abc123..."
}
```

## Running the Test

### Automatic (PR Trigger)
```bash
# Runs automatically on PR creation/update to main or or-control/ops
```

### Manual Trigger
```bash
# Via GitHub UI
Actions → workspace-smoke → Run workflow

# Via CLI
gh workflow run workspace-smoke.yml --ref feature/pr-9-workspace-smoke

# Skip optional tests
gh workflow run workspace-smoke.yml --ref main \
  -f skip_gmail=true \
  -f skip_calendar=true
```

## Required Secrets

### Always Required
- `WIF_PROVIDER` - Workload Identity Provider resource name
- `WIF_SERVICE_ACCOUNT` - Service Account email

### Optional (Gmail/Calendar)
- `GOOGLE_OAUTH_CLIENT_ID` - OAuth 2.0 client ID
- `GOOGLE_OAUTH_CLIENT_SECRET` - OAuth 2.0 client secret
- `GOOGLE_OAUTH_REFRESH_TOKEN` - User refresh token
- `TEST_EMAIL_RECIPIENT` - Email recipient for test (defaults to self)

## Service Account Permissions

### Drive API
- Scope: `https://www.googleapis.com/auth/drive.file`
- Operations: Create files in SA's Drive

### Gmail API (User OAuth)
- Scope: `https://www.googleapis.com/auth/gmail.send`
- Operations: Send emails as user

### Calendar API (User OAuth)
- Scope: `https://www.googleapis.com/auth/calendar.events`
- Operations: Create events in user's calendar

## Graceful Degradation

The workflow implements graceful degradation:

1. **Check OAuth Secrets**: Verify all 3 required secrets exist
2. **Attempt Token Exchange**: Try to get access token from refresh token
3. **Conditional Execution**:
   - If OAuth available → Run Gmail/Calendar tests
   - If OAuth missing → Log "skipped" entries to ledger
4. **No Failures**: Missing OAuth does not fail the workflow

## Zero-Touch Compliance

- ✅ Or performs no technical actions
- ✅ All operations logged to ledger
- ✅ No PII/secrets in logs
- ✅ Hybrid auth (SA + User OAuth)
- ✅ Atomic ledger writes (3 retries)
- ✅ Graceful degradation (no hard failures)

## Expected Outcomes

### Scenario 1: Full OAuth Available
- ✅ Drive: File created
- ✅ Gmail: Email sent
- ✅ Calendar: Event created
- **Ledger Entries:** 3 (all success)

### Scenario 2: No OAuth (WIF+SA Only)
- ✅ Drive: File created
- ⊘ Gmail: Skipped (logged)
- ⊘ Calendar: Skipped (logged)
- **Ledger Entries:** 3 (1 success + 2 skipped)

### Scenario 3: Partial OAuth (e.g., Gmail only)
- ✅ Drive: File created
- ✅ Gmail: Email sent
- ⊘ Calendar: Skipped (logged)
- **Ledger Entries:** 3 (2 success + 1 skipped)

## Troubleshooting

### Drive Test Fails
- Check WIF_PROVIDER secret format
- Verify service account has drive.file scope
- Confirm WIF binding is active

### Gmail Test Skipped (Unexpected)
- Verify all 3 OAuth secrets are set
- Check refresh token is valid (not expired)
- Confirm gmail.send scope in OAuth consent

### Calendar Test Skipped (Unexpected)
- Verify all 3 OAuth secrets are set
- Check refresh token is valid
- Confirm calendar.events scope in OAuth consent

### Ledger Write Fails
- Check branch protection rules
- Verify GitHub Actions has write permissions
- Review atomic write retry logs

## References

- Drive API: https://developers.google.com/drive/api/v3/reference/files/create
- Gmail API: https://developers.google.com/gmail/api/reference/rest/v1/users.messages/send
- Calendar API: https://developers.google.com/calendar/api/v3/reference/events/insert
- OAuth 2.0: https://developers.google.com/identity/protocols/oauth2
- WIF Setup: https://cloud.google.com/iam/docs/workload-identity-federation