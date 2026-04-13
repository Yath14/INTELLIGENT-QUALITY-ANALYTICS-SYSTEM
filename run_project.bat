@echo off
REM Intelligent Quality Analytics System - Windows Startup Script

cd /d "%~dp0"

IF EXIST ".venv\Scripts\python.exe" (
    call .venv\Scripts\activate.bat
) ELSE IF EXIST "venv\Scripts\python.exe" (
    call venv\Scripts\activate.bat
) ELSE (
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
)

echo Starting the project...
python run_project.py
pause
