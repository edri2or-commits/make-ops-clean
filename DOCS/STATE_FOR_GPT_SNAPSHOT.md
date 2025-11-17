# STATE FOR GPT (Snapshot) – v3 (Post Phase 1.1/1.2 Diagnosis)

**Date**: 2025-11-17  
**Phase**: Post L2 Runtime Diagnosis  
**Status**: Documentation synchronized with reality

---

## 1. Repo Overview

- **owner/repo**: `edri2or-commits/make-ops-clean`
- **default_branch**: `main`
- **visibility**: public
- **purpose**: תשתית MCP + GPT-Agent לאוטונומיה (GitHub + GCP + Google + Windows)

---

## 2. Key Files (GPT-facing)

- **`CAPABILITIES_MATRIX.md`**  
  מפת היכולות והרמות (OS_SAFE / CLOUD_OPS_HIGH) לכל שכבה (GitHub, Google, GCP, Windows/MCP וכו').  
  **Updated 2025-11-17**: הוסף Section 10 על Cloud Run APIs

- **`MCP_GPT_CAPABILITIES_BRIDGE.md`**  
  מדריך עבודה לסוכני GPT: איך לקרוא את המטריצה, איך לגזור ממנה החלטות, ואיך לעדכן אותה.

- **`GPT_REPO_ACCESS_BRIDGE.md`**  
  מידע על החיבור של GPT/Agents לריפו (`make-ops-clean`) – מה מותר לעשות, איך לגשת, ומה הנתיב המועדף.

- **`DOCS/STATE_FOR_GPT_SNAPSHOT.md`** (הקובץ הזה)  
  צילום מצב קנוני ל-GPT על הריפו, היכולות, וה-Backlog.

- **`DOCS/L2_RUNTIME_DIAGNOSIS.md`** ⭐ **NEW**  
  אבחון מפורט של מצב Cloud Run APIs, BUS, ו-github-executor-api (Phase 1.1, 2025-11-17).

- **`DOCS/AGENT_GPT_MASTER_DESIGN.md`**  
  Design ראשי ל-GPT-Agent בשכבת GitHub:
  - תפקידים: Or / GPT-Agent / Claude / Agents אחרים
  - מקורות אמת: Snapshot, Matrix, Bridge
  - מודל תהליך: Intent → Plan → Approval → Execute → Reflect

- **`DOCS/GPT_TASKS_SPEC.md`**  
  פורמט משימות YAML ל-GPT Tasks Executor (עדיין ברמת Design; runtime בעייתי).

- **`.github/workflows/gpt_tasks_executor.yml`**  
  Workflow שמיועד להריץ משימות YAML מ-`.chatops/gpt_tasks/` – כרגע מעוצב אבל runtime בפועל לא יציב.

- **`gpt_agent/github_agent.py`**  
  סוכן GitHub Agent **DRY RUN** (מחזיר Plan בלבד, ללא כתיבה).

---

## 3. Current Capabilities Status (High Level)

### GitHub – Direct Writes / Docs

- **Direct writes (Docs/State)** דרך GPT/Agents → ✅ **Verified (OS_SAFE)**
- **Evidence**:
  - `1c64fd5` – `DOCS/GPT_EXECUTOR_TEST.md`
  - `81cba22` – `DOCS/STATE_FOR_GPT_SNAPSHOT.md`
  - `52e5e39` – `STATE_FOR_GPT.md` update
  - `92de8df` – `MCP_GPT_CAPABILITIES_BRIDGE.md`
  - `b10769b` – `DOCS/AGENT_GPT_MASTER_DESIGN.md`
  - `047eea8` – `gpt_agent/github_agent.py` + workflow

### GitHub – GPT GitHub Agent DRY RUN

- **Agent**: `gpt_agent/github_agent.py`
- **Status**: ✅ **Implemented (OS_SAFE, DRY RUN only)**
- **Functionality**: Reads Snapshot + Matrix + Design → Returns Plan (text only, no file writes/commits)

### GitHub – GPT Tasks Executor (YAML via Actions)

- **Design**: `DOCS/GPT_TASKS_SPEC.md` + `.github/workflows/gpt_tasks_executor.yml`
- **Runtime**: 🟡 **Partial/Broken**
  - Manual dispatch shows "successfully requested" but no actual runs appear
  - **Do not rely on** `.chatops/gpt_tasks/*.yml` as execution channel
- **Status**: Backlog for debugging

### Cloud Run APIs – github-executor-api

⭐ **CRITICAL CLARIFICATION (2025-11-17)**:

**Previously documented as**:
- Two separate services: `google-workspace-api` AND `github-executor-api`

**Actual reality**:
- **ONE service** with confusing naming:
  - **Code location**: `cloud-run/google-workspace-github-api/`
  - **Deployed name**: `github-executor-api`
  - **Actual functionality**: GitHub operations ONLY

**Implemented Endpoints** (verified in code):
1. `GET /` - Health check
2. `POST /github/update-file` - Create/update GitHub files
   - Required: `repo`, `branch`, `path`, `content`, `message`
   - Auth: `GITHUB_TOKEN` environment variable

**Known Issues**:
- ⚠️ **Code typo**: Accept header uses `vund.github` instead of `vnd.github` (line 37)

**Deployment Status**: 🔍 **UNVERIFIED**
- Cannot confirm if service is deployed without Cloud Run access
- GPTs GO reports 404 on `/github/update-file`
- Possible causes: service not deployed, URL mismatch, missing env vars

**BUS System**: ❌ **NOT IMPLEMENTED**
- NO `/bus/process-next-task` endpoint in code
- NO Sheet integration
- NO polling mechanism
- BUS exists only in documentation, not in actual implementation

**Google Workspace Operations**: ❌ **NOT IMPLEMENTED**
- Despite directory name, NO Google Workspace endpoints exist
- Service implements GitHub operations ONLY

**Evidence**: Full code analysis in `DOCS/L2_RUNTIME_DIAGNOSIS.md`

### Google Workspace API (Separate Service)

**Clarification**: The `google-workspace-api` referenced in previous docs is likely a **different service** (not in this repo) that GPTs GO uses for Google operations (Gmail/Sheets/Docs/Drive/Calendar).

- **Status**: Reportedly working (per Or's description)
- **Location**: Not in make-ops-clean repo
- **Functionality**: Google Workspace operations for GPTs GO

### Google / GCP / Windows MCP

- **MCP Servers**: Active (Gmail/Drive/Calendar READ-only, Filesystem, PowerShell)
- **GitHub Actions → GCP**: ✅ Working (WIF, Sheets append verified)
- **Status**: Documented in CAPABILITIES_MATRIX Section 3 (Google Layer) and Section 4 (GCP Layer)

---

## 4. Open TODOs / Backlog (GitHub-oriented)

### Priority 1: github-executor-api Recovery

**Goal**: Fix GPTs GO → GitHub loop

**Tasks**:
1. ⏳ Verify deployment status (via Workflow - CLOUD_OPS_HIGH)
2. ⏳ Fix Accept header typo (PR - CLOUD_OPS_HIGH)
3. ⏳ Decision: BUS vs Direct vs Abandon
4. ⏳ Deploy/test service if needed
5. ⏳ Update GPTs GO OpenAPI with correct URL

**Documentation**: See `DOCS/GITHUB_EXECUTOR_RECOVERY_PLAN.md` (Phase 2, in progress)

### Priority 2: GPT Tasks Executor Debug

**Goal**: Fix or replace broken YAML→Executor loop

**Tasks**:
1. ⏳ Debug why workflow_dispatch doesn't create runs
2. ⏳ OR: Replace with alternative mechanism
3. ⏳ Update STATUS to ✅ when working

### Priority 3: Documentation Sync

✅ **COMPLETE** (Phase 1.2, 2025-11-17):
- Updated CAPABILITIES_MATRIX with Section 10 (Cloud Run APIs)
- Updated STATE_FOR_GPT_SNAPSHOT (this file)
- Created L2_RUNTIME_DIAGNOSIS.md

### Priority 4: Google MCP Full Setup

**Goal**: Enable Claude write operations to Google Workspace

**Status**: Planned (see CAPABILITIES_MATRIX Priority 0)

**Approach**: Separate MCP server with extended OAuth scopes

---

## 5. Architecture Clarifications

### Cloud Run Services (Current Understanding)

```
┌─────────────────────────────────────────────────────────────┐
│ In make-ops-clean repo:                                      │
│                                                               │
│  cloud-run/google-workspace-github-api/                     │
│  │                                                            │
│  ├─ index.js (ONE service with TWO endpoints)               │
│  │  ├─ GET  /                                                │
│  │  └─ POST /github/update-file                             │
│  │                                                            │
│  └─ Deployed as: github-executor-api                        │
│     Region: us-central                                       │
│     Project: edri2or-mcp                                     │
│     Status: 🔍 Unverified                                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ NOT in make-ops-clean repo:                                  │
│                                                               │
│  google-workspace-api (separate service)                    │
│  │                                                            │
│  └─ Google Workspace operations for GPTs GO                 │
│     (Gmail, Sheets, Docs, Drive, Calendar)                   │
│     Status: Reportedly working                               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Integration Flows

**GPTs GO → Google Workspace** ✅ Working:
```
GPTs GO → google-workspace-api → Google APIs
```

**GPTs GO → GitHub** ❌ Broken (404):
```
GPTs GO → github-executor-api (/github/update-file) → 404
         (possible causes: not deployed, wrong URL, missing auth)
```

**BUS System** ❌ Not Implemented:
```
GPTs GO → github-executor-api (/bus/process-next-task)
         └─ DOES NOT EXIST (design only)
```

---

## 6. GPT GitHub Agent – DRY RUN (Current Contract)

**Purpose**: Plan generator only (no execution)

**Inputs**:
- `DOCS/AGENT_GPT_MASTER_DESIGN.md`
- `DOCS/STATE_FOR_GPT_SNAPSHOT.md`
- `CAPABILITIES_MATRIX.md`
- `--intent` parameter

**Output**: Textual Plan only

**Limitations**:
- ❌ Does NOT write files
- ❌ Does NOT create commits
- ❌ Does NOT trigger workflows

**Use Case**: Analysis and "What-If" planning before actual changes

---

## 7. Key Changes from Previous Versions

### v3 (2025-11-17) - Phase 1.1/1.2 Complete

**Major Updates**:
1. ⭐ **Service naming clarified**: ONE service (google-workspace-github-api → github-executor-api), not two
2. ⭐ **BUS status corrected**: Marked as design-only, not implemented
3. ⭐ **Endpoints documented**: Only `/` and `/github/update-file` exist in code
4. **Code issues identified**: Accept header typo (vund.github)
5. **Deployment status**: Marked as unverified (cannot confirm without Cloud Run access)
6. **Added diagnosis doc**: `DOCS/L2_RUNTIME_DIAGNOSIS.md`
7. **Backlog updated**: github-executor-api recovery now Priority 1

### v2 (2025-11-15)

- Added GPT GitHub Agent DRY RUN
- Added detailed GitHub Layer runtime notes
- GPT Tasks Executor marked as broken runtime

### v1 (2025-11-14)

- Initial snapshot
- Basic capability documentation

---

## 8. Next Steps for GPT/Agents

When working with make-ops-clean:

1. **Always read SSOT first**:
   - `CAPABILITIES_MATRIX.md` (updated 2025-11-17)
   - `DOCS/STATE_FOR_GPT_SNAPSHOT.md` (this file)
   - `DOCS/L2_RUNTIME_DIAGNOSIS.md` (for Cloud Run details)

2. **For GitHub operations**:
   - Direct writes (Docs/State): ✅ Use Agent Mode (OS_SAFE)
   - Code/Workflows: Use PRs with Or approval (CLOUD_OPS_HIGH)

3. **For Cloud Run / GPTs GO integration**:
   - Status: Under investigation (Phase 2)
   - BUS: Do not assume it exists
   - github-executor-api: Deployment status unknown

4. **Always update documentation**:
   - When capabilities change: Update CAPABILITIES_MATRIX
   - When architecture changes: Update STATE_FOR_GPT_SNAPSHOT
   - When issues found: Create evidence docs (like L2_RUNTIME_DIAGNOSIS)

---

**Maintained by**: Claude (with אור's approval)  
**Last Updated**: 2025-11-17  
**Next Review**: After Phase 2 (github-executor-api recovery)
