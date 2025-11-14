# Trigger Layer Design - Autonomous Cloud Shell Execution

**Goal**: Enable Claude to trigger Cloud Shell workflows without manual intervention

**Created**: 2025-11-14  
**Status**: Design Phase → Awaiting Approval for Implementation

---

## 🎯 Requirements

1. **Zero Manual Intervention**: Claude writes request → Actions runs → Claude reads results
2. **Uses Existing Capabilities**: GitHub MCP, Filesystem, existing workflows
3. **Audit Trail**: Every request tracked and logged
4. **Approval Gates**: Can integrate אור's approval where needed

---

## 🏗️ Architecture Options Evaluated

### Option 1: Job Request File Pattern ⭐ **RECOMMENDED**

**Concept**: Claude writes a job request file to repo → Workflow monitors for new files → Executes automatically

**Flow**:
```
Claude writes → jobs/requests/cloud-shell-req-<timestamp>.json
                    ↓
GitHub Actions (on push) → Detects new request file
                    ↓
Reads request → Validates → Executes cloud-shell-exec.yml
                    ↓
Writes result → jobs/results/cloud-shell-res-<timestamp>.json
                    ↓
Claude reads result → Processes output
```

**Pros**:
- ✅ Uses existing GitHub MCP (create_or_update_file)
- ✅ Fully auditable (all requests in repo)
- ✅ Simple to implement (file-based queue)
- ✅ Works with existing workflow_dispatch
- ✅ No API extensions needed
- ✅ Zero new dependencies

**Cons**:
- Slight delay (push → workflow trigger ~5-10s)
- Creates files in repo (manageable with cleanup)

**Verdict**: Best fit for current capabilities

---

### Option 2: Repository Dispatch Pattern

**Concept**: Claude sends repository_dispatch event → Workflow triggers

**Status**: ❌ **Not Currently Viable**
- GitHub MCP doesn't support repository_dispatch
- Would require MCP extension
- Less visible audit trail

---

### Option 3: Webhook-Based (External Service)

**Status**: ❌ **Not Recommended**
- Adds external dependency
- Unnecessary complexity
- Authentication overhead

---

## 🎖️ Selected Design: Job Request File Pattern

### Directory Structure

```
make-ops-clean/
├── jobs/
│   ├── requests/      # Claude writes here
│   │   └── cloud-shell-req-<timestamp>.json
│   ├── results/       # Workflows write here
│   │   └── cloud-shell-res-<timestamp>.json
│   └── archive/       # Optional cleanup destination
```

### Request Format

```json
{
  "type": "cloud-shell",
  "timestamp": "2025-11-14T12:30:45Z",
  "request_id": "cloud-shell-req-20251114_123045",
  "command": "echo 'Hello Cloud Shell' && whoami && pwd",
  "project_id": "edri2or-mcp",
  "requester": "claude",
  "priority": "normal",
  "metadata": {
    "session_id": "optional",
    "tags": ["test", "validation"]
  }
}
```

### Result Format

```json
{
  "request_id": "cloud-shell-req-20251114_123045",
  "status": "success",
  "timestamp_start": "2025-11-14T12:30:50Z",
  "timestamp_end": "2025-11-14T12:31:15Z",
  "execution_time_seconds": 25,
  "github_run_id": "12345678",
  "github_run_url": "https://github.com/.../actions/runs/12345678",
  "exit_code": 0,
  "output_preview": "Hello Cloud Shell\nedri2@...\n/home/edri2",
  "output_file": "artifacts/cloud-shell/cloud_shell_output_20251114_123045.txt",
  "artifact_name": "cloud-shell-execution-20251114_123045",
  "errors": []
}
```

---

## 🔄 Claude's Execution Loop

### Step 1: Create Request

```python
# Pseudocode
timestamp = get_utc_timestamp()
request_id = f"cloud-shell-req-{timestamp}"

request = {
    "type": "cloud-shell",
    "timestamp": timestamp_iso,
    "request_id": request_id,
    "command": user_command,
    "project_id": "edri2or-mcp",
    "requester": "claude"
}

github.create_or_update_file(
    path=f"jobs/requests/{request_id}.json",
    content=json_dumps(request),
    message=f"L1: Cloud Shell request - {request_id}"
)
```

### Step 2: Poll for Result

```python
# Wait for result file to appear
max_wait = 300  # 5 minutes
interval = 10   # 10 seconds

for attempt in range(max_wait // interval):
    result = github.get_file_contents(
        path=f"jobs/results/{request_id}.json"
    )
    if result.exists:
        break
    sleep(interval)
```

### Step 3: Process Result

```python
result_data = json.parse(result.content)

if result_data.status == "success":
    output = result_data.output_preview
    # Optional: download full artifact
else:
    handle_error(result_data.errors)
```

### Step 4: Cleanup (Optional)

```python
# Archive old requests/results
github.move_file(
    from=f"jobs/requests/{request_id}.json",
    to=f"jobs/archive/requests/{request_id}.json"
)
```

---

## 🏗️ Implementation Components

### Component 1: Job Dispatcher Workflow

**File**: `.github/workflows/job-dispatcher.yml`

**Purpose**: Monitor `jobs/requests/` and trigger appropriate workers

**Triggers**:
```yaml
on:
  push:
    paths:
      - 'jobs/requests/**/*.json'
```

