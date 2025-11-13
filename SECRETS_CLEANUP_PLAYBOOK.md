# SECRETS_CLEANUP_PLAYBOOK (L1.5)

**Created**: 2025-11-14  
**Status**: DRAFT - Awaiting Approval  
**Based On**: `SECURITY_FINDINGS_SECRETS.md`  
**Owner**: אור (Or)

---

## 1. Scope & Goals

### 1.1 What Are We Fixing?

**5 Active Plaintext Secrets**:
- ✓ GCP Service Account Keys (3 `.pem` files)
- ✓ Google OAuth Secrets (2 `.json` files)
- ✓ Quarantined credentials (archive folder)
- ✓ Archives (12 `.zip` files, potential secrets)
- ✓ Git history (potential exposures)

**Out of Scope**:
- ✗ GitHub credentials (already remediated)
- ✗ Template files (no active secrets)

### 1.2 Goals

1. **Zero plaintext secrets** in working directory
2. **Zero secrets in git history**
3. **Documented secure retrieval**
4. **Audit trail maintained**

**Storage Targets**:
1. GCP Secret Manager (for GCP keys)
2. Windows Credential Manager (for OAuth, local dev)
3. GitHub Secrets (for CI/CD if needed)
4. Secure deletion (for rotated/obsolete secrets)

---

## 2. Assets to Fix

### Asset Group A: GCP Service Account Keys

| Asset | Path | Risk | Target |
|-------|------|------|--------|
| A1 | `Credentials/auditor-ops.2025-11-07.private-key.pem` | HIGH | GCP Secret Manager |
| A2 | `Credentials/auditor-ops.2025-11-07.private-key (1).pem` | HIGH | DELETE (duplicate) |
| A3 | `Credentials/auditor-ops.2025-11-08.private-key.pem` | HIGH | GCP Secret Manager |

**Service Account**: `auditor-ops@edri2or-mcp.iam.gserviceaccount.com`  
**Purpose**: GCP API access (Sheets/Drive automation)

### Asset Group B: OAuth Client Secrets

| Asset | Path | Risk | Target |
|-------|------|------|--------|
| B1 | `GOOGLE/client_secret_212701048029-4mdl6kaopt235pfpa4c7c75k70hbm1mi.apps.googleusercontent.com.json` | MED-HIGH | Credential Manager |
| B2 | `GPT/client_secret_212701048029-6kck3l0jmebtf6k4ee2iina11p1dq96j.apps.googleusercontent.com.json` | MED-HIGH | Credential Manager |

**Client Type**: Installed Application (Desktop OAuth)  
**Risk Context**: Semi-public by design, but shouldn't be in repos

### Asset Group C: Quarantine Folder

| Asset | Path | Status | Action |
|-------|------|--------|--------|
| C1 | `_audit/purged_2025-11-11/CLAUDE_TOK.txt` | Quarantined | Review → Secure Delete |
| C2 | `_audit/purged_2025-11-11/key.pem` | Quarantined | Review → Secure Delete |
| C3 | `_audit/purged_2025-11-11/client_secret_google.json` | Quarantined | Review → Secure Delete |

**Date**: 2025-11-11 (Phase 1 PURGE)  
**Current Risk**: LOW (quarantined)

### Asset Group D: Archive Files

**Priority**:
1. `token_check_report*.zip` - HIGH (likely contains tokens)
2. `workflows_bundle*.zip` - MEDIUM (may contain CI secrets)
3. `EVIDENCE_STORE*.zip` - MEDIUM (may contain OAuth/API keys)
4. `knowledge_pack*.zip` - LOW (likely docs only)

---

## 3. Remediation Plan

### Phase Overview

| Phase | Name | Risk | Reversible | Approval |
|-------|------|------|------------|----------|
| A | Pre-Flight Checks | None | N/A | ✅ Single |
| B | GCP Keys | LOW | ✅ Yes | ✅ Single |
| C | OAuth Secrets | LOW | ✅ Yes | ✅ Single |
| D | Archives | MEDIUM | ✅ Yes | ✅ Single per archive |
| E | Quarantine | HIGH | ❌ No | ✅✅ Double |
| F | Git Scan | MEDIUM | N/A | ✅ Single |
| G | Git Cleanup | CRITICAL | ❌ No | ✅✅ Double |

