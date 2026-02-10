@echo off
setlocal

cd /d "%~dp0"

if exist ".venv\Scripts\activate.bat" (
  call ".venv\Scripts\activate.bat"
) else if exist "venv\Scripts\activate.bat" (
  call "venv\Scripts\activate.bat"
)

set "PYTHON=python"
where %PYTHON% >nul 2>nul
if errorlevel 1 (
  set "PYTHON=python3"
  where %PYTHON% >nul 2>nul
  if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.
    exit /b 1
  )
)

%PYTHON% -c "import importlib, sys; missing=[]; [missing.append(m) for m in ['flask','flask_socketio','watchdog'] if importlib.util.find_spec(m) is None]; sys.exit(1 if missing else 0)"
if errorlevel 1 (
  echo [INFO] Installing missing UI dependencies
  %PYTHON% -m pip install -r requirements-groq.txt
  %PYTHON% -m pip install watchdog
)

echo [INFO] Starting control panel on http://localhost:8421
%PYTHON% control_panel.py
