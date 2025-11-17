# Google MCP OAuth Architecture (Phase G2.1)

**Document Type**: Technical Specification (OS_SAFE)  
**Created**: 2025-11-17  
**Status**: 📝 DESIGN_READY (G2.1)  
**Purpose**: Complete technical architecture for Google MCP OAuth + authentication

---

## 🎯 Executive Summary

**Goal**: Enable Claude Desktop to access Google Workspace APIs (Gmail, Drive, Calendar, Sheets, Docs) through MCP with:
- **Keyless architecture** (no static keys/credentials in code)
- **Defense in depth** (multiple security layers)
- **Full observability** (every operation logged and auditable)
- **Preparedness framework** (autonomous misuse prevention)

**Scope**: This document is OS_SAFE (planning only). No OAuth configuration, no secrets, no runtime changes.

**Guiding Principles**:
- **SRE**: Reduce toil, automate safely, monitor everything
- **Gates' Vision**: Personal agent that knows you, trusted, proactive
- **Jensen's Philosophy**: Natural language as programming interface
- **OpenAI Preparedness**: Autonomy tracking, safeguards, continuous monitoring

---

## A. Logical Architecture - High Level

### A.1 Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Or (אור)                             │
│                                                          │
│  Actions:                                                │
│  1. Strategic approval (Intent + GO)                    │
│  2. ONE-TIME OAuth consent click (Google)               │
│  3. Approval for CLOUD_OPS_HIGH operations              │
└───────────────┬─────────────────────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────────────────────┐
│              Architect GPT (Optional)                    │
│                                                          │
│  Role: High-level planning, task breakdown              │
│  Can trigger Claude via chat or structured input        │
└───────────────┬─────────────────────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────────────────────┐
│              Claude Desktop (Client)                     │
│                                                          │
│  Components:                                             │
│  ├─ MCP Client (built-in)                               │
│  ├─ CAPABILITIES_MATRIX reader                          │
│  ├─ Approval gate logic (OS_SAFE/MEDIUM/HIGH)          │
│  └─ Local filesystem access                             │
│                                                          │
│  Capabilities:                                           │
│  ├─ Read Google data (via MCP)                         │
│  ├─ Create drafts, analyze, plan (OS_SAFE)             │
│  ├─ Request approval for writes (CLOUD_OPS_HIGH)       │
│  └─ Update CAPABILITIES_MATRIX after operations        │
└───────────────┬─────────────────────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────────────────────┐
│         Google MCP Server (Extended Scopes)             │
│                                                          │
│  Location: Local process on Or's machine                │
│  Config: claude_desktop_config.json                     │
│                                                          │
│  Components:                                             │
│  ├─ OAuth 2.0 client (Google APIs)                     │
│  ├─ Token management (refresh automatically)           │
│  ├─ API request handlers (Gmail/Drive/etc)             │
│  ├─ Rate limiting & quota management                   │
│  └─ Logging & audit trail                              │
│                                                          │
│  Authentication:                                         │
│  ├─ Client ID: From GCP Secret Manager                 │
│  ├─ Client Secret: From GCP Secret Manager             │
│  └─ Refresh Token: From GCP Secret Manager             │
└───────────────┬─────────────────────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────────────────────┐
│              Google Workspace APIs                       │
│                                                          │
│  Services:                                               │
│  ├─ Gmail API (read, compose, send, organize)          │
│  ├─ Drive API (read, create, edit, share)              │
│  ├─ Docs API (read, create, edit)                      │
│  ├─ Sheets API (read, create, update)                  │
│  └─ Calendar API (read, create, edit events)           │
│                                                          │
│  Rate Limits: Per-service quotas enforced by Google    │
└─────────────────────────────────────────────────────────┘
```

### A.2 Infrastructure Layer (GitHub + GCP)

```
┌─────────────────────────────────────────────────────────┐
│                 GitHub Repository                        │
│              (edri2or-commits/make-ops-clean)           │
│                                                          │
│  Contents:                                               │
│  ├─ Workflows (.github/workflows/)                     │
│  │  ├─ google-mcp-enable-apis.yml                      │
│  │  ├─ google-mcp-create-oauth-client.yml              │
│  │  └─ google-mcp-update-config.yml                    │
│  │                                                       │
│  ├─ Config Templates (config/)                         │
│  │  └─ google-mcp-server-template.json                 │
│  │                                                       │
│  ├─ Documentation (DOCS/)                               │
│  │  ├─ CLAUDE_GOOGLE_MCP_AUTONOMY_PLAN.md              │
│  │  ├─ GOOGLE_AGENTS_RACI.md                           │
│  │  └─ GOOGLE_MCP_OAUTH_ARCH.md (this doc)            │
│  │                                                       │
│  └─ Capabilities Tracking                               │
│     ├─ CAPABILITIES_MATRIX.md                           │
│     └─ STATE_FOR_GPT_SNAPSHOT.md                        │
│                                                          │
│  Secrets (GitHub Secrets):                              │
│  └─ (none - all in GCP Secret Manager)                 │
└───────────────┬─────────────────────────────────────────┘
                │
                │ Workload Identity Federation (OIDC)
                ↓
