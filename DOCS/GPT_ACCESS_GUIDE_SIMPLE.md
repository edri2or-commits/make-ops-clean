# GPT Access Guide (Simple)

**Purpose**: Clear, simple instructions for GPT-CEO to access and work with the `edri2or-commits/make-ops-clean` repository  
**Created**: 2025-11-18  
**Status**: ✅ Active  
**Audience**: GPT-CEO and other AI agents

---

## 🎯 Quick Start

**Your primary method of repository access: GPT Agent Mode**

You access this repository **directly through ChatGPT's Agent Mode** - not through Cloud Run APIs, not through GitHub Actions (for now). Keep it simple.

---

## ✅ What You CAN Do (Without Approval)

### Read Operations (Always Allowed)
- ✅ Read any file in the repository
- ✅ Search code, commits, issues
- ✅ View workflow files and history
- ✅ Check repository structure

### Write Operations (OS_SAFE - Documentation Only)
You can **create and update** these types of files directly:

1. **Documentation files** (`DOCS/` directory):
   - Status updates
   - Analysis reports
   - Planning documents
   - Architecture diagrams
   - Meeting notes

2. **State files** (root or `DOCS/`):
   - `STATE_FOR_GPT*.md`
   - System status snapshots
   - Current capability summaries

3. **Log files** (`logs/` directory):
   - Operation logs
   - Evidence collection
   - Audit trails
   - Change documentation

4. **Evidence files** (`OPS/` directory):
   - Status reports
   - Verification results
   - Test outputs

### Examples of Allowed Operations

**✅ GOOD - Do These:**
```
- Create DOCS/GPT_ANALYSIS_2025-11-18.md
- Update DOCS/STATE_FOR_GPT_SNAPSHOT.md
- Create logs/LOG_OPERATION_XYZ.md
- Update OPS/STATUS/service_health.json
```

---

## ❌ What You CANNOT Do (Without Explicit Approval)

### Code Changes - REQUIRES APPROVAL
- ❌ Modify application code (Python, JavaScript, etc.)
- ❌ Change Cloud Run service code
- ❌ Edit MCP server implementations
- ❌ Modify utility scripts

### Infrastructure Changes - REQUIRES APPROVAL
- ❌ Create/modify GitHub Actions workflows (`.github/workflows/`)
- ❌ Change workflow configurations
- ❌ Modify deployment scripts
- ❌ Edit CI/CD pipelines

### Sensitive Configuration - REQUIRES APPROVAL
- ❌ Change authentication configs
- ❌ Modify secrets or credentials
- ❌ Edit service account settings
- ❌ Change OAuth configurations

### Examples of FORBIDDEN Operations (Without Approval)

**❌ BAD - Don't Do These Without Asking:**
```
- Modify .github/workflows/index-append.yml
- Change cloud-run/google-workspace-github-api/index.js
- Edit gcloud configurations
- Modify CAPABILITIES_MATRIX.md structure without coordination
```

---

## 🔄 Your Workflow Pattern

### Pattern A: Simple Documentation Update

**When**: You need to document something, create a status file, or log an operation

**Steps**:
1. Decide on file path (DOCS/, logs/, or OPS/)
2. Create/update file directly via Agent Mode
3. Commit with clear message
4. Report back to אור

**Example**:
```
User: "GPT, document the current system status"
You: 
- Create DOCS/SYSTEM_STATUS_2025-11-18.md
- Commit: "docs: add system status snapshot"
- Report: "Created status document at DOCS/SYSTEM_STATUS_2025-11-18.md"
```

### Pattern B: Code/Infrastructure Change (Requires Approval)

**When**: You need to modify code, workflows, or infrastructure

**Steps**:
1. **STOP** - Don't make changes yet
2. Create a **plan document** in DOCS/
3. Present plan to אור with:
   - What you want to change
   - Why it's needed
   - Risk assessment
   - Rollback plan
4. Wait for explicit approval (usually Hebrew phrase: "מאשר כתיבה")
5. If approved: Make change via PR or direct commit (depending on risk)
6. Document the change in logs/

**Example**:
```
User: "GPT, fix the Cloud Run API typo"
You:
- Create DOCS/PLAN_FIX_API_TYPO.md with:
  - What: Fix Accept header in index.js
  - Why: API calls failing
  - Risk: Low (typo fix)
  - Rollback: Git revert
- Present to אור: "I've created a plan for the typo fix. Awaiting approval."
- [Wait for "מאשר כתיבה"]
- [Then create PR or commit]
```

