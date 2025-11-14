# Trigger Files Directory

This directory contains state files that trigger GitHub Actions workflows via `on: push` triggers.

## Pattern

```
Claude writes trigger file → commit+push
  ↓
GitHub detects push
  ↓
Workflow runs automatically
  ↓
Workflow updates trigger file (marks complete)
```

## Active Triggers

- `google-mcp-enable-apis.flag` - Enable Google APIs for MCP
- `google-mcp-create-oauth.flag` - Create OAuth client credentials
- `google-mcp-store-secrets.flag` - Store credentials in Secret Manager
