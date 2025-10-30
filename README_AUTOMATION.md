# CI Bootstrap: Health & Inso

## Required secrets (repo → Settings → Secrets and variables → Actions)
- `GH_PAT_SECRETS_READ` — Fine-grained PAT (this repo only) with **Secrets: Read** (optional: **Actions: Read**)
- (Optional) `TELEGRAM_BOT_TOKEN` — for Telegram `getMe`
- (Optional) `MAKE_API_TOKEN` — for Make `/users/me` (Authorization: `Token <token>`)

> Notes:
> - Listing repo secrets returns names + timestamps only (never values).
> - Make API base differs by zone (e.g., `eu1.make.com`, `us1.make.com`).

## Workflows
### 1) Repo Health & Integrations
Dispatch manually (Actions → Run workflow). Outputs artifact `discovery-status/`:
- `repo_secrets.json` / `repo_secrets_min.json`
- `workflows.json` / `workflow_runs.json`
- `telegram_getMe.json` (if token exists)
- `make_users_me.json` (if token exists)

### 2) Insomnia Inso CI
Dispatch manually. Set `working_dir` to a path that includes `.insomnia` or an Insomnia export (`*.json`/`*.yaml`).
Runs `inso lint spec --ci` and `inso run test --ci`.
