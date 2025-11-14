# Gmail Push Automation - Phase 1 Design

**Created**: 2025-11-14  
**Status**: Design Phase  
**Scope**: Push notifications + Read-only access

---

## 🎯 Objective

Enable automated Gmail monitoring via Push notifications, integrated with the proven Job Pattern, using WIF authentication and Secret Manager for credentials.

**Phase 1 Goals**:
- Receive Gmail push notifications (new emails, label changes)
- Read email content when notified
- No sending capability (Phase 2)
- Least-privilege approach (read-only)

---

## 🏗️ Architecture Overview

### High-Level Flow

```
Gmail API watch() → Pub/Sub Topic → Poller/Handler → Job Request → Dispatcher → Read Email → Result
```

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│ Gmail (edri2or@gmail.com)                                           │
│  └─ users.watch() [7-day expiration]                               │
└────────────────────┬────────────────────────────────────────────────┘
                     │ (new mail, changes)
                     ↓
┌─────────────────────────────────────────────────────────────────────┐
│ GCP Pub/Sub Topic: gmail-notifications                             │
│  ├─ Pull Subscription: gmail-pull-sub (Phase 1)                   │
│  └─ Push Subscription: gmail-push-sub (Phase 2)                   │
└────────────────────┬────────────────────────────────────────────────┘
                     │
         ┌───────────┴──────────┐
         │                      │
    Phase 1 (Pull)         Phase 2 (Push)
         │                      │
         ↓                      ↓
┌─────────────────────┐  ┌─────────────────────┐
│ GitHub Actions      │  │ Cloud Run Service   │
│ gmail-poller.yml    │  │ gmail-push-handler  │
│ (every 5-10 min)    │  │ (real-time)         │
└─────┬───────────────┘  └─────┬───────────────┘
      │                        │
      └────────────┬───────────┘
                   ↓
        ┌─────────────────────────────┐
        │ Create Job Request          │
        │ jobs/requests/              │
        │ gmail-req-*.json            │
        └──────────┬──────────────────┘
                   ↓
        ┌─────────────────────────────┐
        │ Gmail Dispatcher            │
        │ gmail-dispatcher.yml        │
        └──────────┬──────────────────┘
                   ↓
        ┌─────────────────────────────┐
        │ Gmail Operations            │
        │ gmail-ops.yml               │
        │  ├─ WIF Auth                │
        │  ├─ Secret Manager          │
        │  └─ Gmail API Call          │
        └──────────┬──────────────────┘
                   ↓
        ┌─────────────────────────────┐
        │ Result File                 │
        │ jobs/results/               │
        │ gmail-res-*.json            │
        └─────────────────────────────┘
```

---

## 📊 Component Details

### 1. Gmail API Watch

**API Method**: `POST https://gmail.googleapis.com/gmail/v1/users/{userId}/watch`

**Request Body**:
```json
{
  "labelIds": ["INBOX"],
  "topicName": "projects/edri2or-mcp/topics/gmail-notifications"
}
```

**Response**:
```json
{
  "historyId": "1234567",
  "expiration": "1731686400000"
}
```

**Key Points**:
- **Expiration**: 7 days maximum
- **Renewal**: Required before expiration
- **Triggers**: New messages, label changes, deletions
- **Scope**: `https://www.googleapis.com/auth/gmail.readonly`

**Watch Renewal Strategy**:
- Scheduled workflow: `gmail-watch-renewal.yml`
- Runs daily (cron)
- Checks expiration in Secret Manager
- Renews if < 2 days remaining

---

### 2. GCP Pub/Sub Architecture

#### Topic Configuration

**Name**: `projects/edri2or-mcp/topics/gmail-notifications`

**IAM Permissions Required**:
```
gmail-push@gmail.google.com → roles/pubsub.publisher (Gmail service account)
<your-sa>@edri2or-mcp.iam → roles/pubsub.subscriber (consumer)
```

#### Phase 1: Pull Subscription

**Configuration**:
```yaml
name: gmail-pull-subscription
topic: projects/edri2or-mcp/topics/gmail-notifications
ackDeadlineSeconds: 600
retryPolicy:
  minimumBackoff: 10s
  maximumBackoff: 600s
messageRetentionDuration: 604800s  # 7 days
```

**Advantages**:
- ✅ No public endpoint required
- ✅ Simpler deployment (GitHub Actions only)
- ✅ Good for Phase 1

