# CAPABILITIES MATRIX - Section 3 Google Layer (G2.1 Update)

**Last Updated**: 2025-11-17 (Phase G2.1 Complete)  
**Status**: DESIGN_READY (OAuth Architecture Complete)

---

## 3️⃣ Google Layer (via MCP) - UPDATED

**🔄 PHASE G2.1 COMPLETE** (2025-11-17)

**Status**: DESIGN_READY (OS_SAFE)  
**Current Phase**: G2.1 (OAuth Architecture Design) ✅ COMPLETE  
**Next Phase**: G2.2 (Technical Bootstrap - requires Executor + Or's OAuth consent)

**Architecture Documents**:
- **Phase G1**: [`DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md`](DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md) (28.7KB) - Vision & Scopes
- **Phase G1**: [`DOCS/GOOGLE_AGENTS_RACI.md`](DOCS/GOOGLE_AGENTS_RACI.md) (22.4KB) - Claude vs GPTs GO responsibilities
- **Phase G2.1**: [`DOCS/GOOGLE_MCP_OAUTH_ARCH.md`](DOCS/GOOGLE_MCP_OAUTH_ARCH.md) (52.6KB) - Complete OAuth & Auth architecture ⭐ NEW

**Autonomy Model**:
- **OS_SAFE**: Read, analyze, draft (no external impact)
- **CLOUD_OPS_MEDIUM**: Organize personal data (reversible)
- **CLOUD_OPS_HIGH**: Send, share, delete (external impact, requires approval)

**Authentication Pattern** (G2.1 Decision):
- **OAuth 2.0** (user consent) + **Service Account** (automation) + **WIF** (keyless GitHub→GCP)
- **Zero static keys** in code or config
- **Secrets**: Stored in GCP Secret Manager only
- **Or's Role**: ONE-TIME OAuth consent click only

**Safeguards** (Top 3):
1. **Approval Gate**: CLOUD_OPS_HIGH requires explicit Or approval (60-min TTL)
2. **Rate Limiting**: Hard limits per service (Gmail: 10 sends/hour, Drive: 3 shares/day)
3. **Mandatory Logging**: Every operation logged to `OPS/LOGS/google-operations.jsonl` (permanent audit trail)

**Recommended First Capability** (Phase G2.2):
- Start with **Gmail Drafts Only** (`gmail.compose`)
- Risk: LOW (drafts not sent)
- Value: HIGH (contextual email drafting)
- Gradually expand after validation

---

### 3.1 Gmail (Updated with Safeguards Column)

| From | To | Capability | Status | Details | Safeguards | Last Verified |
|------|----|-----------| -------|---------|------------|---------------|
| Claude MCP | Gmail API | Read profile | ✅ Verified | Get user email | None (OS_SAFE) | 2025-11-13 |
| Claude MCP | Gmail API | Search messages | ✅ Verified | Full Gmail search syntax | None (OS_SAFE) | 2025-11-13 |
| Claude MCP | Gmail API | Read threads | ✅ Verified | Full thread context | None (OS_SAFE) | 2025-11-13 |
| Claude MCP | Gmail API | List messages | ✅ Verified | Pagination supported | None (OS_SAFE) | 2025-11-13 |
| Claude MCP | Gmail API | Create drafts | 🔄 G2.2 | Requires `gmail.compose` scope | None (OS_SAFE - drafts not sent) | Pending G2.2 |
| Claude MCP | Gmail API | Organize (labels) | 🔄 G2.2 | Requires `gmail.modify` scope | CLOUD_OPS_MEDIUM + logged | Pending G2.2 |
| Claude MCP | Gmail API | Send email | 🔄 G2.3 | Requires `gmail.send` | (1) CLOUD_OPS_HIGH approval (2) Rate: 10/hour (3) Logged (4) TTL: 60min (5) No forwarding rules | Pending G2.3 |
| Claude MCP | Gmail API | Download attachments | 🔄 G2.2 | Requires expanded scopes | None (OS_SAFE - read-only) | Pending G2.2 |

**Authentication**: OAuth 2.0 via Google MCP Server (extended scopes)  
**Current Scopes**: `gmail.readonly` (native Claude integration)  
**Target Scopes**: `gmail.readonly`, `gmail.modify`, `gmail.compose`, `gmail.send`  
**Expansion Method**: Separate Google MCP server with OAuth client from GCP Secret Manager  
**Approval Gates**: 
- OS_SAFE: Read, draft, analyze (no approval needed)
- CLOUD_OPS_MEDIUM: Label, archive (Or notified)
- CLOUD_OPS_HIGH: Send (explicit "מאשר שליחה" required each time)

**Agent Routing** (per RACI):
- **Claude (R)**: Email triage, contextual drafting, single sends
- **GPTs GO (R)**: Bulk operational sends, template-based, campaigns

---

### 3.2 Google Drive (Updated with Safeguards Column)

| From | To | Capability | Status | Details | Safeguards | Last Verified |
|------|----|-----------| -------|---------|------------|---------------|
| Claude MCP | Drive API | Search files | ✅ Verified | Full query syntax | None (OS_SAFE) | 2025-11-13 |
| Claude MCP | Drive API | Fetch documents | ✅ Verified | Get document content | None (OS_SAFE) | 2025-11-13 |
| Claude MCP | Drive API | List folders | ✅ Verified | Navigate folder structure | None (OS_SAFE) | 2025-11-13 |
| Claude MCP | Drive API | Create files | 🔄 G2.2 | Requires `drive.file` scope | None (OS_SAFE - in Claude folder) | Pending G2.2 |
| Claude MCP | Drive API | Edit files | 🔄 G2.2 | Requires `drive.file` or `drive` | CLOUD_OPS_MEDIUM (shared files) + logged + version history | Pending G2.2 |
| Claude MCP | Drive API | Share files | 🔄 G2.3 | Requires `drive` | (1) CLOUD_OPS_HIGH approval (2) Rate: 3/day (3) Logged (4) No public write access | Pending G2.3 |
| Claude MCP | Drive API | Delete files | 🔄 G2.3 | Requires `drive` | (1) CLOUD_OPS_HIGH approval (2) Logged (3) Move to trash first (reversible 30 days) | Pending G2.3 |

**Authentication**: OAuth 2.0 via Google MCP Server  
**Current Scopes**: `drive.readonly` (native Claude integration)  
**Target Scopes**: `drive.readonly`, `drive.file`, `drive.metadata.readonly`, `drive` (full)  
**Expansion Method**: Same OAuth client as Gmail  
**Approval Gates**:
- OS_SAFE: Read, create in designated folders
- CLOUD_OPS_MEDIUM: Edit files (version history provides safety)
- CLOUD_OPS_HIGH: Share externally, delete (requires explicit approval)

**Agent Routing** (per RACI):
- **Claude (R)**: Strategic docs, reports, semantic search, individual file operations
- **GPTs GO (R)**: Structured data logging to Sheets, bulk operations

---

### 3.3 Google Calendar (Updated with Safeguards Column)

| From | To | Capability | Status | Details | Safeguards | Last Verified |
|------|----|-----------| -------|---------|------------|---------------|
| Claude MCP | Calendar API | List events | ✅ Verified | Full event listing | None (OS_SAFE) | 2025-11-13 |
| Claude MCP | Calendar API | Search events | ✅ Verified | Query-based search | None (OS_SAFE) | 2025-11-13 |
| Claude MCP | Calendar API | Find free time | ✅ Verified | Free/busy lookup | None (OS_SAFE) | 2025-11-13 |
| Claude MCP | Calendar API | Get event details | ✅ Verified | Full event metadata | None (OS_SAFE) | 2025-11-13 |
| Claude MCP | Calendar API | Create events (personal) | 🔄 G2.2 | Requires `calendar.events` | None (OS_SAFE - no attendees) | Pending G2.2 |
| Claude MCP | Calendar API | Create events (with invites) | 🔄 G2.2 | Requires `calendar.events` | (1) CLOUD_OPS_MEDIUM approval (2) Rate: 10/hour (3) Logged (4) Sends invites automatically | Pending G2.2 |
| Claude MCP | Calendar API | Delete events | 🔄 G2.3 | Requires `calendar` | (1) CLOUD_OPS_HIGH if attendees (2) Logged (3) Notifies attendees | Pending G2.3 |

**Authentication**: OAuth 2.0 via Google MCP Server  
**Current Scopes**: `calendar.readonly` (native Claude integration)  
**Target Scopes**: `calendar.readonly`, `calendar.events`, `calendar` (full)  
**Expansion Method**: Same OAuth client as Gmail/Drive  
**Approval Gates**:
- OS_SAFE: Read, find free time, propose meetings (no invites sent)
- CLOUD_OPS_MEDIUM: Create events with attendees (invites sent automatically)
- CLOUD_OPS_HIGH: Delete events with external attendees (notifies everyone)

**Agent Routing** (per RACI):
- **Claude (R)**: Individual scheduling, contextual decisions, analysis
- **GPTs GO (R)**: Bulk scheduling from Sheets, batch RSVP operations

---

### 3.4 Google Sheets & Docs (Updated with Safeguards Column)

| From | To | Capability | Status | Details | Safeguards | Last Verified |
|------|----|-----------| -------|---------|------------|---------------|
| Claude MCP | Sheets API | Read sheets | 🔄 G2.2 | Via MCP server expansion | None (OS_SAFE) | Pending G2.2 |
| Claude MCP | Sheets API | Create sheets | 🔄 G2.2 | Requires `spreadsheets` scope | None (OS_SAFE - new files) | Pending G2.2 |
| Claude MCP | Sheets API | Update cells | 🔄 G2.2 | Requires `spreadsheets` scope | CLOUD_OPS_MEDIUM (shared) + logged + version history | Pending G2.2 |
| Claude MCP | Docs API | Read docs | 🔄 G2.2 | Via MCP server expansion | None (OS_SAFE) | Pending G2.2 |
| Claude MCP | Docs API | Create docs | 🔄 G2.2 | Requires `docs` scope | None (OS_SAFE - new files) | Pending G2.2 |
| Claude MCP | Docs API | Edit docs | 🔄 G2.2 | Requires `docs` scope | CLOUD_OPS_MEDIUM (shared) + logged + version history | Pending G2.2 |

**Note**: Sheets currently accessible via GitHub Actions → WIF (verified)  
**Target Scopes**: `spreadsheets.readonly`, `spreadsheets`, `docs.readonly`, `docs`  
**Expansion Method**: Same OAuth client as Gmail/Drive/Calendar  
**Approval Gates**:
- OS_SAFE: Create, edit in designated locations (Claude's folder)
- CLOUD_OPS_MEDIUM: Modify shared documents (version history provides safety)
- CLOUD_OPS_HIGH: Share externally (requires explicit approval)

**Agent Routing** (per RACI):
- **Claude (R)**: Dashboard design, ad-hoc updates, analytical queries
- **GPTs GO (R)**: High-frequency logging, structured data updates, automated imports

---

### 3.5 Google MCP OAuth & Auth Architecture (NEW)

**Phase G2.1 Complete** ✅

| Component | Status | Details | Risk | Last Updated |
|-----------|--------|---------|------|--------------|
| **OAuth Architecture** | ✅ Design Complete | Full technical specification in GOOGLE_MCP_OAUTH_ARCH.md | AUTONOMY / DATA ACCESS (tracked) | 2025-11-17 |
| **Authentication Pattern** | ✅ Design Ready | OAuth 2.0 + Service Account + WIF (keyless) | LOW (no static keys) | 2025-11-17 |
| **Workflow Skeletons** | ✅ Design Ready | 4 GitHub Actions workflows designed (not executed) | NONE (OS_SAFE) | 2025-11-17 |
| **Safeguards Framework** | ✅ Design Complete | Approval gates, rate limiting, logging, policy blocks | Preparedness tracked | 2025-11-17 |
| **Observability Plan** | ✅ Design Complete | Status files, health checks, audit trails | Prevents github-executor-api issue | 2025-11-17 |

**Key Decisions** (Phase G2.1):
1. **Zero static keys**: All credentials in GCP Secret Manager
2. **WIF for GitHub→GCP**: Keyless authentication (already working)
3. **OAuth consent**: Or clicks ONCE, subsequent access uses refresh token
4. **Incremental rollout**: Start with Gmail Drafts (OS_SAFE), gradually expand

**Safeguards** (Per GOOGLE_MCP_OAUTH_ARCH.md Section E):
- **Layer 1**: Capability tracking (CAPABILITIES_MATRIX as guardrail)
- **Layer 2**: Approval templates (structured, explicit, time-bound)
- **Layer 3**: Rate limiting (per-service hard limits)
- **Layer 4**: Mandatory logging (every CLOUD_OPS_MEDIUM/HIGH)
- **Layer 5**: Policy blocks (technical enforcement of forbidden operations)

**Preparedness Tracking** (Monthly):
- Volume metrics (operations per week)
- Approval rate (% requiring CLOUD_OPS_HIGH)
- Error rate (% failed operations)
- Safeguard triggers (rate limits, policy blocks)
- Scope usage patterns

**References**:
- **Complete Architecture**: [`DOCS/GOOGLE_MCP_OAUTH_ARCH.md`](DOCS/GOOGLE_MCP_OAUTH_ARCH.md)
- **Autonomy Plan**: [`DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md`](DOCS/CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md)
- **RACI Matrix**: [`DOCS/GOOGLE_AGENTS_RACI.md`](DOCS/GOOGLE_AGENTS_RACI.md)

---

## Google MCP Roadmap (Updated)

**Phase G1** ✅ COMPLETE (2025-11-17):
- Design & Policy framework
- Autonomy model defined
- RACI matrix created
- Scope analysis complete

**Phase G2.1** ✅ COMPLETE (2025-11-17):
- OAuth architecture designed
- Authentication pattern chosen
- Workflow skeletons created
- Safeguards framework defined
- Observability plan complete

**Phase G2.2** ⏳ NEXT (Requires Executor + Or):
- Enable Google APIs (automated)
- Create OAuth client (automated)
- Or clicks consent URL (ONE-TIME)
- Store tokens in Secret Manager (automated)
- Update Claude Desktop config
- Verify MCP server functionality
- Update CAPABILITIES_MATRIX → Status: Verified

**Phase G3** ⏳ FUTURE (Controlled Autonomy):
- Operational Google access with approval gates
- Claude creates/sends with approval
- Full audit trail operational
- Monthly Preparedness reviews

**Phase G4** ⏳ FUTURE (Advanced Autonomy):
- Proactive suggestions
- Cross-service orchestration
- Pattern learning
- Predictive operations

---

**See Full Section 3**: This is an update extract. Complete CAPABILITIES_MATRIX maintained at repository root.

**Maintained by**: Claude (with Or's approval)  
**Last Updated**: 2025-11-17 (Phase G2.1 Complete)  
**Next Review**: After Phase G2.2 execution
