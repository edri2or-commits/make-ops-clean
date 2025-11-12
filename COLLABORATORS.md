# Collaborators & Access Management

## Current Team

### Core Team
- **Or Edri** (`edri2or-commits`) - Owner, Full Access
- **Claude** (AI Agent) - Via GitHub App/Token, Automated Operations
- **GPT** (Google Workspace Assistant) - Via API, Drive/Gmail/Calendar Access

## Adding GPT as Collaborator

### Method 1: GitHub Personal Access Token (Recommended)
```bash
# GPT creates a GitHub account and PAT
1. GPT: Create GitHub account (if not exists)
2. GPT: Generate PAT with scopes: repo, workflow
3. Or: Add GPT's GitHub username as collaborator:
   Settings → Collaborators → Add people
4. GPT: Accept invitation
5. GPT: Clone repo with PAT:
   git clone https://[PAT]@github.com/edri2or-commits/make-ops-clean.git
```

### Method 2: GitHub App (Advanced)
```bash
# Create GitHub App for GPT
1. Settings → Developer settings → GitHub Apps → New
2. Configure permissions:
   - Repository permissions:
     * Contents: Read & Write
     * Pull requests: Read & Write
     * Issues: Read & Write
     * Workflows: Read & Write
3. Install app on make-ops-clean repo
4. Generate private key for GPT
```

### Method 3: Deploy Keys (Read-Only)
```bash
# For read-only access
1. GPT: Generate SSH key pair
2. Or: Settings → Deploy keys → Add
3. Paste GPT's public key
4. Check "Allow write access" if needed
```

## Access Levels

### Claude (AI Agent)
- **Access Type**: GitHub App via MCP
- **Permissions**: 
  - ✅ Read repository
  - ✅ Create branches
  - ✅ Push commits
  - ✅ Create PRs
  - ❌ Merge PRs (requires approval)
  - ❌ Delete branches
  - ❌ Modify settings

### GPT (Google Workspace Assistant)  
- **Access Type**: To be configured
- **Desired Permissions**:
  - ✅ Read repository
  - ✅ Create branches
  - ✅ Push commits
  - ✅ Create PRs
  - ✅ Comment on PRs
  - ❌ Merge PRs (requires Or's approval via chat)
  - ❌ Modify settings

### Or Edri (Owner)
- **Access Type**: Owner
- **Control Method**: Chat-only (no direct GitHub interaction)
- **Permissions**: All (but delegates to agents)

## Workflow Philosophy

### Zero-Touch for Or
```
Or speaks → Claude & GPT execute → PR created → Or approves via chat → Merged
```

### Agent Collaboration
```
Claude: Desktop, GitHub, Code
GPT: Drive, Gmail, Calendar, Evidence
Both: Sync via this repo
```

### Approval Flow
```
1. Agent creates PR
2. Agent notifies Or (Telegram)
3. Or reviews in chat
4. Or approves: "merge it" / "looks good"
5. Agent merges PR
6. Agent confirms
```

## Setting Up GPT Access (Quick Start)

### Option A: GPT has GitHub account
```bash
# Or runs:
gh api /repos/edri2or-commits/make-ops-clean/collaborators/[GPT_USERNAME] \
  --method PUT \
  -f permission=push

# GPT accepts:
gh api /user/repository_invitations/[INVITATION_ID] --method PATCH
```

### Option B: GPT uses token only
```bash
# Or creates token:
gh auth login --scopes "repo,workflow"
gh auth token

# Or shares token securely with GPT (encrypted)
# GPT stores in secure location
# GPT exports:
export GITHUB_TOKEN="ghp_..."
gh auth login --with-token <<< "$GITHUB_TOKEN"
```

## Security Notes
- ⚠️ **Tokens expire** - Rotate quarterly
- ✅ **Use fine-grained PATs** when possible
- ✅ **Enable 2FA** on all accounts
- ✅ **Audit access logs** monthly
- ✅ **Revoke unused tokens** immediately

## Communication Channels
- **Primary**: Chat (Claude.ai)
- **Notifications**: Telegram (when configured)
- **Evidence**: Google Drive (Evidence_Store)
- **Logs**: This repo (DECISION_LOG.md)

---
**Created**: 2025-11-12  
**Purpose**: Document team access and collaboration workflow  
**Branch**: unified/desktop-merge