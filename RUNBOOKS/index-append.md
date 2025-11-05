# RUNBOOK — index-append
## Objective
Append index data (Sheets) via GitHub Actions.
## Normal operation
1. Trigger via manual dispatch or schedule.
2. Inspect step logs in Actions summary.
## Failure handling
- Log to summary, comment on this issue, and open `index-append:manual_step` with context.
## Rollback
- Re-run last green commit or disable schedule.
## Metrics
- Success rate (last 20 runs) and avg runtime.
