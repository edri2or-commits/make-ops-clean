# Tasks Directory

## Purpose
This directory contains task definitions and metadata for Zero-Touch operations.

## Structure
```
tasks/
├── README.md           # This file
└── <task_id>/         # Future: Individual task definitions
    ├── payload.json   # repository_dispatch payload
    ├── manifest.json  # Files to be changed
    └── rollback.sh    # Rollback procedure
```

## Usage

### Creating a Task
1. Create task directory: `tasks/<task_id>/`
2. Define payload in `payload.json`
3. List affected files in `manifest.json`
4. Document rollback in `rollback.sh`

### Triggering via Telegram
1. Claude runs: `create-approval-request.sh <task_id> ...`
2. Make.com sends to Telegram
3. Or clicks ✅ Execute
4. Make.com sends `repository_dispatch`
5. `execute-on-approval.yml` runs

## Task ID Convention
Format: `L<layer>.<sequence>-<description>`

Examples:
- `L1.2-001` - First L1.2 task
- `L2.1-003` - Third L2.1 task

## Security
- Tasks reviewed before approval
- No secrets in task files
- All changes auditable via Git history
