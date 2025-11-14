# MCP Meta-Installer Design

**Created**: 2025-11-14  
**Status**: Phase 1 Design  
**Purpose**: Generic pattern for adding new MCP servers with full audit and approval

---

## 🎯 Objective

Create a standardized, auditable, and approval-gated process for expanding Claude's capabilities through MCP server integration. Enable maximum autonomy within strict safety boundaries.

**Core Principle**: Claude can prepare everything (design, scripts, configs, evidence), but requires explicit approval for any OS-level changes.

---

## 🏗️ Current MCP Landscape

### Active MCP Servers (from CAPABILITIES_MATRIX.md)

1. **PowerShell MCP** (ps_exec)
   - Location: `C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\ps_exec\`
   - Status: ✅ Verified - 10 whitelisted commands
   - Limitations: No arbitrary script execution

2. **GitHub MCP**: ✅ Verified - Full repo operations via PAT

3. **Google MCPs**: ✅ Verified - Gmail, Drive, Calendar (read-only, OAuth 2.0)

4. **Canva MCP**: ✅ Verified - Design operations

5. **Filesystem MCP**: ✅ Verified - Read/write in allowed directories

6. **Web Search/Fetch**: ✅ Verified - Brave search, URL fetch

---

## 🚧 Constraints & Boundaries

### What Claude CAN Do ✅

**Design & Planning**:
- Analyze MCP requirements
- Design installation approach
- Create configuration snippets
- Write installation scripts (NOT execute)
- Document everything

**File Operations**:
- Read existing configs via filesystem tools
- Create new files in GitHub repo
- Commit to GitHub
- Update CAPABILITIES_MATRIX.md

**Information Gathering**:
- Detect installed tools (via ps_exec whitelisted commands)
- Read documentation (web_search, web_fetch)
- Analyze dependencies

### What Claude CANNOT Do ❌ (Without Approval)

**OS-Level Changes**:
- Install npm/pip packages
- Modify system PATH
- Run installation scripts
- Restart Claude Desktop
- Edit `claude_desktop_config.json` directly

**Network Operations**:
- Download executables
- Install from external sources
- Direct API calls requiring new auth

### Critical Constraint: Claude Desktop Config

**Path**: `%APPDATA%\Claude\claude_desktop_config.json`

- Claude **CANNOT** modify this file directly (not in allowed directories)
- Claude **CAN** prepare exact snippet to add
- **אור MUST** approve and apply changes manually
- Any MCP addition requires Claude Desktop restart (only אור can do this)

---

## 📋 Generic MCP Addition Pattern

### Phase 1: Discovery & Design

**Input**: MCP server name or requirement (e.g., "Windows-MCP", "mouse control")

**Claude's Actions**:
1. **Research** (web_search, web_fetch):
   - Find MCP on GitHub, npm, PyPI
   - Read official documentation
   - Check compatibility

2. **Analyze**:
   - Installation method (npm, pip, binary)
   - Dependencies (Node.js version, Python, OS requirements)
   - Configuration format
   - Capabilities offered
   - Security implications (permissions, access level)

3. **Create Design Document**:
   - File: `docs/MCP_<NAME>_DESIGN.md`
   - Include: source, installation steps, config snippet, capabilities, risks

**Output**:
- Design document committed to GitHub
- No system changes
- Status in CAPABILITIES_MATRIX: ⚠️ Planned

---

### Phase 2: Preparation

**Claude's Actions**:

1. **Create Installation Script**:
   ```
   File: scripts/install_mcp_<NAME>.ps1
   Contents: All installation commands
   Verification: Installation success checks
   Execution: NOT executed, just created
   ```

2. **Create Config Snippet**:
   ```
   File: config/snippets/mcp_<NAME>_config.json
   Contents: Exact JSON to add to claude_desktop_config.json
   Format: Properly formatted, ready to copy-paste
   ```

3. **Create Evidence Log**:
   ```
   File: logs/LOG_MCP_<NAME>_INSTALLATION.md
   Contents: 
   - Complete installation process
   - Expected outcomes
   - Risks and mitigation
   - Rollback procedure
   ```

4. **Update CAPABILITIES_MATRIX.md**:
   - Add new section for MCP
   - Status: ⚠️ Planned
   - Evidence: Links to design, scripts, logs
   - Gaps: Clear about what's NOT implemented yet

**Output**:
- All files committed to GitHub
- Ready for approval
- No system changes

---

### Phase 3: Approval Request

**Claude presents**:

```markdown
## MCP Addition Request: <NAME>

**Status**: Ready for approval

**What will be installed**:
- Package: <source/name>
- Method: <npm install -g @x/y OR pip install x>
- Location: <expected installation path>

**What it enables**:
- Capability 1 (Status: Planned)
- Capability 2 (Status: Planned)
- Capability 3 (Status: Planned)

**Security considerations**:
- Permission level: <read-only / read-write / system control>
- Access scope: <what can it touch>
- Risk level: 🟢 Low / 🟡 Medium / 🔴 High

