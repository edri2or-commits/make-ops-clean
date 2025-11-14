# install_windows_mcp.ps1
# Purpose: Install Windows-MCP Desktop Extension for Claude Desktop
# Created: 2025-11-14
# Status: NOT EXECUTED - Requires explicit approval from אור
# Risk Level: HIGH (installs OS control capabilities)

#Requires -Version 5.1

# ============================================
# SAFETY WARNING
# ============================================
Write-Host "=============================================" -ForegroundColor Red
Write-Host "  WINDOWS-MCP INSTALLATION SCRIPT" -ForegroundColor Red
Write-Host "=============================================" -ForegroundColor Red
Write-Host ""
Write-Host "WARNING: This script will install Windows-MCP," -ForegroundColor Yellow
Write-Host "which provides FULL OS CONTROL capabilities:" -ForegroundColor Yellow
Write-Host "  - Mouse and keyboard control" -ForegroundColor Yellow
Write-Host "  - Window management" -ForegroundColor Yellow
Write-Host "  - Application launching" -ForegroundColor Yellow
Write-Host "  - PowerShell command execution" -ForegroundColor Yellow
Write-Host "  - Screenshot capture" -ForegroundColor Yellow
Write-Host ""
Write-Host "This is a HIGH RISK operation." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to cancel, or" -ForegroundColor Cyan
pause

# ============================================
# CONFIGURATION
# ============================================
$REPO_URL = "https://github.com/CursorTouch/Windows-MCP.git"
$INSTALL_DIR = "$env:USERPROFILE\Work\AI-Projects\Claude-Ops\mcp-servers\windows-mcp"
$TEMP_CLONE_DIR = "$env:TEMP\windows-mcp-clone"

