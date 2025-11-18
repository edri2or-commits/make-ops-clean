# 🔐 Token Automation System

## 🚀 Overview

**Automatic token generation, rotation, and management system with AI-powered workflows.**

GPT can now:
- ✅ Generate any type of token
- ✅ Automatically rotate tokens on schedule
- ✅ Create custom rotation workflows
- ✅ Monitor token health
- ✅ Get smart suggestions
- ✅ Track rotation history

---

## 📡 API Endpoints

### Generate Token
```
POST /tokens/generate
Body: {
  "type": "github_pat",
  "length": 40,
  "prefix": "ghp_",
  "include_special": false
}
```

**Token Types:**
- `github_pat` - GitHub Personal Access Token
- `api_key` - API key for services
- `secret_key` - Secret keys
- `password` - Strong passwords
- Custom types

### Rotate Token
```
POST /tokens/rotate
Body: {
  "token_name": "GITHUB_TOKEN",
  "new_token": "ghp_OPTIONAL_SPECIFIC_TOKEN"
}
```

Automatically:
1. Generates new token (or uses provided)
2. Updates in secrets system
3. Commits to git
4. Tracks history

### Setup Auto-Rotation
```
POST /tokens/setup-rotation
Body: {
  "token_name": "API_KEY",
  "interval_hours": 24,
  "auto_rotate": true,
  "notify": true
}
```

Token will automatically rotate every X hours!

### Create Rotation Workflow
```
POST /tokens/workflow/create
Body: {
  "workflow_name": "daily_security_rotation",
  "tokens": ["GITHUB_TOKEN", "API_KEY", "SECRET_KEY"],
  "schedule": "0 0 * * *"
}
```

Rotate multiple tokens together!

### Run Workflow
```
POST /tokens/workflow/run
Body: {
  "workflow_name": "daily_security_rotation"
}
```

### Get Token Health
```
GET /tokens/health
```

Returns:
```json
{
  "total_tokens": 5,
  "needs_rotation": ["OLD_TOKEN"],
  "recently_rotated": ["FRESH_TOKEN"],
  "never_rotated": ["UNUSED_TOKEN"],
  "high_risk": ["EXPIRED_TOKEN"]
}
```

### Get Suggestions
```
GET /tokens/suggest
```

AI-powered suggestions on what to rotate!

### Get Status
```
GET /tokens/status
```

Complete overview of all tokens, rules, workflows, and history.

---

## 💡 Usage Examples

### Example 1: Generate GitHub Token
```python
import requests

response = requests.post('http://localhost:5000/tokens/generate', json={
    "type": "github_pat",
    "length": 40,
    "prefix": "ghp_"
})

token = response.json()['token']
print(f"New GitHub token: {token}")
```

### Example 2: Setup Auto-Rotation (Every 24 Hours)
```python
# Setup auto-rotation for GitHub token
requests.post('http://localhost:5000/tokens/setup-rotation', json={
    "token_name": "GITHUB_TOKEN",
    "interval_hours": 24,
    "auto_rotate": True,
    "notify": True
})

# Now it will automatically rotate every 24 hours!
```

### Example 3: Create Security Workflow
```python
# Create workflow to rotate all security tokens daily
requests.post('http://localhost:5000/tokens/workflow/create', json={
    "workflow_name": "security_daily",
    "tokens": [
        "GITHUB_TOKEN",
        "API_KEY_OPENAI",
        "API_KEY_ANTHROPIC",
        "SECRET_DATABASE"
    ],
    "schedule": "0 2 * * *"  # 2 AM daily
})

# Run it manually
requests.post('http://localhost:5000/tokens/workflow/run', json={
    "workflow_name": "security_daily"
})
```

### Example 4: Health Check & Suggestions
```python
# Check token health
health = requests.get('http://localhost:5000/tokens/health').json()
print(f"Tokens needing rotation: {health['needs_rotation']}")

# Get AI suggestions
suggestions = requests.get('http://localhost:5000/tokens/suggest').json()
for s in suggestions['suggestions']:
    print(s)

# ⚠️  HIGH PRIORITY: OLD_TOKEN
# 📋 Should rotate: TOKEN1, TOKEN2
# 🆕 Never rotated: NEW_TOKEN
```

### Example 5: Manual Rotation
```python
# Rotate specific token
result = requests.post('http://localhost:5000/tokens/rotate', json={
    "token_name": "API_KEY"
})

new_token = result.json()['new_token']
print(f"Rotated! New token: {new_token}")
```

---

## 🤖 GPT Instructions

### Tell GPT:

```
You now have a Token Automation System at http://localhost:5000/tokens/*

Capabilities:
1. Generate tokens: POST /tokens/generate
2. Rotate tokens: POST /tokens/rotate
3. Setup auto-rotation: POST /tokens/setup-rotation
4. Create workflows: POST /tokens/workflow/create
5. Monitor health: GET /tokens/health
6. Get suggestions: GET /tokens/suggest

Common Tasks:

"Generate a new GitHub token"
→ POST /tokens/generate {"type": "github_pat", "length": 40, "prefix": "ghp_"}

"Rotate the API key"
→ POST /tokens/rotate {"token_name": "API_KEY"}

"Setup daily rotation for all tokens"
→ POST /tokens/workflow/create {
    "workflow_name": "daily_rotation",
    "tokens": ["TOKEN1", "TOKEN2"],
    "schedule": "0 0 * * *"
  }

"Check which tokens need rotation"
→ GET /tokens/health
→ GET /tokens/suggest

"Rotate expired tokens"
→ For each token in health['needs_rotation']:
  POST /tokens/rotate {"token_name": token}

Always commit after rotating: POST /git/commit
```

