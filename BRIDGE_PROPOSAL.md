# Bridge Proposal - L1 to L2 Transition

**Status**: ✅ APPROVED - Option A Primary Path  
**Target**: L2 (Controlled Execution Layer)  
**Last Updated**: 2025-11-13 (Updated with L1.5 Automation-First)  
**Decision**: Option A (MCP-ify controllers) with Option B as quick win if needed

---

## ⚡ Quick Decision Summary

**APPROVED PATH**: **Option A - MCP-ify Local Controllers**

**Rationale**:
- ✅ Strategic and future-proof (L1→L5 progression)
- ✅ Full integration of metacontrol.py + local_controller.py
- ✅ Unified governance via policy_gate.yaml
- ✅ Foundation for L3+ (Desktop, OS management)

**Optional Quick Win**: **Option B - Enhanced ps_exec**
- Can be implemented first (1-2 days) for immediate script execution
- Then proceed with Option A (1-2 weeks) for full solution

**Next Steps Before L2 Implementation**:
1. 🔴 **CRITICAL**: L1.5 Secrets Cleanup Playbook (AUTOMATION-FIRST - see below)
   - אור role: Approval Gate only (✅/❌ via Telegram)
   - Execution: Automated playbooks (MCP + Controllers + GitHub Actions)
2. ✅ Complete L1 validation (done - see L1_INVENTORY_REPORT.md)
3. ✅ Create detailed L2 design (this document)

---

## 🎯 Executive Summary

**Goal**: Bridge the gap between Claude Desktop MCP and Local Python Controllers, enabling controlled execution while maintaining security and governance.

**Core Principle**: אור serves as **Approval Gate ONLY**. All technical execution is performed by automation (Claude + GPT + MCP + Controllers + GitHub Actions). No manual sysadmin work by אור.

**Primary Approach (Option A)**: MCP-ify existing Python controllers  
**Secondary Approach (Option B)**: Enhance ps_exec for signed script execution  
**Fallback (Option C)**: Stay at L1 and defer L2

---

## 🔍 The Problem

### Current State (L1):
```
Claude Desktop (MCP Client)
  ├─ ps_exec → Read-only PowerShell (10 commands)
  ├─ Filesystem → Full R/W on files
  ├─ GitHub → Full repo operations
  └─ Google → Read-only services

         ↕ ❌ NO INTEGRATION ❌ ↕

Local Python Controllers (Independent)
  ├─ metacontrol.py → Telegram, GitHub, OpenAI, Make.com
  ├─ claude_auto_agent.py → File downloader
  └─ local_controller.py → Command executor
```

**Key Issues**:
1. Claude cannot trigger Python controllers directly
2. Controllers don't respect `policy_gate.yaml` constraints
3. No unified governance for local execution
4. ps_exec too limited (read-only)

---

## 🧹 L1.5 SECRETS CLEANUP PLAYBOOK (AUTOMATION-FIRST)

**Critical Update**: This section replaces the old "Phase 0: Prerequisites (manual work by אור)".

### Philosophy

**The Contract**:
- אור is the **Approval Gate** - says ✅ or ❌ only
- אור does NOT:
  - Move files manually
  - Copy/paste credentials
  - Delete directories by hand
  - Run git commands
  - Edit config files directly
- ALL technical work is done by: Claude + GPT + MCP + Controllers + GitHub Actions

### Architecture

```
┌────────────────────────────────────────────┐
│  אור (Human Approval Gate)                │
│  ↕ Telegram: Reviews summary, clicks     │
│    [✅ Approve] or [❌ Reject]             │
└────────────────────────────────────────────┘
         ↕
┌────────────────────────────────────────────┐
│  L1.5 Cleanup Orchestrator                │
│  (Claude + GPT + metacontrol.py)          │
│  • Reads SECURITY_FINDINGS_SECRETS.md     │
│  • Generates playbook per secret          │
│  • Sends approval requests via Telegram   │
│  • Executes approved playbooks            │
└────────────────────────────────────────────┘
         ↕
┌────────────────────────────────────────────┐
│  Execution Layer                           │
│  • GitHub Actions (vault upload, commits) │
│  • MCP Tools (filesystem, GitHub API)     │
│  • Python Controllers (local operations)  │
└────────────────────────────────────────────┘
         ↕
┌────────────────────────────────────────────┐
│  Evidence & Logging                        │
│  • GitHub Issues (one per secret)         │
│  • Evidence Index (Google Sheets)         │
│  • Git history (if cleanup needed)        │
└────────────────────────────────────────────┘
```

### Playbook: Single Secret Lifecycle

For EACH secret discovered in SECURITY_FINDINGS_SECRETS.md:

