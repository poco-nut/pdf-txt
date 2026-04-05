@echo off
echo Running diagnostic tool...
echo.
cd /d "%~dp0backend"
python start_diagnostic.py
echo.
echo Diagnostic completed.
echo Press any key to exit...
pause >nul