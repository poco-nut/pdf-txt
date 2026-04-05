@echo off
echo ========================================
echo   PDF to TXT Converter - Launcher
echo ========================================
echo.

REM Display current directory
echo Current directory: %cd%
echo.

REM Change to backend directory
echo Changing to backend directory...
cd /d "%~dp0backend"
if errorlevel 1 (
    echo ERROR: Cannot change to backend directory!
    echo Please check the file path.
    pause
    exit /b 1
)

echo New directory: %cd%
echo.

REM Check Python
echo Checking Python...
where python >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH!
    echo.
    echo Trying with full path...
    "C:\Users\charl\AppData\Local\Programs\Python\Python312\python.exe" --version >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python not found!
        echo Please install Python 3.8 or higher.
        pause
        exit /b 1
    )
    set PYTHON_CMD="C:\Users\charl\AppData\Local\Programs\Python\Python312\python.exe"
    echo Using Python at: %PYTHON_CMD%
) else (
    set PYTHON_CMD=python
    echo Python found in PATH
)

echo.
echo ========================================
echo Starting server on http://localhost:5000
echo ========================================
echo.
echo IMPORTANT:
echo 1. Keep this window open while using the converter
echo 2. Press CTRL+C to stop the server
echo 3. Open browser to: http://localhost:5000
echo.
echo Server is starting... Please wait.
echo.

REM Start the server
%PYTHON_CMD% start_simple.py

echo.
echo Server has stopped.
echo.
pause