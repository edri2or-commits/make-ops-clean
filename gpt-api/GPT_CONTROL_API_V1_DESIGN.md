# GPT_CONTROL_API_V1 Design Document

**Version:** 1.0  
**Status:** Production  
**Last Updated:** 2025-11-19

---

## Overview

**GPT_CONTROL_API_V1** is the single, stable control gateway that allows GPT (ChatGPT, Claude with extended capabilities, or other AI agents) to interact with the `make-ops-clean` repository.

### Purpose
- Provide a unified API for GPT to perform git operations, file management, secrets handling, and basic token generation
- Serve as the **only production control point** - all other servers/automation systems are experimental/lab-only
- Maintain simplicity and stability over feature richness

### Location
- **Base URL:** `http://localhost:5001`
- **Implementation:** `gpt-api/server_simple.py`
- **Server Type:** Flask API server
- **Environment:** Local development machine only (not exposed to internet)

---

## Core Principles

1. **Single Gateway:** This is the ONE API that GPT uses for repo control
2. **Simplicity First:** No background jobs, no schedulers, no complex automation
3. **Explicit Operations:** Every action is triggered by explicit API call, nothing happens automatically
4. **Security Conscious:** All secrets stored in `.gitignore`'d locations
5. **Backwards Compatible:** Endpoint contracts remain stable

---

## API Endpoints

### Git Operations

#### `GET /git/status`
**Purpose:** Get current git repository status

**Request:**
```http
GET /git/status HTTP/1.1
Host: localhost:5001
```

**Response:**
```json
{
  "stdout": "On branch main\nYour branch is up to date...",
  "stderr": "",
  "returncode": 0
}
```

**Use Case:** Check for uncommitted changes before operations

---

#### `POST /git/commit`
**Purpose:** Add all changes, commit with message, and push to origin/main

**Request:**
```http
POST /git/commit HTTP/1.1
Host: localhost:5001
Content-Type: application/json

{
  "message": "Auto commit message",
  "push": true
}
```

**Parameters:**
- `message` (string, optional): Commit message. Default: "GPT automated commit"
- `push` (boolean, optional): Whether to push after commit. Default: true

**Response:**
```json
{
  "commit": {
    "stdout": "[main abc1234] Auto commit message...",
    "stderr": "",
    "returncode": 0
  },
  "push": {
    "stdout": "To github.com:...",
    "stderr": "",
    "returncode": 0
  }
}
```

**Behavior:**
1. Runs `git add .`
2. Runs `git commit -m "<message>"`
3. If push=true and commit succeeded: runs `git push origin main`

**⚠️ Warning:** This commits **all** staged and unstaged changes. No review process.

---

### File Operations

#### `GET /files/read`
**Purpose:** Read content of a file in the repository

**Request:**
```http
GET /files/read?path=README.md HTTP/1.1
Host: localhost:5001
```

**Parameters:**
- `path` (string, required): Relative path from repository root

**Response:**
```json
{
  "path": "README.md",
  "content": "# Make Ops Clean\n\n..."
}
```

**Error Response (404):**
```json
{
  "error": "File not found"
}
```

---

#### `POST /files/write`
**Purpose:** Create or overwrite a file in the repository

**Request:**
```http
POST /files/write HTTP/1.1
Host: localhost:5001
Content-Type: application/json

{
  "path": "config/new_config.json",
  "content": "{\n  \"key\": \"value\"\n}"
}
```

**Parameters:**
- `path` (string, required): Relative path from repository root
- `content` (string, required): File content (text)

**Response:**
```json
{
  "success": true,
  "path": "config/new_config.json"
}
```

**Behavior:**
- Creates parent directories if they don't exist
- Overwrites existing files without warning
- Does NOT automatically commit changes

---

### Secrets Management

#### `GET /secrets/list`
**Purpose:** List all secrets with masked values

**Request:**
```http
GET /secrets/list HTTP/1.1
Host: localhost:5001
```

**Response:**
```json
{
  "secrets": {
    "GITHUB_TOKEN": "ghp_Mqxxxx***",
    "MY_API_KEY": "api_xxxx***",
    "TEST_SECRET": "test***"
  }
}
```

