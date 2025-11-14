# Windows-MCP Installation Playbook

**Created**: 2025-11-14  
**For**: אור (Manual Installation Guide)  
**Status**: Ready for execution (requires approval)  
**Risk**: 🔴 HIGH

---

## 🎯 Purpose

This playbook guides you through installing Windows-MCP Desktop Extension into Claude Desktop. The script does most of the work, but you need to perform the final installation steps manually.

---

## ⚠️ Before You Begin

### What You're Installing

**Windows-MCP** provides Claude with:
- ✅ Mouse and keyboard control
- ✅ Window management
- ✅ Application launching
- ✅ PowerShell command execution
- ✅ Screenshot capabilities
- ✅ System state monitoring

### Risk Assessment

🔴 **HIGH RISK**

This gives Claude **full control** over your computer's GUI and system. Use extreme caution.

**Mitigations in Place**:
- ✅ All operations logged
- ✅ You maintain approval authority
- ✅ Can disable instantly if needed
- ✅ Testing will be gradual (read-only first)

---

## 📋 Prerequisites Check

Before running the script, verify:

```powershell
# Check Python 3.13+
python --version
# Should show: Python 3.13.x or higher

# Check Node.js 18+
node --version
# Should show: v18.x or higher

# Check Git
git --version
# Should show: git version x.x.x
```

**If any are missing**:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/
- Git: https://git-scm.com/downloads

---

## 🚀 Installation Steps

### Step 1: Review the Script

**Location**: `scripts/install_windows_mcp.ps1`

**What it does**:
1. Checks all prerequisites
2. Clones Windows-MCP repository
3. Builds Desktop Extension (.dxt file)
4. Copies to installation directory
5. Creates installation log

**What it does NOT do**:
- ❌ Does not modify `claude_desktop_config.json`
- ❌ Does not restart Claude Desktop
- ❌ Does not install the extension in Claude

**Review the script** before running. Look for:
- No secrets embedded
- No dangerous system modifications
- Clear error handling
- Appropriate warnings

---

### Step 2: Run the Installation Script

**Open PowerShell** (as regular user, NOT administrator unless needed):

```powershell
# Navigate to repository
cd C:\Users\edri2\Work\AI-Projects\Claude-Ops\make-ops-clean

# Run installation script
powershell -ExecutionPolicy Bypass -File .\scripts\install_windows_mcp.ps1
```

**Expected output**:
```
=============================================
  WINDOWS-MCP INSTALLATION SCRIPT
=============================================

WARNING: This script will install Windows-MCP...
[warnings displayed]

Press Ctrl+C to cancel, or
Press any key to continue...
```

**Press any key** if you want to proceed.

**Script will**:
- ✅ Check prerequisites (Python, Node, Git, UV, DXT)
- ✅ Clone repository to temp location
- ✅ Build .dxt extension file
- ✅ Copy to: `%USERPROFILE%\Work\AI-Projects\Claude-Ops\mcp-servers\windows-mcp`
- ✅ Save installation log

**Expected result**:
```
=============================================
INSTALLATION COMPLETE!
=============================================

Windows-MCP has been prepared for Claude Desktop.

NEXT STEPS (MANUAL):
[manual steps listed]
```

---

### Step 3: Install Extension in Claude Desktop

**1. Locate the DXT file**:
```
C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\windows-mcp\windows-mcp.dxt
```

**2. Open Claude Desktop**

**3. Navigate to Extensions**:
- Click: Settings (gear icon)
- Select: Extensions

**4. Install Extension**:
- Click: "Install Extension" button
- Browse to the `.dxt` file location
- Select: `windows-mcp.dxt`
- Click: "Open" or "Install"

**5. Confirm Installation**:
- Claude Desktop should show "Extension installed successfully"
- Or similar confirmation message

---

### Step 4: Restart Claude Desktop

**CRITICAL**: You **MUST** restart Claude Desktop completely.

**How**:
1. Close all Claude Desktop windows
2. Check Task Manager - ensure Claude Desktop is NOT running
3. Reopen Claude Desktop

**Do NOT skip this step** - extension won't load without restart.

---

### Step 5: Verify Installation

**1. Check Claude Desktop Logs** (optional but recommended):

Logs location:
```
%APPDATA%\Claude\logs\
```

Look for:
- "Windows-MCP" connection message
- No error messages related to Windows-MCP

**2. Test in Claude Desktop**:

In a new conversation, try:
```
Claude, take a screenshot of my desktop
```

Or:
```
Claude, what applications are currently running on my computer?
```

**Expected**:
- Claude should respond with actual data
- Screenshot should be captured
- Or list of running applications should appear

**If it works**: ✅ Installation successful!

---

## ❌ Troubleshooting

### Extension Not Appearing

**Check**:
1. Did you restart Claude Desktop?
2. Is the `.dxt` file in the correct location?
3. Check Claude Desktop logs for errors

