# L1 Filesystem Map

**Generated**: 2025-11-14  
**Scope**: `C:\Users\edri2\Work\AI-Projects\Claude-Ops`  
**Method**: Read-only directory tree scan

---

## 📂 Root Structure

```
Claude-Ops/
├── 📁 Archives/              (12 ZIP archives - evidence, workflows, tokens)
├── 📁 Assets/Images/         (5 images - screenshots, diagrams)
├── 📁 Config/                (5 config files - env, yaml, csv)
├── 📁 Credentials/           ⚠️ SKIPPED - contains private keys & secrets
├── 📁 Data/                  (12 data files - xlsx, tsv, json)
├── 📁 Documentation/         (5 markdown docs + 9 PDFs)
├── 📁 edri2or-mcp/           (GCP MCP application project)
├── 📁 canvas_draw/           (Python web app for drawing)
├── 📁 gh-controls-draft/     (4 GitHub control templates)
├── 📁 GOOGLE/                (2 OAuth client secrets)
├── 📁 GPT/                   (GPT integration files)
├── 📁 Logs/                  (1 system log file)
├── 📁 MAKE/                  (empty)
├── 📁 MCP/                   **⭐ Main MCP workspace**
├── 📁 mcp-servers/           **⭐ MCP Server implementations**
├── 📁 ops/                   (diagnostics subfolder)
├── 📁 Scripts/               (5 shell/ps1/gs scripts)
├── 📁 _audit/                (audit logs & backups)
├── 📁 טוקנים/                (Hebrew: "tokens" - env files)
├── 📁 טלגרם/                 (Hebrew: "telegram" - empty)
├── 📁 קבצים גיט האב וורקפלוו/  (Hebrew: GitHub workflow YMLs)
├── 📁 קנולג 2.11.25/         (Hebrew: "Knowledge" - templates & docs)
└── [56 root-level files]     (scripts, configs, state files)
```

---

## 🔑 Critical Directories

### 1. MCP/ - Main Control Infrastructure

```
MCP/
├── 📄 local_controller.py        ⭐ Local operations controller
├── 📄 mcp_agent.py                ⭐ MCP agent implementation
├── 📄 experiment_controller.py    Experiment orchestrator
├── 📄 auto_commit_pusher.py       Git automation
├── 📄 secret_auto_updater.py      Secret rotation utility
├── 📄 mcp_google_init.py          Google services init
├── 📁 make-ops-clean/             **Local GitHub repo clone**
│   ├── 📁 .git/                   Git metadata (extensive branch history)
│   ├── 📁 .github/                GitHub config (CODEOWNERS, workflows, scripts)
│   ├── 📁 platform/manifest/      Platform manifest files
│   └── 📁 _staging/L1.2/          Staging area for L1.2 features
├── 📄 BOOTSTRAP_INSTRUCTIONS.md
├── 📄 ROB_HANDOFF.json
├── 📄 experiment_queue.json
├── 📄 github_secrets.json
└── [10 other config/state files]
```

**Notes**:
- `make-ops-clean/` is a full local git clone with extensive branch history
- Contains the same repo we're committing to (recursive structure)
- `.git/` directory is fully populated with objects, refs, logs

### 2. mcp-servers/ - MCP Server Implementations

```
mcp-servers/
└── ps_exec/                       **PowerShell MCP Server**
    ├── 📄 dispatcher.ps1           ⭐ PowerShell command dispatcher
    ├── 📄 index.js                 Node.js MCP server entry point
    ├── 📄 package.json             Dependencies manifest
    ├── 📄 install.bat              Installation script
    └── 📁 node_modules/            NPM packages (@modelcontextprotocol/sdk, zod, etc.)
```

**Notes**:
- This is the MCP server that enables PowerShell execution from Claude
- Uses `@modelcontextprotocol/sdk` for MCP protocol
- Fully installed with node_modules (~14 packages)

### 3. canvas_draw/ - Drawing Web Application

```
canvas_draw/
├── 📄 app.py                      Flask/Python web app
├── 📁 docs/                       API documentation
├── 📁 schemas/                    Python schemas (canvas, response, shape)
├── 📁 tests/                      Integration tests
├── 📄 Dockerfile                  Container definition
├── 📄 Makefile                    Build automation
└── 📄 requirements.txt            Python dependencies
```

### 4. edri2or-mcp/ - GCP MCP Application

```
edri2or-mcp/
├── 📄 app.py                      Base app (3 versions: base, extended, ultimate)
├── 📄 deploy.sh                   Deployment scripts (2 versions)
├── 📄 auto_oauth.sh               OAuth automation
├── 📄 update_oauth_ultimate.py    OAuth credential updater
├── 📄 Dockerfile
├── 📁 .github/workflows/          (empty - no workflows yet)
└── [8 other config/doc files]
```

---

## 📝 Root-Level Scripts by Category

### Bootstrap Scripts (4)
- `bootstrap_clean.py`
- `bootstrap_final.py` 
- `bootstrap_final_extracted.py`
- `bootstrap_final_fixed.py`

