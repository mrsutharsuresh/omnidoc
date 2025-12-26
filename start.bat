@ECHO OFF
SETLOCAL

:: Check for Python
python --version >NUL 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error: Python is not installed or not in PATH.
    PAUSE
    EXIT /B 1
)

:: Set project root
SET "PROJECT_ROOT=%~dp0"

:: Check if running from source or installed
IF EXIST "%PROJECT_ROOT%run.py" (
    ECHO Starting OmniDoc from source...
    python "%PROJECT_ROOT%run.py"
) ELSE (
    ECHO Starting OmniDoc...
    omnidoc start
)

ENDLOCAL