**Logic**:
1. Detect new request file
2. Parse and validate JSON
3. Determine job type (cloud-shell, secret-manager, etc.)
4. Trigger appropriate workflow via workflow_call
5. Monitor execution
6. Write result to `jobs/results/`

---

### Component 2: Enhanced cloud-shell-exec.yml

**Changes Needed**:
1. Accept job request as input (instead of direct command)
2. Read from `jobs/requests/<id>.json`
3. Execute command
4. Write result to `jobs/results/<id>.json`
5. Include metadata (run_id, artifact name, etc.)

---

### Component 3: Result Writer

**Responsibility**: Standardize result format across all job types

**Fields**:
- Request metadata (ID, timestamp, command)
- Execution metadata (run_id, duration, exit_code)
- Output summary (preview + artifact references)
- Error details (if any)

---

## 📊 Comparison: Current vs Proposed

| Aspect | Current (Manual Trigger) | Proposed (Job File) |
|--------|-------------------------|---------------------|
| **Trigger** | Manual click or API | Auto (file push) |
| **Audit** | GitHub Actions logs | Git history + logs |
| **Approval** | Permissions-based | Can add PR workflow |
| **Claude Access** | No automated path | Full automation |
| **Visibility** | UI-only | Files in repo |
| **Multi-Session** | Lost between sessions | Persistent |
| **Queue** | N/A | Natural (file-based) |

---

## 🔐 Security & Validation

### Request Validation

```yaml
# In job-dispatcher.yml
- name: Validate request
  run: |
    # Check JSON schema
    # Validate command (no injection)
    # Check project_id allowlist
    # Verify requester identity
    # Rate limit check (optional)
```

### Approval Gate (Optional)

For sensitive operations, can require:
1. Request file → Opens PR automatically
2. אור reviews PR
3. Merge triggers execution

**Example**:
```yaml
# High-security commands
if: contains(request.command, 'delete') || contains(request.command, 'drop')
# Require manual approval
```

---

## 🚀 Implementation Plan

### Phase 1: Core Infrastructure (Priority: HIGH)

**Tasks**:
1. ✅ Create `jobs/requests/` directory (via GitHub MCP)
2. ✅ Create `jobs/results/` directory
3. ⏳ Build `job-dispatcher.yml` workflow
4. ⏳ Enhance `cloud-shell-exec.yml` for job pattern
5. ⏳ Test with manual request file

**Deliverables**:
- Working job queue system
- Request/result file flow operational
- End-to-end test successful

**Time Estimate**: 2-3 hours  
**Blocker**: None

---

### Phase 2: Claude Integration (Priority: HIGH)

**Tasks**:
1. Document request format
2. Create helper templates
3. Test Claude → Cloud Shell loop
4. Verify result parsing

**Deliverables**:
- Claude can trigger jobs autonomously
- Results automatically retrieved
- Full loop verified

**Time Estimate**: 1 hour  
**Blocker**: Phase 1 complete

---

### Phase 3: Enhancements (Priority: MEDIUM)

**Tasks**:
1. Add cleanup workflow (archive old jobs)
2. Implement job status tracking
3. Add retry mechanism
4. Build job queue dashboard (optional)

**Deliverables**:
- Automated cleanup
- Better observability
- Resilient execution

**Time Estimate**: 2-3 hours  
**Blocker**: Phase 2 complete

---

## 💡 Key Advantages

### 1. **Full Transparency**
Every Cloud Shell request = Git commit  
Complete audit trail by design

### 2. **Approval Integration**
Can easily add PR-based approval for sensitive commands  
```
Request → PR → Review → Merge → Execute
```

### 3. **Multi-Instance Support**
Multiple Claudes can queue jobs simultaneously  
File system naturally handles concurrency

### 4. **Persistence**
Jobs survive across Claude sessions  
Can resume/retry failed jobs

### 5. **Extensibility**
Same pattern works for:
- Secret Manager operations
- GCS file operations
- BigQuery queries
- Any GCP service

---

## 📈 Success Metrics

**After Implementation**:
- ✅ Claude can trigger Cloud Shell commands autonomously
- ✅ Results retrieved automatically (no manual download)
- ✅ Complete audit trail (every request tracked)
- ✅ Zero manual intervention required
- ✅ Pattern reusable for other GCP services

**Status Update in CAPABILITIES_MATRIX**:
```
Claude → Cloud Shell (Automated exec): 🟡 Partial → ✅ Verified
```

---

## 🎬 Next Steps

### Immediate Action: Implementation

**Awaiting Approval**: Proceed with Phase 1?

**If Approved**:
1. Create directory structure
2. Build job-dispatcher.yml
3. Enhance cloud-shell-exec.yml
4. Test end-to-end
5. Document usage
6. Update CAPABILITIES_MATRIX

**Time to Full Automation**: ~4-6 hours of development

---

## 📝 Summary

**Pattern Selected**: Job Request File ✅  
**Advantages**: 
- Zero new dependencies
- Uses existing GitHub MCP
- Superior audit trail
- Extensible to other services

**Status**: Design complete, ready for implementation  
**Blocker**: Awaiting אור's approval to proceed  
**Confidence**: High (builds on proven patterns)

---

**Created**: 2025-11-14  
**Author**: Claude  
**Approval Gate**: אור  
**Next**: Implementation Phase 1
