# Job Requests Directory

This directory contains Cloud Shell execution requests in JSON format.

## Request Format

```json
{
  "type": "cloud-shell",
  "timestamp": "2025-11-14T12:00:00Z",
  "request_id": "cloud-shell-req-20251114_120000",
  "command": "echo 'Hello Cloud Shell' && whoami && pwd",
  "project_id": "edri2or-mcp",
  "requester": "claude",
  "priority": "normal"
}
```

## Workflow

1. Claude writes request file: `cloud-shell-req-<timestamp>.json`
2. GitHub Actions detects new file (push trigger)
3. Job dispatcher validates and executes
4. Result written to `jobs/results/`

## Status

Files in this directory trigger automated execution.
