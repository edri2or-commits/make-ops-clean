# Google MCP Status Report

**Date**: 2025-11-18  
**Status**: ⚠️ **PARTIAL - Search Functions Investigation Needed**

---

## ✅ What Works

### Gmail Operations
```
✅ read_gmail_profile
   - Returns: emailAddress, messagesTotal, threadsTotal, historyId
   - Evidence: Successfully retrieved edri2or@gmail.com profile
   - Status: OPERATIONAL

❌ search_gmail_messages
   - Returns: Empty/no results
   - Query tested: "CAPABILITIES_MATRIX"
   - Status: NOT WORKING (investigation needed)

❌ read_gmail_thread
   - Depends on: search_gmail_messages to get thread_id
   - Status: BLOCKED (can't test without search)
```

### Google Drive Operations
```
✅ google_drive_fetch
   - Works with: Specific document ID
   - Evidence: Can read docs when ID is known
   - Status: OPERATIONAL

❌ google_drive_search
   - Returns: Empty/no results (tool ran without output)
   - Queries tested:
     - name contains 'Evidence'
     - name contains 'CAPABILITIES'
   - Status: NOT WORKING (investigation needed)
```

---

## 🔍 Investigation Hypotheses

### Hypothesis 1: OAuth Scope Missing
**Likelihood**: Medium

**Theory**: Search operations require additional OAuth scopes not granted during MCP setup.

**Evidence**:
- ✅ Basic read operations work (profile, fetch by ID)
- ❌ Search operations don't work
- 📊 Suggests permission boundary

**Test Needed**:
```
Check OAuth consent screen for granted scopes:
- Gmail: gmail.readonly vs gmail.modify
- Drive: drive.readonly vs drive.file vs drive
```

**If This Is The Issue**:
- Would require: Re-authenticating Google MCP with broader scopes
- Approval needed: From Or (manual OAuth flow)

---

### Hypothesis 2: MCP Tool Bug
**Likelihood**: High

**Theory**: Search functions have implementation bug in MCP server.

**Evidence**:
- ✅ Direct API calls (fetch by ID) work
- ❌ Search API calls return empty
- 📊 Suggests tool-level issue, not API issue

**Test Needed**:
```
Compare:
1. MCP tool search call → empty response
2. Direct API call with same OAuth token → results?
```

**If This Is The Issue**:
- Would require: MCP server update (not in our control)
- Workaround: Use known document IDs from other sources

---

### Hypothesis 3: API Rate Limiting
**Likelihood**: Low

**Theory**: Google APIs temporarily rate-limiting search queries.

**Evidence**:
- ❌ No rate limit error messages
- ❌ No 429 status codes
- ✅ Other operations work fine

**If This Is The Issue**:
- Would resolve: Automatically after cooldown period
- Action: Retry searches later

---

### Hypothesis 4: Empty Query Results (Actual)
**Likelihood**: Very Low

**Theory**: User actually has no matching documents/emails.

**Evidence**:
- ❌ Gmail profile shows 50,694 messages
- ❌ "CAPABILITIES" definitely exists in Gmail history
- ❌ Evidence Index spreadsheet definitely exists in Drive

**Conclusion**: Not the issue

---

## 📊 Comparison Matrix

| Operation | Works? | Network Path | Auth Type | Hypothesis |
|-----------|--------|--------------|-----------|------------|
| Gmail Profile | ✅ Yes | MCP OAuth | User token | - |
| Gmail Search | ❌ No | MCP OAuth | User token | Scope or Bug |
| Drive Fetch | ✅ Yes | MCP OAuth | User token | - |
| Drive Search | ❌ No | MCP OAuth | User token | Scope or Bug |
| bash curl | ❌ No | Desktop proxy | N/A | Network policy (expected) |

---

## 🎯 Recommended Actions

### Immediate (No Or Action Needed)
1. ✅ **Document Status** (this file)
2. ✅ **Update CAPABILITIES_MATRIX** with current state
3. ✅ **Use Workarounds**:
   - For Drive: Copy files to Filesystem
   - For Gmail: Use profile info, avoid search

### Future Investigation (When Needed)
1. Check OAuth scopes in Google Cloud Console
2. Test direct API calls outside MCP
3. Compare MCP tool code with API documentation
4. Report bug to Anthropic if confirmed

### Not Recommended
- ❌ Don't ask Or to manually search Drive/Gmail
- ❌ Don't ask Or to re-auth until hypothesis confirmed
- ❌ Don't assume it's a vendor outage (other ops work)

---

## 🔐 Security Note

No credentials or tokens exposed during this investigation. All operations used proper OAuth flows through MCP.

---

## 📝 Current Workarounds

### For Google Drive Documents
```
Option 1: Copy to Filesystem
- Or copies CAPABILITIES_MATRIX.md to local dir
- Claude reads via Filesystem MCP ✅

Option 2: Use Direct IDs
- Get document ID from URL
- Use google_drive_fetch with ID ✅

Option 3: GitHub as Source
- Store docs in GitHub repo
- Read via GitHub MCP ✅
```

### For Gmail Operations
```
Option 1: Use Profile Info
- Get message counts, history ID ✅
- Sufficient for monitoring

Option 2: Export to Files
- Or exports relevant emails to .eml files
- Claude reads via Filesystem MCP ✅

Option 3: GitHub Issues/PRs
- Use GitHub notifications instead
- Track via GitHub MCP ✅
```

---

## ✅ Operational Status

**Google MCP: PARTIAL**
- Read operations: ✅ OPERATIONAL
- Search operations: ❌ UNDER INVESTIGATION
- Workarounds: ✅ AVAILABLE
- Impact: 🟡 MEDIUM (manageable with alternatives)

---

**Report Complete**: 2025-11-18T20:15:00Z  
**Next Update**: When hypothesis is tested or issue resolves  
**No Action Required**: Workarounds sufficient for current operations
