# Glossary

**Purpose**: Define key terms used across the system

---

## Core Concepts

### SSOT (Single Source of Truth)
The authoritative source for a piece of information. In our system:
- **Evidence Index** (spreadsheet) is SSOT for all proofs
- **config.json** is SSOT for service configurations
- **make-ops-clean** repo is SSOT for code and docs

### Proof Pack
A structured bundle of evidence that documents:
- What API was called
- What was the request
- What was the response
- When it happened
- Hash for verification

See: `PROOF_PACK_SPEC.json`

### Anchors
Key reference points that don't change:
- Evidence Index URL
- Repository URL
- Config file structure
- Operating mode definitions

### Auditor Pass
A review process where:
1. Check sources cited
2. Verify scopes used
3. Ensure GET before write
4. Validate proof existence

### DoD (Definition of Done)
Criteria that must be met before moving to next level:
- **L1 DoD**: All APIs validated, evidence collected
- **L2 DoD**: Write operations tested, rollback verified
- **L3 DoD**: Automation scheduled, monitoring active

### Canary
A small test change to verify system behavior:
- Deploy to subset
- Monitor for issues
- Rollback if needed
- Full deploy if successful

### Idempotency
An operation that can be repeated without changing the result:
- GET requests are naturally idempotent
- PUT should be idempotent (same result if repeated)
- POST is usually not idempotent (creates new each time)

---

## Operating Modes

### L1 (Read-Only)
- Only GET operations
- Collect evidence
- Build proof packs
- No state changes

### L2 (Controlled-Write)
- Write operations allowed
- PR-first when possible
- Canary + Rollback
- Immediate proof

### L3 (Automations)
- Scheduled operations
- Triggered workflows
- Observability required
- Only after L2 DoD

---

## Integration Terms

### MCP (Model Context Protocol)
Protocol for Claude to access external systems:
- Filesystem MCP
- GitHub MCP  
- Gmail MCP
- Google Drive MCP

### WIF (Workload Identity Federation)
Google Cloud authentication without keys:
- GitHub Actions → OIDC token
- OIDC token → Google access token
- Access Google APIs securely

### Webhook
HTTP callback for async notifications:
- Make.com webhooks
- GitHub webhooks
- Telegram webhooks (or polling)

---

**Updated**: 2025-11-12  
**Branch**: unified/desktop-merge