**Files prepared** (in GitHub):
- scripts/install_mcp_<NAME>.ps1
- config/snippets/mcp_<NAME>_config.json
- logs/LOG_MCP_<NAME>_INSTALLATION.md
- docs/MCP_<NAME>_DESIGN.md

**Required actions from אור**:
1. Review installation script: `scripts/install_mcp_<NAME>.ps1`
2. Execute: `powershell -File scripts/install_mcp_<NAME>.ps1`
3. Copy snippet from `config/snippets/mcp_<NAME>_config.json`
4. Add to: `%APPDATA%\Claude\claude_desktop_config.json`
5. Restart Claude Desktop
6. Confirm "MCP connected" or similar

**Approval required**: מאושר לביצוע? (YES/NO)
```

---

### Phase 4: Post-Installation Verification

**After אור approves and executes**:

1. **Verification**:
   - Claude attempts to use new MCP
   - Tests basic capabilities
   - Documents actual behavior vs expected

2. **CAPABILITIES_MATRIX Update**:
   ```
   Status: ⚠️ Planned → ✅ Verified OR 🟡 Partial
   Limitations: Document discovered gaps
   Evidence: Link to verification log
   ```

3. **Create Verification Log**:
   ```
   File: logs/LOG_MCP_<NAME>_VERIFICATION.md
   Contents:
   - Test results
   - Actual vs expected capabilities
   - Performance notes
   - Issues encountered
   ```

---

## 🎯 Example Target: Windows OS Control MCP

### Research Phase

**Potential MCPs for Windows Control**:
1. **windows-mcp** (https://github.com/3choff/windows-mcp) - if exists
2. **MCPControl** - need to verify if this is real
3. **computer-use MCP** - Anthropic's reference implementation
4. **Custom ps_exec expansion** - extend existing server

**Typical OS Control Capabilities**:
- Window management (list, focus, resize, close)
- Mouse control (move, click, drag)
- Keyboard simulation (type, shortcuts)
- Process management (list, start, stop)
- Screenshot capture
- Clipboard access
- System information

### Security Analysis for OS Control

**Risk Level**: 🔴 **HIGH**

**Why High Risk**:
- ⚠️ Mouse/keyboard control can interact with ANY application
- ⚠️ Process control can start/stop critical programs
- ⚠️ Window management can manipulate sensitive UI
- ⚠️ Screenshot can capture confidential information

**Required Mitigations**:
1. **Least Privilege**: Only enable essential capabilities
2. **Approval Per Action Type**: Separate approval for each dangerous operation
3. **Audit Trail**: Log every OS interaction
4. **Quick Disable**: Ability to remove MCP immediately if needed
5. **Sandboxing**: If possible, limit to specific applications

**Recommendation**: Start with **read-only OS info** (windows list, process list) before enabling control operations

---

## 📊 Risk Matrix

| MCP Type | Examples | Risk | Approval | Audit |
|----------|----------|------|----------|-------|
| **Read-only data** | Weather, stocks | 🟢 Low | Design only | Standard |
| **Read-only APIs** | Gmail (current) | 🟢 Low | Design only | Standard |
| **Read-write APIs** | Drive edit | 🟡 Medium | Per capability | Enhanced |
| **OS Info** | Process list, window list | 🟡 Medium | Design + Install | Enhanced |
| **OS GUI Control** | Mouse, keyboard, window | 🔴 High | Per action type | Full |
| **Process Control** | Start/stop apps | 🔴 High | Per operation | Full |
| **System Modification** | Registry, services | 🔴 Critical | Per change | Maximum |

---

## 🔄 Self-Expansion Loop

### Vision

Claude can:
1. **Identify gap**: "I need to control windows to help with X task"
2. **Research solution**: Find appropriate MCP
3. **Prepare package**: Scripts + configs + docs
4. **Request approval**: Present complete plan to אור
5. **Verify installation**: Test new capabilities
6. **Update truth**: CAPABILITIES_MATRIX reflects reality

### Metrics

**Before Meta-Installer**:
- MCP additions: Manual, ad-hoc, undocumented
- Approval: Implicit or unclear
- Audit trail: Partial or missing
- Rollback: Difficult

**After Meta-Installer**:
- MCP additions: Standardized, documented, tracked
- Approval: Explicit with full transparency
- Audit trail: Complete (GitHub commits)
- Rollback: Clear procedure

---

## 🚀 Implementation Roadmap

### Phase 1: Pattern Design ✅ (This Document)

**Deliverables**:
- ✅ Design document
- ✅ Generic pattern defined
- ✅ Risk matrix established
- ✅ Templates created
- ⏳ First target identified (requires research)

### Phase 2: First MCP Implementation ⏳

**Target**: TBD (Windows control OR other based on priority)

**Deliverables**:
- Design doc for specific MCP
- Installation script
- Config snippet
- Evidence logs
- CAPABILITIES_MATRIX update (Status: Planned)

**Claude's Work**: 100% (all files prepared)  
**אור's Work**: Review + Execute + Restart

### Phase 3: Installation & Approval ⏳

**Owner**: אור

**Tasks**:
1. Review all materials in GitHub
2. Execute installation script
3. Apply config to claude_desktop_config.json
4. Restart Claude Desktop
5. Confirm MCP appears in logs/UI

### Phase 4: Verification & Documentation ⏳

**Deliverables**:
- Verification tests
- CAPABILITIES_MATRIX update (Status: Verified/Partial)
- Lessons learned
- Pattern refinement if needed

---

## ⚠️ Critical Safety Rules

### Rule 1: Never Assume Capability

Claude MUST NOT:
- ❌ Assume it can modify claude_desktop_config.json
- ❌ Assume it can restart Claude Desktop
- ❌ Assume it can install packages
- ❌ Assume any OS-level permission
- ❌ Claim capabilities not verified

### Rule 2: Full Transparency

Every action that affects the system MUST:
- ✅ Be documented in advance
- ✅ Be presented for approval
- ✅ Include clear "what will change"
- ✅ Provide rollback procedure
- ✅ List all risks

### Rule 3: Fail Safe

If anything is unclear:
- 🛑 STOP immediately
- 📝 Document the blocker
- ❓ Ask for clarification
- ⏸️ Do NOT proceed with assumptions

### Rule 4: Evidence-Based Only

CAPABILITIES_MATRIX updates MUST:
- ✅ Be based on actual test results
- ✅ Include evidence (logs, commits, tests)
- ❌ Never claim unverified capabilities
- 🏷️ Clearly mark: Planned vs Partial vs Verified

---

## 📝 File Templates

### Installation Script Template

```powershell
# scripts/install_mcp_<NAME>.ps1
# Purpose: Install <NAME> MCP server
# Created: <DATE>
# Status: NOT EXECUTED - Requires approval from אור

