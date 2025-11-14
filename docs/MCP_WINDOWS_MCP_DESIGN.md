# Windows-MCP Design Document

**Created**: 2025-11-14  
**Target**: CursorTouch/Windows-MCP  
**Status**: Phase 2 - Installation Package Ready  
**Risk Level**: 🔴 HIGH (OS Control)

---

## 🎯 Project Overview

**Repository**: https://github.com/CursorTouch/Windows-MCP  
**Author**: Jeomon George (CursorTouch)  
**License**: MIT  
**Purpose**: Lightweight MCP server for complete Windows OS automation

**What It Does**:
Windows-MCP enables AI agents to directly control the Windows operating system through a rich set of automation tools. It provides mouse, keyboard, window management, application control, and system interaction capabilities.

---

## 🛠️ Capabilities

### Mouse & Keyboard Control
- **Click-Tool**: Click at specific coordinates
- **Type-Tool**: Type text (with optional clear)
- **Drag-Tool**: Drag from point A to point B
- **Move-Tool**: Move mouse pointer
- **Scroll-Tool**: Vertical/horizontal scrolling
- **Shortcut-Tool**: Keyboard shortcuts (Ctrl+C, Alt+Tab, etc.)
- **Key-Tool**: Press single keys

### Window & Application Management
- **Launch-Tool**: Launch apps from Start menu
- **Resize-Tool**: Move/resize application windows
- **State-Tool**: Get system state (active apps, UI elements, screenshot)
- **Screenshot-Tool**: Capture desktop screenshot

### System Operations
- **Shell-Tool**: Execute PowerShell commands
- **Clipboard-Tool**: Copy/paste operations
- **Wait-Tool**: Pause execution
- **Scrape-Tool**: Scrape webpage information

---

## 📋 Requirements

### System Requirements
- **OS**: Windows 7/8/8.1/10/11
- **Language**: English as default Windows language (CRITICAL)
  - OR disable Launch-Tool and Resize-Tool for non-English

### Software Requirements
- **Python**: 3.13+ (latest version required by Windows-MCP)
- **UV**: Package manager from Astral (`pip install uv`)
- **DXT**: Desktop Extension tool from Anthropic (`npm install -g @anthropic-ai/dxt`)
- **Node.js**: Required for DXT (v18+)

### Claude Desktop
- Anthropic Claude Desktop app
- Extensions capability enabled

---

## 🚨 Security & Risk Analysis

### Risk Level: 🔴 **CRITICAL HIGH**

**Why Critical**:
1. ⚠️ **Full OS Control**: Can click/type anywhere, including sensitive apps
2. ⚠️ **Process Control**: Shell-Tool can execute ANY PowerShell command
3. ⚠️ **No Sandboxing**: Direct system access, no isolation
4. ⚠️ **Screenshot Capture**: Can capture confidential information
5. ⚠️ **Application Launch**: Can start any installed program

**Specific Dangerous Capabilities**:
- **Shell-Tool**: Can execute `Restart-Computer`, delete files, modify registry
- **Launch-Tool**: Can open Task Manager, CMD, PowerShell ISE
- **Click-Tool + Type-Tool**: Can interact with UAC dialogs, password fields
- **Clipboard-Tool**: Can access clipboard with passwords/sensitive data

### Mitigation Strategy

**Phase 1 (Current - Installation Only)**:
- ✅ Installation only (no execution)
- ✅ Full documentation of risks
- ✅ Explicit approval required from אור
- ✅ All actions will be logged

**Phase 2 (Post-Installation - Testing)**:
- 🔄 Start with read-only operations (State-Tool, Screenshot-Tool)
- 🔄 Gradual enablement of control operations
- 🔄 Approval per action type from אור
- 🔄 Complete audit log of all operations

**Phase 3 (Operational - Controlled Use)**:
- 🔄 Disable dangerous tools if not needed (Shell-Tool, Launch-Tool)
- 🔄 Create safety guardrails (restricted command lists)
- 🔄 Emergency disable procedure documented
- 🔄 Approval gate for every high-risk operation

---

## 📦 Installation Methods

Windows-MCP supports two installation paths:

### Method 1: Desktop Extension (DXT) - ✅ RECOMMENDED

