@echo off
setlocal EnableDelayedExpansion

:: get the path to the current script's parent directory
set SCRIPT_PARENT_DIR=%~dp0..

:: Navigate to the parent directory and get its absolute path
pushd %SCRIPT_PARENT_DIR%
set SCRIPT_PARENT_DIR=%CD%
popd

:: set setting directory
set SETTING_DIR=%SCRIPT_PARENT_DIR%\settings

:: check if the settings directory exists
if exist %SETTING_DIR% (
    echo Error: Settings directory already exists. Please delete it and try again.
    exit /b 1
)

:: create a new folder for settings
mkdir %SETTING_DIR%
if errorlevel 1 (
    echo Error: Failed to create settings directory.
    exit /b 1
)

:: set the path to the config file
set CONFIG_FILE=%SETTING_DIR%\config.json

:: write the config file
(
    echo {
    echo     "tool_dir": "!SCRIPT_PARENT_DIR:\=\\!",
    echo }
) > %CONFIG_FILE%

:: Check if writing to config file was successful
if errorlevel 1 (
    echo Error: Failed to write to config file.
    exit /b 1
)

:: Print success message
echo Wrote config file to %CONFIG_FILE%
echo Setup complete. Please add "%SCRIPT_PARENT_DIR%" to your PATH.
echo ================================================================
echo Note you must install the following dependencies:
echo     - Python 3.9 or higher
echo     - Git

:: End of script
exit /b 0