**Solution**:
- Try reinstalling extension
- Restart Claude Desktop again
- Check file permissions

---

### Tools Not Working

**Check**:
1. Are you on Windows 7/8/10/11?
2. Is Windows language set to English?
3. Check Claude Desktop logs

**Common Issues**:
- **Launch-Tool fails**: Windows not in English
  - Solution: Disable Launch-Tool or switch language
- **Python errors**: Python version < 3.13
  - Solution: Upgrade Python

---

### Script Fails

**Common Causes**:
1. Missing prerequisites (Python, Node, Git)
2. Network issues (can't clone repository)
3. Permissions issues

**Solution**:
1. Verify all prerequisites installed
2. Check internet connection
3. Run PowerShell as administrator if needed
4. Check script output for specific error

---

## 🧪 Post-Installation Testing

### Phase 1: Read-Only Tests (SAFE)

**Test these first**:

```
1. "Take a screenshot"
   → Should capture desktop

2. "What applications are running?"
   → Should list active apps

3. "Show me the state of my system"
   → Should return system info
```

**Risk**: 🟢 Low (no system changes)

---

### Phase 2: Safe Operations (MEDIUM)

**After Phase 1 works**:

```
1. "Move the mouse to the center of the screen"
   → Should move cursor

2. "Open Notepad and type 'Hello World'"
   → Should open app and type

3. "Copy this text to clipboard: [text]"
   → Should copy to clipboard
```

**Risk**: 🟡 Medium (reversible operations)

**Require approval before**: Testing dangerous tools (Shell-Tool)

---

### Phase 3: Full Operations (HIGH CAUTION)

**Only after Phase 2 works AND with explicit approval**:

```
1. Shell-Tool commands (VERY CAREFULLY)
2. Application launching (system apps)
3. Window management (resize, move)
```

**Risk**: 🔴 High

**Always approve**: Before executing any Shell-Tool command

---

## 🚨 Emergency Procedures

### Disable Windows-MCP Immediately

**If something goes wrong**:

**Method 1: Via Claude Desktop**:
1. Settings → Extensions
2. Find: Windows-MCP
3. Click: Disable or Uninstall
4. Restart Claude Desktop

**Method 2: Manual**:
1. Close Claude Desktop
2. Delete or rename the `.dxt` file
3. Restart Claude Desktop

---

### Rollback Installation

**If you want to remove completely**:

```powershell
# Remove installation directory
Remove-Item -Path "$env:USERPROFILE\Work\AI-Projects\Claude-Ops\mcp-servers\windows-mcp" -Recurse -Force

# Uninstall from Claude Desktop (via Settings)
```

---

## ✅ Success Checklist

**Installation**:
- [ ] Script ran without errors
- [ ] `.dxt` file created
- [ ] Files in installation directory
- [ ] Extension installed in Claude Desktop
- [ ] Claude Desktop restarted

**Verification**:
- [ ] Extension appears in Claude Desktop
- [ ] No errors in logs
- [ ] Screenshot test works
- [ ] System state query works

**Safety**:
- [ ] Understand risks
- [ ] Know how to disable
- [ ] Testing plan established
- [ ] Approval process clear

---

## 📝 Evidence Collection

**After installation, collect**:

1. **Installation log**:
   ```
   %USERPROFILE%\Work\AI-Projects\Claude-Ops\logs\windows_mcp_install_*.log
   ```

2. **Claude Desktop logs**:
   ```
   %APPDATA%\Claude\logs\
   ```

3. **Test results**:
   - Screenshot of successful test
   - System state output
   - Any error messages

**Save to**: `logs/LOG_MCP_WINDOWS_MCP_VERIFICATION.md`

---

## 🎯 Next Steps After Installation

**1. Update CAPABILITIES_MATRIX**:
   - Change status: Planned → Verified (or Partial)
   - Add evidence links
   - Document limitations

**2. Create Verification Log**:
   - Test results
   - Actual vs expected capabilities
   - Performance notes

**3. Establish Operating Procedures**:
   - Which tools require approval
   - Monitoring approach
   - Incident response

---

## 📚 References

**Design Document**: `docs/MCP_WINDOWS_MCP_DESIGN.md`  
**Installation Script**: `scripts/install_windows_mcp.ps1`  
**Official Repo**: https://github.com/CursorTouch/Windows-MCP  
**MCP Docs**: https://modelcontextprotocol.io/

---

## 🤝 Support

**If you encounter issues**:

1. Check this playbook's troubleshooting section
2. Review installation logs
3. Check Claude Desktop logs
4. Review Windows-MCP GitHub issues
5. Ask Claude for help (before installation completes)

---

**Installation Playbook Version**: 1.0  
**Created**: 2025-11-14  
**Status**: Ready for execution with approval  
**Risk Level**: 🔴 HIGH - Proceed with caution
