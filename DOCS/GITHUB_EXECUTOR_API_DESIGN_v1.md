# GitHub Executor API - Design Document v1

**Created**: 2025-11-18  
**Status**: DESIGN_COMPLETE → DEPLOYMENT_IN_PROGRESS  
**Purpose**: Enable GPT Unified Agent (Google + GitHub) to interact with GitHub repository safely

---

## 🎯 Executive Summary

**Goal**: Provide GPT with stable, production-grade GitHub access via Cloud Run service, similar to existing Google Workspace integration.

**Approach**: Refactor existing `cloud-run/google-workspace-github-api/` service to become comprehensive GitHub Executor V1.

**Scope**: OS_SAFE operations only (documentation, state, logs) - NO code/workflow/infrastructure changes without explicit approval.

---

## 📊 Current State Assessment

### Existing Code Analysis

**Location**: `cloud-run/google-workspace-github-api/`

**Files**:
- `index.js` (2.4KB) - Main service code
- `package.json` - Dependencies (express, axios, googleapis)
- `Dockerfile` - Container build
- `cloudbuild.yaml` - GCP Cloud Build configuration

### Issues Found

1. **⚠️ Critical Typo** (Line 37):
   ```javascript
   Accept: 'application/vund.github+json'  // WRONG
   ```
   Should be:
   ```javascript
   Accept: 'application/vnd.github+json'   // CORRECT
   ```

2. **❌ Missing Endpoint**: No `/repo/read-file` capability
   - Current: Only write operations (`/github/update-file`)
   - Needed: Read operations for full CRUD

3. **🔓 No Path Restrictions**: 
   - Current implementation allows writing to ANY path in repository
   - Risk: Could modify code, workflows, infrastructure
   - Required: Whitelist-based path validation (OS_SAFE only)

4. **🔍 Deployment Status**: Unknown
   - CAPABILITIES_MATRIX shows: "Runtime Unverified"
   - Observability gap: Cannot confirm if service is deployed
   - Planning assumption: Deploy from scratch

---

## 🏗️ Architectural Decision

### Service Identity

**Name**: GitHub Executor API v1  
**Code Location**: `cloud-run/google-workspace-github-api/` (reuse existing)  
**Deployed Name**: `github-executor-api` (or keep as-is with clear documentation)  
**Project**: `edri2or-mcp`  
**Region**: `us-central1`

**Rationale**: 
- ✅ Leverage existing infrastructure and build configuration
- ✅ Simpler than creating new service from scratch
- ✅ Faster time-to-production
- ⚠️ Note: Directory name is misleading (contains no Google Workspace operations), but code is GitHub-only

---

## 🛣️ API Design

### Endpoint 1: `/repo/read-file`

**Method**: `POST`  
**Purpose**: Read a single file from GitHub repository

**Request Body**:
```json
{
  "owner": "edri2or-commits",
  "repo": "make-ops-clean",
  "path": "DOCS/example.md",
  "ref": "main"  // optional, defaults to default branch
}
```

**Response (Success)**:
```json
{
  "status": "ok",
  "content": "# Example\n\nFile content here...",
  "path": "DOCS/example.md",
  "sha": "abc123...",
  "encoding": "utf-8"
}
```

**Response (Error)**:
```json
{
  "error": "file_not_found",
  "details": "File does not exist at path: DOCS/example.md"
}
```

**Validation**:
- ✅ Path must not contain `../` (prevent directory traversal)
- ✅ Owner/repo must be specified
- ✅ Path must be non-empty

---

### Endpoint 2: `/repo/update-doc`

**Method**: `POST`  
**Purpose**: Create or update a file in OS_SAFE paths only

**Request Body**:
```json
{
  "owner": "edri2or-commits",
  "repo": "make-ops-clean",
  "path": "DOCS/example.md",
  "content": "# Example\n\nNew content...",
  "commit_message": "docs: update example",
  "branch": "main"  // optional
}
```

**Response (Success)**:
```json
{
  "status": "ok",
  "action": "create",  // or "update"
  "commit_sha": "def456...",
  "content": {
    "path": "DOCS/example.md",
    "sha": "ghi789..."
  }
}
```

**Response (Error - Path Validation)**:
```json
{
  "error": "OUT_OF_SAFE_SCOPE",
  "details": "Path '.github/workflows/test.yml' is not in allowed safe paths",
  "allowed_paths": ["DOCS/", "logs/", "OPS/STATUS/", "STATE_FOR_GPT*"]
}
```

**Path Validation (CRITICAL)**:

**✅ ALLOWED Paths** (OS_SAFE):
```
DOCS/
logs/
OPS/STATUS/
OPS/EVIDENCE/
STATE_FOR_GPT*.md
```

