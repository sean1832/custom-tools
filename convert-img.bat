@echo off
setlocal enabledelayedexpansion

:: change here
set PROJECT_NAME=cli-convert-img
set GIT_URL=https://github.com/sean1832/cli-convert-img/releases/download/0.0.2/convert-image-cs-x64.zip

set ROOT_DIR=%~dp0
set TOOL_DIR=%ROOT_DIR%\code\%PROJECT_NAME%
set VENV_DIR=%TOOL_DIR%\venv

:: check if the tool directory exists or not, if exist install, else update
if exist %TOOL_DIR% (
    echo Conver Image CLI
) else (
    echo Installing %PROJECT_NAME%...
    mkdir %TOOL_DIR%
    python %ROOT_DIR%/utilities/download-latest.py %GIT_URL% --output %TOOL_DIR%
)
cd %TOOL_DIR%
:: run the tool
%TOOL_DIR%/convert-img %*
popd