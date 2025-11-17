# CAPABILITIES MATRIX (SSOT)

**Single Source of Truth for Claude's Operational Capabilities**

**Created**: 2025-11-14  
**Last Updated**: 2025-11-17  
**Version**: 1.3.0

---

## 🎯 Purpose

This is the **master reference** for all capabilities across the Claude-Ops system. Every chat session, automation, and tool must reference this document to understand what Claude can and cannot do.

**Update Protocol**: When a new capability is added, this file MUST be updated before the capability is considered operational.

---

## 3️⃣ Google Layer (via MCP)

**🔄 PHASE G1 IN PROGRESS** (2025-11-17)

**Status**: DESIGN_IN_PROGRESS (OS_SAFE)  
**Plan Document**: [`DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md`](DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md) (28.7KB)  
**Current Phase**: G1 (Design & Policy)  
**Next Phase**: G2 (Technical Bootstrap - requires Executor + Or's OAuth consent)

**Autonomy Model**:
- **OS_SAFE**: Read, analyze, draft (no external impact)
- **CLOUD_OPS_MEDIUM**: Organize personal data (reversible)
- **CLOUD_OPS_HIGH**: Send, share, delete (external impact, requires approval)

**Recommended Scope Set** (for Phase G2):
```
gmail.readonly, gmail.modify, gmail.compose, gmail.send
drive.readonly, drive.file, drive.metadata.readonly, drive
docs, spreadsheets
calendar.readonly, calendar.events, calendar
```

See [`CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md`](DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md) Section C for full scope analysis and risk matrix.

---

### 3.1 Gmail

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | Gmail API | Read profile | ✅ Verified | Get user email | Read-only |
| Claude MCP | Gmail API | Search messages | ✅ Verified | Full Gmail search syntax | Read-only |
| Claude MCP | Gmail API | Read threads | ✅ Verified | Full thread context | Read-only |
| Claude MCP | Gmail API | List messages | ✅ Verified | Pagination supported | Read-only |
| Claude MCP | Gmail API | Create drafts | 🔄 Phase G2 | Requires `gmail.compose` scope | Planned via MCP expansion |
| Claude MCP | Gmail API | Organize (labels) | 🔄 Phase G2 | Requires `gmail.modify` scope | Planned via MCP expansion |
| Claude MCP | Gmail API | Send email | 🔄 Phase G3 | Requires `gmail.send` + CLOUD_OPS_HIGH approval | Planned via MCP expansion |
| Claude MCP | Gmail API | Download attachments | 🔄 Phase G2 | Requires expanded scopes | Planned via MCP expansion |

**Authentication**: OAuth 2.0 via native Claude integration  
**Current Scopes**: `gmail.readonly`  
**Target Scopes**: `gmail.readonly`, `gmail.modify`, `gmail.compose`, `gmail.send`  
**Expansion Method**: Separate Google MCP server OR native scope expansion  
**Approval Gates**: 
- OS_SAFE: Read, draft, analyze
- CLOUD_OPS_MEDIUM: Label, archive
- CLOUD_OPS_HIGH: Send (requires explicit approval each time)

### 3.2 Google Drive

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | Drive API | Search files | ✅ Verified | Full query syntax | Read-only |
| Claude MCP | Drive API | Fetch documents | ✅ Verified | Get document content | Read-only |
| Claude MCP | Drive API | List folders | ✅ Verified | Navigate folder structure | Read-only |
| Claude MCP | Drive API | Create files | 🔄 Phase G2 | Requires `drive.file` scope | Planned via MCP expansion |
| Claude MCP | Drive API | Edit files | 🔄 Phase G2 | Requires `drive.file` or `drive` | Planned via MCP expansion |
| Claude MCP | Drive API | Share files | 🔄 Phase G3 | Requires `drive` + CLOUD_OPS_HIGH approval | Planned via MCP expansion |
| Claude MCP | Drive API | Delete files | 🔄 Phase G3 | Requires `drive` + CLOUD_OPS_HIGH approval | Planned via MCP expansion |

**Authentication**: OAuth 2.0 via native Claude integration  
**Current Scopes**: `drive.readonly`  
**Target Scopes**: `drive.readonly`, `drive.file`, `drive.metadata.readonly`, `drive` (full)  
**Expansion Method**: Separate Google MCP server OR native scope expansion  
**Approval Gates**:
- OS_SAFE: Read, create in designated folders
- CLOUD_OPS_MEDIUM: Edit, move files
- CLOUD_OPS_HIGH: Share externally, delete (requires explicit approval)

### 3.3 Google Calendar

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | Calendar API | List events | ✅ Verified | Full event listing | Read-only |
| Claude MCP | Calendar API | Search events | ✅ Verified | Query-based search | Read-only |
| Claude MCP | Calendar API | Find free time | ✅ Verified | Free/busy lookup | Read-only |
| Claude MCP | Calendar API | Get event details | ✅ Verified | Full event metadata | Read-only |
| Claude MCP | Calendar API | Create events | 🔄 Phase G2 | Requires `calendar.events` + approval | Planned via MCP expansion |
| Claude MCP | Calendar API | Edit events | 🔄 Phase G2 | Requires `calendar.events` + approval | Planned via MCP expansion |
| Claude MCP | Calendar API | Delete events | 🔄 Phase G3 | Requires `calendar` + CLOUD_OPS_HIGH approval | Planned via MCP expansion |

**Authentication**: OAuth 2.0 via native Claude integration  
**Current Scopes**: `calendar.readonly`  
**Target Scopes**: `calendar.readonly`, `calendar.events`, `calendar` (full)  
**Expansion Method**: Separate Google MCP server OR native scope expansion  
**Approval Gates**:
- OS_SAFE: Read, find free time, propose meetings
- CLOUD_OPS_MEDIUM: Create events (sends invites automatically)
- CLOUD_OPS_HIGH: Delete events with external attendees (requires explicit approval)

### 3.4 Google Sheets & Docs

| From | To | Capability | Status | Details | Limitations |
|------|----|-----------| -------|---------|-------------|
| Claude MCP | Sheets API | Read sheets | 🔄 Phase G2 | Via MCP server expansion | Not yet configured |
| Claude MCP | Sheets API | Create sheets | 🔄 Phase G2 | Requires `spreadsheets` scope | Planned via MCP expansion |
| Claude MCP | Sheets API | Update cells | 🔄 Phase G2 | Requires `spreadsheets` scope | Planned via MCP expansion |
| Claude MCP | Docs API | Read docs | 🔄 Phase G2 | Via MCP server expansion | Not yet configured |
| Claude MCP | Docs API | Create docs | 🔄 Phase G2 | Requires `docs` scope | Planned via MCP expansion |
| Claude MCP | Docs API | Edit docs | 🔄 Phase G2 | Requires `docs` scope | Planned via MCP expansion |

**Note**: Sheets currently accessible via GitHub Actions → WIF (see section 4.1)  
**Target Scopes**: `spreadsheets.readonly`, `spreadsheets`, `docs.readonly`, `docs`  
**Expansion Method**: Same Google MCP server as Gmail/Drive/Calendar  
**Approval Gates**:
- OS_SAFE: Create, edit in designated locations
- CLOUD_OPS_MEDIUM: Modify shared documents
- CLOUD_OPS_HIGH: Share externally (requires explicit approval)

---

**Google MCP Roadmap**:
- **Phase G1** (CURRENT): Design & Policy ✅ Document created 2025-11-17
- **Phase G2** (NEXT): Technical Bootstrap (requires Executor + Or's OAuth consent)
- **Phase G3** (FUTURE): Controlled Autonomy (operational with approval gates)
- **Phase G4** (FUTURE): Advanced Autonomy (proactive, cross-service)

**See**: [`DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md`](DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md) for:
- Complete scope analysis (Section C)
- OS_SAFE vs CLOUD_OPS_HIGH boundaries (Section D)
- Risk matrix and mitigation strategies (Section H)
- Detailed execution roadmap (Section F)

---

## 📝 Update Log

### 2025-11-17 (v1.3.0) - Google MCP Autonomy Plan (Phase G1)
- **Section 3 completely rewritten**: Google Layer now reflects autonomy model
- **Added Phase G1 status**: DESIGN_IN_PROGRESS
- **Linked to AUTONOMY_PLAN**: 28.7KB comprehensive design document
- **Updated all Google subsections**: Gmail, Drive, Calendar, Sheets/Docs
- **Added approval gates**: OS_SAFE, CLOUD_OPS_MEDIUM, CLOUD_OPS_HIGH
- **Added scope recommendations**: For Phase G2 technical bootstrap
- **Added roadmap**: G1 → G2 → G3 → G4 progression
- **Version bump**: 1.2.1 → 1.3.0 (major Google section update)

---

**Note**: This is a partial update. Full CAPABILITIES_MATRIX content above this section remains unchanged. See repository for complete file.

**Maintained by**: Claude (with Or's approval)  
**Last Verified**: 2025-11-17  
**Next Review**: After Phase G1 completion
