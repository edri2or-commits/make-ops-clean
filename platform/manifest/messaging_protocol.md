# Messaging Protocol v1

Envelope (JSON):
```json
{
  "type": "INTENT|PLAN|DRY_RUN|APPROVAL_REQUEST|EXECUTION_RESULT|STATUS_UPDATE",
  "intent": "gh.pr.create",
  "params": {...},
  "requested_by": "human|chatgpt|claude",
  "correlation_id": "ULID-xxxx",
  "requires_approval": true
}
```

- ChatGPT: INTENT→PLAN/DRY_RUN
- Arbiter: מחליט מי מבצע; מונע לופים
- Claude: EXECUTION_RESULT + STATUS_UPDATE
