# GPT API v2.0 - FULL CONTROL

## 🔥 New Capabilities

### Complete Control Over:
- ✅ Secrets & Tokens
- ✅ Environment Variables  
- ✅ GitHub Authentication
- ✅ System Commands
- ✅ Process Management
- ✅ File Search
- ✅ Git Branches
- ✅ GitHub Actions Logs

---

## 🔐 Secrets & Tokens Management

### List All Secrets (Masked)
```
GET /secrets/list
```

Returns all secrets with masked values:
```json
{
  "secrets": {
    "GITHUB_TOKEN": "ghp_Mq****",
    "API_KEY": "sk-****"
  }
}
```

### Get Specific Secret (Full Value)
```
GET /secrets/get?key=GITHUB_TOKEN
```

⚠️ Returns full unmasked value!

### Set/Update Secret
```
POST /secrets/set
Body: {
  "key": "GITHUB_TOKEN",
  "value": "ghp_NEW_TOKEN_HERE",
  "location": "all"  // 'env', 'github', or 'all'
}
```

### Delete Secret
```
DELETE /secrets/delete?key=API_KEY
```

### Test GitHub Token
```
GET /tokens/github/test
```

### Refresh GitHub Token
```
POST /tokens/github/refresh
Body: {
  "token": "ghp_NEW_TOKEN"
}
```

---

## 📂 Enhanced File Operations

### Search Files
```
GET /files/search?pattern=config&path=automation
```

Returns all files matching pattern with sizes.

---

## 🌿 Git Branches

### List All Branches
```
GET /git/branch
```

### Create New Branch
```
POST /git/branch
Body: {
  "branch": "feature/new-feature"
}
```

### Git Log
```
GET /git/log?limit=20
```

### Git Diff
```
GET /git/diff
```

---

## 🚀 Enhanced GitHub Actions

### Get Run Status
```
GET /actions/status?run_id=123456
```

### Get Run Logs
```
GET /actions/logs?run_id=123456
```

Full logs from workflow run!

---

## 🖥️ Environment & System

### List All Environment Variables
```
GET /env/list
```

Returns complete environment!

### Get Specific Env Var
```
GET /env/get?key=PATH
```

### Set Environment Variable
```
POST /env/set
Body: {
  "key": "MY_VAR",
  "value": "my_value"
}
```

### List Running Processes
```
GET /system/processes
```

### System Information
```
GET /system/info
```

### Run ANY Command
```
POST /command/run
Body: {
  "command": "dir",
  "cwd": "C:\\",
  "shell": "cmd"  // 'cmd', 'powershell', or 'direct'
}
```

⚠️ **FULL SYSTEM ACCESS!**

---

## 📊 Ops Automation

### Get Ops Status
```
GET /ops/status
```

Returns autopilot state.

---

## 🎯 Complete API Reference

### Git Operations
| Endpoint | Method | Description |
|----------|--------|-------------|
| /git/status | GET | Repository status |
| /git/pull | POST | Pull changes |
| /git/commit | POST | Commit & push |
| /git/log | GET | Commit history |
| /git/diff | GET | View changes |
| /git/branch | GET/POST | List/create branches |

### File Operations
| Endpoint | Method | Description |
|----------|--------|-------------|
| /files/list | GET | List directory |
| /files/read | GET | Read file |
| /files/write | POST | Write file |
| /files/delete | DELETE | Delete file |
| /files/search | GET | Search files |

### Secrets & Tokens
| Endpoint | Method | Description |
|----------|--------|-------------|
| /secrets/list | GET | List secrets (masked) |
| /secrets/get | GET | Get secret (full) |
| /secrets/set | POST | Set/update secret |
| /secrets/delete | DELETE | Delete secret |
| /tokens/github/test | GET | Test GitHub token |
| /tokens/github/refresh | POST | Refresh token |

### GitHub Actions
| Endpoint | Method | Description |
|----------|--------|-------------|
| /actions/trigger | POST | Trigger workflow |
| /actions/list | GET | List runs |
| /actions/status | GET | Run status |
| /actions/logs | GET | Run logs |