---

## 🎯 Smart Workflows

### Daily Security Rotation
```json
{
  "workflow_name": "daily_security",
  "tokens": ["GITHUB_TOKEN", "API_KEYS"],
  "schedule": "0 2 * * *"
}
```

### Weekly Full Rotation
```json
{
  "workflow_name": "weekly_full",
  "tokens": ["ALL_TOKENS"],
  "schedule": "0 0 * * 0"
}
```

### Hourly High-Security
```json
{
  "workflow_name": "hourly_critical",
  "tokens": ["CRITICAL_TOKEN"],
  "schedule": "0 * * * *"
}
```

---

## 📊 Token Health Monitoring

### Health Indicators:
- 🟢 **Recently Rotated** (< 24 hours)
- 🟡 **Should Rotate** (> 7 days)
- 🟠 **Needs Rotation** (> 14 days)
- 🔴 **HIGH RISK** (> 30 days)

### Auto-Suggestions:
System automatically analyzes all tokens and suggests:
- Which tokens to rotate
- Priority levels
- Optimal rotation schedule

---

## 🔒 Security Features

### Hashing
All tokens are hashed with SHA-256 for tracking without storing plaintext in logs.

### History
Complete audit trail:
- When rotated
- Who/what triggered
- Previous hash
- New hash

### Automation
Set and forget - tokens rotate automatically on schedule.

### Notifications
Get notified when tokens rotate (console + API).

---

## 🎮 CLI Usage

```bash
# Generate token
python token_automation.py generate api_key

# Rotate token
python token_automation.py rotate GITHUB_TOKEN

# Setup auto-rotation (every 24 hours)
python token_automation.py setup-rule GITHUB_TOKEN 24

# Start scheduler (runs continuously)
python token_automation.py start-scheduler

# Check status
python token_automation.py status

# Health check
python token_automation.py health

# Get suggestions
python token_automation.py suggest
```

---

## 📁 File Structure

```
token-automation/
├── token_automation.py      # Main automation engine
├── token_config.json        # Token metadata & rules
├── requirements.txt         # Dependencies
└── README.md               # This file
```

---

## ⚙️ Installation

```bash
cd C:\Users\edri2\Work\AI-Projects\make-ops-clean\gpt-api\token-automation
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### 1. Generate Your First Token
```python
import requests

token = requests.post('http://localhost:5000/tokens/generate', json={
    "type": "api_key",
    "length": 32
}).json()['token']

print(f"Generated: {token}")
```

### 2. Setup Auto-Rotation
```python
requests.post('http://localhost:5000/tokens/setup-rotation', json={
    "token_name": "API_KEY",
    "interval_hours": 24
})

print("Auto-rotation enabled!")
```

### 3. Check Health
```python
health = requests.get('http://localhost:5000/tokens/health').json()
print(health)
```

### 4. Let GPT Handle It!
```
GPT, check our token health and rotate anything that needs it.
```

GPT will:
1. Call `/tokens/health`
2. See what needs rotation
3. Call `/tokens/rotate` for each
4. Commit changes
5. Report back

---

## 🎯 Advanced Features

### Custom Token Formats
```python
# Generate with specific format
token = generate_token(
    type="custom",
    length=50,
    prefix="myapp_",
    include_special=False
)
```

### Batch Rotation
```python
# Rotate multiple tokens at once
for token in ["TOKEN1", "TOKEN2", "TOKEN3"]:
    rotate_token(token)
```

### Scheduled Workflows
```python
# Different schedules for different token types
workflows = {
    "hourly": ["CRITICAL_TOKENS"],
    "daily": ["REGULAR_TOKENS"],
    "weekly": ["LOW_PRIORITY_TOKENS"]
}
```

---

## 🔥 GPT Power Moves

### "Smart Rotate"
```
GPT: "Analyze our tokens and rotate anything that needs it"
```

GPT will:
1. GET /tokens/health
2. GET /tokens/suggest
3. Rotate high-priority tokens
4. Setup rules for others
5. Commit everything

### "Security Audit"
```
GPT: "Do a complete security audit of our tokens"
```

GPT will:
1. Check all token ages
2. Identify risks
3. Suggest rotation schedule
4. Implement recommendations

### "Auto-Everything"
```
GPT: "Setup automatic rotation for all our tokens"
```

GPT will:
1. List all tokens
2. Create optimal rotation rules
3. Setup workflows
4. Enable monitoring

---

## 💪 You're Now In Control!

**GPT can now:**
- Generate unlimited tokens
- Rotate them automatically
- Monitor their health
- Suggest optimizations
- Run custom workflows
- Track everything

**All autonomous. All automatic. All secure.** 🔐

Ready to let GPT handle your token security? 🚀
