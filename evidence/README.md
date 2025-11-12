# Evidence Collection

## Purpose
Track all integration proofs, API validations, and system state snapshots.

## Structure

### Integration Evidence
- `github_evidence.md` - GitHub Actions artifacts, workflows
- `make_evidence.md` - Make.com scenarios, team info  
- `telegram_evidence.md` - Telegram bot webhook status

### Analysis & Strategy Evidence
- `REPOSITORY_CLEANUP_ANALYSIS.md` - ⭐ **NEW**: Complete analysis of all 5 repositories with migration/archive/delete recommendations

### Decision Logs
- `../DECISION_LOG.md` - Major system decisions
- `../decisions/` - Detailed decision records

### Proof Links
All evidence files link to:
- Google Drive proof files (screenshots, API responses)
- Evidence Index spreadsheet (master tracking)

## Evidence Index
📊 **Master Spreadsheet**: [Evidence Index](https://docs.google.com/spreadsheets/d/1PRfN9zLXXdpBkD6m5rpsauOkWRufSwheqxFPh5omEM0/edit)

Contains:
- All integration proofs
- Timestamp tracking
- Status updates
- Scope changes (L1 → L2)

## Recent Evidence (2025-11-12)

### Repository Cleanup Analysis
**File**: `REPOSITORY_CLEANUP_ANALYSIS.md`  
**Type**: Strategy & Decision  
**Status**: Under Review (PR #95)

**Summary**: Comprehensive analysis of all 5 repositories in edri2or-commits account:
- ✅ **make-ops-clean**: Keep as SSOT (current)
- 🟢 **edri2or-mcp**: Migrate (unique Flask API server)
- 🔴 **make-ops**: Archive (legacy)
- 🟡 **gmail-auto-watch**: Delete (empty)
- 🟡 **edri2or-automation**: Delete (empty)

**Key Finding**: edri2or-mcp contains production-ready Google Workspace HTTP API that complements existing MCP protocol clients.

**Next**: Awaiting Or's approval to execute migration and cleanup.

---

## Adding New Evidence

1. **Create proof file** (screenshot/JSON)
2. **Upload to Drive** (Evidence_Store folder)
3. **Add row to Evidence Index**
4. **Create/update markdown** in this folder
5. **Reference in DECISION_LOG.md** if decision-related

## Evidence Types

- 🔑 **Authentication**: Tokens, scopes, permissions
- 📡 **API Responses**: Status codes, payloads
- 📊 **State Snapshots**: System state at key moments
- 📝 **Decisions**: Why we chose X over Y
- ⚠️ **Incidents**: Errors, rollbacks, fixes
- 🏗️ **Strategy**: Repository structure, architecture decisions

---
**Created**: 2025-11-12  
**Last Updated**: 2025-11-12  
**Purpose**: Centralize all system evidence