# MOC - Make-Ops-Clean CLI

🚀 **Command line interface for managing your make-ops-clean repository**

## Quick Start

### 1. Install Dependencies
```powershell
cd C:\Users\edri2\Work\AI-Projects\make-ops-clean\gpt-api
pip install requests
```

### 2. Make Sure API Server is Running
```powershell
# Check if running
netstat -ano | findstr :5000

# If not, start it
.\run.bat
```

### 3. Use MOC!
```powershell
# Check health
python moc.py health

# Show git status
python moc.py status

# List files
python moc.py list

# Read a file
python moc.py read README.md

# And more!
```

---

## 📖 Commands Reference

### Health & Status

**Check API health**
```powershell
python moc.py health
```

**Show git status**
```powershell
python moc.py status
```

**Pull latest changes**
```powershell
python moc.py pull
```

---

### File Operations

**List files in directory**
```powershell
# List root
python moc.py list

# List specific directory
python moc.py list automation/scripts
```

**Read file**
```powershell
python moc.py read README.md

# Save to local file
python moc.py read SYSTEM_STATUS.md > local-status.md
```

**Write file from string**
```powershell
python moc.py write test.md --content "# Test File"
```

**Write file from local file**
```powershell
python moc.py write docs/new-doc.md --from-file local-file.md
```

**Write file from stdin**
```powershell
echo "# New Content" | python moc.py write test.md --from-stdin

# Or from clipboard
Get-Clipboard | python moc.py write notes.md --from-stdin
```

**Delete file**
```powershell
# With confirmation
python moc.py delete old-file.md

# Force delete (no confirmation)
python moc.py delete old-file.md -f
```

---

### Git Operations

**Commit and push**
```powershell
python moc.py commit "feat: add new feature"

python moc.py commit "docs: update README"

python moc.py commit "fix: resolve bug in automation"
```

---

### GitHub Actions

**Trigger workflow**
```powershell
python moc.py trigger index-append-manual.yml
```

**List recent runs**
```powershell
python moc.py runs
```

---

### Quick Operations

**Quick update: write and commit in one command**
```powershell
python moc.py quick docs/guide.md --from-file local-guide.md -m "docs: update guide"
```

---

## 🔥 Real-World Examples

### Example 1: Update Documentation
```powershell
# Edit locally
notepad README.md

# Push to repo
python moc.py write README.md --from-file README.md
python moc.py commit "docs: update README with new features"
```

### Example 2: Quick Fix
```powershell
# Read current file
python moc.py read config/settings.json > settings.json

# Edit locally
code settings.json

# Push back (quick mode)
python moc.py quick config/settings.json --from-file settings.json -m "fix: correct settings"
```

### Example 3: Automation Script
```powershell
# Create new automation script
@"
def new_automation():
    print('Hello from automation!')
"@ | python moc.py write automation/new_script.py --from-stdin

python moc.py commit "feat: add new automation script"
```

### Example 4: Bulk Operations
```powershell
# List all markdown files
python moc.py list | findstr .md

# Read multiple files
python moc.py read README.md
python moc.py read SYSTEM_STATUS.md
python moc.py read DECISION_LOG.md
```

### Example 5: Workflow Management
```powershell
# Check current workflows
python moc.py runs

# Trigger manual workflow
python moc.py trigger index-append-manual.yml

# Check status after
python moc.py runs
```

---

## 🐍 Python API Usage

You can also use the client directly in Python:

```python
from client import MakeOpsCleanClient

client = MakeOpsCleanClient()

# Read file
content = client.read_file("README.md")
print(content)

# Write file
client.write_file("test.md", "# Test")

# Commit
client.git_commit("docs: add test file")

# Quick update
client.quick_update(
    "docs/guide.md",
    "# New Guide\n\nContent here...",
    "docs: create new guide"
)

# Trigger workflow
client.trigger_workflow("index-append-manual.yml")
```

---

## 🎯 Common Workflows

### Daily Update Workflow
```powershell
# 1. Pull latest
python moc.py pull

# 2. Check status
python moc.py status

# 3. Make changes locally
notepad docs/daily-notes.md

# 4. Push changes
python moc.py write docs/daily-notes.md --from-file docs/daily-notes.md
python moc.py commit "docs: daily update"

# 5. Trigger automation
python moc.py trigger index-append-manual.yml
```

### New Feature Workflow
```powershell
# 1. Create files locally

# 2. Upload all
python moc.py write feature/new-feature.py --from-file new-feature.py
python moc.py write docs/feature-guide.md --from-file feature-guide.md

# 3. Commit
python moc.py commit "feat: implement new feature with docs"

# 4. Verify
python moc.py status
python moc.py runs
```

---

## 💡 Tips & Tricks

### Alias for Quick Access
Add to PowerShell profile:
```powershell
function moc { python C:\Users\edri2\Work\AI-Projects\make-ops-clean\gpt-api\moc.py $args }
```

Then use:
```powershell
moc health
moc status
moc read README.md
```

### Pipe Operations
```powershell
# Backup before editing
python moc.py read important.md > backup.md

# Edit and push back
notepad important.md
python moc.py write important.md --from-file important.md
python moc.py commit "docs: update important.md"
```

### Watch for Changes
```powershell
# Monitor git status
while ($true) { 
    python moc.py status
    Start-Sleep -Seconds 30
}
```

---

## 🔧 Advanced Usage

### Custom API URL
```powershell
python moc.py --base-url http://192.168.1.100:5000 health
```

### Scripting
```powershell
# Automated deployment script
$files = @("deploy/script1.py", "deploy/script2.py")

foreach ($file in $files) {
    python moc.py write $file --from-file "local/$file"
}

python moc.py commit "deploy: update deployment scripts"
python moc.py trigger "deploy-workflow.yml"
```

---

## 📚 Related Files

- `client.py` - Python API client
- `server.py` - Flask API server
- `GPT_INSTRUCTIONS.md` - Instructions for GPT integration

---

## 🐛 Troubleshooting

**"Connection refused"**
→ Make sure API server is running: `.\run.bat`

**"Module not found"**
→ Install dependencies: `pip install requests`

**"File not found"**
→ Check path is relative to repo root

**Git operations fail**
→ Make sure you have git configured and authenticated

---

**Happy automating! 🚀**
