# 🔥 Token Automation System - Complete Guide

## Overview

GPT now has **COMPLETE AUTOMATED TOKEN MANAGEMENT** capabilities!

You can:
- ✅ Generate tokens automatically (any type, any format)
- ✅ Rotate tokens on schedule
- ✅ Create automation rules
- ✅ Run background scheduler
- ✅ Bulk operations
- ✅ Backup & restore

---

## 🎯 Quick Start

### 1. Generate a New Token

```http
POST /tokens/generate
{
  "service": "MY_API",
  "type": "api_key",
  "prefix": "sk_",
  "length": 64,
  "charset": "alphanumeric"
}
```

**Token Types:**
- `api_key` - Standard API key
- `github` - GitHub format (ghp_...)
- `oauth` - OAuth token
- `jwt` - JWT signing secret

**Charsets:**
- `alphanumeric` - Letters + numbers
- `hex` - Hexadecimal
- `base64` - Base64 characters
- `full` - All characters

### 2. Rotate a Token

```http
POST /tokens/rotate
{
  "service": "MY_API",
  "auto_generate": true
}
```

Auto-generates new token using same config as original.

### 3. Bulk Rotate

```http
POST /tokens/bulk-rotate
{
  "services": ["API_1", "API_2", "API_3"]
}
```

Or rotate ALL tokens:
```http
POST /tokens/bulk-rotate
{}
```

### 4. List All Tokens

```http
GET /tokens/list-all
```

Returns all tokens with metadata:
```json
{
  "tokens": {
    "MY_API": {
      "type": "api_key",
      "created_at": "2025-11-18T...",
      "last_rotated": "2025-11-19T...",
      "preview": "sk_abc123...",
      "history_count": 5
    }
  }
}
```

---

## 🤖 Automation Rules

### Create Rule

```http
POST /automation/rules
{
  "rule_name": "rotate_api_keys_monthly",
  "config": {
    "service": "MY_API",
    "action": "rotate",
    "schedule": "monthly",
    "conditions": {
      "age_days": 30
    },
    "auto_generate": true
  }
}
```

**Schedules:**
- `daily` - Every 24 hours
- `weekly` - Every 7 days
- `monthly` - Every 30 days

**Actions:**
- `rotate` - Rotate specific token
- `generate` - Generate new token
- `bulk_rotate` - Rotate multiple tokens

**Conditions:**
- `age_days` - Token age threshold
- `usage_count` - Usage threshold (if tracked)

### List Rules

```http
GET /automation/rules
```

### Execute Rule Manually

```http
POST /automation/execute
{
  "rule_name": "rotate_api_keys_monthly"
}
```

### Delete Rule

```http
DELETE /automation/rules?rule_name=rotate_api_keys_monthly
```

### Check All Rules

```http
POST /automation/check
```

Checks all active rules and executes those that are due.

---

## ⏰ Background Scheduler

### Start Scheduler

```http
POST /automation/scheduler/start
{
  "interval_minutes": 60
}
```

Runs in background, checking rules every N minutes.

### Stop Scheduler

```http
POST /automation/scheduler/stop
```

---

## 💾 Backup & Restore

### Create Backup

```http
POST /tokens/backup
```

Returns:
```json
{
  "success": true,
  "backup_file": "C:\\...\\backups\\tokens_backup_20251118_235900.json",
  "token_count": 15
}
```

Backups include:
- All tokens
- Token registry (metadata)
- Automation rules

---

## 📋 Example Workflows

### Workflow 1: Setup New Service

```python
# 1. Generate token
POST /tokens/generate
{
  "service": "NEW_SERVICE",
  "type": "api_key",
  "prefix": "ns_",
  "length": 64
}

# 2. Create rotation rule
POST /automation/rules
{
  "rule_name": "rotate_new_service",
  "config": {
    "service": "NEW_SERVICE",
    "action": "rotate",
    "schedule": "monthly",
    "auto_generate": true
  }
}

# 3. Done! Token will auto-rotate monthly
```

### Workflow 2: Emergency Rotation

```python
# Rotate all tokens immediately
POST /tokens/bulk-rotate
{}

# Backup after rotation
POST /tokens/backup
```

### Workflow 3: Scheduled Maintenance

```python
# Create daily check rule
POST /automation/rules
{
  "rule_name": "daily_security_check",
  "config": {
    "action": "bulk_rotate",
    "schedule": "daily",
    "conditions": {
      "age_days": 7
    }
  }
}

# Start scheduler
POST /automation/scheduler/start
{
  "interval_minutes": 60
}
```

### Workflow 4: Custom Rotation Schedule

```python
# Rotate every 2 weeks
POST /automation/rules
{
  "rule_name": "biweekly_rotation",
  "config": {
    "service": "IMPORTANT_API",
    "action": "rotate",
    "schedule": "weekly",
    "conditions": {
      "age_days": 14
    },
    "auto_generate": true
  }
}
```

---

## 🎭 Advanced Use Cases

### Use Case 1: Multi-Environment Setup

