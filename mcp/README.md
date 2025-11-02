# MCP Layer (Self‑Hosted Connectors)

This folder bootstraps a **self‑hosted connector layer** using the Model Context Protocol (MCP). Chat interfaces (like ChatGPT) can attach to this MCP server to execute actions against GitHub, Google Drive, and other tools — without relying on vendor beta connectors.

## Why
- Portable across devices (phone/desktop).
- Auditable (changes flow through PRs in this repo).
- Minimize secret sprawl via least‑privilege and federation.

## Docs
- OpenAI: MCP overview and server docs — see the "Technical documentation" link from *Apps & Connectors* help.
- GitHub Apps: least‑privilege, short‑lived tokens.
- Google: service accounts + domain‑wide delegation (Workspace) or Shared Drives membership.

## Structure
- `google/` — Drive/Gmail/Sheets setup guides.
- `github/` — GitHub App setup and scopes.

## Healthcheck
A trivial CI workflow `.github/workflows/mcp_healthcheck.yml` prints `OK` to validate CI wiring.

## Next
1. Stand up a lightweight MCP server (Node/TS or Python).
2. Add tool handlers for GitHub & Google APIs.
3. Connect Chat client to this MCP endpoint.

Created: 2025-11-02
