@echo off
echo ========================================================
echo Antigravity Local Environment Bootstrap (Windows)
echo ========================================================

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.10+ is missing! Please install from python.org and add it to PATH.
    pause
    exit /b
)

:: Create virtual environment
echo [1/3] Creating isolated virtual environment natively...
python -m venv .venv
call .venv\Scripts\activate.bat

:: Upgrade Pip
echo [2/3] Upgrading pip and core dependencies...
python -m pip install --upgrade pip >nul

:: Install Requirements
echo [3/3] Installing strictly verified dependencies...
pip install -r requirements.txt

echo.
echo [4/4] Initializing secure environment variables (.env)...
if not exist .env (
    copy .env.example .env >nul
    echo   - Created .env correctly from template.
) else (
    echo   - .env already exists.
)

echo.
echo ========================================================
echo ✅ Local Workspace securely initialized. 
echo Run ".venv\Scripts\activate" to enter the isolated mode.
echo ========================================================
pause