```python
# Production tokens - rotate monthly
for env in ["PROD_API", "PROD_DB", "PROD_CACHE"]:
    POST /tokens/generate {"service": env, "length": 128}
    POST /automation/rules {
        "rule_name": f"rotate_{env}_monthly",
        "config": {"service": env, "schedule": "monthly"}
    }

# Staging tokens - rotate weekly
for env in ["STAGE_API", "STAGE_DB"]:
    POST /tokens/generate {"service": env, "length": 64}
    POST /automation/rules {
        "rule_name": f"rotate_{env}_weekly",
        "config": {"service": env, "schedule": "weekly"}
    }
```

### Use Case 2: Progressive Rotation

```python
# Rotate oldest tokens first
GET /tokens/list-all
# Sort by age
# Rotate top 5 oldest
POST /tokens/bulk-rotate {"services": [oldest_5]}
```

### Use Case 3: Conditional Rotation

```python
# Only rotate if > 90 days old
POST /automation/rules
{
  "rule_name": "age_based_rotation",
  "config": {
    "action": "bulk_rotate",
    "schedule": "daily",
    "conditions": {
      "age_days": 90
    }
  }
}
```

---

## 🔐 Security Best Practices

### 1. Regular Backups
```python
# Daily backup schedule
POST /automation/rules
{
  "rule_name": "daily_backup",
  "config": {
    "action": "backup",
    "schedule": "daily"
  }
}
```

### 2. Rotation Strategy
- Critical tokens: Rotate weekly
- Standard tokens: Rotate monthly
- Development tokens: Rotate quarterly

### 3. Audit Trail
All operations are logged in:
- `token_registry.json` - Token history
- `automation_rules.json` - Rule execution log

### 4. Emergency Procedures
```python
# If token compromised:
# 1. Immediate rotation
POST /tokens/rotate {"service": "COMPROMISED", "auto_generate": true}

# 2. Backup old state
POST /tokens/backup

# 3. Update all configs referencing old token
# (via file operations)
```

---

## 📊 Monitoring

### Check Token Health

```python
# Get all tokens
tokens = GET /tokens/list-all

# Check age
for service, data in tokens["tokens"].items():
    created = datetime.fromisoformat(data["created_at"])
    age_days = (datetime.now() - created).days
    
    if age_days > 90:
        print(f"⚠️ {service} is {age_days} days old")
```

### Check Automation Status

```python
# List all rules
rules = GET /automation/rules

# Check last execution
for rule_name, rule in rules["rules"].items():
    last_exec = rule.get("last_executed")
    if not last_exec:
        print(f"⚠️ {rule_name} never executed")
```

---

## 🚨 Troubleshooting

### Token Generation Fails
```python
# Check if service already exists
GET /tokens/list-all

# If exists, rotate instead
POST /tokens/rotate {"service": "X"}
```

### Scheduler Not Running
```python
# Check status (look for running threads)
GET /system/processes

# Restart scheduler
POST /automation/scheduler/stop
POST /automation/scheduler/start {"interval_minutes": 60}
```

### Rule Not Executing
```python
# Manually execute to test
POST /automation/execute {"rule_name": "X"}

# Check rule config
GET /automation/rules

# Verify schedule and conditions
```

---

## 💡 GPT Instructions

When user asks you to:

**"Generate a token for X"**
→ Use `/tokens/generate` with appropriate config

**"Rotate the X token"**
→ Use `/tokens/rotate` with auto_generate=true

**"Setup automatic rotation for X"**
→ Create automation rule with schedule

**"Rotate all tokens"**
→ Use `/tokens/bulk-rotate`

**"Check if any tokens need rotation"**
→ Use `/tokens/list-all` and analyze ages

**"Setup monthly rotation"**
→ Create rule with schedule="monthly"

**"Start the token automation"**
→ Start the scheduler

**"Backup all tokens"**
→ Use `/tokens/backup`

---

## 🎯 Complete Example

```python
# Full setup for new project

# 1. Generate all needed tokens
POST /tokens/generate {"service": "API_KEY", "type": "api_key", "prefix": "sk_"}
POST /tokens/generate {"service": "DATABASE", "type": "api_key", "length": 128}
POST /tokens/generate {"service": "JWT_SECRET", "type": "jwt"}
POST /tokens/generate {"service": "OAUTH_CLIENT", "type": "oauth"}

# 2. Setup rotation rules
POST /automation/rules {
    "rule_name": "rotate_critical_monthly",
    "config": {
        "action": "bulk_rotate",
        "services": ["API_KEY", "JWT_SECRET"],
        "schedule": "monthly"
    }
}

POST /automation/rules {
    "rule_name": "rotate_database_quarterly",
    "config": {
        "service": "DATABASE",
        "schedule": "monthly",
        "conditions": {"age_days": 90}
    }
}

# 3. Start scheduler
POST /automation/scheduler/start {"interval_minutes": 60}

# 4. Create initial backup
POST /tokens/backup

# Done! Fully automated token management 🎉
```

---

**GPT now has FULL TOKEN AUTONOMY!** 🔥💪

Use it wisely to keep systems secure and tokens fresh!
