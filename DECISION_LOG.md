# Decision Log — index (Latest first, RFC3339Z)

## 2025-11-12T12:25:00Z — Repository Cleanup Analysis Complete
**Decision**: Analyzed all 5 repositories in edri2or-commits account
**Type**: Analysis & Strategy
**Proof**: PR #95 created with comprehensive analysis
**Document**: evidence/REPOSITORY_CLEANUP_ANALYSIS.md

**Repositories Analyzed**:
1. make-ops-clean ✅ - Keep as SSOT (current)
2. edri2or-mcp 🟢 - Migrate to mcp/api-server/ (unique Flask API)
3. make-ops 🔴 - Archive (legacy, superseded)
4. gmail-auto-watch 🟡 - Delete (empty, created yesterday)
5. edri2or-automation 🟡 - Delete (empty, created yesterday)

**Key Finding**: edri2or-mcp contains production-ready Flask API server for Google Workspace that complements existing MCP protocol clients. Different integration method (HTTP vs MCP) serves different agents (GPT Actions vs Claude).

**Recommendations**:
- KEEP: make-ops-clean (continue as SSOT)
- MIGRATE: edri2or-mcp → make-ops-clean/mcp/api-server/
- ARCHIVE: make-ops (preserve history, mark deprecated)
- DELETE: gmail-auto-watch (no content)
- DELETE: edri2or-automation (no content)

**Next Steps**:
1. Get Or's approval on PR #95
2. Execute migration of edri2or-mcp
3. Archive make-ops with deprecation notice
4. Delete empty repositories
5. Update SYSTEM_STATUS.md

**Status**: Awaiting approval
**Impact**: High (achieves single SSOT goal)
**Risk**: Low (analysis only, no code changes yet)

---

## 2025-11-12T12:00:00Z — Desktop Files Unified (PR #94 Merged)
**Decision**: Merged all scattered Desktop files into unified repo structure
**Type**: Repository Unification
**Proof**: PR #94 merged to main
**Commit**: Multiple commits in unified/desktop-merge branch

**Files Added**:
- docs/ONBOARDING_MAP.md
- docs/LOCAL_TOOLS_INVENTORY.md
- config/ directory with config.json
- evidence/ directory (github, make, telegram)
- knowledge/ directory (GLOSSARY, OPERATING_MODES, specs)
- COLLABORATORS.md (team access guide)
- SYSTEM_STATUS.md (live tracking)
- .gitignore (comprehensive protection)

**Rationale**: 
- Desktop had 20+ scattered files/folders
- No single source of truth
- Secrets at risk (טוקנים/ folder)
- Documentation fragmented
- Evidence not tracked

**Result**: 
✅ Single unified repository
✅ All documentation centralized
✅ Secrets protected via .gitignore
✅ Evidence tracking established
✅ Team access documented
✅ System status live-tracked

**Authorization**: Or approved GPT as co-decision maker with "אני והוא זה אחד"

**Status**: Complete ✅

---

## 2025-11-02T04:06:30Z — L2 Controlled-Write: demo edit
proof: PR=https://github.com/edri2or-commits/make-ops-clean/pull/30 ; file=https://github.com/edri2or-commits/make-ops-clean/blob/main/ops/demo.txt (sha=557db03de997c86a4a028e1ebd3a1ceb225be238) ; run=https://github.com/edri2or-commits/make-ops-clean/actions/runs/19007046319
commit=fd4a40196df405fa5719b932e5662eaf4f111221 ; content_b64=SGVsbG8gV29ybGQ+
result: DoD met (PR merged + file_on_main + run_success)
status=approved
note: iPhone-only control: YES (use Actions – Run workflow links)