**Sources:**
- `SECRETS/.env.local` (primary secrets file)
- `C:\Users\edri2\.github_token` (GitHub token file)
- Environment variables (GITHUB_TOKEN, GOOGLE_OAUTH_CLIENT_ID, etc.)

**Security:**
- Values are masked (shows first 4-7 chars + ***)
- Full values never logged

---

#### `POST /secrets/set`
**Purpose:** Set or update a secret value

**Request:**
```http
POST /secrets/set HTTP/1.1
Host: localhost:5001
Content-Type: application/json

{
  "key": "MY_NEW_TOKEN",
  "value": "secret_value_here",
  "location": "env"
}
```

**Parameters:**
- `key` (string, required): Secret name
- `value` (string, required): Secret value
- `location` (string, optional): Where to store. Options: "env", "github", "all". Default: "env"

**Response:**
```json
{
  "success": true,
  "results": {
    "env": "updated"
  }
}
```

**Storage Locations:**
- `"env"`: Stores in `SECRETS/.env.local`
- `"github"`: Stores in `C:\Users\edri2\.github_token` (only for GITHUB_TOKEN key)
- `"all"`: Both locations

**Security:**
- `SECRETS/.env.local` is in `.gitignore`
- Keys are appended with timestamp comment
- Existing keys are updated, not duplicated

---

### Token Generation

#### `POST /tokens/generate`
**Purpose:** Generate a secure random token and save it to secrets

**Request:**
```http
POST /tokens/generate HTTP/1.1
Host: localhost:5001
Content-Type: application/json

{
  "service": "MY_API",
  "prefix": "api_",
  "length": 64
}
```

**Parameters:**
- `service` (string, required): Name of the service (becomes key name in secrets)
- `prefix` (string, optional): Prefix for the token. Default: ""
- `length` (integer, optional): Length of random portion. Default: 64

**Response:**
```json
{
  "success": true,
  "service": "MY_API",
  "token": "api_Kj9mL3pQ7rX2nY8vB5wC1dF4gH6sA0zT...",
  "length": 68
}
```

**Behavior:**
1. Generates cryptographically secure random token using `secrets` module
2. Uses alphanumeric characters (a-z, A-Z, 0-9)
3. Automatically saves to `SECRETS/.env.local` as `<service>=<token>`
4. Appends to file, preserves existing secrets

**Token Format:**
- Characters: `[a-zA-Z0-9]`
- Total length: `len(prefix) + length`
- Example: `"api_"` (4) + 64 random chars = 68 total

**Storage:**
```
SECRETS/.env.local:

MY_API=api_Kj9mL3pQ7rX2nY8vB5wC1dF4gH6sA0zT...
```

---

## Current Limitations

### What GPT_CONTROL_API_V1 Does NOT Do:

❌ **No Automatic Token Rotation**
- Tokens are generated on-demand only
- No background scheduling
- No automatic expiration tracking
- No rotation policies

❌ **No GitHub Actions Integration**
- Cannot trigger GitHub Actions workflows
- Cannot check workflow status
- Cannot retrieve workflow logs

❌ **No Advanced Token Automation**
- The full `token_automation.py` system is NOT active
- No bulk operations
- No automation rules engine
- No backup/restore of tokens

❌ **No Background Jobs**
- No schedulers running
- No cron-like tasks
- No periodic checks
- Every operation is synchronous and explicit

❌ **No Authentication (Currently)**
- API is open on localhost
- No API key validation
- No rate limiting
- No audit logging

❌ **No Environment Variable Management**
- Cannot set system environment variables
- Cannot restart processes
- No service management

❌ **No Advanced Git Operations**
- No branch management
- No pull operations
- No merge/rebase
- No conflict resolution
- Only: status, add all, commit, push to main

---

## Security Considerations

### ✅ Current Security Measures:

1. **Local Only:** Server runs on `localhost:5001`, not exposed to internet
2. **Secrets Isolation:** 
   - All secrets stored in `SECRETS/.env.local`
   - Directory is in `.gitignore`
   - Never committed to git
3. **No Hardcoded Secrets:** API server code contains no secret values
4. **File System Boundaries:** All operations scoped to repository directory

### ⚠️ Security Warnings:

1. **No Authentication:** Any process on the local machine can access the API
2. **Full Write Access:** GPT can modify any file in the repository
3. **Auto-commit to Main:** No review process before pushing to GitHub
4. **Secret Visibility:** GPT can read all secrets via `/secrets/list`
5. **No Rate Limiting:** GPT can make unlimited requests
6. **No Audit Trail:** Operations are not logged with timestamps/actor