---

### Phase A: Pre-Flight Checks

**Verify**:
- [ ] GCP CLI authenticated
- [ ] Secret Manager API enabled
- [ ] Credential Manager accessible
- [ ] Backups created

**Commands** (read-only):
```bash
gcloud auth list
gcloud services list --enabled --filter="secretmanager"
cmdkey /list
```

**Backup**:
```powershell
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$backup = "C:\Users\edri2\Secure-Backup\secrets-$timestamp"
Copy-Item "Credentials" "$backup\Credentials" -Recurse
Copy-Item "GOOGLE" "$backup\GOOGLE" -Recurse
Copy-Item "GPT" "$backup\GPT" -Recurse
```

**Identify Active Key**:
```bash
# Test each key
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.pem"
gcloud auth application-default print-access-token
```

**Approval**: ✅ Single

---

### Phase B: GCP Service Account Keys

**Process**:

1. **Upload to Secret Manager**:
```bash
gcloud secrets create auditor-ops-private-key \
  --data-file="Credentials/auditor-ops.2025-11-08.private-key.pem" \
  --replication-policy="automatic"
```

2. **Update Code**:
```python
# FROM: Credentials.from_service_account_file('key.pem')
# TO: Retrieve from Secret Manager
from google.cloud import secretmanager
client = secretmanager.SecretManagerServiceClient()
name = "projects/edri2or-mcp/secrets/auditor-ops-private-key/versions/latest"
response = client.access_secret_version(request={"name": name})
key_data = response.payload.data.decode('UTF-8')
```

3. **Test Application**

4. **Archive Local Files** (after success):
```powershell
$archive = "_audit\migrated-gcp-keys-$(Get-Date -Format 'yyyyMMdd')"
New-Item -ItemType Directory $archive
Move-Item "Credentials\*.pem" $archive
```

**Rollback**: Files remain available until archived

**Approval**: ✅ Single

---

### Phase C: OAuth Client Secrets

**Process**:

1. **Store in Credential Manager**:
```powershell
$oauth = Get-Content "GOOGLE\client_secret_*.json" | ConvertFrom-Json
cmdkey /generic:"google-oauth-client-mcp" `
       /user:"$($oauth.installed.client_id)" `
       /pass:"$($oauth.installed.client_secret)"
```

2. **Update Code**:
```python
import win32cred
cred = win32cred.CredRead('google-oauth-client-mcp', win32cred.CRED_TYPE_GENERIC)
client_secret = cred['CredentialBlob'].decode('utf-16')
```

3. **Test OAuth Flow**

4. **Archive JSON Files**:
```powershell
$archive = "_audit\oauth-migrated-$(Get-Date -Format 'yyyyMMdd')"
Move-Item "GOOGLE\client_secret_*.json" $archive
Move-Item "GPT\client_secret_*.json" $archive
```

**Approval**: ✅ Single

---

### Phase D: Archive Scanning

**Scan Tool**:
```bash
# List without extracting
unzip -l archive.zip

# Search for secrets
unzip -p archive.zip | grep -E "(token|secret|key|password)" -i
```

**Decision Tree**:
- IF secrets found → Extract to secure temp → Process → Delete original
- ELSE → Mark as SCANNED_CLEAN → Keep

**Approval**: ✅ Single (✅✅ Double for HIGH risk archives)

---

### Phase E: Quarantine Cleanup

⚠️ **PERMANENT DELETION**

**Prerequisites**:
- [ ] New secrets tested and working (30+ days)
- [ ] No code references to old paths
- [ ] External backup exists
- [ ] Audit log complete

**Secure Deletion**:
```powershell
# Using SDelete (7-pass DoD 5220.22-M)
sdelete64.exe -p 7 -s "_audit\purged_2025-11-11\*"
Remove-Item "_audit\purged_2025-11-11" -Force
```

**Approval**: ✅✅ Double (type "DELETE QUARANTINE")

---

### Phase F: Git History Scan

**Tools**:
```bash
# trufflehog
trufflehog --regex --entropy=True file://. > scan-results.txt

# gitleaks
gitleaks detect --source=. --report-path=report.json
```