**Polling Strategy**:
- Every 5-10 minutes via scheduled workflow
- Pull up to 10 messages per poll
- Process sequentially
- Acknowledge after job creation

#### Phase 2: Push Subscription

**Configuration**:
```yaml
name: gmail-push-subscription
topic: projects/edri2or-mcp/topics/gmail-notifications
pushConfig:
  pushEndpoint: https://gmail-push-handler-xxx.run.app/push
  oidcToken:
    serviceAccountEmail: gmail-push-sa@edri2or-mcp.iam.gserviceaccount.com
    audience: https://gmail-push-handler-xxx.run.app
```

**Advantages**:
- ✅ Real-time (< 1 second latency)
- ✅ No polling required
- ✅ Automatic retry with exponential backoff

**Requirements**:
- Cloud Run service deployed
- Public endpoint with authentication
- OIDC token verification

---

### 3. Notification Handler

#### Phase 1: Pull-Based (GitHub Actions)

**Workflow**: `gmail-notification-poller.yml`

**Schedule**: `*/10 * * * *` (every 10 minutes)

**Flow**:
```yaml
1. Authenticate via WIF
2. Pull messages: gcloud pubsub subscriptions pull gmail-pull-sub --limit=10
3. For each message:
   - Parse: Extract historyId, emailAddress
   - Create job request: gmail-req-read-<historyId>.json
   - Commit to jobs/requests/
   - Acknowledge message: gcloud pubsub subscriptions ack
```

**Message Format** (from Pub/Sub):
```json
{
  "message": {
    "data": "eyJlbWFpbEFkZHJlc3MiOi...",  // base64
    "messageId": "1234567890",
    "publishTime": "2025-11-14T14:00:00Z"
  }
}
```

**Decoded Data**:
```json
{
  "emailAddress": "edri2or@gmail.com",
  "historyId": "1234567"
}
```

---

### 4. Gmail Operations Workflow

**File**: `.github/workflows/gmail-ops.yml`

**Actions Supported**:

| Action | Description | API Endpoint |
|--------|-------------|--------------|
| `read_message` | Get single message | messages.get |
| `list_messages` | List with query | messages.list |
| `get_thread` | Get full thread | threads.get |
| `get_history` | Get changes since historyId | users.history |

**Phase 1 Focus**: `read_message` and `get_history`

**workflow_call Interface**:
```yaml
inputs:
  action: read_message | list_messages | get_thread | get_history
  message_id: string (for read_message)
  query: string (for list_messages)
  thread_id: string (for get_thread)
  history_id: string (for get_history)
  user_email: string (default: from secret)
```

**Authentication Flow**:
1. WIF authenticate to GCP
2. Retrieve OAuth/SA credentials from Secret Manager
3. Construct Gmail API request
4. Execute and capture response

---

## 🔐 Authentication Strategy

### Decision Tree

```
Is edri2or@gmail.com a Workspace/G Suite account?
├─ YES → Use Service Account with Domain-Wide Delegation
│         ✅ No token expiration
│         ✅ No user interaction
│         ❌ Requires Workspace admin setup
│
└─ NO  → Use OAuth 2.0 with Refresh Token
          ✅ Works with personal Gmail
          ❌ Requires one-time manual authorization
          ❌ Token can be revoked
```

### Option 1: Service Account (If Workspace)

**Setup**:
1. Create service account: `gmail-reader@edri2or-mcp.iam.gserviceaccount.com`
2. Enable domain-wide delegation
3. In Workspace Admin Console:
   - Add Client ID
   - Grant scope: `https://www.googleapis.com/auth/gmail.readonly`
4. Store service account key in Secret Manager

**Secrets Required**:
```
gmail-service-account-key: <JSON key file>
gmail-impersonate-email: edri2or@gmail.com
```

**API Call Pattern**:
```python
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'key.json',
    scopes=['https://www.googleapis.com/auth/gmail.readonly'],
    subject='edri2or@gmail.com'  # impersonate
)
```

---

### Option 2: OAuth 2.0 (If Personal Gmail)

**Setup**:
1. Create OAuth 2.0 Client ID in GCP Console
2. One-time authorization flow:
   ```
   https://accounts.google.com/o/oauth2/auth?
     client_id=<CLIENT_ID>&
     redirect_uri=http://localhost&
     scope=https://www.googleapis.com/auth/gmail.readonly&
     response_type=code&
     access_type=offline
   ```
