@echo off
setlocal enabledelayedexpansion
echo [RUN_AUTOPILOT] starting
RUNSEC=NONE
if exist "%~dp0venv\Scripts\python.exe" (set "PY=%~dp0venv\Scripts\python.exe") 
else (set "PY=python")
if exist main.py (
  "$PY" -u main.py
  set "RC=%ERRORLEVEL%")
else (
  echo main.py not found - no-op..
  set RC=0)
echo [RUN_AUTOPILIOT] finished with code $RC
exit /b $RC