@echo off
setlocal enabledelayedexpansion
set TOOL_DIR=C:\_PATH\custom-tools\src\python-autocite
set VENV_DIR=%TOOL_DIR%\venv
set GIT_URL=https://github.com/sean1832/python-autocite.git

if not exist "%TOOL_DIR%" (
    echo python-autocite does not exist.
    set /p user_input="Do you want to clone from %GIT_URL% (y/n)? "
    set user_input=!user_input:~0,1!
    if /i "!user_input!" neq "y" (
        echo Exiting...
        exit /b 1
    )
    git clone %GIT_URL% %TOOL_DIR%
    if errorlevel 1 (
        echo Failed to clone python-autocite. Exiting...
        exit /b 1
    )
) else (
    pushd "%TOOL_DIR%"
    git remote update
    set LOCAL_STATUS=
    for /f "tokens=*" %%a in ('git status -uno ^| find "Your branch is behind"') do set LOCAL_STATUS=%%a
    if not "%LOCAL_STATUS%"=="" (
        set /p user_input="Your local branch is behind the remote branch. Do you want to pull the latest changes (y/n)? "
        set user_input=!user_input:~0,1!
        if /i "!user_input!" neq "y" (
            echo Exiting...
            exit /b 1
        )
        git pull
        if errorlevel 1 (
            echo Failed to pull the latest changes. Exiting...
            exit /b 1
        )
    )
    popd
)

if not exist "%VENV_DIR%" (
    echo Virtual environment does not exist.
    set /p user_input="Do you want to create a virtual environment (y/n)? "
    if /i "%user_input%" neq "y" (
        echo Exiting...
        exit /b 1
    )
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo Failed to create virtual environment. Exiting...
        exit /b 1
    )
)

call "%VENV_DIR%\Scripts\activate"

python -c "import pkg_resources; pkg_resources.get_distribution('python_autocite')"
if errorlevel 1 (
    echo python_autocite is not installed.
    set /p user_input="Do you want to install python_autocite (y/n)? "
    if /i "%user_input%" neq "y" (
        echo Exiting...
        exit /b 1
    )
    pushd "%TOOL_DIR%"
    python setup.py install
    if errorlevel 1 (
        echo Failed to install python_autocite. Exiting...
        exit /b 1
    )
    popd
)
cls
autocite %*