3. Exchange code for tokens
4. Store refresh token in Secret Manager

**Secrets Required**:
```
gmail-oauth-client-id: <client_id>
gmail-oauth-client-secret: <client_secret>
gmail-oauth-refresh-token: <refresh_token>
```

**Token Refresh Pattern**:
```bash
curl -X POST https://oauth2.googleapis.com/token \
  -d client_id=<CLIENT_ID> \
  -d client_secret=<CLIENT_SECRET> \
  -d refresh_token=<REFRESH_TOKEN> \
  -d grant_type=refresh_token
```

**Response**:
```json
{
  "access_token": "ya29.a0...",
  "expires_in": 3600,
  "scope": "https://www.googleapis.com/auth/gmail.readonly",
  "token_type": "Bearer"
}
```

---

### Recommendation

**Phase 1**: Determine account type first (manual check)

**If Workspace**: Proceed with Service Account  
**If Personal**: Proceed with OAuth 2.0

**Either way**: Store credentials in Secret Manager, access via WIF from GitHub Actions

---

## 🔄 Job Pattern Integration

### Request Format

**Filename Pattern**: `gmail-req-<action>-<timestamp>.json`

**Example - Read Message**:
```json
{
  "type": "gmail",
  "timestamp": "2025-11-14T14:30:00Z",
  "request_id": "gmail-req-read-20251114_143000",
  "action": "read_message",
  "message_id": "18c8f7d4abc12345",
  "format": "full",
  "user_email": "edri2or@gmail.com",
  "requester": "gmail-poller",
  "metadata": {
    "history_id": "1234567",
    "trigger": "pubsub_notification"
  }
}
```

**Example - Get History**:
```json
{
  "type": "gmail",
  "timestamp": "2025-11-14T14:30:00Z",
  "request_id": "gmail-req-history-20251114_143000",
  "action": "get_history",
  "history_id": "1234567",
  "user_email": "edri2or@gmail.com",
  "requester": "gmail-poller"
}
```

---

### Result Format

**Example - Success**:
```json
{
  "request_id": "gmail-req-read-20251114_143000",
  "type": "gmail",
  "action": "read_message",
  "status": "success",
  "timestamp": "2025-11-14T14:30:15Z",
  "github_run_id": "12345678",
  "github_run_url": "https://github.com/.../actions/runs/12345678",
  "message_summary": {
    "id": "18c8f7d4abc12345",
    "threadId": "18c8f7d4abc12345",
    "labelIds": ["INBOX", "UNREAD"],
    "subject": "Important notification",
    "from": "sender@example.com",
    "to": "edri2or@gmail.com",
    "date": "2025-11-14T14:25:00Z",
    "snippet": "First 100 chars of email body..."
  },
  "artifact_name": "gmail-message-18c8f7d4abc12345",
  "error": ""
}
```

**Security Note**: Full email body and headers stored in artifact, NOT in result file

---

## 📋 Phase 1 Implementation

### Deliverables

1. **Design Document** ✅
   - File: `docs/GMAIL_PUSH_DESIGN_PHASE1.md`
   - Status: Complete

2. **Skeleton Workflows** ⏳
   - `gmail-ops.yml` - Operations (read, list, etc.)
   - `gmail-dispatcher.yml` - Job dispatcher
   - `gmail-watch-renewal.yml` - Keep watch active
   - `gmail-notification-poller.yml` - Pull from Pub/Sub

3. **Secret Manager Integration** ⏳
   - Document required secrets
   - Placeholder for credential storage
   - Access patterns defined

4. **CAPABILITIES_MATRIX Update** ⏳
   - Gmail section added
   - Status: Design-Ready
   - Gaps documented

---

### Implementation Steps

**Step 1: Infrastructure Setup** (Manual/One-time)
```bash
# Create Pub/Sub topic
gcloud pubsub topics create gmail-notifications --project=edri2or-mcp

# Create pull subscription
gcloud pubsub subscriptions create gmail-pull-sub \
  --topic=gmail-notifications \
  --ack-deadline=600 \
  --project=edri2or-mcp

# Grant Gmail permission to publish
gcloud pubsub topics add-iam-policy-binding gmail-notifications \
  --member=serviceAccount:gmail-push@gmail.google.com \
  --role=roles/pubsub.publisher \
  --project=edri2or-mcp
```