┌─────────────────────────────────────────────────────────┐
│              GCP Project (edri2or-mcp)                   │
│                                                          │
│  IAM:                                                    │
│  ├─ Workload Identity Pool                             │
│  ├─ Service Account (github-actions@)                  │
│  └─ WIF Provider (GitHub → GCP auth)                   │
│                                                          │
│  Secret Manager:                                         │
│  ├─ google-mcp-client-id                               │
│  ├─ google-mcp-client-secret                           │
│  └─ google-mcp-refresh-token                           │
│                                                          │
│  APIs Enabled:                                           │
│  ├─ Gmail API                                           │
│  ├─ Drive API                                           │
│  ├─ Docs API                                            │
│  ├─ Sheets API                                          │
│  ├─ Calendar API                                        │
│  └─ Secret Manager API                                  │
│                                                          │
│  OAuth Consent Screen:                                  │
│  ├─ App name: "Claude Desktop MCP"                     │
│  ├─ User: Or (edri2or@gmail.com)                       │
│  └─ Scopes: (as defined in Autonomy Plan)              │
└─────────────────────────────────────────────────────────┘
```

---

## B. Authentication Pattern - Keyless Architecture

### B.1 Chosen Pattern: OAuth 2.0 + Service Account + WIF

**Philosophy**: **Zero static keys in code or config**

**Components**:

1. **OAuth 2.0 Client** (User consent):
   - **What**: Google OAuth app for user (Or) consent
   - **Where**: GCP Project `edri2or-mcp`
   - **Who Creates**: Executor via GitHub Actions (automated)
   - **Or's Role**: Clicks "Allow" once on OAuth consent screen
   - **Grants**: Access to Or's Google Workspace data
   - **Storage**: Client ID + Secret in GCP Secret Manager

2. **Service Account** (Automation):
   - **What**: Identity for GitHub Actions to access GCP
   - **Where**: GCP Project `edri2or-mcp`
   - **Who Creates**: Executor via GitHub Actions (automated)
   - **Grants**: Access to Secret Manager, enable APIs
   - **No Keys**: Uses Workload Identity Federation (WIF)

3. **Workload Identity Federation** (Keyless GitHub → GCP):
   - **What**: OIDC-based auth (no static keys)
   - **Where**: IAM Workload Identity Pool
   - **Who Creates**: Executor via GitHub Actions (automated)
   - **Grants**: GitHub Actions can call GCP APIs without keys
   - **Evidence**: Already working (WIF → Sheets verified)

### B.2 Security Comparison

| Pattern | Risk | Our Approach |
|---------|------|--------------|
| **Static Service Account Keys** | ❌ HIGH - Keys can leak, no rotation, long-lived | ❌ NOT USED |
| **OAuth without refresh rotation** | 🟡 MEDIUM - Refresh token long-lived | 🟡 ACCEPTABLE (Google manages rotation) |
| **OAuth + Secret Manager** | ✅ LOW - Centralized secret management | ✅ USED |
| **WIF (Keyless)** | ✅ LOWEST - No static credentials | ✅ USED |

**Risk Assessment**:

| Component | Risk Level | Mitigation |
|-----------|-----------|------------|
| OAuth Client ID/Secret | MED | Stored in Secret Manager, not in code |
| OAuth Refresh Token | MED | Stored in Secret Manager, auto-rotates |
| WIF Provider | LOW | Keyless, time-bound tokens |
| MCP Server Config | LOW | References secrets by name, not value |

### B.3 Why This Pattern?

**Alignment with Best Practices**:

1. **Google Cloud Security Best Practices**:
   - ✅ Avoid service account keys ([Google recommendation](https://cloud.google.com/iam/docs/best-practices-service-accounts))
   - ✅ Use Workload Identity Federation ([Google recommendation](https://cloud.google.com/iam/docs/workload-identity-federation))
   - ✅ Centralize secrets in Secret Manager

2. **OpenAI Preparedness Framework**:
   - ✅ Minimize attack surface (no keys in repos)
   - ✅ Defense in depth (multiple auth layers)
   - ✅ Auditability (all secret access logged)

3. **SRE Principles**:
   - ✅ Reduce toil (auto token refresh)
   - ✅ Eliminate manual key rotation
   - ✅ Built-in observability

### B.4 Who Does What

| Task | Or | Claude | Executor | Google |
|------|----|----|----------|---------|
| **Strategic approval** | ✅ Intent + GO | Plans | N/A | N/A |
| **Create OAuth client** | Approves | Designs workflow | ✅ Runs workflow | N/A |
| **OAuth consent click** | ✅ Clicks "Allow" | N/A | Provides URL | Validates |
| **Store secrets** | Approves | Designs workflow | ✅ Runs workflow | N/A |
| **Use MCP** | Approves ops | ✅ Calls MCP | N/A | Serves APIs |
| **Rotate secrets** | Approves (if manual) | Monitors | ✅ Automated | Auto-refresh |

**Key Principle**: Or never touches secrets manually, never opens consoles to create keys

---

## C. Primary Flows

### C.1 Flow 1: Initial OAuth Setup (ONE-TIME)

**Goal**: Get OAuth refresh token from Or's Google account

**Participants**: Executor (via GitHub Actions) + Or (one click)

**Steps**:

```
1. [EXECUTOR] Enable Google APIs
   ├─ Workflow: google-mcp-enable-apis.yml
   ├─ Action: gcloud services enable (gmail, drive, docs, sheets, calendar)
   ├─ Auth: WIF (keyless)
   └─ Output: APIs enabled confirmation

2. [EXECUTOR] Create OAuth 2.0 Client
   ├─ Workflow: google-mcp-create-oauth-client.yml
   ├─ Action: gcloud alpha iap oauth-clients create
   ├─ Params:
   │  ├─ App name: "Claude Desktop MCP"
   │  ├─ Redirect URI: http://localhost:8080
   │  └─ Scopes: (from AUTONOMY_PLAN Section C.2)
   ├─ Output: Client ID + Client Secret
   └─ Store: GCP Secret Manager
      ├─ Secret: google-mcp-client-id
      └─ Secret: google-mcp-client-secret

3. [EXECUTOR] Generate OAuth Consent URL
   ├─ Workflow: google-mcp-create-oauth-client.yml (continued)
   ├─ Action: Construct OAuth URL
   ├─ URL Format:
   │  https://accounts.google.com/o/oauth2/v2/auth
   │    ?client_id={CLIENT_ID}
   │    &redirect_uri=http://localhost:8080
   │    &response_type=code
   │    &scope={SCOPES}
   │    &access_type=offline
   │    &prompt=consent
   └─ Output: Write URL to OPS/STATUS/google-oauth-url.txt
      └─ Commit to repo (Claude can read)

4. [OR] Click OAuth Consent
   ├─ Or opens URL from OPS/STATUS/google-oauth-url.txt
   ├─ Google shows consent screen with requested scopes
   ├─ Or reviews scopes (matches AUTONOMY_PLAN)
   ├─ Or clicks "Allow"
   └─ Google redirects to http://localhost:8080?code=AUTH_CODE

5. [OR] Copy Authorization Code
   ├─ Or copies AUTH_CODE from redirect URL
   └─ Or provides code to Executor (via secure channel)

6. [EXECUTOR] Exchange Code for Tokens
   ├─ Workflow: google-mcp-complete-oauth.yml
   ├─ Input: AUTH_CODE (from Or)
   ├─ Action: POST to https://oauth2.googleapis.com/token
   ├─ Params:
   │  ├─ code: AUTH_CODE
   │  ├─ client_id: (from Secret Manager)
   │  ├─ client_secret: (from Secret Manager)
   │  ├─ redirect_uri: http://localhost:8080
   │  └─ grant_type: authorization_code
   ├─ Response:
   │  ├─ access_token: (short-lived, ~1 hour)
   │  ├─ refresh_token: (long-lived)
   │  └─ expires_in: 3600
   └─ Store: refresh_token → GCP Secret Manager
      └─ Secret: google-mcp-refresh-token

