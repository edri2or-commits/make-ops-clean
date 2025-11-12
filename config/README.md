# Configuration Guide

## Overview
Centralized configuration for all system integrations and services.

## Services Available
- **GitHub** (repo sync, automation)
- **Telegram** (notifications, approval flows)
- **Make.com** (webhooks, scenarios)
- **Google Workspace** (via MCP - Drive, Gmail, Calendar)
- **OpenAI** (optional AI capabilities)

## Setup Instructions

### 1. GitHub Integration
```bash
# Create Personal Access Token
1. Visit: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: repo (all), workflow
4. Copy token to config.json → github.token
```

### 2. Telegram Bot
```bash
# Create Bot
1. Open Telegram, search @BotFather
2. Send: /newbot
3. Follow instructions, copy token
4. Get your chat_id from @userinfobot
5. Update config.json → telegram section
```

### 3. Make.com Webhook
```bash
# Setup Webhook
1. Login: https://www.make.com/en/login
2. Create new scenario
3. Add "Webhooks > Custom webhook"
4. Copy URL to config.json → make.webhook_url
```

### 4. Google Workspace (MCP)
```bash
# Already configured via MCP
# See: integrations/google/README.md
```

## Environment Variables
For production, use environment variables instead of config.json:

```bash
export GITHUB_TOKEN="ghp_..."
export TELEGRAM_BOT_TOKEN="123456:ABC..."
export MAKE_WEBHOOK_URL="https://hook.eu2.make.com/..."
```

See `.env.example` in each integration folder for details.

## Security Notes
- ⚠️ **Never commit config.json with real tokens**
- ✅ Use `.env` files (gitignored)
- ✅ Store secrets in GitHub Secrets for CI/CD
- ✅ Rotate tokens periodically

---
**Updated**: 2025-11-12  
**Branch**: unified/desktop-merge