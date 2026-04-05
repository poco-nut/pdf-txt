@echo off
echo PDF to TXT Converter Launcher
echo ==============================
echo.

REM Check if we're in the right place
if not exist "backend\app.py" (
    echo Error: Please place this file in the main project folder.
    echo Current folder: %cd%
    echo.
    pause
    exit /b 1
)

echo 1. Switching to backend folder...
cd backend
echo    Current folder: %cd%
echo.

echo 2. Checking Python...
where python >nul 2>&1
if errorlevel 1 (
    echo    WARNING: Python not in system PATH.
    echo    Trying common Python locations...

    REM Try common Python paths
    set "PYTHON_EXE="

    if exist "C:\Users\charl\AppData\Local\Programs\Python\Python312\python.exe" (
        set "PYTHON_EXE=C:\Users\charl\AppData\Local\Programs\Python\Python312\python.exe"
    ) else if exist "C:\Python312\python.exe" (
        set "PYTHON_EXE=C:\Python312\python.exe"
    ) else if exist "C:\Python311\python.exe" (
        set "PYTHON_EXE=C:\Python311\python.exe"
    ) else if exist "C:\Python310\python.exe" (
        set "PYTHON_EXE=C:\Python310\python.exe"
    ) else if exist "C:\Python39\python.exe" (
        set "PYTHON_EXE=C:\Python39\python.exe"
    ) else if exist "C:\Python38\python.exe" (
        set "PYTHON_EXE=C:\Python38\python.exe"
    ) else if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
        set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    )

    if "%PYTHON_EXE%"=="" (
        echo    ERROR: Python not found!
        echo    Please install Python 3.8 or higher.
        echo.
        pause
        exit /b 1
    )

    echo    Using Python at: %PYTHON_EXE%
) else (
    set "PYTHON_EXE=python"
    echo    Python found in PATH
)

echo.
echo 3. Starting server...
echo    ========================================
echo    IMPORTANT:
echo    1. Keep this window open
echo    2. Open browser to http://localhost:5000
echo    3. Press CTRL+C to stop server
echo    ========================================
echo.
echo Server is starting. If you see errors below, please report them.
echo.

REM Run the server with unbuffered output
%PYTHON_EXE% -u start_simple.py

REM If we get here, the server stopped
echo.
echo ========================================
echo Server has stopped.
echo ========================================
echo.
pause