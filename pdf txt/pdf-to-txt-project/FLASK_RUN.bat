@echo off
echo PDF to TXT Converter (Flask Run)
echo ================================
echo.

REM Check if in correct directory
if not exist "backend\app.py" (
    echo ERROR: backend\app.py not found!
    echo Please place this file in the project root.
    pause
    exit /b 1
)

echo Starting server using Flask CLI...
echo.
echo IMPORTANT:
echo 1. A new window will open with the server
echo 2. Keep THAT window open while using the converter
echo 3. Server will run on: http://localhost:5000
echo 4. Press CTRL+C in THAT window to stop
echo.
echo Opening server window...
timeout /t 2 /nobreak >nul

REM Start Flask in a new window
start "PDF to TXT Server" cmd /k "cd /d "%~dp0backend" && set FLASK_APP=app.py && flask run --host=0.0.0.0 --port=5000 --no-debugger --no-reload"

echo.
echo Server window should be open now!
echo Open browser to: http://localhost:5000
echo.
pause