7. [EXECUTOR] Update Claude Desktop Config
   ├─ Workflow: google-mcp-update-config.yml
   ├─ Action: Update claude_desktop_config.json
   ├─ Config:
   │  {
   │    "mcpServers": {
   │      "google-workspace-extended": {
   │        "command": "npx",
   │        "args": ["-y", "@modelcontextprotocol/server-google-workspace"],
   │        "env": {
   │          "GOOGLE_CLIENT_ID": "${SECRET:google-mcp-client-id}",
   │          "GOOGLE_CLIENT_SECRET": "${SECRET:google-mcp-client-secret}",
   │          "GOOGLE_REFRESH_TOKEN": "${SECRET:google-mcp-refresh-token}"
   │        }
   │      }
   │    }
   │  }
   └─ Note: ${SECRET:...} syntax for secret reference (implementation-specific)

8. [EXECUTOR] Verify MCP Server
   ├─ Workflow: google-mcp-verify.yml
   ├─ Action: Test API call (e.g., Gmail profile)
   ├─ Success: Write to OPS/STATUS/google-mcp-ready.json
   └─ Update: CAPABILITIES_MATRIX → Status: Verified

9. [CLAUDE] Restart & Verify
   ├─ Or restarts Claude Desktop
   ├─ Claude reads OPS/STATUS/google-mcp-ready.json
   ├─ Claude updates internal state
   └─ Claude confirms to Or: "Google MCP ready"
```

**Security Notes**:
- Auth code is short-lived (~10 minutes)
- Refresh token stored securely, never in code
- Or sees consent screen ONCE
- Subsequent access uses refresh token (auto-renews)

**Observability**:
- Every step writes to OPS/STATUS/*.json
- CAPABILITIES_MATRIX updated at end
- Full audit trail in GitHub Actions logs

---

### C.2 Flow 2: Runtime Operation (Claude → Google)

**Example**: Send email (CLOUD_OPS_HIGH)

**Steps**:

```
1. [USER → CLAUDE] Request
   User: "Send this email to customer@example.com"

2. [CLAUDE] Check Capabilities
   ├─ Read: CAPABILITIES_MATRIX.md
   ├─ Check: Section 3.1 Gmail → "Send email"
   ├─ Status: ✅ Verified (after G2.2 execution)
   ├─ Scope: gmail.send (confirmed available)
   └─ Risk: CLOUD_OPS_HIGH

3. [CLAUDE] Check RACI
   ├─ Read: GOOGLE_AGENTS_RACI.md
   ├─ Section: 1.3 Email Sending Operations
   ├─ "Send single email": Claude (R), GPTs GO (C)
   └─ Confirm: Claude is responsible

4. [CLAUDE] Analyze Request
   ├─ Read email context (thread, attachments, etc.)
   ├─ Generate draft email (OS_SAFE)
   ├─ Present to Or for review
   └─ Identify: CLOUD_OPS_HIGH (external impact)

5. [CLAUDE → OR] Request Approval
   Claude: "I've created this email draft:
   
   To: customer@example.com
   Subject: [Subject]
   Body: [Draft]
   
   This is a CLOUD_OPS_HIGH operation (send email).
   
   To approve, reply: מאשר שליחה
   
   Approval expires in 60 minutes."

6. [OR → CLAUDE] Approval
   Or: "מאשר שליחה"
   
   ├─ Claude logs approval:
   │  ├─ Timestamp: 2025-11-17T20:45:00Z
   │  ├─ Operation: Gmail send
   │  ├─ Target: customer@example.com
   │  ├─ Approval: "מאשר שליחה"
   │  └─ TTL: 60 minutes
   └─ Approval recorded in memory (temp)

7. [CLAUDE → MCP] Execute
   ├─ MCP Call: gmail.send
   ├─ Params:
   │  ├─ to: customer@example.com
   │  ├─ subject: [Subject]
   │  ├─ body: [Draft]
   │  └─ threadId: [if reply]
   │
   ├─ MCP Server:
   │  ├─ Reads: GOOGLE_REFRESH_TOKEN (from Secret Manager)
   │  ├─ Gets: Fresh access_token (from Google OAuth)
   │  ├─ Calls: Gmail API (send message)
   │  └─ Logs: Operation to MCP log
   │
   └─ Response:
      ├─ Success: { messageId: "abc123", threadId: "xyz789" }
      └─ Or error: { error: "rate_limit_exceeded" }

8. [CLAUDE] Log Operation
   ├─ Create: OPS/LOGS/google-operations.jsonl
   ├─ Entry:
   │  {
   │    "timestamp": "2025-11-17T20:45:05Z",
   │    "operation": "gmail.send",
   │    "risk_level": "CLOUD_OPS_HIGH",
   │    "approval": "מאשר שליחה",
   │    "approved_by": "Or",
   │    "target": "customer@example.com",
   │    "message_id": "abc123",
   │    "status": "success"
   │  }
   └─ Commit to repo (permanent audit trail)

9. [CLAUDE] Update State
   ├─ Update: STATE_FOR_GPT_SNAPSHOT.md
   │  └─ "Last Google operation: gmail.send (success)"
   │
   └─ Confirm to Or:
      "✅ Email sent successfully
       Message ID: abc123
       Logged to: OPS/LOGS/google-operations.jsonl"

10. [CLAUDE] Rate Limit Check
    ├─ Check: Gmail API quota (250 units/user/second)
    ├─ Current usage: [tracked in memory or external]
    └─ If approaching limit: Warn Or, suggest delay
```

**Safeguards**:
- ✅ Approval required for CLOUD_OPS_HIGH
- ✅ 60-minute TTL on approval
- ✅ Full audit trail (logged operation)
- ✅ Rate limit monitoring
- ✅ Error handling (if API fails, no silent failure)

**OS_SAFE Alternative** (if no approval):
```
If Or doesn't approve:
├─ Claude saves draft to Drive (OS_SAFE)
├─ Or can review later
└─ No email sent
```

---

### C.3 Flow 3: Capability Update & Preparedness

**Goal**: Track every capability expansion with safeguards

**Trigger Events**:
1. New scope added (e.g., gmail.send → gmail.settings.basic)
2. New operation tested (e.g., first successful email send)
3. Limitation discovered (e.g., rate limit hit)
4. Security issue (e.g., suspicious activity detected)

**Steps**:

```
1. [TRIGGER] Capability Change
   Example: Adding gmail.settings.basic scope
   
   ├─ Who: Executor (via workflow)
   ├─ Why: Or approved strategic expansion
   └─ What: New scope enables Gmail filter creation

