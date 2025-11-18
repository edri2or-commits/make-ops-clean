# GPT API for make-ops-clean

🤖 **Full GPT control over the make-ops-clean repository**

## Quick Start

### 1. Install Dependencies
```powershell
cd C:\Users\edri2\Work\AI-Projects\make-ops-clean\gpt-api
pip install -r requirements.txt
```

### 2. Start Server
```powershell
python server.py
```

Server will run on: `http://localhost:5000`

## API Endpoints

### Git Operations

**Get Status**
```
GET /git/status
```

**Pull Changes**
```
POST /git/pull
```

**Commit & Push**
```
POST /git/commit
Body: {"message": "Your commit message"}
```

### File Operations

**List Files**
```
GET /files/list?path=folder/subfolder
```

**Read File**
```
GET /files/read?path=README.md
```

**Write File**
```
POST /files/write
Body: {
  "path": "new-file.md",
  "content": "File content here"
}
```

**Delete File**
```
DELETE /files/delete?path=file-to-delete.md
```

### GitHub Actions

**Trigger Workflow**
```
POST /actions/trigger
Body: {"workflow": "index-append-manual.yml"}
```

**List Recent Runs**
```
GET /actions/list
```

### Ops Commands

**Run Autopilot Command**
```
POST /ops/run
Body: {"command": "your-command"}
```

## GPT Custom Instructions

Add this to your GPT:

```
You have access to the make-ops-clean repository via API at http://localhost:5000

Available operations:
- Git: status, pull, commit/push
- Files: list, read, write, delete
- GitHub Actions: trigger workflows, list runs
- Ops: run autopilot commands

Base URL: http://localhost:5000

Always check git status before making changes.
Always commit with clear messages after changes.
```

## Security Notes

⚠️ This API runs locally and has full access to the repository
⚠️ Make sure to review changes before committing
⚠️ GitHub token is embedded - keep this secure

## Usage Example

```python
import requests

# Check status
response = requests.get('http://localhost:5000/git/status')
print(response.json())

# Read a file
response = requests.get('http://localhost:5000/files/read?path=README.md')
print(response.json()['content'])

# Make changes and commit
requests.post('http://localhost:5000/files/write', json={
    "path": "new-doc.md",
    "content": "# New Document"
})

requests.post('http://localhost:5000/git/commit', json={
    "message": "Added new documentation"
})
```

## Troubleshooting

**Server won't start?**
- Check if port 5000 is available
- Make sure Flask is installed: `pip install flask`

**Git operations fail?**
- Verify git is in PATH
- Check GitHub authentication
- Ensure you're in the right directory

**File operations fail?**
- Check file paths are relative to repo root
- Verify permissions

## Auto-Start Script

Save as `start-gpt-api.ps1`:

```powershell
cd C:\Users\edri2\Work\AI-Projects\make-ops-clean\gpt-api
python server.py
```

Run on startup or manually when needed.
