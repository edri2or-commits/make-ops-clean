# GPT-CEO Routing Cheat Sheet

**Purpose**: Quick reference for GPT-CEO to route operations based on CAPABILITIES_MATRIX v1.3.0  
**Created**: 2025-11-18  
**Version**: 1.0  
**Status**: ✅ Active

---

## 🎯 How to Use This Sheet

1. **User makes request** → Identify domain (GitHub, Google, Local, etc.)
2. **Check section below** → Find capability status
3. **Route accordingly**:
   - ✅ **Ready Now** → Execute via Claude
   - 📋 **Design Phase** → Create playbook
   - 🚫 **Not Available** → Explain limitation

---

## 📂 GitHub Operations

### ✅ Ready Now (Execute Immediately)

| Operation | GPT-CEO Ready? | Approval? | Tool/Method |
|-----------|----------------|-----------|-------------|
| **Read repos/files** | Yes | No | Claude MCP → GitHub API |
| **Search code** | Yes | No | Claude MCP → GitHub API |
| **List commits** | Yes | No | Claude MCP → GitHub API |
| **Create DOCS files** | Yes | No | Claude MCP → GitHub API |
| **Update STATE files** | Yes | No | Claude MCP → GitHub API |
| **Create issues** | Yes | No | Claude MCP → GitHub API |
| **Comment on issues** | Yes | No | Claude MCP → GitHub API |

**Pattern**: Direct execution via Claude  
**Reference**: FLOW_001 → Pattern A (Simple File Update)

### 📋 Design Phase (Create Playbook/PR)

| Operation | GPT-CEO Ready? | Approval? | Action |
|-----------|----------------|-----------|--------|
| **Update code files** | Yes | Yes | Create PR → Await approval |
| **Update workflows** | Planned | Yes | Design → PR |
| **Trigger workflows** | Planned | Depends | Design orchestration |
| **Create branches** | Planned | No | Design first |
| **Merge PRs** | Planned | Yes | Design approval flow |
| **Fork repos** | Planned | No | Design strategy |

**Pattern**: Design document → PR → Approval  
**Reference**: FLOW_001 → Pattern B (Code Change via PR)

### 🚫 Not Available

- None (GitHub fully accessible for read/write via MCP)

---

## 📧 Google Operations

### ✅ Ready Now (Read-Only)

| Service | Operations | GPT-CEO Ready? | Approval? | Tool |
|---------|-----------|----------------|-----------|------|
| **Gmail** | Search, Read threads, List | Yes | No | Claude MCP → Gmail API |
| **Drive** | Search, Fetch docs, List folders | Yes | No | Claude MCP → Drive API |
| **Calendar** | List, Search, Find free time | Yes | No | Claude MCP → Calendar API |

**Pattern**: Direct execution via Claude MCP  
**Reference**: FLOW_002 → Pattern A (Read Operation)

### 📋 Design Phase (Write Operations - Awaiting OAuth)

| Service | Operations | GPT-CEO Ready? | Approval? | Blocker |
|---------|-----------|----------------|-----------|---------|
| **Gmail** | Send, Draft, Labels | Planned | Yes/Depends | OAuth scopes |
| **Drive** | Create, Edit, Share | Planned | Depends | OAuth scopes |
| **Calendar** | Create/Edit events | Planned | Depends | OAuth scopes |
| **Sheets** | All operations | Planned | Depends | MCP not configured |
| **Docs** | All operations | Planned | Depends | MCP not configured |

**Pattern**: Create playbook → Wait for OAuth expansion  
**Reference**: FLOW_002 → Pattern B (Write Operation Design)

**Existing Templates**:
- `DOCS/PILOT_GMAIL_SEND_FLOW.md`
- `DOCS/PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md`
- `DOCS/PILOT_CALENDAR_FOCUS_EVENT_FLOW.md`

### 🚫 Not Available

- Direct API calls (network restrictions)
- Sheets/Docs (MCP server not configured)

---

## 💻 Local Desktop Operations

### ✅ Available via Claude (GPT Cannot Direct)

| Operation | GPT-CEO Ready? | Action |
|-----------|----------------|--------|
| **Read files** | No* | Request Claude to read & report |
| **Write files** | No* | Request Claude to write & confirm |
| **List directory** | No* | Request Claude to list & report |
| **PowerShell commands** | No* | Request Claude to execute (11 whitelisted) |
| **Screenshot** | No* | Request Claude to capture & provide |

**Note**: GPT-CEO cannot execute directly (lacks MCP access), but can request Claude to perform and report results.

**Pattern**:
```
GPT-CEO → Claude: "Please take screenshot and describe what you see"
Claude: [Executes ps_exec screenshot] → Returns description
GPT-CEO → Or: [Presents analysis based on Claude's report]
```

**Available PowerShell Commands** (via Claude):
1. `dir`, `type`, `test_path`
2. `whoami`, `get_process`, `get_service`
3. `get_env`, `test_connection`, `get_item_property`
4. `measure_object`, `screenshot`

### 🚫 Not Available

- Direct filesystem access by GPT (architectural limitation)
- Arbitrary PowerShell/Python script execution (security constraint)

---

## ☁️ Cloud Run / github-executor-api

### ⚠️ Runtime Unverified (Do Not Rely On)

| Service | Endpoint | Status | GPT-CEO Ready? | Action |
|---------|----------|--------|----------------|--------|
| **github-executor-api** | `/` (health) | 🔍 Unverified | Yes* | DO NOT USE yet |
| **github-executor-api** | `/github/update-file` | 🔍 Unverified | Yes* | DO NOT USE yet |

