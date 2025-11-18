# NETWORK RESTRICTION ANALYSIS

**Date**: 2025-11-18  
**Time**: 22:06 IST (20:06 UTC)  
**Status**: ✅ OPERATING NORMALLY (within restrictions)

---

## 🔍 **Root Cause: Claude Desktop Network Policy**

### Error Code
```
curl: (56) CONNECT tunnel failed, response 403
HTTP/1.1 403 Forbidden
x-deny-reason: host_not_allowed
```

### Analysis
This is **NOT a vendor outage** (like Cloudflare).  
This is **Claude Desktop's egress proxy** enforcing allowed domain restrictions.

---

## 📋 **Network Restrictions (By Design)**

### Allowed Domains (bash curl):
```
api.anthropic.com
archive.ubuntu.com
crates.io
files.pythonhosted.org
github.com (limited)
index.crates.io
npmjs.com
npmjs.org
pypi.org
pythonhosted.org
registry.npmjs.org
registry.yarnpkg.com
security.ubuntu.com
static.crates.io
www.npmjs.com
www.npmjs.org
yarnpkg.com
```

### ❌ NOT Allowed (bash curl):
- `googleapis.com` - Google APIs
- `cloudflare.com` - Cloudflare
- `raw.githubusercontent.com` - GitHub raw content
- Most external APIs

---

## ✅ **What Works:**

### GitHub MCP
- ✅ **Direct API calls** via MCP tool
- ✅ Read files from repos
- ✅ Write files to repos
- ✅ Create commits, issues, PRs
- ❌ **bash curl** to GitHub (blocked by proxy)

### Google MCP
- ✅ **Gmail Profile** - basic info
- ✅ **Drive Fetch** - with specific document ID
- ❌ **Drive Search** - API not working (separate issue)
- ❌ **Gmail Search** - API not working (separate issue)

### Filesystem MCP
- ✅ **Full access** to allowed directories
- ✅ Read/write on user's computer
- ✅ No network restrictions

### PowerShell/Windows-Shell MCP
- ✅ **All whitelisted commands** work
- ✅ Local operations only
- ✅ No network dependencies

---

## 🚨 **Separate Issue: Google MCP Tools**

### Observation
Google Drive Search and Gmail Search return **no results** (empty responses).

### Possible Causes
1. **MCP Tool Bug** - Search functions not working
2. **OAuth Scope Issue** - Missing permissions
3. **API Rate Limit** - Temporary block
4. **Actual Vendor Outage** - Google APIs down

### Status
❓ **INVESTIGATION NEEDED**  
Cannot distinguish between:
- MCP tool bug vs.
- Google API outage vs.
- Permission issue

### Workaround
- ✅ Use `google_drive_fetch` with known document IDs
- ✅ Use `read_gmail_profile` for basic info
- ✅ Copy files to local filesystem for access

---

## 🎯 **Corrected Assessment**

### Previous Assumption (WRONG)
❌ "Cloudflare outage blocking all network access"

### Correct Understanding (RIGHT)
✅ "Claude Desktop network policy restricts bash curl to specific domains"  
✅ "MCP tools use different network path (allowed)"  
❓ "Google MCP Search tools may have separate issue"

---

## 📝 **Implications for Claude-Ops**

### GitHub Executor API Deployment
- **Status**: Can proceed with MCP-based deployment
- **No Change**: GH_EX secret assumed to exist
- **Next Step**: Run workflow when ready (no network blocker)

### CAPABILITIES_MATRIX Access
- **Status**: Use GitHub MCP (not bash curl)
- **Workaround**: Copy to local filesystem (in progress)
- **No Blocker**: Can proceed

### Future Operations
- ✅ Use MCP tools for API access (not bash)
- ✅ Use Filesystem MCP for local operations
- ❌ Don't rely on bash curl for external APIs

---

## ✅ **Resolution**

**VENDOR_OUTAGE_2025-11-18.md is OBSOLETE**

Replacing with this accurate analysis:
- Network restrictions are **by design** (not a bug)
- MCP tools still functional (different network path)
- No vendor outage detected
- Operations can continue normally

---

**Report Complete**: 2025-11-18T20:10:00Z  
**Status**: ✅ OPERATIONAL (within documented restrictions)
