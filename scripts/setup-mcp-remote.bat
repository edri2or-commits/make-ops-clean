@echo off
REM ========================================
REM MCP Remote Setup Script (Windows)
REM ========================================

echo.
echo ╔═══════════════════════════════════════════╗
echo ║   MCP Remote Setup - Automated           ║
echo ╚═══════════════════════════════════════════╝
echo.

REM Check if running from correct directory
if not exist "scripts\setup-mcp-remote.bat" (
    echo Error: Please run this script from the repository root
    echo Example: scripts\setup-mcp-remote.bat
    pause
    exit /b 1
)

REM Check for Git Bash
where bash >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Git Bash not found
    echo Please install Git for Windows from https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Run the bash script
echo Running setup script...
bash scripts/setup-mcp-remote.sh

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ═══════════════════════════════════════════
    echo Setup completed successfully!
    echo ═══════════════════════════════════════════
    echo.
    echo Check mcp/server/CONNECTION_INSTRUCTIONS.md for next steps
    echo.
) else (
    echo.
    echo Setup failed! Check error messages above.
    echo.
)

pause
