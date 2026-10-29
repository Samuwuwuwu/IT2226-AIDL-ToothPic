@echo off
setlocal EnableExtensions
cd /d "%~dp0"
chcp 65001 >nul
title AIDL GROUP 7 - DEV
if not exist "services\api\.venv\Scripts\python.exe" (
  echo [FAIL] Run setup-dev.bat first.
  exit /b 1
)
"services\api\.venv\Scripts\python.exe" "scripts\dev.py"
exit /b %errorlevel%
