# Observability & Fallback
- One pattern for all flows:
  - Log per flow in ./logs/<flow>.log (or central logger).
  - Alert to Telegram #ops-alerts via bot on failure.
  - Autocreate `manual_step` issue on fallback.

## Artifacts
- Use actions/upload-artifact@v4 to publish outputs and link from run summary.
  Artifacts are downloadable per run for auditing.
