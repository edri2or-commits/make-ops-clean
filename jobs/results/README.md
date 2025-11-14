# Job Results Directory

This directory contains execution results for Cloud Shell jobs.

## Result Format

```json
{
  "request_id": "cloud-shell-req-20251114_120000",
  "status": "success",
  "timestamp_start": "2025-11-14T12:00:10Z",
  "timestamp_end": "2025-11-14T12:00:35Z",
  "execution_time_seconds": 25,
  "github_run_id": "12345678",
  "github_run_url": "https://github.com/edri2or-commits/make-ops-clean/actions/runs/12345678",
  "exit_code": 0,
  "output_preview": "Hello Cloud Shell\nedri2\n/home/edri2",
  "artifact_name": "cloud-shell-execution-20251114_120000",
  "errors": []
}
```

## Workflow

1. Job dispatcher executes Cloud Shell command
2. Result automatically written here
3. Claude polls for result file
4. Claude processes output

## Status

Results persist for audit trail and retrieval.
