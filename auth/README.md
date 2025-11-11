# GitHub App Authentication Migration

## Overview

This directory contains scaffolding for migrating from Personal Access Tokens (PAT) to GitHub App authentication.

## Files

### `jwt_wrapper.py`

Python wrapper for GitHub App authentication:
- JWT generation (RS256)
- Installation Token minting
- Auto-refresh before expiry
- Integration placeholders for Credential Manager / Secret Manager

**Key Features:**
- Never stores private key in plaintext
- Tokens auto-refresh 5 minutes before expiry
- Scoped permissions per repository
- ~1 hour token lifetime (vs 30+ days for PAT)

### `.github/workflows/app-auth-ready.yml`

Workflow to test GitHub App authentication readiness:
- Checks for required secrets (GH_APP_ID, GH_APP_PRIVATE_KEY_PEM)
- Generates JWT if credentials available
- Placeholder for Installation Token minting
- Summary report of readiness status

## Migration Path

### Phase 1: Preparation (Current)
✅ Create JWT wrapper code
✅ Create readiness check workflow
✅ Document migration steps

### Phase 2: Credential Setup (Requires Or)
⏸️ Regenerate GitHub App private key
⏸️ Store in Windows Credential Manager
⏸️ Configure repository secrets (if using in CI)

### Phase 3: Integration
⏸️ Implement Credential Manager read in jwt_wrapper.py
⏸️ Test JWT generation and token minting
⏸️ Update MCP client configuration

### Phase 4: Cutover
⏸️ Switch MCP from PAT to App tokens
⏸️ Revoke temporary PAT
⏸️ Verify all operations work

## Current Status

**Scaffold**: ✅ Complete
**App Key**: ❌ Not regenerated (deleted in Phase 1 PURGE)
**Integration**: ⏸️ Awaiting key regeneration

## Next Actions

1. **Or must**: Regenerate App private key at https://github.com/settings/apps (App ID: 2251005)
2. **Or must**: Store in Credential Manager: `github-app-2251005-private-key`
3. **Claude will**: Implement Credential Manager read
4. **Claude will**: Test end-to-end flow
5. **Claude will**: Update MCP configuration

## Security Notes

- ✅ No private keys in code or config files
- ✅ Short-lived tokens (~1h vs 30+ days)
- ✅ Scoped permissions per repository
- ✅ Auto-refresh before expiry
- ✅ Audit trail via GitHub App

## Usage Example

```python
from auth.jwt_wrapper import GitHubAppAuth

# Initialize
auth = GitHubAppAuth(
    app_id="2251005",
    installation_id="<INSTALLATION_ID>"
)

# Get token (auto-refreshes)
token = auth.get_installation_token(
    private_key_source="credential_manager",
    repositories=["make-ops-clean"],
    permissions={
        "contents": "write",
        "pull_requests": "write"
    }
)

# Use token
import requests
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "https://api.github.com/repos/edri2or-commits/make-ops-clean",
    headers=headers
)
```

## References

- [GitHub Apps Authentication](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app)
- [Installation Access Tokens](https://docs.github.com/en/rest/apps/apps#create-an-installation-access-token-for-an-app)
- [JWT Authentication](https://jwt.io/introduction)
