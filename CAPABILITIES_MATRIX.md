# CAPABILITIES MATRIX (SSOT)

**Single Source of Truth for Claude's Operational Capabilities**

**Created**: 2025-11-14  
**Last Updated**: 2025-11-18  
**Version**: 1.3.2 (GitHub Executor API v1 - Planned)

---

## 🎯 Purpose

This is the **master reference** for all capabilities across the Claude-Ops system. Every chat session, automation, and tool must reference this document to understand what Claude can and cannot do.

**Update Protocol**: When a new capability is added, this file MUST be updated before the capability is considered operational.

---

## ⚡ GLOBAL EXECUTION MODEL

**CRITICAL CONTRACT**

```
┌─────────────────────────────────────────────────────┐
│                   Or (אור)                           │
│                                                      │
│  Role: Intent + Approval ONLY                       │
│  - Defines objectives ("enable Google full access") │
│  - Approves HIGH RISK operations                    │
│  - Clicks OAuth consent (when required by provider) │
│                                                      │
│  NEVER:                                              │
│  ❌ Opens consoles (GCP, Azure, AWS, etc.)          │
│  ❌ Enables APIs manually                           │
│  ❌ Creates credentials manually                    │
│  ❌ Edits config files manually                     │
│  ❌ Runs commands manually                          │
│  ❌ Executes scripts manually                       │
│                                                      │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓
┌─────────────────────────────────────────────────────┐
│                Claude (Executor)                     │
│                                                      │
│  Role: Technical Execution via Automation           │
│  - Plans automation strategy                        │
│  - Creates GitHub Actions workflows                 │
│  - Triggers workflows via API                       │
│  - Monitors execution                               │
│  - Reads results from artifacts/logs                │
│  - Updates config files via MCP/filesystem          │
│  - Documents changes in CAPABILITIES_MATRIX.md      │
│                                                      │
│  Tools:                                              │
│  ✅ GitHub Actions (WIF → GCP)                      │
│  ✅ Cloud Shell (via Actions)                       │
│  ✅ MCP Servers (filesystem, ps_exec, etc.)         │
│  ✅ REST APIs (GCP, GitHub, etc.)                   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Translation of this model**:
- Or provides **strategic direction** ("I want full Google capabilities")
- Claude provides **tactical execution** (creates workflows, runs automation)
- Or provides **approval gates** for HIGH RISK operations
- Or provides **one-time clicks** when OAuth providers require human consent

**This is not negotiable**. Any plan, workflow, or documentation that asks Or to:
- Run commands
- Open web consoles
- Edit files manually
- Configure systems manually

...is **INVALID** and violates the core contract.

**Replacement strategy**: If a step requires Or's manual action, Claude MUST either:
1. Automate it via GitHub Actions / Cloud Shell / MCP
2. Document it as a ONE-TIME human click (OAuth consent only)
3. Mark it as a gap and propose automation path

---

## 📊 Capability Matrix

### Legend

**Status**:
- ✅ **Verified** - Tested and confirmed working
- 🟡 **Partial** - Works with limitations
- ⚠️ **Planned** - Defined but not yet implemented
- ❌ **Blocked** - Cannot be done (technical/security constraint)
- 🔄 **In Progress** - Currently being built
- 🔍 **Unverified** - Code exists but deployment/runtime status unknown

**Claude at Runtime** (🆕 v1.3.0):
- `Yes` - Claude required during execution (interactive, real-time decisions)
- `No` - Runs autonomously without Claude (scheduled jobs, automated workflows)
- `Builder-Only` - Claude builds automation but not involved in runtime
- `Unknown` - Not yet determined

**GPT-CEO Ready** (🆕 v1.3.0):
- `Yes` - GPT-CEO can serve as Primary Agent now
- `No` - GPT-CEO cannot (lacks tools/capabilities)
- `Planned` - Designed/planned, not yet ready
- `Unknown` - Not yet determined

**Human Approval** (🆕 v1.3.0):
- `Yes` - Explicit approval always required (CLOUD_OPS_HIGH)
- `No` - No approval needed (OS_SAFE, read-only)
- `Depends` - Depends on specific operation context
- `Unknown` - Not yet determined

---

## 1️⃣ GitHub Layer

### 1.1 Repository Operations

| From | To | Capability | Status | Claude at Runtime? | GPT-CEO Ready? | Human Approval? | Details | Limitations |
|------|----|-----------| -------|-------------------|----------------|-----------------|---------|-------------|
| Claude MCP | GitHub API | Read repos | ✅ Verified | Yes | Yes | No | Full read access via PAT | None |
| Claude MCP | GitHub API | Create/update files | ✅ Verified | Yes | Yes | Depends | Can create, commit, push | Docs=No, Code=Yes approval |
| Claude MCP | GitHub API | Create branches | ✅ Verified | Yes | Planned | No | Full branch management | None |
| Claude MCP | GitHub API | Create PRs | ✅ Verified | Yes | Planned | Depends | Open, update, merge PRs | Merge needs approval |
| Claude MCP | GitHub API | Create issues | ✅ Verified | Yes | Yes | No | Open, close, comment | None |
| Claude MCP | GitHub API | Search code | ✅ Verified | Yes | Yes | No | Full code search | None |
| Claude MCP | GitHub API | List commits | ✅ Verified | Yes | Yes | No | Access commit history | None |
| Claude MCP | GitHub API | Fork repos | ✅ Verified | Yes | Planned | No | Can fork to account | None |

**Authentication**: GitHub Personal Access Token (via MCP)  
**Scope**: Full access to `edri2or-commits` repositories

**Notes on GPT-CEO Readiness**:
- **Yes**: Basic read/write operations that GPT can perform via Actions or direct API
- **Planned**: Complex workflows (PRs, branch management) require orchestration design

---

### 1.1.1 GPT Agent Mode - Direct Repository Access ⭐ PRIMARY PATH

**🎯 Status**: ✅ **VERIFIED & ACTIVE** - This is GPT-CEO's primary method of repository access

| Capability | Status | Details | Scope | Approval Required? |
|-----------|--------|---------|-------|-------------------|
| **Read Operations** | ✅ Verified | Full read access to all files, commits, issues, PRs | Unlimited | No |
| **Write - Documentation** | ✅ Verified | Create/update files in `DOCS/`, `logs/`, `OPS/` | OS_SAFE | No |
| **Write - State Files** | ✅ Verified | Create/update `STATE_FOR_GPT*.md` and similar | OS_SAFE | No |
| **Write - Code/Workflows** | ✅ Verified | Can technically write, but requires approval | CLOUD_OPS_HIGH | Yes (מאשר כתיבה) |
| **Write - Infrastructure** | ✅ Verified | Can technically write, but requires approval | CLOUD_OPS_HIGH | Yes (מאשר כתיבה) |

**Access Method**: ChatGPT Agent Mode → Direct GitHub integration  
**Authentication**: Managed by ChatGPT platform  
**Evidence**: Commits f6da151, 1c64fd5, 81cba22, 52e5e39, 92de8df, b10769b, 047eea8, 3e1d1a0, 30fafb5, e9d57e6, c6c8573, 63708408

**✅ Allowed Without Approval (OS_SAFE)**:
```
DOCS/*.md              - All documentation files
logs/*.md              - Operation logs
OPS/STATUS/*.json      - Status tracking files
OPS/EVIDENCE/*.json    - Evidence collection
STATE_FOR_GPT*.md      - State snapshots
```

**⚠️ Requires Explicit Approval (CLOUD_OPS_HIGH)**:
```
.github/workflows/*.yml           - CI/CD pipelines
cloud-run/**/*.js                - Service code
gpt_agent/*.py                   - Agent implementations
*.py (application code)          - Scripts
*.json (config files)            - Configurations
CAPABILITIES_MATRIX.md (major)   - Structural changes only
```

**🔄 Recommended Workflow**:
1. **For Documentation**: Create/update directly via Agent Mode
2. **For Code Changes**: Create plan document → Get approval → Execute via PR or direct commit
3. **For Infrastructure**: Create detailed plan → Get approval → Execute with rollback plan

**📚 Reference Guide**: See `DOCS/GPT_ACCESS_GUIDE_SIMPLE.md` for complete instructions

---

### 1.1.2 GitHub Executor API v1 (Cloud Run) ⭐ NEW - PLANNED

**🎯 Status**: ⚠️ **PLANNED - AWAITING SECRET**

**Purpose**: Stable Cloud Run API for GPT Unified Agent to perform GitHub operations independently

| Capability | Status | Details | Scope | Approval Required? |
|-----------|--------|---------|-------|-------------------|
| **Health Check** (`/`) | ⚠️ Planned | Service status verification | N/A | No |
| **Read File** (`/repo/read-file`) | ⚠️ Planned | Read any file from repository | Unlimited | No |
| **Update Doc** (`/repo/update-doc`) | ⚠️ Planned | Create/update files in safe paths only | OS_SAFE | No (safe paths), Yes (other) |

**Implementation**: ✅ **Code Complete**  
**Deployment**: ⏸️ **Blocked - Missing GitHub PAT**

**Code Location**: `cloud-run/google-workspace-github-api/`  
**Service Name**: `github-executor-api` (planned)  
**Region**: `us-central1` (planned)  
**Project**: `edri2or-mcp`

**Authentication**: 
- Method: GitHub Personal Access Token
- Storage: GCP Secret Manager (planned: `github-executor-api-token`)
- Scope Required: `repo` (full repository access)
- Status: ❌ **Secret not found in automated search**

**Path Validation** (Server-side enforcement):

✅ **Allowed Paths** (OS_SAFE):
```
DOCS/                 - Documentation
logs/                 - Operation logs
OPS/STATUS/          - Status files
OPS/EVIDENCE/        - Evidence collection
STATE_FOR_GPT*.md    - State snapshots
```

❌ **Forbidden Paths** (Returns HTTP 403):
```
.github/workflows/   - CI/CD pipelines
cloud-run/          - Service code
*.py, *.js          - Application code
*.yml (infra)       - Infrastructure configs
```

**Documentation**:
- Design: `DOCS/GITHUB_EXECUTOR_API_DESIGN_v1.md` ✅
- OpenAPI: `DOCS/GITHUB_EXECUTOR_API_OPENAPI.yaml` ✅
- Status: `DOCS/GITHUB_EXECUTOR_API_DEPLOYMENT_STATUS.md` ✅

**Blocker Details**:
- Search completed: Local environment, config files, Secret Manager
- Result: No existing GitHub PAT found
- Resolution: Or must provide PAT or create new one
- Estimated deployment time: ~25 minutes after PAT is available

**Notes**:
- Claude at Runtime: `Builder-Only` (Claude built service, GPT consumes)
- GPT-CEO Ready: `Planned` (after deployment)
- Human Approval: `No` (OS_SAFE paths), `Yes` (deployment itself)

**Alternative**: Use GPT Agent Mode (Section 1.1.1) - Already working

**Evidence**:
- Commits: 3e1d1a0 (design), 30fafb5 (code), e9d57e6 (OpenAPI), c6c8573 (status), 63708408 (search results)

---

### 1.2 GitHub Actions Integration

[Previous content unchanged]

---

[Rest of CAPABILITIES_MATRIX continues with sections 2-10...]

---

## 📝 Update Log

### 2025-11-18 (v1.3.2) - GitHub Executor API v1 (Planned)
- **Added Section 1.1.2**: GitHub Executor API v1 capability
- **Status**: ⚠️ Planned - Code complete, deployment blocked
- **Blocker**: GitHub PAT not found in automated search
- **Documentation**: Complete (design, OpenAPI, deployment status)
- **Code**: Refactored with 2 new endpoints + path validation
- **Evidence**: Commits 3e1d1a0, 30fafb5, e9d57e6, c6c8573, 63708408
- **Alternative**: GPT Agent Mode (Section 1.1.1) continues to work

### 2025-11-18 (v1.3.1) - GPT Agent Mode Clarification
[Previous entry unchanged]

### 2025-11-18 (v1.3.0) - מנה R6: Role Fields Addition
[Previous entry unchanged]

---

[Rest of file unchanged]