2. [EXECUTOR] Update OAuth Scopes
   ├─ Workflow: google-mcp-update-scopes.yml
   ├─ Action: Regenerate OAuth client with new scopes
   ├─ Result: Or must re-consent (new permissions)
   └─ Write: OPS/STATUS/scope-update-pending.json

3. [OR] Re-Consent (if needed)
   ├─ Or clicks new consent URL
   ├─ Google shows ONLY new scopes (incremental)
   ├─ Or approves
   └─ New refresh token obtained

4. [CLAUDE] Assess Autonomy Risk
   ├─ Read: OpenAI Preparedness Framework
   ├─ Analyze: gmail.settings.basic
   │  ├─ Can create filters (auto-process emails)
   │  ├─ Can modify forwarding (data exfiltration risk)
   │  └─ Risk Level: HIGH (autonomous potential)
   │
   └─ Determine Safeguards:
      ├─ Safeguard 1: Require approval for each filter
      ├─ Safeguard 2: Log all settings changes
      ├─ Safeguard 3: Daily summary to Or
      └─ Safeguard 4: Disable forwarding by policy

5. [CLAUDE] Update CAPABILITIES_MATRIX
   ├─ File: CAPABILITIES_MATRIX.md
   ├─ Section: 3.1 Gmail
   ├─ Add Row:
   │  | Claude MCP | Gmail API | Modify settings | ✅ Verified | Create filters, labels | CLOUD_OPS_HIGH approval + cannot modify forwarding |
   │
   └─ Update Notes:
      "Safeguards: (1) Approval required, (2) Logged, (3) Daily summary, (4) Forwarding blocked"

6. [CLAUDE] Update STATE_FOR_GPT
   ├─ File: STATE_FOR_GPT_SNAPSHOT.md
   ├─ Section: Google MCP Capabilities
   ├─ Add:
      "gmail.settings.basic: Verified 2025-11-17
       - Can create filters/labels
       - Cannot modify forwarding (blocked)
       - Requires CLOUD_OPS_HIGH approval
       - All changes logged to OPS/LOGS/"
   └─ Commit

