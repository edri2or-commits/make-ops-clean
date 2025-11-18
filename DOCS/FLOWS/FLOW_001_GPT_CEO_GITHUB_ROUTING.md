# FLOW_001 – GPT-CEO GitHub Routing Flow

**Flow ID**: FLOW_001  
**Created**: 2025-11-18  
**Owner**: GPT-CEO  
**Executor**: Claude Desktop  
**Version**: 1.0  
**Status**: ✅ Active (OS_SAFE operations only)

---

## 🎯 Purpose

This flow defines **how GPT-CEO orchestrates GitHub operations** based on CAPABILITIES_MATRIX v1.3.0, establishing clear routing rules between GPT-CEO (strategic planner) and Claude (tactical executor).

**Scope**: GitHub repository operations including:
- Documentation and state files (DOCS/, logs/, STATE)
- Code and workflow changes (via PR)
- Issues, comments, and project management
- Workflow triggering and monitoring

---

## 📍 When to Use This Flow

GPT-CEO should invoke FLOW_001 when Or requests:

### ✅ Direct Execution (OS_SAFE)
- **Create/update DOCS files** (STATE_FOR_GPT, FLOW specs, logs, design docs)
- **Create GitHub issues** (feature requests, bug reports, task tracking)
- **Search code/repos** (finding files, reviewing code, analyzing structure)
- **List commits** (reviewing history, finding changes)
- **Read any GitHub content** (repos, files, branches, PRs, issues)

