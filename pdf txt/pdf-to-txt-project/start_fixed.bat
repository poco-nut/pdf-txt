@echo off
echo ========================================
echo   PDF to TXT Converter - Fixed Launcher
echo ========================================
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"
echo Script directory: %SCRIPT_DIR%

REM Change to backend directory
echo Changing to backend directory...
cd /d "%SCRIPT_DIR%backend"
if errorlevel 1 (
    echo ERROR: Cannot change to backend directory!
    echo Please check if the 'backend' folder exists.
    pause
    exit /b 1
)

echo Current directory: %cd%
echo.

REM Check for Python
echo Checking for Python...
where python >nul 2>&1
if errorlevel 1 (
    echo WARNING: Python not in PATH, trying known location...
    if exist "C:\Users\charl\AppData\Local\Programs\Python\Python312\python.exe" (
        set "PYTHON=C:\Users\charl\AppData\Local\Programs\Python\Python312\python.exe"
        echo Using Python at: %PYTHON%
    ) else (
        echo ERROR: Python not found!
        echo Please install Python 3.8 or higher.
        pause
        exit /b 1
    )
) else (
    set "PYTHON=python"
    echo Python found in PATH
)

echo.
echo ========================================
echo Starting PDF to TXT Converter Server
echo ========================================
echo.
echo IMPORTANT:
echo 1. This window MUST stay open while using the converter
echo 2. Server will start on http://localhost:5000
echo 3. Press CTRL+C to stop the server
echo 4. Then open browser to: http://localhost:5000
echo.
echo If server fails to start, error details will be shown below.
echo ========================================
echo.

REM Run the robust startup script
echo Starting server...
echo.
%PYTHON% start_robust.py
set "EXIT_CODE=%errorlevel%"

echo.
echo ========================================
if %EXIT_CODE% equ 0 (
    echo Server stopped normally.
) else (
    echo SERVER FAILED TO START (exit code: %EXIT_CODE%)
    echo.
    echo Possible issues:
    echo 1. Missing Python packages - run: pip install -r requirements.txt
    echo 2. Port 5000 already in use - close other programs using port 5000
    echo 3. App code has errors - check error messages above
    echo.
    echo For detailed diagnostics, run:
    echo   cd backend ^&^& python start_diagnostic.py
)
echo ========================================
echo.
pause