@echo off
setlocal
cd /d "%~dp0"

set "HOST=127.0.0.1"
set "PORT=8765"
set "URL=http://%HOST%:%PORT%/"

echo ========================================
echo  EvilTrace one-click launcher
echo ========================================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python was not found on PATH.
  echo Install Python 3.12+ or open this folder in a terminal with Python available.
  echo.
  pause
  exit /b 1
)

echo Starting EvilTrace at %URL%
echo A browser window will open automatically.
echo Keep this terminal open while using the app.
echo Press Ctrl+C here to stop the server.
echo.

start "" powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process '%URL%'"
python -m eviltrace.server

echo.
echo EvilTrace server stopped.
pause
