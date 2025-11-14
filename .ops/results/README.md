# Results Directory

This directory contains results from GitHub Actions workflow executions.

## Pattern

```
Workflow completes
  ↓
Workflow writes result JSON
  ↓
Workflow commits result
  ↓
Claude reads result via GitHub API
```

## Active Results

- `google-apis-enabled.json` - APIs enablement status
- `oauth-client-created.json` - OAuth client creation result
- `secrets-stored.json` - Secret Manager storage confirmation