### Environment & System
| Endpoint | Method | Description |
|----------|--------|-------------|
| /env/list | GET | All env vars |
| /env/get | GET | Specific env var |
| /env/set | POST | Set env var |
| /system/processes | GET | Running processes |
| /system/info | GET | System info |
| /command/run | POST | Run any command |

### Ops Automation
| Endpoint | Method | Description |
|----------|--------|-------------|
| /ops/run | POST | Run ops command |
| /ops/status | GET | Get ops status |

---

## 🔒 Security Warning

⚠️ **THIS API HAS COMPLETE SYSTEM ACCESS:**
- Can read/write ANY file
- Can execute ANY command
- Can access ALL secrets
- Can modify environment
- Can trigger workflows
- Can change GitHub tokens

**NEVER expose this API to the internet without proper authentication!**

### Recommended Security:

1. **Keep it local** - Only `localhost:5000`
2. **Use firewall** - Block external access
3. **Add authentication** - Require API key
4. **Monitor usage** - Log all requests
5. **Review changes** - Check commits before push

---

## 💡 Usage Examples

### Example 1: Rotate GitHub Token
```python
import requests

# Generate new token on GitHub
new_token = "ghp_NEW_TOKEN_HERE"

# Update token
response = requests.post('http://localhost:5000/tokens/github/refresh', 
    json={"token": new_token})

print(response.json())
# {"success": True, "token_saved": True}
```

### Example 2: Search and Update Files
```python
# Search for config files
response = requests.get('http://localhost:5000/files/search',
    params={"pattern": "config", "path": "automation"})

files = response.json()['matches']

# Update each config
for file in files:
    # Read
    content = requests.get(f'http://localhost:5000/files/read',
        params={"path": file['path']}).json()['content']
    
    # Modify
    new_content = content.replace('old_value', 'new_value')
    
    # Write
    requests.post('http://localhost:5000/files/write',
        json={"path": file['path'], "content": new_content})

# Commit all changes
requests.post('http://localhost:5000/git/commit',
    json={"message": "Updated all config files"})
```

### Example 3: System Management
```python
# Check system info
info = requests.get('http://localhost:5000/system/info').json()

# List processes
processes = requests.get('http://localhost:5000/system/processes').json()

# Run custom command
result = requests.post('http://localhost:5000/command/run',
    json={
        "command": "Get-Service | Where-Object {$_.Status -eq 'Running'}",
        "shell": "powershell"
    })
```

### Example 4: Complete Workflow
```python
# 1. Update secrets
requests.post('http://localhost:5000/secrets/set',
    json={
        "key": "API_KEY",
        "value": "new_secret_key",
        "location": "env"
    })

# 2. Update code files
new_code = """
def new_function():
    return "Updated!"
"""

requests.post('http://localhost:5000/files/write',
    json={
        "path": "automation/new_script.py",
        "content": new_code
    })

# 3. Commit changes
requests.post('http://localhost:5000/git/commit',
    json={"message": "[Automation] Updated secrets and code"})

# 4. Trigger workflow
requests.post('http://localhost:5000/actions/trigger',
    json={"workflow": "deploy.yml"})

# 5. Monitor workflow
import time
time.sleep(30)
status = requests.get('http://localhost:5000/actions/list').json()
print(status)
```

---

## 🆕 What's New in v2.0

✅ Complete secrets management
✅ Token rotation capabilities
✅ Environment variable control
✅ System command execution
✅ File search functionality
✅ Git branch operations
✅ GitHub Actions logs access
✅ Process monitoring
✅ Custom command runner

---

## 🚀 Restart Instructions

**Kill the old server:**
```powershell
Get-Process | Where-Object {$_.Name -eq "python" -and $_.Path -like "*gpt-api*"} | Stop-Process
```

**Start new server:**
```powershell
cd C:\Users\edri2\Work\AI-Projects\make-ops-clean\gpt-api
python server.py
```

Or just run `run.bat` again!

---

**GPT now has ABSOLUTE CONTROL! Use wisely! 💪🔥**