---

## 📚 Key Reference Documents

When working with this repository, always check these in order:

1. **CAPABILITIES_MATRIX.md** (Primary SSOT)
   - What Claude can do
   - What GPT can do
   - What requires approval
   - Current system capabilities

2. **This guide** (GPT_ACCESS_GUIDE_SIMPLE.md)
   - Your access method
   - Your permissions
   - Your workflow

3. **INDEX_FOR_GPT_CEO.md**
   - Navigation to other docs
   - Quick references
   - Decision flowcharts

4. **STATE_FOR_GPT_SNAPSHOT.md**
   - Current system state
   - Known issues
   - Open TODOs

---

## 🚫 What's NOT Your Current Path (For Now)

These mechanisms exist in documentation but are **not active** for your use:

### ❌ GPT Tasks Executor (Inactive)
- **What**: YAML-based task execution via GitHub Actions
- **Status**: Code exists but runtime broken
- **Decision**: Don't use until debugged and reactivated
- **Files**: `.github/workflows/gpt_tasks_executor.yml`, `.chatops/gpt_tasks/*.yml`

### ❌ Cloud Run API (Status Unknown)
- **What**: `github-executor-api` service for GitHub operations
- **Status**: Code exists, deployment status unknown, GPTs GO receives 404
- **Decision**: Don't use until verified and tested
- **Files**: `cloud-run/google-workspace-github-api/`

### 📋 Future Possibilities
אור and Claude may activate these mechanisms later. When they do:
- You'll receive explicit instructions
- This guide will be updated
- CAPABILITIES_MATRIX will reflect the change

**For now: Stick to Agent Mode - it works!**

---

## 🎓 Best Practices

### 1. Read Before Writing
- Always check CAPABILITIES_MATRIX first
- Verify file type is in allowed list
- Confirm no conflicts with existing work

### 2. Clear Communication
- Use descriptive commit messages
- Document your reasoning
- Report actions taken to אור

### 3. Transparency Over Speed
- If unsure → Ask before acting
- If it's code/infra → Create plan first
- If it seems risky → Escalate to אור

### 4. Update Documentation
- When capabilities change → Update CAPABILITIES_MATRIX
- When you learn something → Document in DOCS/
- When operations complete → Log in logs/

---

## 🔐 Security Reminders

1. **Never commit secrets** - No API keys, tokens, passwords
2. **Never bypass approval** - Code/infra always needs אור's "מאשר כתיבה"
3. **Verify scope** - If it's not in the "allowed" list above, ask first
4. **Log everything** - OS_SAFE operations still need documentation

---

## 📞 When in Doubt

**The Golden Rule**: If you're not 100% sure it's allowed → **Ask אור first**

**Escalation Path**:
1. Check this guide
2. Check CAPABILITIES_MATRIX.md
3. If still unclear → Create a plan document
4. Present plan to אור
5. Wait for approval
6. Proceed only after explicit approval

---

## 🎯 Success Criteria

You're using this guide correctly when:
- ✅ You create docs/logs/state files confidently
- ✅ You ask before touching code/workflows
- ✅ You reference CAPABILITIES_MATRIX as SSOT
- ✅ You keep אור informed of actions
- ✅ You use Agent Mode as primary access method

---

## 📝 Appendix: File Path Quick Reference

### ✅ Always Safe (OS_SAFE)
```
DOCS/*.md              - Documentation
logs/*.md              - Operation logs
OPS/STATUS/*.json      - Status files
OPS/EVIDENCE/*.json    - Evidence collection
STATE_FOR_GPT*.md      - State snapshots
```

### ⚠️ Requires Approval (CLOUD_OPS_HIGH)
```
.github/workflows/*.yml           - CI/CD pipelines
cloud-run/**/*.js                - Service code
gpt_agent/*.py                   - Agent code
*.py (application code)          - Scripts
*.json (config files)            - Configurations
```

### 🔍 Context-Dependent (Ask First)
```
CAPABILITIES_MATRIX.md  - SSOT (coordinate changes)
README.md              - Main docs (coordinate changes)
*.yml (non-workflow)   - Task configs (depends)
```

---

**Remember**: This is your clean, simple path forward. Agent Mode → Documentation/State → Coordination with אור for anything else. 

Keep it simple. Keep it safe. Keep אור informed. 🌿

---

**Last Updated**: 2025-11-18  
**Next Review**: When access mechanisms change  
**Maintained By**: Claude (with אור's approval)
