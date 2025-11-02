# GitHub – App (Least‑Privilege)

Prefer a **GitHub App** over PATs. It uses short‑lived tokens and fine‑grained repo access.

## Steps
1. Register a private GitHub App.
2. Permissions (minimum for repo changes via MCP):
   - **Contents**: Read & Write
   - **Pull requests**: Read & Write
   - **Metadata**: Read‑only
   (add Issues if you want to file issues)
3. Install the App on the target repo/org (`make-ops-clean`).
4. Provide App creds to the MCP server; it will mint **installation tokens** per call.

## CI (no long‑lived secrets)
Use **OIDC → Workload Identity Federation** to access cloud APIs from GitHub Actions (no JSON keys).

References: GitHub Apps overview; Creating a GitHub App; token model & permissions.

Created: 2025-11-02