7. [CLAUDE] Document Safeguards
   ├─ Create: DOCS/GOOGLE_SAFEGUARDS.md (if doesn't exist)
   ├─ Add Entry:
      ## Gmail Settings (gmail.settings.basic)
      
      **Risk Level**: HIGH
      **Autonomous Potential**: Can auto-process all future emails
      
      **Safeguards**:
      1. **Approval Gate**: Every filter/setting change requires Or approval
      2. **Logging**: All changes logged to OPS/LOGS/google-operations.jsonl
      3. **Daily Summary**: Or receives daily email with all setting changes
      4. **Forwarding Block**: Policy prevents forwarding rule creation
      5. **Rate Limit**: Max 5 filter changes per day
      
      **Monitoring**:
      - Alert if >5 filter changes in 24h
      - Alert if forwarding rule attempted
      - Weekly review of all filters
   └─ Commit

8. [CLAUDE] Test New Capability
   ├─ Workflow: google-mcp-test-capability.yml
   ├─ Test: Create test filter (with Or approval)
   ├─ Verify: Filter created successfully
   ├─ Verify: Logged correctly
   ├─ Verify: Can be rolled back
   └─ Update MATRIX: Status → Verified

9. [CLAUDE] Observability Check
   ├─ Verify: OPS/LOGS/google-operations.jsonl exists
   ├─ Verify: All operations since G2.2 are logged
   ├─ Verify: No operations missing from log
   └─ If gap found:
      ├─ Create: OPS/INCIDENTS/missing-logs-[date].md
      ├─ Investigate: Why logging failed
      ├─ Fix: Ensure future operations log
      └─ Report to Or

10. [CLAUDE → OR] Capability Ready
    Claude: "✅ New capability verified: Gmail Settings
    
    Scope: gmail.settings.basic
    Risk: HIGH (autonomous potential)
    Safeguards: 5 layers (see DOCS/GOOGLE_SAFEGUARDS.md)
    Status: Verified
    
    Updated:
    - CAPABILITIES_MATRIX.md
    - STATE_FOR_GPT_SNAPSHOT.md
    - DOCS/GOOGLE_SAFEGUARDS.md
    
    Ready to use with CLOUD_OPS_HIGH approval."
```

**Key Preparedness Principles**:

1. **Capability = Capability + Safeguards**
   - Never add capability without safeguards
   - Document safeguards before using capability

2. **Observability = Non-Negotiable**
   - Every operation logged
   - Logs committed to repo (permanent)
   - Weekly review of all logs

3. **Defense in Depth**:
   - Approval gate (human in loop)
   - Rate limiting (prevent abuse)
   - Policy blocks (hard constraints)
   - Monitoring (detect anomalies)
   - Audit trail (forensics)

4. **Continuous Tracking**:
   - Weekly: Review all Google operations
   - Monthly: Assess autonomy risk level
   - Quarterly: Update safeguards based on usage

---

## D. Workflow Skeletons (OS_SAFE - NOT EXECUTED)

### D.1 Workflow: Enable Google APIs

**File**: `.github/workflows/google-mcp-enable-apis.yml`

```yaml
name: Google MCP - Enable APIs

on:
  workflow_dispatch:
    inputs:
      apis:
        description: 'APIs to enable (comma-separated)'
        required: false
        default: 'gmail,drive,docs,sheets,calendar'

permissions:
  contents: write  # Write status files
  id-token: write  # WIF auth

jobs:
  enable-apis:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Authenticate to GCP via WIF
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ vars.WIF_PROVIDER_PATH }}
          service_account: ${{ vars.GCP_SA_EMAIL }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Enable APIs
        id: enable
        run: |
          PROJECT_ID="edri2or-mcp"
          APIS="${{ github.event.inputs.apis }}"
          
          # Convert comma-separated to array
          IFS=',' read -ra API_ARRAY <<< "$APIS"
          
          ENABLED=()
          FAILED=()
          
          for api in "${API_ARRAY[@]}"; do
            API_NAME="${api}.googleapis.com"
            echo "Enabling $API_NAME..."
            
            if gcloud services enable "$API_NAME" --project="$PROJECT_ID"; then
              ENABLED+=("$api")
              echo "✅ $api enabled"
            else
              FAILED+=("$api")
              echo "❌ $api failed"
            fi
          done
          
          # TODO: Write results to JSON for Claude
          # TODO: Update CAPABILITIES_MATRIX
          
          echo "enabled=${ENABLED[*]}" >> $GITHUB_OUTPUT
          echo "failed=${FAILED[*]}" >> $GITHUB_OUTPUT

      - name: Write status file
        run: |
          mkdir -p OPS/STATUS
          
          cat > OPS/STATUS/google-apis-enabled.json <<EOF
          {
            "task": "google-mcp-enable-apis",
            "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
            "status": "complete",
            "enabled": "${{ steps.enable.outputs.enabled }}",
            "failed": "${{ steps.enable.outputs.failed }}",
            "project": "edri2or-mcp",
            "workflow_run": "${{ github.run_id }}"
          }
          EOF
          
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add OPS/STATUS/google-apis-enabled.json
          git commit -m "[skip ci] Google MCP: APIs enabled"
          git push
```

**TODO for Executor**:
- Replace PROJECT_ID with actual value
- Verify WIF_PROVIDER_PATH and GCP_SA_EMAIL variables exist
- Test with dry-run first

---

### D.2 Workflow: Create OAuth Client

**File**: `.github/workflows/google-mcp-create-oauth-client.yml`

```yaml
name: Google MCP - Create OAuth Client

on:
  workflow_dispatch:
    inputs:
      app_name:
        description: 'OAuth app name'
        required: false
        default: 'Claude Desktop MCP'

permissions:
  contents: write
  id-token: write

jobs:
  create-oauth:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Authenticate to GCP via WIF
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ vars.WIF_PROVIDER_PATH }}
          service_account: ${{ vars.GCP_SA_EMAIL }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Create OAuth 2.0 Client
        id: oauth
        run: |
          PROJECT_ID="edri2or-mcp"
          APP_NAME="${{ github.event.inputs.app_name }}"
          
          # TODO: Create OAuth client
          # gcloud alpha iap oauth-clients create \
          #   --project="$PROJECT_ID" \
          #   --display_name="$APP_NAME"
          
          # TODO: Get client ID and secret from output
          # CLIENT_ID="..."
          # CLIENT_SECRET="..."
          
          echo "client_id=TODO" >> $GITHUB_OUTPUT
          echo "client_secret=TODO" >> $GITHUB_OUTPUT

      - name: Store secrets in Secret Manager
        run: |
          PROJECT_ID="edri2or-mcp"
          CLIENT_ID="${{ steps.oauth.outputs.client_id }}"
          CLIENT_SECRET="${{ steps.oauth.outputs.client_secret }}"
          
          # TODO: Store in Secret Manager
          # echo -n "$CLIENT_ID" | gcloud secrets create google-mcp-client-id \
          #   --project="$PROJECT_ID" \
          #   --data-file=-
          
          # echo -n "$CLIENT_SECRET" | gcloud secrets create google-mcp-client-secret \
          #   --project="$PROJECT_ID" \
          #   --data-file=-

      - name: Generate OAuth consent URL
        id: consent
        run: |
          CLIENT_ID="${{ steps.oauth.outputs.client_id }}"
          
          # Scopes from AUTONOMY_PLAN Section C.2
          SCOPES="https://www.googleapis.com/auth/gmail.readonly"
          SCOPES="$SCOPES https://www.googleapis.com/auth/gmail.modify"
          SCOPES="$SCOPES https://www.googleapis.com/auth/gmail.compose"
          SCOPES="$SCOPES https://www.googleapis.com/auth/gmail.send"
          SCOPES="$SCOPES https://www.googleapis.com/auth/drive.readonly"
          SCOPES="$SCOPES https://www.googleapis.com/auth/drive.file"
          SCOPES="$SCOPES https://www.googleapis.com/auth/drive"
          SCOPES="$SCOPES https://www.googleapis.com/auth/documents"
          SCOPES="$SCOPES https://www.googleapis.com/auth/spreadsheets"
          SCOPES="$SCOPES https://www.googleapis.com/auth/calendar.readonly"
          SCOPES="$SCOPES https://www.googleapis.com/auth/calendar.events"
          SCOPES="$SCOPES https://www.googleapis.com/auth/calendar"
          
          # URL-encode scopes
          ENCODED_SCOPES=$(echo "$SCOPES" | sed 's/ /%20/g')
          
          CONSENT_URL="https://accounts.google.com/o/oauth2/v2/auth"
          CONSENT_URL="$CONSENT_URL?client_id=$CLIENT_ID"
          CONSENT_URL="$CONSENT_URL&redirect_uri=http://localhost:8080"
          CONSENT_URL="$CONSENT_URL&response_type=code"
          CONSENT_URL="$CONSENT_URL&scope=$ENCODED_SCOPES"
          CONSENT_URL="$CONSENT_URL&access_type=offline"
          CONSENT_URL="$CONSENT_URL&prompt=consent"
          
          echo "consent_url=$CONSENT_URL" >> $GITHUB_OUTPUT

      - name: Write OAuth URL for Or
        run: |
          mkdir -p OPS/STATUS
          
          cat > OPS/STATUS/google-oauth-url.txt <<EOF
          OAuth Consent URL for Or:
          
          ${{ steps.consent.outputs.consent_url }}
          
          Instructions:
          1. Open this URL in your browser
          2. Review the requested scopes
          3. Click "Allow"
          4. Copy the authorization code from the redirect URL
          5. Provide code to Executor for next step
          EOF
          
          cat > OPS/STATUS/google-oauth-status.json <<EOF
          {
            "task": "google-mcp-create-oauth",
            "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
            "status": "awaiting_or_consent",
            "consent_url": "${{ steps.consent.outputs.consent_url }}",
            "next_step": "Or must click consent URL and provide auth code",
            "workflow_run": "${{ github.run_id }}"
          }
          EOF
          
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add OPS/STATUS/google-oauth-*
          git commit -m "[skip ci] Google MCP: OAuth client created, awaiting Or consent"
          git push
```

**TODO for Executor**:
- Verify `gcloud alpha iap oauth-clients create` command syntax
- Test Secret Manager write permissions
- Ensure consent URL is accessible to Or

---

### D.3 Workflow: Complete OAuth Flow

**File**: `.github/workflows/google-mcp-complete-oauth.yml`

```yaml
name: Google MCP - Complete OAuth Flow

on:
  workflow_dispatch:
    inputs:
      auth_code:
        description: 'Authorization code from Or (after consent)'
        required: true

permissions:
  contents: write
  id-token: write

jobs:
  complete-oauth:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Authenticate to GCP via WIF
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ vars.WIF_PROVIDER_PATH }}
          service_account: ${{ vars.GCP_SA_EMAIL }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Get client credentials from Secret Manager
        id: secrets
        run: |
          PROJECT_ID="edri2or-mcp"
          
          CLIENT_ID=$(gcloud secrets versions access latest \
            --secret="google-mcp-client-id" \
            --project="$PROJECT_ID")
          
          CLIENT_SECRET=$(gcloud secrets versions access latest \
            --secret="google-mcp-client-secret" \
            --project="$PROJECT_ID")
          
          echo "::add-mask::$CLIENT_ID"
          echo "::add-mask::$CLIENT_SECRET"
          
          echo "client_id=$CLIENT_ID" >> $GITHUB_OUTPUT
          echo "client_secret=$CLIENT_SECRET" >> $GITHUB_OUTPUT

      - name: Exchange auth code for tokens
        id: tokens
        run: |
          AUTH_CODE="${{ github.event.inputs.auth_code }}"
          CLIENT_ID="${{ steps.secrets.outputs.client_id }}"
          CLIENT_SECRET="${{ steps.secrets.outputs.client_secret }}"
          
          # Exchange code for tokens
          RESPONSE=$(curl -s -X POST https://oauth2.googleapis.com/token \
            -d "code=$AUTH_CODE" \
            -d "client_id=$CLIENT_ID" \
            -d "client_secret=$CLIENT_SECRET" \
            -d "redirect_uri=http://localhost:8080" \
            -d "grant_type=authorization_code")
          
          # Extract tokens
          ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
          REFRESH_TOKEN=$(echo "$RESPONSE" | jq -r '.refresh_token')
          EXPIRES_IN=$(echo "$RESPONSE" | jq -r '.expires_in')
          
          echo "::add-mask::$ACCESS_TOKEN"
          echo "::add-mask::$REFRESH_TOKEN"
          
          echo "refresh_token=$REFRESH_TOKEN" >> $GITHUB_OUTPUT
          echo "expires_in=$EXPIRES_IN" >> $GITHUB_OUTPUT

      - name: Store refresh token in Secret Manager
        run: |
          PROJECT_ID="edri2or-mcp"
          REFRESH_TOKEN="${{ steps.tokens.outputs.refresh_token }}"
          
          # Create or update secret
          if gcloud secrets describe google-mcp-refresh-token --project="$PROJECT_ID" &>/dev/null; then
            echo "$REFRESH_TOKEN" | gcloud secrets versions add google-mcp-refresh-token \
              --project="$PROJECT_ID" \
              --data-file=-
          else
            echo "$REFRESH_TOKEN" | gcloud secrets create google-mcp-refresh-token \
              --project="$PROJECT_ID" \
              --data-file=-
          fi

      - name: Write completion status
        run: |
          mkdir -p OPS/STATUS
          
          cat > OPS/STATUS/google-oauth-complete.json <<EOF
          {
            "task": "google-mcp-complete-oauth",
            "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
            "status": "complete",
            "tokens_obtained": true,
            "refresh_token_stored": true,
            "next_step": "Update Claude Desktop config",
            "workflow_run": "${{ github.run_id }}"
          }
          EOF
          
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add OPS/STATUS/google-oauth-complete.json
          git commit -m "[skip ci] Google MCP: OAuth flow complete, tokens stored"
          git push
```

**TODO for Executor**:
- Verify curl and jq are available in runner
- Test Secret Manager read/write flow
- Handle error cases (invalid code, expired code)

---

### D.4 gcloud Commands Reference (NOT TO RUN YET)

**Enable APIs**:
```bash
gcloud services enable gmail.googleapis.com --project=edri2or-mcp
gcloud services enable drive.googleapis.com --project=edri2or-mcp
gcloud services enable docs.googleapis.com --project=edri2or-mcp
gcloud services enable sheets.googleapis.com --project=edri2or-mcp
gcloud services enable calendar-json.googleapis.com --project=edri2or-mcp
gcloud services enable secretmanager.googleapis.com --project=edri2or-mcp
```

**Create Service Account** (for Executor, if needed):
```bash
gcloud iam service-accounts create google-mcp-executor \
  --display-name="Google MCP Executor" \
  --project=edri2or-mcp
```

**Grant Permissions**:
```bash
# Secret Manager access
gcloud projects add-iam-policy-binding edri2or-mcp \
  --member="serviceAccount:google-mcp-executor@edri2or-mcp.iam.gserviceaccount.com" \
  --role="roles/secretmanager.admin"

# Service enablement
gcloud projects add-iam-policy-binding edri2or-mcp \
  --member="serviceAccount:google-mcp-executor@edri2or-mcp.iam.gserviceaccount.com" \
  --role="roles/serviceusage.serviceUsageAdmin"
```

**Bind to WIF** (keyless GitHub → GCP):
```bash
# Already exists from previous WIF setup
# No additional binding needed if using same service account
```

---

## E. Autonomy Risks & Safeguards

### E.1 Autonomous Misuse Scenarios

**Aligned with OpenAI Preparedness Framework** - Model Autonomy category

| Scenario | Risk | Likelihood | Impact | Mitigation |
|----------|------|-----------|---------|------------|
| **Mass email spam** | Claude sends 1000s of emails autonomously | LOW | HIGH | Rate limit (10 emails/hour), approval required |
| **Data exfiltration** | Claude shares Drive files externally | LOW | CRITICAL | Approval required, logging, no auto-share |
| **Calendar bombing** | Claude creates 100s of fake events | LOW | MEDIUM | Rate limit (5 events/hour), approval for invites |
| **Settings tampering** | Claude modifies Gmail filters/forwarding | MEDIUM | HIGH | Block forwarding, approval for filters |
| **Credential leakage** | OAuth tokens exposed in logs/files | LOW | CRITICAL | Secrets in Secret Manager, masked in logs |
| **Approval bypass** | Claude tricks Or into approving malicious action | MEDIUM | HIGH | Clear approval prompts, 60-min TTL |
| **Scope creep** | Gradual expansion of permissions without review | MEDIUM | MEDIUM | Quarterly capability review, explicit scope list |

---

### E.2 System-Level Safeguards

#### Layer 1: Capability Tracking

**CAPABILITIES_MATRIX as Guardrail**:
- Every new capability requires MATRIX update
- MATRIX includes "Safeguards" column (required)
- No capability marked "Verified" without tested safeguards
- Claude checks MATRIX before every operation

**Example Entry**:
```markdown
| Claude MCP | Gmail API | Send email | ✅ Verified | Full send capability | CLOUD_OPS_HIGH approval required + rate limit (10/hour) + logged + 60-min TTL |
```

#### Layer 2: Approval Templates

**Structured Approval Prompts**:
```
Operation: {operation_name}
Risk Level: {OS_SAFE | CLOUD_OPS_MEDIUM | CLOUD_OPS_HIGH}
Target: {recipient/file/calendar}
Details: {what will happen}
Reversible: {yes/no}

To approve, reply: {approval_phrase}
Approval expires in: {minutes}

[Preview of action]
```

**No Ambiguous Approvals**:
- Or must see EXACTLY what will happen
- Or must use EXPLICIT approval phrase
- Or's "yes" is NOT sufficient for CLOUD_OPS_HIGH

#### Layer 3: Rate Limiting

**Per-Service Limits**:
| Service | Operation | Limit | Period | Override |
|---------|-----------|-------|--------|----------|
| Gmail | Send email | 10 | Hour | Or approval |
| Gmail | Create filter | 5 | Day | Or approval |
| Drive | Share external | 3 | Day | Or approval |
| Calendar | Create event w/ invites | 10 | Hour | Or approval |
| Sheets | Bulk update | 50 | Hour | Or approval |

**Implementation**:
- In-memory counter (resets on Claude restart)
- Persistent counter in OPS/RATE_LIMITS.json
- Alert Or at 80% of limit
- Hard block at 100% (requires Or override)

#### Layer 4: Mandatory Logging

**Every CLOUD_OPS_MEDIUM/HIGH operation**:
```json
{
  "timestamp": "2025-11-17T20:45:05Z",
  "operation": "gmail.send",
  "risk_level": "CLOUD_OPS_HIGH",
  "approval": "מאשר שליחה",
  "approved_by": "Or",
  "target": "customer@example.com",
  "details": {
    "subject": "Re: Project Update",
    "body_preview": "Thank you for your email...",
    "attachments": [],
    "thread_id": "xyz789"
  },
  "result": {
    "status": "success",
    "message_id": "abc123",
    "sent_at": "2025-11-17T20:45:06Z"
  },
  "metadata": {
    "claude_session": "session-123",
    "workflow_run": null,
    "duration_ms": 1234
  }
}
```

**Log Storage**:
- File: `OPS/LOGS/google-operations.jsonl` (append-only)
- Committed to repo (permanent audit trail)
- Weekly summary generated for Or
- Retained indefinitely (no automatic deletion)

#### Layer 5: Policy Blocks

**Hard Constraints** (enforced at MCP server level):
```python
# Pseudo-code for MCP server
BLOCKED_OPERATIONS = [
    "gmail.users.settings.updateForwarding",  # No email forwarding
    "gmail.users.settings.updateAutoReply",    # No auto-responders (without approval)
    "drive.permissions.create(role='writer', anyone=True)"  # No public write access
]

def before_api_call(operation, params):
    if operation in BLOCKED_OPERATIONS:
        raise BlockedOperationError(f"{operation} is blocked by policy")
    
    if is_bulk_operation(params) and not has_approval():
        raise ApprovalRequiredError("Bulk operations require approval")
    
    if exceeds_rate_limit(operation):
        raise RateLimitError(f"{operation} rate limit exceeded")
```

**Benefits**:
- Technical enforcement (not just policy)
- Cannot be bypassed by prompt injection
- Clear error messages to Claude
- Or doesn't need to worry about "did Claude respect the rule"

---

### E.3 Preparedness Tracking

**Monthly Autonomy Assessment**:

**Metrics to Track**:
1. **Volume**: How many Google operations per week?
2. **Approval Rate**: What % require CLOUD_OPS_HIGH approval?
3. **Error Rate**: What % of operations fail?
4. **Safeguard Triggers**: How many times were safeguards triggered (rate limits, policy blocks)?
5. **Scope Usage**: Which scopes are used most?

**Review Questions**:
1. Are we using capabilities as intended (per RACI)?
2. Are safeguards sufficient (no bypasses discovered)?
3. Are there emerging risk patterns (e.g., approval fatigue)?
4. Should we tighten or relax any safeguards?

**Escalation Criteria**:
- **Yellow**: >50 operations/week OR >5 safeguard triggers/week
- **Orange**: >100 operations/week OR >10 safeguard triggers/week OR any policy bypass attempt
- **Red**: Credential leak OR unauthorized external access OR >20 safeguard triggers/week

**Actions per Level**:
- **Yellow**: Weekly review meeting with Or
- **Orange**: Temporarily reduce capabilities, increase approval requirements
- **Red**: Immediately revoke OAuth tokens, conduct security audit

---

### E.4 CAPABILITIES_MATRIX Integration

**Enhanced Format**:

```markdown
### 3.1 Gmail

| From | To | Capability | Status | Details | Safeguards | Last Verified |
|------|----|-----------| -------|---------|------------|---------------|
| Claude MCP | Gmail API | Send email | ✅ Verified | Full send | CLOUD_OPS_HIGH approval + rate limit (10/h) + logged + 60min TTL + no forwarding | 2025-11-17 |
```

**New Column**: **Safeguards** (mandatory for all Verified capabilities)

**Safeguard Types** (documented in each row):
1. **Approval**: Which risk level (OS_SAFE/MEDIUM/HIGH)
2. **Rate Limit**: Numerical limit + period
3. **Logging**: Always/conditional
4. **TTL**: Approval expiration
5. **Policy Blocks**: What's forbidden

**Example**: Full Gmail entry with safeguards
```markdown
| Claude MCP | Gmail API | Send email | ✅ Verified | Send on Or's behalf | (1) CLOUD_OPS_HIGH approval required (2) Rate: 10/hour (3) Logged to OPS/LOGS/ (4) Approval TTL: 60min (5) Cannot modify forwarding rules | 2025-11-17 |
```

---

## F. Security & Privacy

### F.1 Secret Storage

**Where Secrets Live**:
| Secret | Storage | Access Method | Rotation |
|--------|---------|---------------|----------|
| OAuth Client ID | GCP Secret Manager | WIF → gcloud | Manual (rarely needed) |
| OAuth Client Secret | GCP Secret Manager | WIF → gcloud | Manual (rarely needed) |
| OAuth Refresh Token | GCP Secret Manager | WIF → gcloud | Auto (Google manages) |
| Access Token | MCP Server (memory) | Auto-refresh | Every 1 hour |

**What's NOT stored as secrets**:
- ❌ API responses (may contain user data)
- ❌ Email content in logs (only metadata)
- ❌ Drive file content (only IDs/names)

### F.2 Data Minimization

**Logging Principle**: Log **what happened**, not **full content**

**Email Send Log** (good):
```json
{
  "operation": "gmail.send",
  "to": "customer@example.com",
  "subject": "Re: Project Update",
  "body_preview": "Thank you for your email... [first 50 chars]",
  "attachments_count": 0,
  "thread_id": "xyz789"
}
```

**Email Send Log** (bad - too much):
```json
{
  "operation": "gmail.send",
  "to": "customer@example.com",
  "subject": "Re: Project Update",
  "body": "[FULL 10KB EMAIL BODY]",  // ❌ Too much
  "attachments": "[BASE64 DATA]"      // ❌ Way too much
}
```

### F.3 Audit Trail

**What's Auditable**:
1. Every OAuth consent (who, when, which scopes)
2. Every secret access (via GCP Secret Manager audit logs)
3. Every API call (via MCP server logs + OPS/LOGS/)
4. Every approval (timestamp, operation, Or's phrase)
5. Every safeguard trigger (rate limit, policy block)

**Audit Log Locations**:
- GitHub Actions logs (workflow execution)
- GCP Audit Logs (Secret Manager access, API enablement)
- OPS/LOGS/google-operations.jsonl (Claude's operations)
- MCP Server logs (local, if implemented)

---

## G. Observability

### G.1 Lessons from github-executor-api

**What Went Wrong**:
- Workflow ran, but no status files created
- Claude had no way to verify deployment
- "Runtime Unverified" became permanent state

**How Google MCP Avoids This**:
1. **Every workflow MUST write to OPS/STATUS/**
2. **Status files committed to repo** (Claude can read)
3. **Failure cases also write status** (don't go silent)
4. **Health checks built into verification workflows**

### G.2 Status File Pattern

**Standard Status File**:
```json
{
  "task": "google-mcp-{operation}",
  "timestamp": "2025-11-17T20:45:00Z",
  "status": "success|failed|pending",
  "details": {
    // Operation-specific details
  },
  "next_step": "Human-readable next action",
  "workflow_run": "github.com/.../actions/runs/123",
  "errors": []  // If failed
}
```

**Location**: `OPS/STATUS/google-{operation}.json`

**Committed**: Every workflow commits status before exit

### G.3 Health Checks

**After G2.2 execution**, verify:

1. **OAuth Consent**: Check `OPS/STATUS/google-oauth-complete.json`
2. **MCP Server**: Claude calls health check endpoint
3. **API Access**: Claude attempts read-only operation (Gmail profile)
4. **Capabilities**: CAPABILITIES_MATRIX updated with ✅ Verified

**If ANY check fails**:
- Write to `OPS/INCIDENTS/google-mcp-health-{date}.md`
- Alert Or immediately
- Block CLOUD_OPS_HIGH operations until resolved

---

## H. Next Steps (Phase G2.2)

### H.1 Prerequisites

**Before executing G2.2**:
- [x] G1 Complete (Autonomy Plan, RACI)
- [x] G2.1 Complete (this OAuth Architecture)
- [ ] Or approves G2.1 design
- [ ] Executor identified and authorized
- [ ] Or ready for one-time OAuth consent click

### H.2 Execution Plan (Future)

**Phase G2.2 tasks** (CLOUD_OPS_HIGH, requires Executor):

1. Enable Google APIs (workflow)
2. Create OAuth client (workflow)
3. Or clicks consent URL (one-time)
4. Exchange code for tokens (workflow)
5. Store tokens in Secret Manager (workflow)
6. Update Claude Desktop config (manual or workflow)
7. Restart Claude Desktop
8. Verify MCP server (workflow + Claude)
9. Update CAPABILITIES_MATRIX (Claude)
10. Celebrate 🎉

**Estimated Time**: 30-60 minutes (mostly automated)

### H.3 "First Capability" Approach

**After G2.2**, don't use ALL scopes immediately.

**Recommended**: Start with **Gmail Drafts Only**
- Scope: `gmail.readonly` + `gmail.compose` (already have readonly)
- Risk: LOW (drafts are not sent)
- Value: HIGH (can draft contextual emails)
- Test: Create draft, verify in Gmail
- Safeguards: None needed (OS_SAFE operation)

**Then gradually add**:
1. Gmail send (with safeguards)
2. Drive create (in designated folder)
3. Calendar read/create
4. Sheets update (tracking logs)
5. Full suite (after all working)

**Benefits**:
- Easier to debug (one capability at a time)
- Build confidence incrementally
- Validate safeguards work
- Less overwhelming for Or

---

## I. Summary & Recommendations

### I.1 Chosen Architecture

**OAuth 2.0 + Service Account + WIF**:
- ✅ Keyless (no static credentials)
- ✅ Proven pattern (WIF already working)
- ✅ Centralized secrets (Secret Manager)
- ✅ Auditable (GCP audit logs)
- ✅ Automated (workflows handle setup)
- ✅ Or-friendly (one OAuth click)

### I.2 Top 3 Safeguards

**1. Approval Gate (CLOUD_OPS_HIGH)**:
- Every sensitive operation requires explicit Or approval
- Clear prompt showing exact action
- 60-minute TTL (approval expires)
- Logged with approval phrase

**2. Rate Limiting**:
- Hard limits per service (Gmail: 10 sends/hour, etc.)
- Alert at 80%, block at 100%
- Override requires Or approval
- Prevents runaway automation

**3. Mandatory Logging**:
- Every CLOUD_OPS_MEDIUM/HIGH operation logged
- Logs committed to repo (permanent audit trail)
- Weekly summary for Or
- Safeguard trigger logging

**Honorable Mention**: Policy Blocks (technical enforcement of forbidden operations)

### I.3 Status

**Phase G2.1**: ✅ COMPLETE (OS_SAFE)
- Full technical architecture documented
- Workflows designed (skeletons)
- Safeguards defined
- Observability built-in
- Ready for Or's approval

**Next**: Or reviews → Approves → Phase G2.2 (CLOUD_OPS_HIGH execution)

---

**Maintained by**: Claude  
**Created**: 2025-11-17  
**Status**: DESIGN_READY, awaiting Or approval  
**Risk Level**: NONE (OS_SAFE documentation)
