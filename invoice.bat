@echo off
setlocal enabledelayedexpansion

:: change here
set PROJECT_NAME=Invoice-CLI
set GIT_URL=https://github.com/sean1832/Invoice-CLI/releases/download/0.1.0/InvoiceCLI_0.1.0_x64.zip

set ROOT_DIR=%~dp0
set TOOL_DIR=%ROOT_DIR%\code\%PROJECT_NAME%

:: check if the tool directory exists or not, if exist install, else update
if exist %TOOL_DIR% (
    echo Tool already installed. Continuing...
) else (
    echo Installing %PROJECT_NAME%...
    mkdir %TOOL_DIR%
    python %ROOT_DIR%/utilities/download-latest.py %GIT_URL% --output %TOOL_DIR%
)
cd %TOOL_DIR%
:: run the tool
%TOOL_DIR%/invoice %*
popd