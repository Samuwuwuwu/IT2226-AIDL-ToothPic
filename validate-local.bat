@echo off
setlocal EnableExtensions
cd /d "%~dp0"
chcp 65001 >nul
title AIDL GROUP 7 - LOCAL CHECKS
set "FAILED=0"
if not exist "services\api\.venv\Scripts\python.exe" (
  echo [FAIL] Run setup-dev.bat first.
  exit /b 1
)

echo [API] Unit tests
pushd "services\api"
".venv\Scripts\python.exe" -m pytest
if errorlevel 1 set "FAILED=1"
echo [API] Ruff
".venv\Scripts\python.exe" -m ruff check .
if errorlevel 1 set "FAILED=1"
popd

echo [WEB] TypeScript and build
pushd "apps\web"
call npm run build
if errorlevel 1 set "FAILED=1"
popd

echo [ML] Data-audit tests
set "PYTHONPATH=%CD%\ml\src"
"services\api\.venv\Scripts\python.exe" -m pytest "ml\tests"
if errorlevel 1 set "FAILED=1"

if "%FAILED%"=="1" (echo [FAIL] Some local checks failed. & exit /b 1)
echo [OK] Local validation passed.
exit /b 0