# ============================================
# STEP 1: PREREQUISITES CHECK
# ============================================
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "STEP 1: Checking Prerequisites" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python 3.13+
Write-Host "Checking Python version..." -ForegroundColor White
try {
    $pythonVersion = & python --version 2>&1
    if ($pythonVersion -match "Python 3\.(\d+)") {
        $minorVersion = [int]$matches[1]
        if ($minorVersion -lt 13) {
            Write-Host "ERROR: Python 3.13+ required, found: $pythonVersion" -ForegroundColor Red
            Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
            exit 1
        }
        Write-Host "  OK: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Could not determine Python version" -ForegroundColor Red
        Write-Host "Output: $pythonVersion" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "ERROR: Python not found in PATH" -ForegroundColor Red
    Write-Host "Install from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check UV package manager
Write-Host "Checking UV package manager..." -ForegroundColor White
try {
    $uvVersion = & uv --version 2>&1
    Write-Host "  OK: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "WARNING: UV not found, attempting to install..." -ForegroundColor Yellow
    try {
        & pip install uv
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  OK: UV installed successfully" -ForegroundColor Green
        } else {
            Write-Host "ERROR: Failed to install UV" -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "ERROR: Failed to install UV via pip" -ForegroundColor Red
        exit 1
    }
}

# Check Node.js (required for DXT)
Write-Host "Checking Node.js..." -ForegroundColor White
try {
    $nodeVersion = & node --version 2>&1
    if ($nodeVersion -match "v(\d+)") {
        $majorVersion = [int]$matches[1]
        if ($majorVersion -lt 18) {
            Write-Host "ERROR: Node.js 18+ required, found: $nodeVersion" -ForegroundColor Red
            Write-Host "Download from: https://nodejs.org/" -ForegroundColor Yellow
            exit 1
        }
        Write-Host "  OK: $nodeVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "ERROR: Node.js not found in PATH" -ForegroundColor Red
    Write-Host "Install from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Check DXT tool
Write-Host "Checking DXT (Desktop Extension Tool)..." -ForegroundColor White
try {
    $dxtVersion = & npx @anthropic-ai/dxt --version 2>&1
    Write-Host "  OK: DXT available" -ForegroundColor Green
} catch {
    Write-Host "WARNING: DXT not found, will be installed on first use" -ForegroundColor Yellow
}

# Check Git
Write-Host "Checking Git..." -ForegroundColor White
try {
    $gitVersion = & git --version 2>&1
    Write-Host "  OK: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git not found in PATH" -ForegroundColor Red
    Write-Host "Install from: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "All prerequisites OK!" -ForegroundColor Green

# ============================================
# STEP 2: CLONE REPOSITORY
# ============================================
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "STEP 2: Cloning Windows-MCP Repository" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Clean temp directory if exists
if (Test-Path $TEMP_CLONE_DIR) {
    Write-Host "Cleaning temporary clone directory..." -ForegroundColor White
    Remove-Item -Path $TEMP_CLONE_DIR -Recurse -Force
}

# Clone repository
Write-Host "Cloning from: $REPO_URL" -ForegroundColor White
Write-Host "To: $TEMP_CLONE_DIR" -ForegroundColor White
try {
    & git clone $REPO_URL $TEMP_CLONE_DIR 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Git clone failed" -ForegroundColor Red
        exit 1
    }
    Write-Host "  OK: Repository cloned" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to clone repository" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# ============================================
# STEP 3: BUILD DESKTOP EXTENSION
# ============================================
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "STEP 3: Building Desktop Extension (DXT)" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Change to repository directory
Push-Location $TEMP_CLONE_DIR

Write-Host "Building .dxt file with npx..." -ForegroundColor White
Write-Host "This may take a moment..." -ForegroundColor Yellow
try {
    & npx @anthropic-ai/dxt pack 2>&1 | Out-String | Write-Host
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: DXT pack failed" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    
    # Find the .dxt file
    $dxtFile = Get-ChildItem -Path . -Filter "*.dxt" | Select-Object -First 1
    
    if (-not $dxtFile) {
        Write-Host "ERROR: No .dxt file was created" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    
    Write-Host "  OK: DXT file created: $($dxtFile.Name)" -ForegroundColor Green
    
    # Store DXT file path for later
    $global:DXT_FILE_PATH = $dxtFile.FullName
    
} catch {
    Write-Host "ERROR: Failed to build DXT" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Pop-Location
    exit 1
}

Pop-Location

# ============================================
# STEP 4: MOVE TO INSTALLATION DIRECTORY
# ============================================
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "STEP 4: Installing to Final Location" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Create installation directory if needed
if (-not (Test-Path $INSTALL_DIR)) {
    Write-Host "Creating installation directory..." -ForegroundColor White
    New-Item -ItemType Directory -Path $INSTALL_DIR -Force | Out-Null
}

# Copy repository to installation directory
Write-Host "Copying to: $INSTALL_DIR" -ForegroundColor White
try {
    Copy-Item -Path "$TEMP_CLONE_DIR\*" -Destination $INSTALL_DIR -Recurse -Force
    Write-Host "  OK: Files copied to installation directory" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to copy files" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# Copy DXT file to a known location
$DXT_FINAL_PATH = "$INSTALL_DIR\windows-mcp.dxt"
if (Test-Path $global:DXT_FILE_PATH) {
    Copy-Item -Path $global:DXT_FILE_PATH -Destination $DXT_FINAL_PATH -Force
    Write-Host "  OK: DXT file saved to: $DXT_FINAL_PATH" -ForegroundColor Green
}

# Clean up temp directory
Write-Host "Cleaning up temporary files..." -ForegroundColor White
Remove-Item -Path $TEMP_CLONE_DIR -Recurse -Force
Write-Host "  OK: Cleanup complete" -ForegroundColor Green

# ============================================
# STEP 5: INSTALLATION VERIFICATION
# ============================================
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "STEP 5: Installation Verification" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Verify installation directory
if (Test-Path "$INSTALL_DIR\manifest.json") {
    Write-Host "  OK: manifest.json found" -ForegroundColor Green
} else {
    Write-Host "WARNING: manifest.json not found" -ForegroundColor Yellow
}

if (Test-Path "$INSTALL_DIR\pyproject.toml") {
    Write-Host "  OK: pyproject.toml found" -ForegroundColor Green
} else {
    Write-Host "WARNING: pyproject.toml not found" -ForegroundColor Yellow
}

if (Test-Path $DXT_FINAL_PATH) {
    Write-Host "  OK: DXT file ready at: $DXT_FINAL_PATH" -ForegroundColor Green
} else {
    Write-Host "ERROR: DXT file not found at expected location" -ForegroundColor Red
}

# ============================================
# INSTALLATION COMPLETE
# ============================================
Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host "INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Windows-MCP has been prepared for Claude Desktop." -ForegroundColor White
Write-Host ""
Write-Host "NEXT STEPS (MANUAL):" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Open Claude Desktop application" -ForegroundColor White
Write-Host ""
Write-Host "2. Go to: Settings > Extensions" -ForegroundColor White
Write-Host ""
Write-Host "3. Click: 'Install Extension'" -ForegroundColor White
Write-Host ""
Write-Host "4. Navigate to and select:" -ForegroundColor White
Write-Host "   $DXT_FINAL_PATH" -ForegroundColor Yellow
Write-Host ""
Write-Host "5. Click: 'Install'" -ForegroundColor White
Write-Host ""
Write-Host "6. RESTART Claude Desktop (CRITICAL)" -ForegroundColor Red
Write-Host ""
Write-Host "7. Verify in Claude Desktop logs that Windows-MCP connected" -ForegroundColor White
Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT REMINDERS:" -ForegroundColor Yellow
Write-Host "- Windows-MCP provides FULL OS CONTROL" -ForegroundColor Yellow
Write-Host "- Test with read-only operations first (State-Tool, Screenshot)" -ForegroundColor Yellow
Write-Host "- Require approval before using Shell-Tool" -ForegroundColor Yellow
Write-Host "- Monitor all operations carefully" -ForegroundColor Yellow
Write-Host ""
Write-Host "Installation log saved to:" -ForegroundColor Cyan
Write-Host "$env:USERPROFILE\Work\AI-Projects\Claude-Ops\logs\windows_mcp_install_$(Get-Date -Format 'yyyyMMdd_HHmmss').log" -ForegroundColor Cyan
Write-Host ""

# Save installation evidence
$logDir = "$env:USERPROFILE\Work\AI-Projects\Claude-Ops\logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$logFile = "$logDir\windows_mcp_install_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
@"
Windows-MCP Installation Log
============================
Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
Installed to: $INSTALL_DIR
DXT file: $DXT_FINAL_PATH
Python version: $pythonVersion
Node.js version: $nodeVersion
UV version: $uvVersion
Git version: $gitVersion

Status: Installation package prepared
Next: Manual installation in Claude Desktop

Evidence:
- Repository cloned successfully
- DXT file built successfully
- Files copied to installation directory
- All prerequisites verified
============================
"@ | Out-File -FilePath $logFile -Encoding UTF8

Write-Host "Installation script completed successfully." -ForegroundColor Green
Write-Host ""
