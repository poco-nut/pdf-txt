@echo off
echo ========================================
echo  PDF to TXT Converter - Flask Server
echo ========================================
echo.

REM 检查是否在backend目录中
if not exist "app.py" (
    echo Error: Please run this script from the 'backend' directory!
    echo Current directory: %cd%
    pause
    exit /b 1
)

REM 检查Python
where python >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found in PATH!
    echo Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM 检查依赖
echo Checking Python dependencies...
python -c "import flask, pdfplumber, flask_cors" 2>nul
if errorlevel 1 (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo.
echo Starting Flask server on http://localhost:5000
echo Press CTRL+C to stop the server
echo.

REM 运行Flask应用
python app.py

REM 如果服务器停止
echo.
echo Server stopped.
pause