**❌ FORBIDDEN Paths** (Requires explicit approval):
```
.github/workflows/
cloud-run/
*.py (application code)
*.js (application code)
*.yml (infrastructure, except task files)
*.json (configs, except status/evidence)
CAPABILITIES_MATRIX.md (major structural changes)
```

**Validation Logic**:
```javascript
function isPathSafe(path) {
  const safePrefixes = [
    'DOCS/',
    'logs/',
    'OPS/STATUS/',
    'OPS/EVIDENCE/'
  ];
  
  const safePatterns = [
    /^STATE_FOR_GPT.*\.md$/
  ];
  
  // Check prefixes
  if (safePrefixes.some(prefix => path.startsWith(prefix))) {
    return true;
  }
  
  // Check patterns
  if (safePatterns.some(pattern => pattern.test(path))) {
    return true;
  }
  
  return false;
}
```

---

### Endpoint 3: `/` (Health Check)

**Method**: `GET`  
**Purpose**: Service health verification

**Response**:
```json
{
  "service": "github-executor-api",
  "version": "1.0.0",
  "status": "ok",
  "capabilities": ["read-file", "update-doc"]
}
```

---

## 🔐 Security & Authentication

### GitHub Authentication

**Method**: GitHub Personal Access Token (PAT)  
**Storage**: GCP Secret Manager  
**Secret Name**: `github-executor-api-token` (or as defined in CAPABILITIES_MATRIX)  
**Scope Required**: `repo` (full repository access to edri2or-commits/make-ops-clean)

**Best Practices**:
- ✅ Token stored in Secret Manager only
- ✅ Never logged or returned in API responses
- ✅ Cloud Run accesses via Secret Manager integration (not ENV vars with plaintext)
- ✅ Token rotation: Manual (to be automated in future)

**Alternative (Future)**: GitHub App with fine-grained permissions

### Path Validation Security

**Defense in Depth**:
1. **Client-side**: OpenAPI schema validation (pattern matching)
2. **Server-side**: Explicit whitelist checking (primary defense)
3. **Audit**: All operations logged with path, action, timestamp

**Rejection Strategy**:
- Path outside safe scope → HTTP 403 Forbidden
- Clear error message with allowed paths
- Log attempted access for security review

---

## 📦 Deployment Architecture

### Cloud Run Configuration

**Service Name**: `github-executor-api`  
**Project**: `edri2or-mcp`  
**Region**: `us-central1`  
**Container**: Built via Cloud Build from `cloud-run/google-workspace-github-api/`

**Environment Variables**:
- `PORT`: 8080 (Cloud Run default)
- `GITHUB_TOKEN`: Injected from Secret Manager

**Resources**:
- Memory: 512Mi (can adjust based on usage)
- CPU: 1 (can adjust)
- Concurrency: 80 (default)
- Min Instances: 0 (scale to zero)
- Max Instances: 10 (adjust as needed)

**Access Control**:
- Authentication: Allow unauthenticated (API will be public)
- Rate Limiting: Consider adding (future enhancement)
- CORS: Enabled for GPT Actions

### Build & Deploy Process

**Method**: Cloud Build via `cloudbuild.yaml`

**Steps**:
1. Build container image
2. Push to Container Registry
3. Deploy to Cloud Run
4. Configure secrets
5. Verify health check

**Trigger**: Manual (for v1) - Future: CI/CD on main branch

---

## 🧪 Testing Strategy

### E2E Test Plan

**Test File**: `DOCS/GITHUB_EXECUTOR_API_TEST.md`

**Test Cases**:

1. **Health Check**:
   - `GET /`
   - Expected: 200 OK, service info

2. **Read File (Valid)**:
   - `POST /repo/read-file`
   - Path: `CAPABILITIES_MATRIX.md`
   - Expected: 200 OK, file content

3. **Read File (Not Found)**:
   - `POST /repo/read-file`
   - Path: `DOCS/nonexistent.md`
   - Expected: 404 or appropriate error

4. **Update Doc (Safe Path)**:
   - `POST /repo/update-doc`
   - Path: `DOCS/GITHUB_EXECUTOR_API_TEST.md`
   - Expected: 200 OK, commit created

5. **Update Doc (Unsafe Path)**:
   - `POST /repo/update-doc`
   - Path: `.github/workflows/test.yml`
   - Expected: 403 Forbidden, `OUT_OF_SAFE_SCOPE` error

**Test Execution**: Documented in `DOCS/GITHUB_EXECUTOR_API_TEST_RUN.md`

---

## 📖 OpenAPI Specification

**File**: `DOCS/GITHUB_EXECUTOR_API_OPENAPI.yaml`

**Key Elements**:
- OpenAPI 3.1.0
- Two operations: `readFile`, `updateDocFile`
- Clear schemas for requests/responses
- Security scheme: None (public API, path validation is defense)
- Server URL: Dynamic (from Cloud Run deployment)

**Usage**: Import into GPT Actions editor for seamless integration

