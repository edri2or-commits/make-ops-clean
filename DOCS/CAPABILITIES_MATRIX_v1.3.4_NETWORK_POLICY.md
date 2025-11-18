# CAPABILITIES MATRIX v1.3.4 - NETWORK POLICY UPDATE

**Update**: 2025-11-18  
**Added**: Desktop Network Policy Documentation

---

## 🌐 Claude Desktop Network Policy (NEW)

### Outbound Network Access: `RESTRICTED_WHITELIST`

**Status**: ✅ **Operating by Design** (not a limitation, a security feature)

### Allowed Domains (bash curl/wget)
```
api.anthropic.com          ✅ Anthropic API
archive.ubuntu.com         ✅ Ubuntu packages
crates.io                  ✅ Rust packages
files.pythonhosted.org     ✅ Python packages
github.com                 ✅ GitHub (limited)
index.crates.io            ✅ Rust registry
npmjs.com / npmjs.org      ✅ NPM packages
pypi.org                   ✅ Python packages
pythonhosted.org           ✅ Python packages
registry.npmjs.org         ✅ NPM registry
registry.yarnpkg.com       ✅ Yarn registry
security.ubuntu.com        ✅ Security updates
static.crates.io           ✅ Rust static files
www.npmjs.com/org          ✅ NPM web
yarnpkg.com                ✅ Yarn
```

### ❌ NOT Allowed (bash curl/wget)
```
googleapis.com             ❌ Google APIs
run.app                    ❌ Cloud Run
raw.githubusercontent.com  ❌ GitHub raw content
cloudflare.com             ❌ CDN services
Most external APIs         ❌ General web access
```

### ✅ What DOES Work Despite Restrictions

#### GitHub MCP
- ✅ **Full API access** (different network path than bash)
- ✅ Read files, write commits, create issues/PRs
- ✅ All 27+ GitHub operations operational
- ❌ **bash curl** to GitHub blocked (use MCP instead)

#### GitHub Actions (Cloud Environment)
- ✅ **No restrictions** - runners have full internet access
- ✅ Can call Google APIs, Cloud Run, Secret Manager
- ✅ Can deploy to GCP, AWS, Azure
- 🎯 **Strategy**: Execute all cloud operations via workflows

#### Google MCP
- ✅ **OAuth-based access** (different network path)
- ✅ Drive Fetch (with document ID)
- ✅ Gmail Profile read
- ❓ Drive/Gmail Search (separate investigation needed)

#### Filesystem MCP
- ✅ **No network dependency**
- ✅ Full local file access
- ✅ No restrictions

---

## 🎯 Practical Implications

### For GitHub Executor API v1
**Strategy**: Deploy and test **exclusively via GitHub Actions**
- ✅ Workflow has full network access
- ✅ Can deploy to Cloud Run
- ✅ Can test endpoints
- ✅ Can verify secrets
- ❌ **Don't** try to curl Cloud Run from Claude Desktop

### For Google Operations
**Strategy**: Use MCP tools (not bash curl)
- ✅ google_drive_fetch with IDs
- ✅ google_drive_search (when working)
- ✅ Gmail operations via MCP
- ❌ **Don't** try to curl googleapis.com

### For General Cloud Operations
**Strategy**: Execute via GitHub Actions workflows
- ✅ GCP operations in workflows
- ✅ AWS operations in workflows
- ✅ Azure operations in workflows
- ❌ **Don't** try cloud APIs from Desktop bash

---

## 📊 Error Messages to Recognize

### Network Restriction (Expected)
```
curl: (56) CONNECT tunnel failed, response 403
x-deny-reason: host_not_allowed
```
**Action**: Use MCP tool or GitHub Actions workflow instead

### Actual Vendor Outage (Unexpected)
```
curl: (7) Failed to connect to api.github.com port 443: Connection refused
curl: (28) Operation timed out after 30000 milliseconds
HTTP Status: 503 Service Unavailable
```
**Action**: Document as BLOCKED_ON_VENDOR_OUTAGE

---

## 🔄 Update History

### 2025-11-18 (v1.3.4) - Network Policy Documentation
- **Added**: Complete network policy section
- **Clarified**: Restrictions are by design (security feature)
- **Documented**: Allowed domains whitelist
- **Strategy**: Use GitHub Actions for cloud operations
- **Strategy**: Use MCP tools for API access (not bash)
- **Evidence**: STATE_FOR_GPT/NETWORK_RESTRICTION_ANALYSIS_2025-11-18.md

---

**This update supersedes**: Previous assumptions about Cloudflare outages or vendor issues related to network access.