Write-Output "=== <NAME> MCP Installation ==="
Write-Output "WARNING: This script will install <NAME>"
Write-Output "Press Ctrl+C to cancel, or"
pause

# 1. Prerequisites check
Write-Output ""
Write-Output "Step 1: Checking prerequisites..."

$nodeVersion = node --version 2>$null
if (-not $nodeVersion) {
    Write-Error "❌ Node.js not found. Install from https://nodejs.org"
    exit 1
}
Write-Output "✅ Node.js: $nodeVersion"

# 2. Installation
Write-Output ""
Write-Output "Step 2: Installing <NAME>..."
npm install -g <package-name>

if ($LASTEXITCODE -ne 0) {
    Write-Error "❌ Installation failed"
    exit 1
}

# 3. Verification
Write-Output ""
Write-Output "Step 3: Verifying installation..."
$installed = npm list -g --depth=0 2>$null | Select-String "<package-name>"

if ($installed) {
    Write-Output "✅ Installation successful"
} else {
    Write-Error "❌ Verification failed"
    exit 1
}

# 4. Next steps
Write-Output ""
Write-Output "========================================="
Write-Output "✅ Installation complete!"
Write-Output ""
Write-Output "Next steps:"
Write-Output "1. Open: %APPDATA%\Claude\claude_desktop_config.json"
Write-Output "2. Add snippet from: config/snippets/mcp_<NAME>_config.json"
Write-Output "3. Restart Claude Desktop"
Write-Output "4. Verify MCP is connected"
Write-Output "========================================="
```

### Config Snippet Template

```json
{
  "mcpServers": {
    "<server-name>": {
      "command": "node",
      "args": [
        "C:\\Users\\edri2\\AppData\\Roaming\\npm\\node_modules\\<package>\\dist\\index.js"
      ],
      "env": {
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

---

## 📚 References

**MCP Specification**: https://spec.modelcontextprotocol.io/  
**MCP SDKs**: https://github.com/modelcontextprotocol  
**Claude Desktop**: https://claude.ai/download

**Existing Custom MCPs**:
- ps_exec: `C:\Users\edri2\Work\AI-Projects\Claude-Ops\mcp-servers\ps_exec\`

---

## 🎯 Success Criteria

### Pattern Design Success ✅

- ✅ Standardized process documented
- ✅ Safety rules established
- ✅ Risk matrix defined
- ✅ Templates created
- ✅ Approval flow clear

### Per-MCP Implementation Success

- ✅ Design document complete
- ✅ Installation script created (NOT executed)
- ✅ Config snippet validated
- ✅ Evidence logs written
- ✅ CAPABILITIES_MATRIX updated (Planned)
- ✅ Approval obtained from אור
- ✅ Installation successful
- ✅ Capabilities verified
- ✅ CAPABILITIES_MATRIX updated (Verified/Partial)

---

## 🔮 Next Steps

### Immediate (This Session)

1. ✅ Complete this design document
2. ⏳ Commit to GitHub
3. ⏳ Update CAPABILITIES_MATRIX with meta-installer capability
4. ⏳ Await direction on first MCP target

### Next Session (If Prioritized)

1. Research specific MCP (Windows control or other)
2. Create complete implementation package
3. Request approval
4. Guide installation
5. Verify and document

---

**Status**: Design Complete ✅  
**Implementation**: Awaiting first target selection  
**Approval**: Required before any installation  
**Safety**: Maximum (all rules in place)