**Advantages**:
- ✅ Integrated with Claude Desktop Extensions UI
- ✅ Easy enable/disable via Settings
- ✅ Cleaner architecture
- ✅ Better for managed deployments

**Process**:
1. Clone repository
2. Build DXT: `npx @anthropic-ai/dxt pack`
3. Install via Claude Desktop → Settings → Extensions
4. Restart Claude Desktop

### Method 2: Traditional MCP Server

**Advantages**:
- ✅ Works with any MCP client (not just Claude Desktop)
- ✅ More manual control

**Process**:
1. Clone repository
2. Install dependencies: `uv sync`
3. Add config to `claude_desktop_config.json`
4. Restart Claude Desktop

**Our Choice**: Method 1 (DXT) for ease of management

---

## 🔧 Detailed Installation Steps

### Prerequisites Setup

```powershell
# 1. Verify Python 3.13+
python --version
# If not 3.13+, install from python.org

# 2. Install UV package manager
pip install uv

# 3. Verify Node.js (for DXT)
node --version
# If not installed, get from nodejs.org

# 4. Install DXT globally
npm install -g @anthropic-ai/dxt
```

### Repository Setup

```powershell
# Clone Windows-MCP
git clone https://github.com/CursorTouch/Windows-MCP.git
cd Windows-MCP

# Build Desktop Extension
npx @anthropic-ai/dxt pack
# This creates a .dxt file in the current directory
```

### Claude Desktop Installation

1. Open Claude Desktop application
2. Navigate to: Settings → Extensions
3. Click: "Install Extension"
4. Browse to the `.dxt` file created above
5. Click: "Install"
6. **Restart Claude Desktop completely**

### Post-Installation Verification

```powershell
# Check Claude Desktop logs for connection
# Look for: "Windows-MCP server connected" or similar

# Test basic functionality:
# In Claude Desktop, try: "Take a screenshot of my desktop"
# Or: "What applications are currently running?"
```

---

## 📁 Repository Structure

```
Windows-MCP/
├── src/
│   └── windows_mcp/
│       ├── __init__.py
│       ├── server.py          # Main MCP server
│       ├── tools/              # Individual tool implementations
│       │   ├── click.py
│       │   ├── type.py
│       │   ├── shell.py       # ⚠️ DANGEROUS
│       │   └── ... (12+ tools)
│       └── utils/              # Helper utilities
├── manifest.json               # DXT extension manifest
├── pyproject.toml              # Python dependencies
├── README.md                   # Official documentation
└── LICENSE                     # MIT License
```

---

## 🎯 Operational Considerations

### Language Requirement

**CRITICAL**: Windows **MUST** be in English OR disable Launch/Resize tools

**Why**:
- Launch-Tool searches Start menu by application name
- Resize-Tool uses window titles
- Non-English Windows will cause failures

**Solutions**:
1. ✅ Switch Windows display language to English (Settings → Language)
2. ✅ Disable Launch-Tool and Resize-Tool in manifest
3. ✅ Use only language-independent tools (Click, Type, State, etc.)

### Performance Characteristics

**Latency**: 0.7 - 2.5 seconds between actions

**Affected By**:
- Number of active applications (more apps = slower)
- System load (CPU, memory)
- LLM inference speed
- Tool complexity (State-Tool slower than Click-Tool)

### Known Limitations

- ⚠️ Cannot select specific text portions within paragraphs (a11y tree limitation)
- ⚠️ Type-Tool not optimized for programming in IDEs (types entire content)
- ⚠️ Relies on Windows accessibility API (a11y tree)

---

## 🔄 Integration with Existing Infrastructure

### With Current MCP Servers

**PowerShell MCP** (ps_exec):
- Windows-MCP provides **superset** of capabilities
- Can **replace** ps_exec for GUI operations
- Can **complement**: ps_exec for safe system info, Windows-MCP for GUI

**Recommendation**: Keep both, use appropriately
- ps_exec: System info, safe operations
- Windows-MCP: GUI automation, window control

### With GitHub Actions & Job Pattern

**Potential Uses**:
- Capture State-Tool output as evidence
- Execute automation workflows via Shell-Tool
- Screenshot-based verification
- Integration with existing Job Pattern (future)