### Control Scripts (3)
- `metacontrol.py` ⭐
- `claude_auto_agent.py` ⭐
- `claude_writer.py`

### Cloud Shell Scripts (10 - all PS1)
- `check_cloudshell_api.ps1`
- `cloudshell_autotest.ps1`
- `cloudshell_final_success.ps1`
- `cloudshell_final_test.ps1`
- `cloudshell_retry.ps1`
- `cloudshell_working.ps1`
- `test_cloudshell.ps1`
- `test_cloudshell_api.ps1`
- `gcloud_auth.ps1`
- `install_gcloud.ps1`

### Infrastructure (2)
- `check_infrastructure.py`
- `check_infrastructure.sh`

### Setup/Install (Multiple BAT files)
- Various `RUN_*.bat`, `INSTALL_*.bat`, `SETUP_*.bat` files

---

## 🚫 Skipped / Not Mapped

### Credentials/ Directory
**Reason**: Contains private keys and OAuth secrets  
**Files identified**:
- `*.pem` files (3 private keys)
- `client_secret_*.json` (1 OAuth secret)

### _audit/purged_2025-11-11/ Subdirectory
**Reason**: Contains archived credentials  
**Files identified**:
- `CLAUDE_TOK.txt`
- `client_secret_google.json`
- `key.pem`

### GOOGLE/ & GPT/ Directories
**Partial skip**: Contains OAuth client secrets  
**Mapped**: Directory structure only  
**Not mapped**: Content of JSON files

### node_modules/ 
**Reason**: Standard npm packages, too granular for L1 map  
**Noted**: Uses @modelcontextprotocol/sdk, zod, and 12 other packages

---

## 🗂️ Special Directories

### Archives/
Contains 12 ZIP files:
- Evidence stores (google_policy)
- Knowledge packs (v2, v3)
- Workflow bundles (v1, v2)
- Token check reports
- ChatOps registry
- MCP agent custom path

### Data/
Structured data files:
- **Evidence Index** (xlsx, tsv) - 3 timestamped versions
- **Inbox System** (xlsx)
- **Phoenix System Data** (xlsx)
- **Task Manager Structure** (xlsx)
- Proof packs (json)

### Documentation/
- 5 Markdown decision logs
- 9 PDFs (executive summaries, guides, Hebrew documents)

### Hebrew-Named Directories
- `טוקנים/` (Tokens) - 2 env files
- `טלגרם/` (Telegram) - empty
- `קבצים גיט האב וורקפלוו/` (GitHub Workflow Files) - 9 YML files
- `קנולג 2.11.25/` (Knowledge 2.11.25) - 18 template/policy files

---

## 📊 File Count Summary

| Category | Count |
|----------|-------|
| **Python Scripts** | 33 |
| **PowerShell Scripts** | 13 |
| **Shell Scripts** | 10 |
| **Batch Files** | 15+ |
| **Config Files** | 20+ |
| **Documentation** | 25+ |
| **Data Files** | 12 |
| **Archives** | 15+ |

**Total mapped items**: ~200+ files across 30+ directories

---

## 🎯 Key Findings

### Control Plane Architecture
1. **MetaControl** (`metacontrol.py`) - Top-level orchestrator
2. **Local Controller** (`MCP/local_controller.py`) - Local ops
3. **MCP Agent** (`MCP/mcp_agent.py`) - MCP protocol handler
4. **Auto Agent** (`claude_auto_agent.py`) - Autonomous operations

### MCP Infrastructure
- **PowerShell Server**: Fully functional in `mcp-servers/ps_exec/`
- **Dispatcher**: `dispatcher.ps1` routes 10 whitelisted commands
- **SDK**: Uses official `@modelcontextprotocol/sdk`

### GitHub Integration
- **Local Clone**: Full `make-ops-clean` repo with extensive history
- **Workflows**: GitHub Actions configured in `.github/workflows/`
- **Scripts**: Approval/execution scripts in `.github/scripts/`

### Cloud Shell Ecosystem
- 10 PowerShell scripts for GCP Cloud Shell testing/integration
- Multiple iterations (working, final, success variants)
- OAuth & authentication automation

### Bootstrap System
- 4 Python bootstrap variants (clean, final, extracted, fixed)
- Multiple BAT launchers
- Complete package ZIP available

---

## ⚠️ Security Notes

1. **Credentials Directory**: Completely skipped - contains 4 sensitive files
2. **Audit Purge**: Old credentials archived in `_audit/purged_2025-11-11/`
3. **OAuth Secrets**: Present in GOOGLE/, GPT/, edri2or-mcp/ - not examined
4. **Token Files**: Hebrew "טוקנים" directory contains env files - not examined

---

## 🔄 Recursive Structure Alert

The directory `MCP/make-ops-clean/` contains a clone of the **same repository** we're committing to. This creates a recursive structure where:
- The filesystem contains the repo
- The repo contains the filesystem map
- The map documents itself

**Current depth**: 1 level (local clone only, not nested further)

---

**Last Updated**: 2025-11-14  
**Method**: Filesystem:directory_tree (read-only)  
**Safety**: No credentials accessed, no files modified
