@echo off
setlocal enabledelayedexpansion

:: change here
set PROJECT_NAME=cli-csv-excel
set GIT_URL=https://github.com/sean1832/cli-csv-excel.git

set ROOT_DIR=%~dp0
set TOOL_DIR=%ROOT_DIR%\code\%PROJECT_NAME%
set VENV_DIR=%TOOL_DIR%\venv

:: check if the tool directory exists or not, if exist install, else update
if exist %TOOL_DIR% (
    echo Updating %PROJECT_NAME%...
    python %ROOT_DIR%/utilities/update.py %TOOL_DIR%
) else (
    echo Installing %PROJECT_NAME%...
    python %ROOT_DIR%/utilities/install.py %GIT_URL%
)

:: activate the virtual environment
call "%VENV_DIR%\Scripts\activate"

:: run the tool
python %TOOL_DIR%/csv-excel.py %*
popd