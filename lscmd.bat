@echo off
setlocal enabledelayedexpansion

:: change here
set PROJECT_NAME=cli-csv-excel
set GIT_URL=https://github.com/sean1832/cli-csv-excel.git

set ROOT_DIR=%~dp0
set TOOL_DIR=%ROOT_DIR%\code\%PROJECT_NAME%
set VENV_DIR=%TOOL_DIR%\venv

python %ROOT_DIR%\utilities\lscmd.py -d %ROOT_DIR%
popd