**Analyze**:
- Active secrets (still valid) → CRITICAL
- Historical secrets (rotated) → MEDIUM
- False positives → NONE

**Approval**: ✅ Single

---

### Phase G: Git History Cleanup

⚠️ **REWRITES HISTORY - IRREVERSIBLE**

**When to Clean**:
- ✅ Active secrets in commits
- ✅ High-risk secrets (private keys)
- ❌ Only false positives
- ❌ Already rotated (optional)

**Tool: BFG Repo-Cleaner**:
```bash
# Backup
cp -r .git .git-backup

# Clean
bfg --delete-files "CLAUDE TOK.txt"
bfg --delete-files "*.pem"
bfg --replace-text secrets-to-replace.txt

# Verify
git log --all -S "ghp_" --source --all  # Should be empty

# Force push
git push --force
```

**Approval**: ✅✅ Double (type "REWRITE HISTORY")

---

## 4. Approval Gates

### Single Approval (✅)
Read-only or reversible operations:
- Pre-flight checks
- Key migrations (files archived)
- Archive scanning (initial)
- Git history scanning

### Double Approval (✅✅)
Irreversible operations:
- Quarantine secure deletion
- Git history rewrite
- HIGH-risk archive extraction

### Emergency Stop
**"עצור עכשיו" or "STOP NOW"** → Immediate halt

---

## 5. Open Questions

### Q1: Which GCP Key is Active?
**Need**: GCP Console verification or safe test  
**Impact**: Can't delete without knowing

### Q2: OAuth Usage Identification?
**Need**: Code search for import/usage  
**Impact**: Can't migrate without knowing dependencies

### Q3: Archive Contents?
**Need**: Permission to scan or אור's knowledge  
**Impact**: Can't prioritize without knowing risk

### Q4: Repository Exposure History?
**Need**: Has repo ever been public/forked?  
**Impact**: Determines if history cleanup is worth it

### Q5: Acceptable Downtime?
**Need**: Maintenance window approval  
**Impact**: Determines migration approach

### Q6: Credential Manager Sufficient?
**Alternative**: Azure Key Vault, HashiCorp Vault?  
**Trade-off**: Simple vs. enterprise-grade security

### Q7: Rotation Cadence?
**Need**: Policy decision (90 days? 1 year?)  
**Impact**: Determines if automation needed

### Q8: Multi-User Scenario?
**Need**: Are other machines/users involved?  
**Impact**: Local storage vs. shared secret storage

---

## 6. Success Criteria

✅ **Zero plaintext secrets on disk**  
✅ **All secrets in secure storage**  
✅ **Clean git history** (or documented false positives)  
✅ **Comprehensive audit trail**  
✅ **Functional verification** (all apps work)  
✅ **Documentation updated**

---

## 7. Timeline Estimate

| Phase | Time | Dependencies |
|-------|------|--------------|
| A. Pre-Flight | 2-4 hrs | GCP access, tools |
| B. GCP Keys | 3-5 hrs | Phase A, testing |
| C. OAuth | 2-3 hrs | Phase A, OAuth testing |
| D. Archives | 4-8 hrs | Archive count/size |
| E. Quarantine | 1-2 hrs | 30-day wait, approvals |
| F. Git Scan | 1-2 hrs | Tool install, scan |
| G. Git Cleanup | 2-4 hrs | Phase F, backup |
| **Total** | **15-28 hrs** | Multiple days |

**Recommended**: 4-week schedule, one phase per week

---

## 8. Command Reference

### GCP Secret Manager
```bash
gcloud secrets create NAME --data-file=PATH
gcloud secrets versions access latest --secret=NAME
gcloud secrets delete NAME
```

### Windows Credential Manager
```powershell
cmdkey /generic:TARGET /user:USER /pass:PASS
cmdkey /list
cmdkey /delete:TARGET
```

### Git Scanning
```bash
trufflehog --regex --entropy=True file://PATH
gitleaks detect --source=PATH --report-path=REPORT
```

### Secure Deletion
```powershell
sdelete64.exe -p 7 -s FILE  # Windows
cipher /w:PATH              # Windows built-in
shred -vfz -n 7 FILE        # Linux
```

---

**Status**: DRAFT - Awaiting Approval  
**Next Step**: אור reviews → Answers open questions → Approves Phase A
