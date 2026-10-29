@echo off
setlocal EnableExtensions
cd /d "%~dp0"
chcp 65001 >nul
title AIDL GROUP 7 - SETUP

echo ============================================================
echo                   AIDL GROUP 7 SETUP
echo ============================================================

where node >nul 2>&1
if errorlevel 1 (echo [FAIL] Install Node.js 22 or newer. & exit /b 1)
node -e "if (Number(process.versions.node.split('.')[0]) < 22) process.exit(1)"
if errorlevel 1 (echo [FAIL] Node.js 22 or newer is required. & exit /b 1)
where npm >nul 2>&1
if errorlevel 1 (echo [FAIL] npm is required. & exit /b 1)

if exist "services\api\.venv\Scripts\python.exe" goto python_ready
py -3 -m venv "services\api\.venv"
if errorlevel 1 (echo [FAIL] Python 3.11+ needed via py launcher. & exit /b 1)
:python_ready
"services\api\.venv\Scripts\python.exe" -c "import sys; raise SystemExit(sys.version_info < (3, 11))"
if errorlevel 1 (echo [FAIL] Python 3.11+ needed. & exit /b 1)
"services\api\.venv\Scripts\python.exe" -m pip install -e "services\api[dev]"
if errorlevel 1 (echo [FAIL] API dependency install failed. & exit /b 1)

pushd "apps\web"
if exist package-lock.json (
  call npm ci
) else (
  call npm install
)
if errorlevel 1 (popd & echo [FAIL] npm install failed. & exit /b 1)
popd

echo [OK] Setup finished. Next: start-dev.bat
exit /b 0
