# CAPABILITIES MATRIX - Drive Create Strategy Doc Entry (OS_SAFE)

**Updated**: 2025-11-17  
**Addition**: Drive Create Strategy Doc capability (PILOT_DESIGNED)

---

## 3.2 Drive - New: Create Strategy Doc

### Complete Drive Capabilities Table

| From | To | Capability | Status | Details | Safeguards | Last Verified | Reference |
|------|----|-----------| -------|---------|------------|---------------|-----------|
| Claude MCP | Drive API | Search files | ✅ Verified | Full Drive search | None (OS_SAFE) | 2025-11-13 | Native integration |
| Claude MCP | Drive API | Fetch documents | ✅ Verified | Read Google Docs content | None (OS_SAFE) | 2025-11-13 | Native integration |
| Claude MCP | Drive API | **Create strategy doc** | **🔄 PILOT_DESIGNED** | **Create strategic documents in dedicated folder** | **(1) Outline review (conversational) (2) Rate: 20 docs/hour (soft, optional) (3) Log: Standard to OPS/LOGS/ (4) Scope: drive.file + docs.file (app-created only) (5) Blocks: No external share, no delete existing, dedicated folder only** | **Pending G2.4** | **[PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md](DOCS/PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md)** |
| Claude MCP | Drive API | Edit documents | 🔄 G2.4 | Requires `docs.file` scope | CLOUD_OPS_MEDIUM + logged | Pending G2.4 | AUTONOMY_PLAN |
| Claude MCP | Drive API | Share documents | 🔄 G2.5 | Requires permissions API | CLOUD_OPS_HIGH + approval | Pending G2.5 | AUTONOMY_PLAN |

---

## Drive Create Strategy Doc - Detailed Entry

**Capability**: Create strategic documents in Google Drive  
**Status**: 🔄 PILOT_DESIGNED (Phase G2.1-Pilot)  
**Operational After**: G2.4 execution (OAuth scope expansion + testing)

### What it does

**Primary function**:
- Creates strategic documents in Google Drive
- Gathers context from multiple sources (repo, emails, meetings, local files)
- Proposes document outline for Or's review
- Generates organized content with formatting
- Stores in dedicated folder (private, no external sharing)

**Use cases**:
- Strategy documents (Q1 planning, roadmaps, initiatives)
- Technical architecture docs (system design, decisions)
- Project retrospectives (lessons learned, improvements)
- Internal reports (analysis, research, findings)

**Not supported** (different flows):
- Bulk document generation → GPTs GO territory per RACI
- Document editing (existing docs) → Separate capability
- External sharing → CLOUD_OPS_HIGH, separate flow

### Risk Level: OS_SAFE

**Why OS_SAFE**:
1. **No external impact**: Document stays private (no sharing)
2. **Fully reversible**: Or can delete document anytime
3. **Version history**: Google Docs tracks all changes (rollback)
4. **No data loss**: Creating new content (not modifying existing)
5. **Internal only**: No external parties affected
6. **Controlled scope**: Create in dedicated folder only

**Comparison with Gmail Send**:
| Aspect | Gmail Send (CLOUD_OPS_HIGH) | Drive Create Doc (OS_SAFE) |
|--------|----------------------------|----------------------------|
| External impact | High (recipient receives) | None (private document) |
| Reversibility | None (cannot unsend) | Full (delete anytime) |
| Affected parties | Recipients (external) | Or only (internal) |
| Safeguards | 5 layers (heavy) | 5 layers (light) |
| Approval | Explicit phrase + TTL | Outline review (conversational) |
| Rate limit | 10/hour (hard block) | 20/hour (soft, optional) |

### Safeguards (ALL 5 LAYERS - LIGHT for OS_SAFE)

**Layer 1: Approval Gate** (LIGHT)
- **Type**: Outline review (conversational)
- **Process**:
  1. Claude presents proposed document structure
  2. Or reviews (sections make sense?)
  3. Or approves: "Looks good" / "Create it" / "Approved" (any positive response)
  4. Claude creates document