---

## 🔄 Integration with CAPABILITIES_MATRIX

### New Capability Entry

**Name**: `GPT_UNIFIED_AGENT_GITHUB_DOCS_V1`

**Properties**:
- **Status**: READY (after deployment)
- **From**: GPT Unified Agent (Google + GitHub)
- **To**: GitHub Repository (`edri2or-commits/make-ops-clean`)
- **Capability**: Read full repo + Write OS_SAFE paths only
- **Method**: Cloud Run API (github-executor-api)
- **Claude at Runtime**: No (GPT operates independently)
- **GPT-CEO Ready**: Yes (primary use case)
- **Human Approval**: No (OS_SAFE), Yes (code/infra)

**Details**:
- Service URL: `https://github-executor-api-<hash>-uc.a.run.app` (from deployment)
- OpenAPI: `DOCS/GITHUB_EXECUTOR_API_OPENAPI.yaml`
- Auth: GitHub PAT via Secret Manager (name: `github-executor-api-token`)

**Limitations**:
- Write operations limited to: DOCS/, logs/, OPS/STATUS/, STATE_FOR_GPT*
- No code, workflow, or infrastructure changes
- No PR creation/merge (future enhancement)

---

## 📋 Migration from Previous Mechanisms

### Status of Alternatives

**GPT Agent Mode** (Direct):
- Status: ✅ Still available
- Use Case: Interactive sessions with Claude
- Limitation: Not suitable for GPT autonomous operations

**GPT Tasks Executor** (GitHub Actions):
- Status: 🟡 Broken runtime
- Decision: Mark as DEPRECATED (not removed)
- Future: May be revived if needed

**Cloud Run API** (Previous):
- Status: 🔍 Runtime unverified
- Decision: This IS the Cloud Run API (refactored)
- Version: v1 (formalized and documented)

---

## 🚀 Deployment Checklist

**Pre-Deployment** (OS_SAFE):
- [x] Design document created
- [x] Code refactored (typo fixed, endpoints added)
- [x] Path validation implemented
- [x] OpenAPI spec created
- [x] CAPABILITIES_MATRIX updated (planned)

**Deployment** (CLOUD_OPS_HIGH):
- [ ] GitHub PAT created/verified
- [ ] Secret stored in Secret Manager
- [ ] Cloud Build triggered
- [ ] Service deployed to Cloud Run
- [ ] Secret Manager integration configured
- [ ] Health check verified

**Post-Deployment** (Verification):
- [ ] E2E test executed
- [ ] Test results documented
- [ ] CAPABILITIES_MATRIX updated (actual)
- [ ] GPT Action configured
- [ ] Or verification complete

---

## 🎓 GPT Integration Guide (Preview)

### Action Configuration

**Action Name**: `GitHub Executor`

**Description**: 
```
Read and update documentation files in the edri2or-commits/make-ops-clean repository. 
Safe for OS_SAFE operations (DOCS, logs, state files). 
Cannot modify code or infrastructure.
```

**OpenAPI URL**: 
```
https://raw.githubusercontent.com/edri2or-commits/make-ops-clean/main/DOCS/GITHUB_EXECUTOR_API_OPENAPI.yaml
```

**Example Usage**:
```
User: "Update DOCS/STATUS.md with today's deployment notes"

GPT → calls updateDocFile:
{
  "owner": "edri2or-commits",
  "repo": "make-ops-clean",
  "path": "DOCS/STATUS.md",
  "content": "# Status - 2025-11-18\n\nDeployment completed successfully...",
  "commit_message": "docs: update deployment status"
}

→ File updated, commit created
→ GPT confirms to user
```

---

## 📊 Success Criteria

**v1 is successful when**:
- ✅ Service deployed and accessible
- ✅ Health check returns 200 OK
- ✅ Can read any file from repository
- ✅ Can write to OS_SAFE paths (DOCS/, logs/, etc.)
- ✅ Blocks writes to unsafe paths (code, workflows)
- ✅ GPT Action configured and operational
- ✅ CAPABILITIES_MATRIX reflects READY status
- ✅ E2E test passes
- ✅ Or verification complete

**Future Enhancements** (v2+):
- PR creation/management
- Branch operations
- Issue creation
- Wider path permissions (with approval)
- Rate limiting
- Metrics/monitoring
- GitHub App authentication

---

## 📝 Document History

### 2025-11-18 - Initial Creation
- Architectural decision: Refactor existing service
- API design: 2 endpoints (read-file, update-doc)
- Security model: Path whitelisting
- Deployment strategy: Cloud Run with Secret Manager
- Integration: CAPABILITIES_MATRIX + GPT Actions

---

**Maintained by**: Claude  
**Approved by**: אור  
**Status**: DESIGN_COMPLETE → DEPLOYMENT_IN_PROGRESS  
**Next**: Code refactoring (Step 2)
