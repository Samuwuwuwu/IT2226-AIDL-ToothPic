@echo off
setlocal EnableExtensions
cd /d "%~dp0"
chcp 65001 >nul
if "%~1"=="" (
  echo Usage: audit-data.bat data\raw\dataset-folder
  exit /b 1
)
set "PYTHONPATH=%CD%\ml\src"
if exist "services\api\.venv\Scripts\python.exe" (
  "services\api\.venv\Scripts\python.exe" -m aidl_ml.audit "%~1"
) else (
  py -3 -m aidl_ml.audit "%~1"
)
exit /b %errorlevel%