- **No exact phrase required** (unlike CLOUD_OPS_HIGH)
- **No TTL** (approval doesn't expire)
- **Revisable**: Can modify outline before creation
- **Why conversational**: OS_SAFE (private, reversible)

**Layer 2: Rate Limiting** (OPTIONAL)
- **Limit**: 20 documents per hour (soft, not enforced)
- **Tracking**: None (optional)
- **Alert**: Warning if creating many docs quickly
- **No hard block** (OS_SAFE doesn't need)
- **Why optional**: Private docs, no external impact

**Layer 3: Mandatory Logging** (STANDARD)
- **Location**: OPS/LOGS/google-operations.jsonl
- **Format**: JSON (~500 bytes per doc, lighter than Gmail Send)
- **Content**:
  - Metadata (timestamp, operation, risk, status)
  - Document (title, ID, folder, URL)
  - Stats (sections, word count)
  - Context (sources consulted)
  - Approval (outline approved by Or)
- **NOT logged**: Approval phrase, TTL, rate limit (not needed for OS_SAFE)
- **Retention**: Permanent (audit trail)
- **Why standard**: Lower risk than CLOUD_OPS_HIGH

**Layer 4: Scope Limitation**
- **Scopes**: `drive.file` + `docs.file`
- **Access**: App-created files only (cannot edit Or's existing docs)
- **Cannot**:
  - Edit Or's existing documents
  - Share documents externally
  - Delete Or's files
  - Modify folder structure (outside dedicated folder)
- **Why limited**: Minimal access principle

**Layer 5: Policy Blocks** (TECHNICAL)
- **Blocked operations**:
  1. External sharing (document must stay private)
  2. Delete existing files (can only delete app-created)
  3. Modify folder structure (create in dedicated folder only)
  4. Edit existing documents (scope limited to app-created)
  5. Bulk creation without review (soft warning at 20+)
- **Enforcement**: MCP server + Claude logic + API scopes
- **Prompt injection proof**: Technical blocks

**Comparison with Gmail Send safeguards**:
| Layer | Gmail Send (CLOUD_OPS_HIGH) | Drive Create Doc (OS_SAFE) |
|-------|----------------------------|----------------------------|
| 1. Approval | Explicit phrase + TTL | Outline review (conversational) |
| 2. Rate Limit | 10/hour (hard block) | 20/hour (soft, optional) |
| 3. Logging | Detailed (~1000 bytes) | Standard (~500 bytes) |
| 4. Scope | gmail.send only | drive.file + docs.file |
| 5. Policy Blocks | No forward/BCC/bulk/schedule | No share/delete/modify existing |

**Key difference**: OS_SAFE = lighter enforcement, but all 5 layers present

### Required Scopes

**OAuth scopes**:
1. **drive.file**: Create/manage files created by app
2. **docs.file**: Add content to Google Docs

**Grants**:
- Create files/folders in Drive (app-created only)
- Add/edit content in Google Docs (app-created only)

**Does NOT grant**:
- Edit Or's existing documents
- Share documents externally
- Delete Or's files
- Access Drive settings

**Requires**: Or's one-time OAuth consent (Phase G2.4)
**Current status**: Not yet granted (pending G2.4)

### Agent Routing (per RACI)

**Per GOOGLE_AGENTS_RACI.md Section 2.2**:

| Use Case | Claude | GPTs GO | Why |
|----------|--------|---------|-----|
| Single strategic doc | **R** (Responsible) | C (Consulted) | Claude has deep context from multiple sources |
| Bulk doc generation | C (Consulted) | **R** (Responsible) | GPTs GO better for high-volume, templated docs |
| Technical architecture doc | **R** | I (Informed) | Claude can synthesize code + meetings + emails |
| Retrospective doc | **R** | I (Informed) | Claude has context from project history |

**This pilot**: Single strategic docs → Claude is Responsible

### Execution Flow Summary

```
User: "Create strategy doc for X"
  ↓
Claude checks MATRIX → Status: PILOT_DESIGNED (before G2.4) or VERIFIED (after G2.4)
  ↓
Claude checks RACI → Single doc = Claude (R)
  ↓
Claude gathers context:
  - GitHub repos (commits, issues, PRs, docs)
  - Gmail threads (decisions, discussions)
  - Calendar (meetings, planning sessions)
  - Local files (notes, drafts, references)
  - Web research (trends, best practices)
  ↓
Claude synthesizes context (key themes, decisions, data)
  ↓
Claude proposes outline (structure + sections)
  ↓
Claude presents to Or (full structure + sources)
  ↓
Or reviews & approves (conversational: "Looks good")
  ↓
Claude checks/creates dedicated folder
  ↓
Claude creates Google Doc in folder
  ↓
Claude populates sections (content + formatting)
  ↓
Claude logs (standard) to OPS/LOGS/
  ↓
Claude shares link: "✅ Created, Doc ID: doc-123"
```

### Test Plan (8 Test Cases)

**After G2.4 execution**:
1. Basic doc creation → Success
2. Context gathering (multiple sources) → Success
3. Outline revision (add/modify sections) → Success
4. External sharing blocked → Blocked
5. Delete app-created doc → Success
6. Cannot delete Or's existing doc → Blocked
7. Create outside dedicated folder → Blocked (or forced to folder)
8. Network failure → Retry offered

**Success criteria**:
- All 8 tests pass
- Safeguards work as designed
- Logging complete
- Documents private (no external sharing)
- Or can easily review/approve/edit

### Comparison: Three Pilots

| Aspect | Gmail Drafts | Gmail Send | Drive Create Doc |
|--------|--------------|------------|------------------|
| **Domain** | Gmail | Gmail | Drive + Docs |
| **Risk** | OS_SAFE | CLOUD_OPS_HIGH | OS_SAFE |
| **External impact** | None | High | None |
| **Reversibility** | Full | None | Full |
| **Approval** | Content review | "מאשר שליחה" + TTL | Outline review |
| **TTL** | None | 60 minutes | None |
| **Rate limit** | 50/h (optional) | 10/h (hard) | 20/h (optional) |
| **Logging** | Standard | Detailed | Standard |
| **Scope** | gmail.compose | gmail.send | drive.file + docs.file |
| **Policy blocks** | No send | No forward/BCC/bulk | No share/delete existing |
| **Phase** | G2.2 | G2.3 | G2.4 |

**Key insight**: Template works across domains (Gmail, Drive) and risk levels (OS_SAFE, CLOUD_OPS_HIGH)

### Complete Playbook

**Reference**: [`DOCS/PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md`](DOCS/PILOT_DRIVE_CREATE_STRATEGY_DOC_FLOW.md) (43KB)

**Contents**:
- Section 1: Intent & Classification (OS_SAFE, Drive domain)
- Section 2: Actors & RACI (Claude R for single docs)
- Section 3: Plan (19 steps including outline approval)
- Section 4: Execution Skeleton (detailed flow with context gathering)
- Section 5: Safeguards (ALL 5 layers, light for OS_SAFE)
- Section 6: Observability (standard logging, no rate tracking)
- Section 7: CAPABILITIES_MATRIX entry (this row)
- Section 8: Phase tracking & comparison with Gmail pilots
- Section 9: Summary & next steps

### Phase Tracking

**Phase G2.1-Pilot** ✅ (Complete):
- Drive Create Strategy Doc playbook created
- All safeguards documented (OS_SAFE level)
- Test plan defined
- CAPABILITIES_MATRIX entry prepared
- Status: PILOT_DESIGNED (OS_SAFE design only)

**Phase G2.4** ⏳ (Next - Requires Executor + Or):
- Expand OAuth scope (add drive.file + docs.file)
- Or clicks consent URL (one-time)
- Create dedicated folder ("Claude Strategy Docs")
- Test all 8 test cases
- Update MATRIX: PILOT_DESIGNED → VERIFIED

**Critical**: No execution until G2.4 (requires Executor + Or's GO)

---

**Maintained by**: Claude  
**Last Updated**: 2025-11-17 (Phase G2.1-Pilot)  
**Next Update**: After G2.4 execution  
**Template**: [AUTOMATION_PLAYBOOK_TEMPLATE.md](DOCS/AUTOMATION_PLAYBOOK_TEMPLATE.md)  
**Comparison**: [PILOT_GMAIL_DRAFTS_FLOW.md](DOCS/PILOT_GMAIL_DRAFTS_FLOW.md) (OS_SAFE, Gmail), [PILOT_GMAIL_SEND_FLOW.md](DOCS/PILOT_GMAIL_SEND_FLOW.md) (CLOUD_OPS_HIGH, Gmail)
