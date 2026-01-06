@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul 2>nul

echo Starting AI Book Processing Tool - TXT Document Splitter...
echo Language: English (Default)
echo.
where python >nul 2>nul
if errorlevel 1 (
  echo Python not found. Please install Python 3 and add it to PATH.
  pause
  exit /b 1
)

python "%~dp0txt_splitter.py"
if errorlevel 1 (
  echo Failed to start. You may need to install dependencies: pip install -r requirements.txt
  pause
  exit /b %errorlevel%
)

echo Running. Close the GUI window to exit.
exit /b 0