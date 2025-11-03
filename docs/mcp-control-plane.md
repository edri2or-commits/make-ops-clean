# MCP Control Plane (MVP)

Adds 5 workflows with proof artifacts:
- .github/workflows/mcp-open-issue.yml
- .github/workflows/mcp-open-pr-from-branch.yml
- .github/workflows/mcp-protected-merge.yml
- .github/workflows/teams-broadcast.yml
- .github/workflows/telegram-broadcast.yml

Trigger example (Open Issue):
```bash
curl -s -X POST -H \"Authorization: Bearer $GITHUB_APP_INSTALLATION_TOKEN\" -H \"Accept: application/vnd.github+json\"  \
  https://api.github.com/repos/edrisor-commits/make-ops-clean/actions/workflows/mcp-open-issue.yml/dispatches \
  -d '{"ref":"main","inputs":{"title":"Demo","body":"From chat"}}'
```\nSecrets: `TEAMS_FLOW_URL`, `TELEGRAM_BOT_TOKEN`.
