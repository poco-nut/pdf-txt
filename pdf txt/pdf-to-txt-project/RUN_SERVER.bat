@echo off
echo PDF to TXT Converter
echo ====================
echo.

REM Check if backend folder exists
if not exist "backend\app.py" (
    echo ERROR: backend\app.py not found!
    echo Please make sure this file is in the project root folder.
    pause
    exit /b 1
)

echo Starting server in a new window...
echo.
echo IMPORTANT:
echo 1. A new window will open with the server
echo 2. Keep THAT window open while using the converter
echo 3. Server will run on: http://localhost:5000
echo 4. Press CTRL+C in THAT window to stop
echo.
echo Opening server window in 3 seconds...
timeout /t 3 /nobreak >nul

REM Start server in a new command window
start "PDF to TXT Converter Server" cmd /k "cd /d "%~dp0backend" && python start_simple.py"

echo.
echo Server window opened!
echo.
echo Now open your browser to: http://localhost:5000
echo.
echo To stop the server, go to the server window and press CTRL+C.
echo.
pause