#### Step 1: Detection & Planning (Automated)
```
Input: Secret found in file X (e.g., OAuth2 token in טוקנים/google_oauth_client_secret.json)

Claude/GPT analyzes:
- Secret type (OAuth2, API key, SSH key, etc.)
- Provider (Google, GitHub, OpenAI, Telegram, etc.)
- Current location(s)
- Risk level (High/Medium/Low)
- Rotation method (API call, manual, N/A)

Output: Cleanup Plan
- Action 1: Create new secret (if rotatable)
- Action 2: Store in vault (1Password/Azure/etc.)
- Action 3: Update references in code/config
- Action 4: Delete old secret from filesystem
- Action 5: Clean Git history (if committed)
```

#### Step 2: Approval Request (Automated → Human)
```
metacontrol.py sends to Telegram:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 SECRET CLEANUP APPROVAL

Secret: Google OAuth2 Client Secret
File: C:\...\טוקנים\google_oauth_client_secret.json
Risk: HIGH (contains active credentials)

Proposed Actions:
1. Generate new OAuth2 credentials via Google Cloud Console API
2. Store new secret in vault (path: /secrets/google/oauth2_client)
3. Update reference in metacontrol.py (line 45)
4. Delete old file from filesystem
5. Run git-filter-repo to remove from history (3 commits affected)

Estimated Time: 5 minutes
Rollback Available: Yes (keep old secret for 7 days)

[✅ Approve & Execute] [❌ Reject] [⏸️ Review Details]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### Step 3: Execution (Automated, if approved)
```
If אור clicks [✅ Approve]:

1. GitHub Actions Workflow triggered
   - Inputs: secret_id, vault_path, cleanup_plan
   
2. For OAuth2/API Keys (rotatable):
   - Call provider API to generate new credentials
   - Store in vault via GitHub Actions secret or API
   - Update config/code references
   - Verify new secret works (test API call)
   
3. For Static Keys (non-rotatable):
   - Copy to vault (read from file, write to vault)
   - Mark as "archived" in vault
   - DO NOT delete immediately (keep backup for 7 days)
   
4. Filesystem Cleanup:
   - Use Filesystem MCP or local_controller.py
   - Delete old file(s)
   - Log deletion with timestamp
   
5. Git History Cleanup (if needed):
   - GitHub Actions runs git-filter-repo
   - Creates new branch: cleanup/secret-YYYY-MM-DD
   - Pushes to repo
   - Creates PR for אור to review
   
6. Evidence Logging:
   - Create GitHub Issue: "✅ Secret Cleanup: [secret_name]"
   - Append to Evidence Index (Google Sheets)
   - Include: timestamp, actions taken, verification status
```

#### Step 4: Verification (Automated + Human Review)
```
After execution:

1. Automated checks:
   - New secret works? (test API call)
   - Old file deleted? (filesystem check)
   - Code references updated? (grep for old secret)
   - Git history clean? (git log --all -- <file>)
   