### 🔐 Recommended Next Steps:

- [ ] Add API key authentication via `X-API-Key` header
- [ ] Implement request logging with timestamps
- [ ] Add rate limiting per operation type
- [ ] Consider approval workflow for git commits
- [ ] Add file path validation/whitelist
- [ ] Implement secret access controls (read-only for certain keys)

---

## Repository Structure

### Secrets Storage:
```
make-ops-clean/
├── SECRETS/
│   └── .env.local          # Primary secrets (gitignored)
├── gpt-api/
│   ├── secrets/
│   │   └── secrets.env     # API config secrets (gitignored)
│   └── server_simple.py    # This API server
```

### Important Files:
- `gpt-api/server_simple.py` - The API server implementation
- `SECRETS/.env.local` - Where generated tokens are stored
- `.gitignore` - Ensures SECRETS/ is never committed

---

## Usage Examples

### Example 1: Generate Token and Commit
```bash
# Generate token
curl -X POST http://localhost:5001/tokens/generate \
  -H "Content-Type: application/json" \
  -d '{"service":"NEW_API","prefix":"napi_","length":48}'

# Commit the change
curl -X POST http://localhost:5001/git/commit \
  -H "Content-Type: application/json" \
  -d '{"message":"[Tokens] Added NEW_API token"}'
```

### Example 2: Update Config File
```bash
# Read current config
curl "http://localhost:5001/files/read?path=config/config.json"

# Write updated config
curl -X POST http://localhost:5001/files/write \
  -H "Content-Type: application/json" \
  -d '{
    "path": "config/config.json",
    "content": "{\"updated\": true}"
  }'

# Commit
curl -X POST http://localhost:5001/git/commit \
  -H "Content-Type: application/json" \
  -d '{"message":"Updated config"}'
```

### Example 3: Set Secret and Verify
```bash
# Set secret
curl -X POST http://localhost:5001/secrets/set \
  -H "Content-Type: application/json" \
  -d '{"key":"DB_PASSWORD","value":"super_secret_123"}'

# List to verify (will be masked)
curl http://localhost:5001/secrets/list
```

---

## Relationship to Other Systems

### Lab/Experimental Systems (NOT Active in V1):

The following systems exist in the codebase but are **NOT** part of GPT_CONTROL_API_V1:

- `gpt-api/server.py` - Full-featured server (has bugs, not stable)
- `gpt-api/server_v3.py` - Experimental version
- `gpt-api/server_fixed.py` - Attempted fixes
- `gpt-api/token-automation/token_automation.py` - Advanced token system (850+ lines, not tested)
- `gpt-api/TOKEN_AUTOMATION_GUIDE.md` - Docs for unused system

**Why Separated:**
- Stability: V1 focuses on core, tested functionality
- Simplicity: No background jobs or complex scheduling
- Predictability: Every action is explicit API call
- Safety: No automatic token rotation that could break systems

**Future Integration:**
When token automation is tested and stable, it may be integrated into a V2 API. For now, keep production (V1) and lab (experimental) clearly separated.

---

## Version History

### v1.0 (2025-11-19)
- Initial production version
- Git operations: status, commit+push
- File operations: read, write
- Secrets: list, set
- Token generation: basic secure random tokens
- No authentication, no scheduling, no automation

---

## Maintenance Notes

### Starting the Server:
```bash
cd C:\Users\edri2\Work\AI-Projects\make-ops-clean\gpt-api
python server_simple.py
```

### Quick Test:
```bash
curl http://localhost:5001/git/status
```

### Stopping the Server:
- Ctrl+C in terminal
- Or kill process on port 5001

### Log Location:
- Currently: stdout/stderr only
- No persistent logs

---

## Contact & Support

**Repository:** `make-ops-clean`  
**Owner:** edri2or-commits  
**Purpose:** Automation and control infrastructure for Make.com operations

**For Issues:**
- Check that server is running: `curl http://localhost:5001/git/status`
- Verify secrets file exists: `SECRETS/.env.local`
- Check Python version: Python 3.x required
- Review Flask errors in terminal output

---

**END OF DOCUMENT**