**Status**: Code exists, deployment unverified  
**Known Issues**: Typo in Accept header (line 37)  
**Recommendation**: Use direct GitHub MCP instead

**When to Use**: ONLY after:
1. Deployment verified
2. Typo fixed
3. Testing completed
4. CAPABILITIES_MATRIX updated to ✅ Verified

**Current Alternative**: Direct GitHub operations via Claude MCP (fully working)

---

## 🔄 GitHub Actions / Workflows

### 📋 Available via Design (Claude Builds, Actions Run)

| From | To | Status | GPT-CEO Ready? | Pattern |
|------|----|----|----------------|---------|
| **Actions** | Google Sheets | ✅ Verified | Planned | Claude designs workflow → Or approves → Runs autonomously |
| **Actions** | GCP APIs | 🟡 Partial | Planned | WIF configured, needs testing |
| **Actions** | Secret Manager | 🟡 Partial | Planned | WIF configured, needs verification |

**Pattern**: 
- GPT-CEO designs automation
- Claude creates workflow file
- Or approves (if CLOUD_OPS_HIGH)
- Workflow runs autonomously or on trigger

**Note**: 68 workflows exist in `.github/workflows/` - can reference/modify

---

## 🚦 Quick Decision Matrix

```
┌─────────────────────────────────────────────────────────────┐
│ User Request                                                 │
└────────────┬────────────────────────────────────────────────┘
             ↓
    ┌────────┴────────┐
    │                 │
    ↓                 ↓
GitHub?          Google?           Local?        Cloud Run?
    │                 │                │              │
    ↓                 ↓                ↓              ↓
Check CAPS        Check CAPS      Request        DO NOT USE
Section 1         Section 3        Claude         (Unverified)
    │                 │                │              │
    ↓                 ↓                ↓              │
┌───┴───┐        ┌───┴───┐       Report Back        │
│       │        │       │            │              │
↓       ↓        ↓       ↓            │              │
Read   Write    Read   Write          │              │
│       │        │       │            │              │
↓       ↓        ↓       ↓            │              │
Yes    Check    Yes   Planned         │              │
Execute Type   Execute Design         │              │
│       │        │       │            │              │
└───────┴────────┴───────┴────────────┴──────────────┘
                      ↓
              Execute / Design / Report
```

---

## 📋 Approval Quick Reference

### ✅ No Approval Needed (OS_SAFE)
- All read operations
- DOCS/, logs/, STATE file changes
- GitHub issues/comments
- Personal file organization
- Design documents/playbooks

### ⚠️ Depends on Context
- GitHub file updates (DOCS=No, Code=Yes)
- Google file creation (Personal=No, Shared=Yes)
- Calendar events (Small=No, Large meetings=Yes)
- Workflow triggers (Read-only=No, State-changing=Yes)

### 🛑 Always Requires Approval (CLOUD_OPS_HIGH)
- Code/workflow changes
- Email sending (external)
- File sharing (external)
- PR merges
- Infrastructure changes
- Secret/credential operations

**Approval Phrase**: Or says "מאשר" (Hebrew) or explicit English approval

---

## 🎓 Best Practices for GPT-CEO

### 1. Always Check CAPABILITIES_MATRIX First
```
Before ANY operation:
1. Reference CAPABILITIES_MATRIX.md
2. Find exact capability
3. Check GPT-CEO Ready? column
4. Route accordingly
```

### 2. Be Transparent About Status
```
✅ GOOD: "I can do this now via GitHub MCP"
✅ GOOD: "This is designed but awaiting OAuth expansion"
❌ BAD: "I'll do that" (when status is Planned)
```

### 3. Use Existing Patterns
```
Don't reinvent:
- FLOW_001 for GitHub
- FLOW_002 for Google
- PILOT_* docs for templates
```

### 4. Design Over Wait
```
If Planned:
1. Create playbook now
2. Present to Or
3. Explain timeline
4. Offer alternatives
```

### 5. Leverage Claude for Local Ops
```
GPT-CEO cannot access local files, but:
1. Request Claude to read/write/execute
2. Claude reports back
3. GPT-CEO presents analysis to Or
```

---

## 📚 References

**MUST READ**:
- `CAPABILITIES_MATRIX.md` v1.3.0 - Single source of truth
- `FLOW_001_GPT_CEO_GITHUB_ROUTING.md` - GitHub operations
- `FLOW_002_GPT_CEO_GOOGLE_ROUTING.md` - Google operations

**Supporting Docs**:
- `logs/LOG_CAPABILITIES_MATRIX_ROLE_FIELDS_UPDATE_V2.md` - Role field definitions
- `DOCS/PILOT_*.md` - Google operation templates

**For Clarification**:
- Ask Or when unsure about approval requirements
- Reference CAPABILITIES_MATRIX for technical constraints
- Check FLOW docs for execution patterns

---

## 🔄 Version History

### v1.0 (2025-11-18)
- Initial creation
- Based on CAPABILITIES_MATRIX v1.3.0
- Covers: GitHub, Google, Local, Cloud Run
- Includes quick decision matrix
- Approval reference guide

---

**Maintained by**: Claude (via GPT-CEO instructions)  
**Last Updated**: 2025-11-18  
**Next Review**: When CAPABILITIES_MATRIX updates