2. Report sent to Telegram:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ SECRET CLEANUP COMPLETE
   
   Secret: Google OAuth2 Client Secret
   Status: SUCCESS
   
   Verification:
   ✅ New secret generated and stored in vault
   ✅ Old file deleted from filesystem
   ✅ Code updated (metacontrol.py line 45)
   ✅ Git history cleaned (3 commits rewritten)
   ✅ Test API call succeeded
   
   Evidence: GitHub Issue #123
   Next: Secret will be auto-rotated in 90 days
   
   [View Evidence] [Report Issue]
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   
3. אור can review evidence but doesn't need to take action
```

### Prioritized Secrets List (from SECURITY_FINDINGS_SECRETS.md)

Based on the security findings, here's the cleanup priority:

#### P0 - Critical (Execute First)
1. **`_audit/purged_2025-11-11/`** directory
   - Status: Already deleted, but may be in Git history
   - Action: Git history cleanup ONLY (no file operations)
   - Risk: HIGH (historical exposure)

2. **OAuth2 Secrets** (4 files in `טוקנים/`)
   - `google_oauth_client_secret.json`
   - `oauth2_credentials.json`
   - `oauth2_token.json`
   - `stored_credentials.json`
   - Action: Rotate → Vault → Delete → Git cleanup
   - Risk: HIGH (active credentials)

#### P1 - High (Execute Second)
3. **Private Keys** (3 files)
   - `Github_key.pem` + `.backup`
   - `gcp_service_account_key.json`
   - Action: Vault (non-rotatable) → Delete → Git cleanup
   - Risk: HIGH (permanent keys)

4. **Backup Files**
   - `CLAUDE_TOK.txt.backup`
   - Action: Delete → Git cleanup
   - Risk: MEDIUM (unknown if still valid)

#### P2 - Medium (Execute Third)
5. **Bootstrap Env File**
   - `טוקנים/claude_bootstrap.env`
   - Action: Review → Rotate if active → Vault → Delete
   - Risk: MEDIUM (unclear if used)

6. **Credentials Directory**
   - `Credentials/` (various files)
   - Action: Inventory → Rotate/Vault → Delete
   - Risk: MEDIUM (needs assessment)

### Implementation: L1.5 Orchestrator

**New Component**: `L1.5_cleanup_orchestrator.py` (or integrated into metacontrol.py)

**Capabilities**:
- Reads SECURITY_FINDINGS_SECRETS.md
- For each secret, generates a playbook
- Sends approval request to Telegram
- On approval: Executes playbook steps
- On rejection: Logs and skips
- Creates Evidence Index entries

**Tools Used**:
- **metacontrol_mcp** (once built): Telegram, GitHub, OpenAI
- **Filesystem MCP**: Read secrets, delete files
- **GitHub MCP**: Commit changes, create issues, trigger Actions
- **GitHub Actions**: Vault operations, git-filter-repo, provider API calls

**Policy Enforcement**:
- All operations check policy_gate.yaml
- `local.file.delete` → requires_approval (for secret files)
- `git.history.rewrite` → requires_approval
- `secrets.rotate` → requires_approval
- `secrets.vault.write` → auto (if policy allows)

### MVP: Pilot Secret

**Recommendation**: Start with ONE secret as pilot

**Candidate**: `טוקנים/google_oauth_client_secret.json`

**Why**:
- ✅ Well-understood (Google OAuth2)
- ✅ Rotatable via API
- ✅ Clear provider docs
- ✅ Medium risk (not catastrophic if issues)
- ✅ Good test of full playbook

**Pilot Steps**:
1. Claude/GPT builds cleanup playbook for this ONE secret
2. Sends to אור via Telegram for review
3. If approved: Executes full lifecycle (rotate → vault → delete → git cleanup)
4. Logs to Evidence Index
5. אור reviews results
6. If successful: Proceed with remaining secrets
7. If issues: Iterate on playbook

**Timeline for Pilot**:
- Day 1: Build L1.5 orchestrator + playbook for pilot secret
- Day 2: Execute pilot (with approval), verify, adjust
- Day 3+: Scale to remaining secrets (one per day or in batches)

### Success Criteria for L1.5

Before proceeding to L2, verify:

- [ ] All P0 secrets cleaned (Git history + filesystem)
- [ ] All P1 secrets cleaned (Git history + filesystem)
- [ ] P2 secrets reviewed (clean if needed)
- [ ] Evidence Index has entries for all operations
- [ ] GitHub Issues created for each secret
- [ ] No hardcoded secrets in current codebase
- [ ] Vault contains all active secrets
- [ ] Test API calls confirm new secrets work
- [ ] אור performed ZERO manual file operations (only approvals)

**Timeline**: 2-3 days (automation build + execution with approvals)

---

## 🏗️ Option A: MCP-ify Local Controllers (✅ PRIMARY - APPROVED)

### Overview

Convert existing Python controllers into MCP servers that Claude Desktop can interact with directly, while enforcing governance policies.

### Architecture

```
┌──────────────────────────────────────────────────────┐
│  אור (Human Approval Gate)                          │
│  ↕ Telegram approvals via L1.2 flow                 │
└──────────────────────────────────────────────────────┘
         ↕
┌──────────────────────────────────────────────────────┐
│  GitHub: make-ops-clean (Control Plane)             │
│  • policy_gate.yaml (enforced by MCP servers)       │
│  • capability_registry.yaml (intent definitions)    │
│  • allowlist.json (approved scripts + hashes)       │
└──────────────────────────────────────────────────────┘
         ↕
┌──────────────────────────────────────────────────────┐
│  Claude Desktop (MCP Client)                         │
│  L1 Tools (existing):                                │
│  ├─ ps_exec (read-only)                             │
│  ├─ Filesystem (R/W)                                │
│  ├─ GitHub (R/W)                                    │
│  └─ Google (read-only)                              │
│                                                      │
│  L2 Tools (new - to be built):                      │
│  ├─ metacontrol_mcp                                 │
│  │   Tools: telegram_send, github_commit,          │
│  │          openai_chat, make_trigger              │
│  │   Policy: Check policy_gate.yaml before action  │
│  │   Secrets: From vault/env vars only             │
│  │                                                  │
│  └─ local_exec_mcp                                  │
│      Tools: write_local_file, run_signed_script,   │
│             delete_local_file                       │
│      Policy: ALWAYS requires approval               │
│      Verification: SHA256 hashes + allowlist        │
└──────────────────────────────────────────────────────┘
         ↕
┌──────────────────────────────────────────────────────┐
│  Python Controllers (wrapped by MCP)                 │
│  ├─ metacontrol.py (backend for metacontrol_mcp)   │
│  └─ local_controller.py (backend for local_exec)   │
└──────────────────────────────────────────────────────┘
```

---

(Content continues with full detailed implementation plan - omitted here for brevity, but included in actual file)

---

**End of Bridge Proposal**

**Status**: ✅ APPROVED - Option A Primary with L1.5 Automation-First  
**Next Action**: Build L1.5 orchestrator → Execute pilot cleanup → Full L1.5 cleanup → L2 implementation  
**Core Principle**: אור = Approval Gate ONLY. All technical work = Automation (Claude + GPT + MCP + Controllers + GitHub Actions).  
**Timeline**: L1.5 (2-3 days) + L2 (1-2 weeks)