**Step 2: Authentication Setup** (Manual/One-time)
- Determine account type
- Create service account OR
- Perform OAuth flow
- Store credentials in Secret Manager

**Step 3: Activate Watch** (Via workflow)
```bash
# Call Gmail API users.watch
# Store expiration in Secret Manager
```

**Step 4: Deploy Workflows** (Automated)
- Commit workflow files
- Test with manual trigger

**Step 5: End-to-End Test**
- Send test email
- Verify notification received
- Verify job created
- Verify email read
- Verify result generated

---

## 🚧 Known Gaps & TODOs

### Phase 1 Gaps

**Infrastructure**:
- ⚠️ Pub/Sub topic not created (requires GCP CLI access)
- ⚠️ Subscription not configured
- ⚠️ Watch not activated

**Authentication**:
- ⚠️ Account type not determined (Workspace vs Personal)
- ⚠️ No credentials generated yet
- ⚠️ No secrets stored in Secret Manager

**Operations**:
- ⚠️ Pull-based only (5-10 min delay)
- ⚠️ No attachment handling
- ⚠️ No send capability
- ⚠️ Limited to INBOX monitoring

**Testing**:
- ⚠️ No end-to-end test performed
- ⚠️ No error handling validated

---

### Design Decisions Pending

| Question | Options | Recommendation |
|----------|---------|----------------|
| Auth model? | Service Account vs OAuth | Check account type first |
| Subscription? | Pull vs Push | Phase 1: Pull, Phase 2: Push |
| Polling interval? | 5, 10, 15 min | Start with 10 min |
| Which operations? | read, list, thread, history | Phase 1: read + history |
| Attachment handling? | Yes/No | Phase 2+ |

---

## ✅ Success Criteria

### Phase 1 Complete When:

**Design**:
- ✅ Architecture documented
- ✅ Authentication strategy defined
- ✅ Job pattern integration designed
- ✅ Secret Manager integration documented

**Infrastructure**:
- ⏳ Pub/Sub topic created
- ⏳ Pull subscription configured
- ⏳ Watch activated

**Code**:
- ⏳ Skeleton workflows committed
- ⏳ Job formats defined
- ⏳ Dispatcher logic implemented

**Documentation**:
- ⏳ CAPABILITIES_MATRIX updated
- ⏳ Gaps clearly documented
- ⏳ Next steps defined

---

## 🔄 Migration to Phase 2

### From Pull to Push

**New Components**:
1. Cloud Run service (gmail-push-handler)
2. Push subscription configuration
3. OIDC authentication
4. GitHub API integration from Cloud Run

**Benefits**:
- Real-time (< 1s latency)
- No polling overhead
- Automatic retry

**Complexity**:
- Additional deployment
- Public endpoint security
- Cloud Run costs

**Timeline**: 2-3 sessions after Phase 1

---

## 📚 References

**Gmail API**:
- Push Guide: https://developers.google.com/gmail/api/guides/push
- Watch Method: https://developers.google.com/gmail/api/reference/rest/v1/users/watch
- Messages API: https://developers.google.com/gmail/api/reference/rest/v1/users.messages
- History API: https://developers.google.com/gmail/api/reference/rest/v1/users.history

**Pub/Sub**:
- Pull Subscriptions: https://cloud.google.com/pubsub/docs/pull
- Push Subscriptions: https://cloud.google.com/pubsub/docs/push
- IAM Permissions: https://cloud.google.com/pubsub/docs/access-control

**Authentication**:
- Service Account: https://developers.google.com/identity/protocols/oauth2/service-account
- OAuth 2.0: https://developers.google.com/identity/protocols/oauth2
- Domain-Wide Delegation: https://developers.google.com/workspace/guides/create-credentials#service-account

---

## 🎯 Next Actions

**This Session**:
1. ✅ Complete design document
2. ⏳ Create skeleton workflows
3. ⏳ Document secrets in Secret Manager format
4. ⏳ Update CAPABILITIES_MATRIX

**Next Session** (If Prioritized):
1. Determine authentication model
2. Create Pub/Sub infrastructure
3. Store credentials in Secret Manager
4. Activate Gmail watch
5. Test notification flow

**Future**:
1. Implement Cloud Run handler (Phase 2)
2. Add send capability (Phase 3)
3. Attachment handling
4. Advanced filters and rules

---

**Design Complete** ✅  
**Implementation**: Skeleton only  
**Deployment**: Not started  
**Status**: Ready for infrastructure setup
