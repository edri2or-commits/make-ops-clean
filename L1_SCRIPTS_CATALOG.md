# L1 Scripts Catalog

**Generated**: 2025-11-14  
**Source Path**: `C:\Users\edri2\Work\AI-Projects\Claude-Ops`  
**Purpose**: Inventory of all executable scripts in the local Claude-Ops workspace

---

## 📊 Summary

| Type | Count |
|------|-------|
| Python (`.py`) | 33 |
| PowerShell (`.ps1`) | 13 |
| Shell (`.sh`) | 10 |
| **Total** | **56** |

---

## 🐍 Python Scripts (33)

### Bootstrap & Setup
| File | Purpose |
|------|---------|
| `bootstrap_clean.py` | Bootstrap cleanup utility |
| `bootstrap_final.py` | Final bootstrap orchestration |
| `bootstrap_final_extracted.py` | Extracted bootstrap logic |
| `bootstrap_final_fixed.py` | Fixed version of bootstrap |
| `extract_and_run.py` | Extract and execute workflow |
| `EXTRACT_AND_RUN_COMPLETE.py` | Complete extraction runner (2 versions) |

### Control & Agent Systems
| File | Purpose |
|------|---------|
| `claude_auto_agent.py` | Claude autonomous agent controller |
| `claude_downloader.py` | Claude content downloader |
| `claude_writer.py` | Claude output writer |
| `metacontrol.py` | **Main metacontrol orchestrator** |
| `MetaControl_AutopilotLauncher.py` | Autopilot launcher for MetaControl |

### Infrastructure & Testing
| File | Purpose |
|------|---------|
| `check_infrastructure.py` | Infrastructure health checker |
| `download_all_files.py` | Bulk file downloader |

### Canvas/Drawing Application
| File | Purpose |
|------|---------|
| `canvas_draw/app.py` | Canvas drawing web application |
| `canvas_draw/schemas/canvas_schemas.py` | Canvas data schemas |
| `canvas_draw/schemas/response_schemas.py` | API response schemas |
| `canvas_draw/schemas/shape_schemas.py` | Shape definition schemas |

### GCP/Google Integration
| File | Purpose |
|------|---------|
| `edri2or-mcp/app.py` | MCP application (3 versions: base, extended, ultimate) |
| `edri2or-mcp/update_oauth_ultimate.py` | OAuth credential updater |

### MCP Tools & Controllers
| File | Purpose |
|------|---------|
| `MCP/auto_commit_pusher.py` | Automated git commit pusher |
| `MCP/experiment_controller.py` | Experiment orchestrator |
| `MCP/local_controller.py` | **Local operations controller** |
| `MCP/mcp_agent.py` | MCP agent implementation |
| `MCP/mcp_google_init.py` | Google services initializer |
| `MCP/secret_auto_updater.py` | Secret auto-rotation utility |

### GitHub Integration
| File | Purpose |
|------|---------|
| `MCP/make-ops-clean/VALIDATE.py` | Manifest validation script |

### Telegram Setup
| File | Purpose |
|------|---------|
| `setup_telegram.py` | Telegram bot setup utility |

---

## ⚡ PowerShell Scripts (13)

### Cloud Shell & GCP
| File | Purpose |
|------|---------|
| `check_cloudshell_api.ps1` | Cloud Shell API verification |
| `cloudshell_autotest.ps1` | Automated Cloud Shell testing |
| `cloudshell_final_success.ps1` | Final Cloud Shell success handler |
| `cloudshell_final_test.ps1` | Final Cloud Shell test suite |
| `cloudshell_retry.ps1` | Cloud Shell retry logic |
| `cloudshell_working.ps1` | Working Cloud Shell connector |
| `gcloud_auth.ps1` | GCloud authentication |
| `install_gcloud.ps1` | GCloud SDK installer |
| `test_cloudshell.ps1` | Cloud Shell test runner |
| `test_cloudshell_api.ps1` | Cloud Shell API tester |

### System & Maintenance
| File | Purpose |
|------|---------|
| `DELETE_LOGS.ps1` | Log cleanup utility |
| `FULL_AUTOPILOT.ps1` | Full autopilot orchestration |
| `setup_gmail_autowatch.ps1` | Gmail auto-watch setup |

### Autopilot
| File | Purpose |
|------|---------|
| `MetaControl_AutopilotLauncher.ps1` | Autopilot launcher |
| `run_autopilot.ps1` | Autopilot runner (2 versions) |

### MCP Server
| File | Purpose |
|------|---------|
| `mcp-servers/ps_exec/dispatcher.ps1` | **PowerShell command dispatcher for MCP** |

---

## 🐚 Shell Scripts (10)

### Deployment & Setup
| File | Purpose |
|------|---------|
| `check_infrastructure.sh` | Infrastructure checker (Shell version) |
| `COMPLETE_SETUP.sh` | Complete system setup |
| `CREATE_ALL_FILES.sh` | Batch file creator |
| `RUN_THIS.sh` | Quick runner script |
| `run_autopilot_final.sh` | Final autopilot runner |

### Canvas Application
| File | Purpose |
|------|---------|
| `canvas_draw/docs/curl_examples.sh` | Canvas API curl examples |
| `canvas_draw/tests/integration_test.sh` | Canvas integration tests |

### GCP/MCP Deployment
| File | Purpose |
|------|---------|
| `edri2or-mcp/auto_oauth.sh` | Automated OAuth flow |
| `edri2or-mcp/deploy.sh` | Deployment script (2 versions: base, ultimate) |
| `edri2or-mcp/setup.sh` | MCP setup script |

### GitHub Scripts
| File | Purpose |
|------|---------|
| `MCP/make-ops-clean/.github/scripts/apply-changes.sh` | Apply approved changes |
| `MCP/make-ops-clean/.github/scripts/create-approval-request.sh` | Create approval PR |
| `MCP/make-ops-clean/DEPLOY.sh` | Repository deployment |

### App Scripts
| File | Purpose |
|------|---------|
| `Scripts/gh_app_dispatch.sh` | GitHub App dispatcher |
| `Scripts/gh_app_patch_and_trigger.sh` | GitHub App patch + trigger |

---

## 🔑 Key Findings

### Critical Controllers
1. **`metacontrol.py`** - Main orchestration system
2. **`MCP/local_controller.py`** - Local operations
3. **`claude_auto_agent.py`** - Autonomous agent

### MCP Infrastructure
- PowerShell dispatcher: `mcp-servers/ps_exec/dispatcher.ps1`
- MCP agent: `MCP/mcp_agent.py`
- Local controller: `MCP/local_controller.py`

### Cloud Integration
- Multiple Cloud Shell testing scripts (PS1)
- GCP deployment scripts (Shell)
- OAuth automation

### Bootstrap Ecosystem
- 4 bootstrap Python variants
- Complete setup shells
- Extraction/runner utilities

---

## ⚠️ Notes

1. **No scripts skipped** - All files in scope were cataloged
2. **GitHub repo clone** detected at `MCP/make-ops-clean/` (local working copy)
3. **Multiple versions** exist for some scripts (bootstrap, autopilot, deploy)
4. **Credentials folder** present but not cataloged (security)

---

## 🔄 Next Steps

- [ ] Test critical controllers (`metacontrol.py`, `local_controller.py`)
- [ ] Document bootstrap flow variants
- [ ] Audit MCP server functionality
- [ ] Review Cloud Shell integration status