### With CAPABILITIES_MATRIX

**Adds**:
- **New Layer**: OS GUI Control
- **Completes**: "Corner 2" - Full computer control capability
- **Enables**: Restart operations (via Shell-Tool with approval)

---

## 📋 Testing Strategy (Post-Installation)

### Phase 1: Read-Only Operations

**Tools to Test**:
- ✅ State-Tool: `"What apps are running?"`
- ✅ Screenshot-Tool: `"Take a screenshot"`

**Goal**: Verify connectivity, no system changes

**Risk**: 🟢 Low

---

### Phase 2: Safe Interactions

**Tools to Test**:
- ✅ Click-Tool: Click on desktop, safe areas
- ✅ Move-Tool: Move mouse cursor
- ✅ Wait-Tool: Pause execution

**Goal**: Test basic control, reversible operations

**Risk**: 🟡 Medium

---

### Phase 3: Application Control

**Tools to Test**:
- ✅ Launch-Tool: Open safe apps (Notepad, Calculator)
- ✅ Resize-Tool: Move/resize windows
- ✅ Clipboard-Tool: Copy/paste operations
- ✅ Type-Tool: Type in Notepad

**Goal**: Full GUI automation capability

**Risk**: 🟡 Medium-High

---

### Phase 4: System Operations (HIGH CAUTION)

**Tools to Test**:
- ⚠️ Shell-Tool: Execute **safe** PowerShell commands only
- ⚠️ Shortcut-Tool: System shortcuts (with care)
- ⚠️ Drag-Tool: Complex interactions

**Goal**: Full capability verification

**Risk**: 🔴 High

**Requirement**: Explicit approval from אור per command type

---

## 🚫 Prohibited Operations (Without Approval)

### DO NOT Execute:

❌ **Shell-Tool without restrictions**:
- No `Restart-Computer`
- No file deletion
- No registry modification
- No system settings changes

❌ **Launch dangerous apps**:
- No Task Manager
- No Command Prompt
- No PowerShell ISE
- No system utilities

❌ **Interact with sensitive targets**:
- No UAC dialogs
- No password fields
- No banking/financial apps
- No email clients (unless approved)

❌ **Capture sensitive information**:
- No screenshots of passwords
- No clipboard with credentials
- No confidential documents

---

## ✅ Success Criteria

### Installation Success:
- ✅ Python 3.13+ verified
- ✅ UV and DXT installed
- ✅ Repository cloned
- ✅ DXT file built successfully
- ✅ Extension installed in Claude Desktop
- ✅ Server appears in Extensions list
- ✅ No errors in Claude Desktop logs

### Connection Success:
- ✅ Windows-MCP listed as connected
- ✅ Tools appear in Claude's available tools
- ✅ No connection errors

### Functional Success:
- ✅ State-Tool returns system information
- ✅ Screenshot-Tool captures desktop
- ✅ Click-Tool moves cursor
- ✅ Type-Tool types text

### Safety Success:
- ✅ All operations logged
- ✅ No unauthorized system changes
- ✅ Can disable immediately if needed
- ✅ CAPABILITIES_MATRIX accurate

---

## 📚 References

**Official Repository**: https://github.com/CursorTouch/Windows-MCP  
**Author**: Jeomon George (@Jeomon)  
**License**: MIT  
**MCP Protocol**: https://modelcontextprotocol.io/  
**Claude Desktop**: https://claude.ai/download  
**UV Package Manager**: https://github.com/astral-sh/uv  
**DXT Documentation**: https://github.com/anthropics/anthropic-desktop-integration

---

## 🎯 Implementation Status

### ✅ Complete:
- Design document (this file)
- Capability analysis
- Risk assessment
- Installation strategy

### ⏳ Next (Phase 2):
- Installation script creation
- Config snippet preparation
- Installation playbook writing
- Evidence log creation
- CAPABILITIES_MATRIX update

### ⏳ Awaiting Approval:
- Script execution
- Extension installation
- Claude Desktop restart
- Verification testing

---

**Design Status**: ✅ Complete  
**Risk Level**: 🔴 Critical High  
**Recommendation**: Proceed with caution, full approval required  
**Next**: Create installation package
