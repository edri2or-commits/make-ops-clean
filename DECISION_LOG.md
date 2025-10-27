# Decision Log — index (Latest first, RFC3339Z)

## 2025-10-27T00:00:00Z — Locks TTL policy
proof: .chatops/locks.config.v1.json @ main (commit=b8bb495, verified)
idempotency_key_template="tg:${update_id}:${chat_id}"
lock_ttl_minutes=90
store_ttl_hours=48
status=approved

## 2025-10-24T00:00:00Z — init-b bridge
proof: run=18785058322 ; artifact=4364863684 ; commit=8e3247f
result: DoD met (run+artifact+json_head)
gate: integrations-proof-only-until-tokens
status=approved

## 2025-10-24T00:00:00Z — integrations gate
proof: artifact=token_check_report/report.json
status=OPEN (fix required)
observed: make_http_code=401 ; telegram_ok=true
action: update Make token/scopes/region and re-run token-sanity-check ; run=[TBD]