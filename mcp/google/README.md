# Google Workspace / Drive – Auth Patterns

Two secure options — choose one (you can mix):

### A) **Domain‑wide delegation (Workspace)**
Best when you need to act *as users*. Requires Workspace super‑admin.
1. Create a Service Account (enable Drive API).
2. In Admin Console → Security → API controls → *Manage Domain Wide Delegation*: add the SA **Client ID** with Drive scopes you need, e.g.:
   - `https://www.googleapis.com/auth/drive` (full) or tighter: `drive.file`, `drive.readonly`, `drive.metadata.readonly`.
3. Code uses delegated credentials to impersonate a user (`with_subject`).

### B) **Shared Drive membership (personal or mixed)**
No impersonation. Give the Service Account *member* access to a specific **Shared Drive**; it can only read/write there.

---

## Minimal gcloud (project bootstrap)
```sh

gcloud services enable drive.googleapis.com iamcredentials.googleapis.com sts.googleapis.com
# Create service account
 gcloud iam service-accounts create mcp-drive --display-name="MCP Drive"
```

> Prefer **Workload Identity Federation** for CI (no JSON keys). For MCP servers, keep keys only in the server secret store.

## References
- OAuth 2.0 Service Accounts + Domain‑wide Delegation.
- Drive API scopes.

Created: 2025-11-02
