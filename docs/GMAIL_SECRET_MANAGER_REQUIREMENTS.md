# Gmail Automation - Secret Manager Requirements

**Created**: 2025-11-14  
**Status**: Phase 1 Design  
**Purpose**: Document secrets required for Gmail Push automation

---

## 🔐 Required Secrets

### Authentication Path Decision

**First**: Determine if `edri2or@gmail.com` is:
- **Workspace/G Suite account** → Use Service Account path
- **Personal Gmail account** → Use OAuth 2.0 path

---

## Path A: Service Account (Workspace/G Suite)

### Prerequisites
- Google Workspace account
- Admin access to Workspace console
- Domain-wide delegation enabled

### Secrets Required

#### 1. `gmail-service-account-key`
**Type**: JSON  
**Description**: Service account key file with Gmail API access

**Creation**:
```bash
# 1. Create service account
gcloud iam service-accounts create gmail-reader \
  --display-name="Gmail Reader Service Account" \
  --project=edri2or-mcp

# 2. Create key
gcloud iam service-accounts keys create sa-key.json \
  --iam-account=gmail-reader@edri2or-mcp.iam.gserviceaccount.com

# 3. Store in Secret Manager
gcloud secrets create gmail-service-account-key \
  --data-file=sa-key.json \
  --project=edri2or-mcp

# 4. Delete local key file
rm sa-key.json
```

**Workspace Admin Setup**:
1. Go to: Admin Console → Security → API Controls → Domain-wide Delegation
2. Add Client ID from service account
3. Grant scope: `https://www.googleapis.com/auth/gmail.readonly`

**Format** (JSON):
```json
{
  "type": "service_account",
  "project_id": "edri2or-mcp",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "gmail-reader@edri2or-mcp.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

#### 2. `gmail-impersonate-email`
**Type**: String  
**Description**: User email to impersonate  
**Value**: `edri2or@gmail.com`

**Creation**:
```bash
echo -n "edri2or@gmail.com" | gcloud secrets create gmail-impersonate-email \
  --data-file=- \
  --project=edri2or-mcp
```

---

## Path B: OAuth 2.0 (Personal Gmail)

### Prerequisites
- OAuth 2.0 Client ID created in GCP Console
- One-time manual authorization flow

### Secrets Required

#### 1. `gmail-oauth-client-id`
**Type**: String  
**Description**: OAuth 2.0 Client ID

**Creation**:
```bash
# Get from GCP Console → APIs & Services → Credentials
CLIENT_ID="1234567890-abcdef.apps.googleusercontent.com"

echo -n "$CLIENT_ID" | gcloud secrets create gmail-oauth-client-id \
  --data-file=- \
  --project=edri2or-mcp
```

#### 2. `gmail-oauth-client-secret`
**Type**: String  
**Description**: OAuth 2.0 Client Secret

**Creation**:
```bash
# Get from GCP Console → APIs & Services → Credentials
CLIENT_SECRET="GOCSPX-..."

echo -n "$CLIENT_SECRET" | gcloud secrets create gmail-oauth-client-secret \
  --data-file=- \
  --project=edri2or-mcp
```

#### 3. `gmail-oauth-refresh-token`
**Type**: String  
**Description**: Refresh token from initial OAuth flow

**One-Time Authorization Flow**:
```bash
# 1. Generate authorization URL
AUTH_URL="https://accounts.google.com/o/oauth2/auth?\
client_id=$CLIENT_ID&\
redirect_uri=http://localhost&\
scope=https://www.googleapis.com/auth/gmail.readonly&\
response_type=code&\
access_type=offline&\
prompt=consent"

# 2. Open URL in browser, authorize, copy code from redirect

# 3. Exchange code for tokens
curl -X POST https://oauth2.googleapis.com/token \
  -d client_id=$CLIENT_ID \
  -d client_secret=$CLIENT_SECRET \
  -d code=$AUTHORIZATION_CODE \
  -d redirect_uri=http://localhost \
  -d grant_type=authorization_code

# Response includes refresh_token
```

**Store Refresh Token**:
```bash
REFRESH_TOKEN="1//..."

echo -n "$REFRESH_TOKEN" | gcloud secrets create gmail-oauth-refresh-token \
  --data-file=- \
  --project=edri2or-mcp
```

---

## Common Secrets (Both Paths)

### 1. `gmail-watch-expiration`
**Type**: String (timestamp)  
**Description**: Current Gmail watch expiration time  
**Format**: Unix timestamp in milliseconds

**Initial Creation**:
```bash
# Set to 0 initially (will be updated by watch-renewal workflow)
echo -n "0" | gcloud secrets create gmail-watch-expiration \
  --data-file=- \
  --project=edri2or-mcp
```

**Update Pattern** (in workflow):
```bash
# After successful watch renewal
EXPIRATION="1731686400000"  # From Gmail API response
echo -n "$EXPIRATION" | gcloud secrets versions add gmail-watch-expiration \
  --data-file=- \
  --project=edri2or-mcp
```

---

## 📋 Secret Manager Access

### IAM Permissions

**Service Account** (`${{ vars.GCP_SA_EMAIL }}`):
```bash
# Grant Secret Accessor role
gcloud projects add-iam-policy-binding edri2or-mcp \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/secretmanager.secretAccessor"
```

### Access Pattern (from GitHub Actions)

```bash
# Via WIF authentication
gcloud secrets versions access latest \
  --secret="gmail-oauth-refresh-token" \
  --project="edri2or-mcp"
```

---

## 🗂️ Summary

### If Service Account (Workspace):
```
✅ gmail-service-account-key (JSON)
✅ gmail-impersonate-email (string)
✅ gmail-watch-expiration (string)
```

### If OAuth 2.0 (Personal):
```
✅ gmail-oauth-client-id (string)
✅ gmail-oauth-client-secret (string)
✅ gmail-oauth-refresh-token (string)
✅ gmail-watch-expiration (string)
```

---

## 🚧 Current Status

**Phase 1**: Documentation only  
**Secrets Created**: ❌ None yet  
**Next Step**: Determine authentication path (Workspace vs Personal)

**Once Determined**:
1. Create appropriate secrets
2. Test access from workflows
3. Implement Gmail API calls
4. Activate watch

---

## 📚 References

**Service Account**:
- https://developers.google.com/identity/protocols/oauth2/service-account
- https://developers.google.com/workspace/guides/create-credentials#service-account

**OAuth 2.0**:
- https://developers.google.com/identity/protocols/oauth2
- https://developers.google.com/identity/protocols/oauth2/web-server

**Secret Manager**:
- https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets
- https://cloud.google.com/secret-manager/docs/access-control

---

**Status**: Design Complete ✅  
**Implementation**: Pending authentication decision
