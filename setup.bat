@echo off
echo ========================================================
echo Antigravity Local Environment Bootstrap (Windows)
echo ========================================================

:: Check for Python and install via winget if missing
python --version >nul 2>&1
if %errorlevel% neq 0 (
    py -3 --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [System] 'python' missing but 'py -3' found. Using Windows Launcher.
    ) else (
        echo [ERROR] Python 3.10+ is missing! 
        echo [System] Attempting native bootstrap via winget...
        winget install -e --id Python.Python.3.10 --accept-source-agreements --accept-package-agreements
        if %errorlevel% neq 0 (
            echo [CRITICAL] Automatic python installation failed. Please install Python manually from python.org.
            pause
            exit /b
        )
        echo [System] Python installed. Please RESTART this terminal and run setup.bat again.
        pause
        exit /b
    )
)

:: Create or Heal virtual environment
echo [1/3] Creating/Healing isolated virtual environment natively...
set VENV_BROKEN=0
if exist .venv (
    .\.venv\Scripts\python.exe --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [System] .venv is corrupted. Erasing and Auto-healing...
        rmdir /s /q .venv
        set VENV_BROKEN=1
    )
) else (
    set VENV_BROKEN=1
)

if %VENV_BROKEN%==1 (
    python -m venv .venv >nul 2>&1
    if %errorlevel% neq 0 (
        echo [System] python fallback to py -3...
        py -3 -m venv .venv
    )
)
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
    echo [System] Generating cryptographically unique Signature Key...
    python -c "import uuid; open('.env', 'w', encoding='utf-8').write(f'AGENT_PRIVATE_SIGNATURE_KEY={uuid.uuid4().hex}\n')"
    echo   - Created .env correctly with secure dynamic key.
) else (
    echo   - .env already exists.
)

echo.
echo ========================================================
echo ✅ Local Workspace securely initialized. 
echo Run ".venv\Scripts\activate" to enter the isolated mode.
echo ========================================================
pause