### 🔄 Planning → PR Flow (CLOUD_OPS_HIGH)
- **Code changes** (Python, JavaScript, workflows)
- **Workflow modifications** (.github/workflows/*.yml)
- **Config file changes** (claude_desktop_config.json, package.json, etc.)
- **Infrastructure changes** (Cloud Run, GCP configs)

### 📋 Orchestration (Planned)
- **Trigger GitHub Actions workflows** (requires orchestration layer design)
- **Monitor workflow execution** (read logs, artifacts, status)
- **Branch management** (create feature branches)
- **PR operations** (create, update, review, merge)

---

## 🔀 Routing Rules

### Rule 1: Check CAPABILITIES_MATRIX First

**ALWAYS** reference CAPABILITIES_MATRIX.md before execution:

```
1. Find capability row in CAPABILITIES_MATRIX
2. Check "GPT-CEO Ready?" column
3. Route based on value:
   - Yes → Execute directly (Rule 2)
   - Planned → Design/Playbook only (Rule 3)
   - No → Cannot perform (Rule 4)
```

### Rule 2: GPT-CEO Ready = Yes → Direct Execution

**When**: Capability marked `GPT-CEO Ready = Yes`

**Pattern**:
```
Or → GPT-CEO: "Update STATE_FOR_GPT with latest status"
     ↓
GPT-CEO → Claude: [Detailed instructions with exact content]
     ↓
Claude → GitHub: [Executes via MCP]
     ↓
Claude → GPT-CEO: [Reports: file path, commit SHA, success/failure]
     ↓
GPT-CEO → Or: [Summary of what was done]
```

**Examples**:
- ✅ Create `DOCS/NEW_FLOW_SPEC.md`
- ✅ Update `DOCS/STATE_FOR_GPT_SNAPSHOT.md`
- ✅ Create GitHub issue for task tracking
- ✅ Search for all files containing "FLOW_"
- ✅ List recent commits to main branch

**Approval Check**:
- Read operations: `No approval` needed
- DOCS/STATE writes: `No approval` needed (OS_SAFE)
- Check `Human Approval?` column for specific operation

### Rule 3: GPT-CEO Ready = Planned → Design/Playbook

**When**: Capability marked `GPT-CEO Ready = Planned`

**Pattern**:
```
Or → GPT-CEO: "Create workflow to automate X"
     ↓
GPT-CEO: [Analyzes requirement]
     ↓
GPT-CEO → Claude: "Create DOCS/PLAYBOOK_X.md with design"
     ↓
Claude → GitHub: [Creates playbook document]
     ↓
GPT-CEO → Or: "Playbook created. When ready to implement, I'll create PR."
```

**Examples**:
- 📋 Workflow automation (GPT can design, Claude implements via PR)
- 📋 Branch/PR operations (design strategy, then manual approval)
- 📋 Complex orchestrations (multi-step workflows)

**Output**: 
- Design document in DOCS/PLAYBOOKS/
- Clear steps for future implementation
- Approval gates identified
- Risk assessment included

### Rule 4: GPT-CEO Ready = No → Cannot Perform

**When**: Capability marked `GPT-CEO Ready = No`

**Pattern**:
```
Or → GPT-CEO: "Take screenshot of desktop"
     ↓
GPT-CEO → Or: "I cannot perform local desktop operations. 
                This requires Claude with MCP access.
                Shall I ask Claude to do it?"
```

**Typical Cases**:
- ❌ Local filesystem operations (GPT lacks MCP)
- ❌ PowerShell commands (GPT lacks MCP)
- ❌ Direct GCP API calls (network restrictions)

**Alternative**: GPT-CEO can request Claude to perform operation and report back results.

---

## 🔐 Approval Gates

### No Approval Required (OS_SAFE)
```
Human Approval? = No
```

**Operations**:
- All read operations (search, list, fetch)
- DOCS/ and logs/ file creation/updates
- STATE_FOR_GPT updates
- GitHub issue creation/comments
- Non-code documentation

**Execute**: Immediately, no waiting

### Approval Required (CLOUD_OPS_HIGH)
```
Human Approval? = Yes
```

**Operations**:
- Code changes (Python, JS, etc.)
- Workflow file changes (.github/workflows/)
- Config file changes (MCP configs, package.json)
- PR merges
- Infrastructure changes

**Execute**: Only after explicit Or approval (Hebrew: "מאשר")

### Context-Dependent (CLOUD_OPS_SAFE/MEDIUM)
```
Human Approval? = Depends
```

**Depends on**:
- File type (docs=No, code=Yes)
- Scope (personal files=No, shared=Maybe)
- Impact (reversible=No, irreversible=Yes)

**Execute**: Apply decision tree:
1. Is it DOCS/STATE/logs? → No approval
2. Is it code/workflow? → Yes approval
3. Unclear? → Ask Or

---

## 🛠️ Execution Patterns

### Pattern A: Simple File Update (OS_SAFE)

**Use Case**: Update STATE_FOR_GPT_SNAPSHOT.md

**GPT-CEO Message to Claude**:
```
[MESSAGE TO CLAUDE DESKTOP]

Task: Update STATE_FOR_GPT_SNAPSHOT.md
File: DOCS/STATE_FOR_GPT_SNAPSHOT.md
Branch: main

Changes:
1. Update "Current Capabilities Status" section
2. Add note: "FLOW_001 activated (2025-11-18)"
3. Update version to v3.2

Content:
[Exact markdown content or diff]

Expected Response:
- File path
- Commit SHA
- Success confirmation

Approval: None needed (OS_SAFE per CAPABILITIES_MATRIX)
```

**Claude Response**:
```
✅ Updated: DOCS/STATE_FOR_GPT_SNAPSHOT.md
Commit: abc123def
Status: Success
Changes: Updated status section + added FLOW_001 note
```

### Pattern B: Code Change via PR (CLOUD_OPS_HIGH)

**Use Case**: Fix typo in cloud-run/google-workspace-github-api/index.js

**GPT-CEO Message to Claude**:
```
[MESSAGE TO CLAUDE DESKTOP]

Task: Create PR to fix Accept header typo
File: cloud-run/google-workspace-github-api/index.js
Issue: Line 37 - 'vund.github' should be 'vnd.github'

Steps:
1. Create branch: fix/accept-header-typo
2. Make change in branch
3. Create PR with description
4. DO NOT MERGE (await Or approval)

Expected Response:
- Branch name
- PR URL
- Commit SHA

Approval: Required for merge (CLOUD_OPS_HIGH)
```

**Claude Response**:
```
✅ PR Created: #42
Branch: fix/accept-header-typo
Commit: def456abc
URL: https://github.com/edri2or-commits/make-ops-clean/pull/42
Status: Awaiting Or approval for merge
```

### Pattern C: Orchestration (Planned)

**Use Case**: Trigger workflow and monitor results

**Current Status**: `GPT-CEO Ready = Planned`

**Approach**:
1. GPT-CEO creates `DOCS/PLAYBOOKS/WORKFLOW_TRIGGER_ORCHESTRATION.md`
2. Design includes:
   - Trigger mechanism
   - Status polling strategy
   - Result retrieval method
   - Error handling
3. Or reviews and approves design
4. Claude implements orchestration code
5. Test and verify
6. Update CAPABILITIES_MATRIX: `Planned → Yes`

---

## 🚦 Decision Tree

```
┌─────────────────────────────────────┐
│ Or requests GitHub operation        │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ GPT-CEO: Check CAPABILITIES_MATRIX  │
└────────────┬────────────────────────┘
             ↓
        ┌────┴────┐
        │         │
        ↓         ↓
    Read Op   Write Op
        │         │
        ↓         ↓
   No Approval  Check Type
        │         │
        │    ┌────┴────┐
        │    │         │
        │    ↓         ↓
        │  DOCS/    Code/
        │  STATE   Workflow
        │    │         │
        │    ↓         ↓
        │  No Appr  Approval
        │    │      Required
        └────┴─────────┘
             ↓
┌─────────────────────────────────────┐
│ Check GPT-CEO Ready?                │
└────────────┬────────────────────────┘
             │
        ┌────┴────┐
        │         │
        ↓         ↓
      Yes      Planned
        │         │
        ↓         ↓
   Execute   Design Only
        │         │
        │         ↓
        │    Create PR/
        │    Playbook
        │         │
        └─────────┘
             ↓
┌─────────────────────────────────────┐
│ Claude executes / GPT-CEO reports   │
└─────────────────────────────────────┘
```

---

## 📋 Quick Reference Table

| Operation | GPT-CEO Ready? | Approval? | Action |
|-----------|----------------|-----------|--------|
| Read repos/files | Yes | No | Execute |
| Create DOCS files | Yes | No | Execute |
| Update STATE files | Yes | No | Execute |
| Create issues | Yes | No | Execute |
| Search code | Yes | No | Execute |
| Update code files | Yes | Yes | PR → Approval |
| Update workflows | Planned | Yes | Design → PR |
| Trigger workflows | Planned | Depends | Design first |
| Create branches | Planned | No | Design first |
| Merge PRs | Planned | Yes | Design first |

---

## ⚠️ Important Constraints

### Constraint 1: OS_SAFE Boundary
```
✅ Allowed: DOCS/, logs/, STATE files
✅ Allowed: GitHub issues, comments
✅ Allowed: Read operations

❌ Not Allowed: Direct code changes (use PR)
❌ Not Allowed: Workflow changes without approval
❌ Not Allowed: Merging PRs without approval
```

### Constraint 2: github-executor-api Status
```
Status: Runtime Unverified (CAPABILITIES_MATRIX Section 10.2)
GPT-CEO Ready: Yes (design intent)
Reality: DO NOT rely on automated execution yet

Action: For now, use direct GitHub MCP via Claude
Future: When service verified, can use API bridge
```

### Constraint 3: No Local Operations
```
GPT cannot:
- Access local filesystem
- Run PowerShell commands
- Take screenshots
- Read local files

Workaround: Request Claude to perform and report results
```

---

## 🔄 Flow Evolution

### Current (v1.0)
- ✅ Direct DOCS/STATE operations
- ✅ GitHub read operations
- ✅ Issue management
- 📋 Code changes via PR (design exists)

### Next Steps (v1.1)
- 🔄 Implement workflow trigger orchestration
- 🔄 Implement PR creation automation
- 🔄 Test github-executor-api when verified
- 🔄 Update CAPABILITIES_MATRIX: Planned → Yes

### Future (v2.0)
- 🚀 Full GitHub Actions orchestration
- 🚀 Automated PR reviews
- 🚀 Branch management automation
- 🚀 Release automation

---

## 📚 References

**MUST READ**:
- `CAPABILITIES_MATRIX.md` (v1.3.0) - Single source of truth
- `logs/LOG_CAPABILITIES_MATRIX_ROLE_FIELDS_UPDATE_V2.md` - Role field definitions

**Related Flows**:
- `FLOW_002_GPT_CEO_GOOGLE_ROUTING.md` - Google Workspace operations

**Evidence**:
- Direct writes: commits 1c64fd5, 81cba22, 52e5e39
- GPT Agent Mode: Verified OS_SAFE scope

---

**Created**: 2025-11-18  
**By**: Claude (via GPT-CEO instructions)  
**Status**: ✅ Active (OS_SAFE scope)  
**Next Review**: When CAPABILITIES_MATRIX updates (Planned → Yes)
