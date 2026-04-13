# Intelligent Quality Analytics System - Windows Startup Script (PowerShell)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$Python = Join-Path $ScriptDir ".venv\Scripts\python.exe"
if (-Not (Test-Path $Python)) {
    $Python = Join-Path $ScriptDir "venv\Scripts\python.exe"
}

if (-Not (Test-Path $Python)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    & python -m pip install --upgrade pip
    & python -m pip install -r requirements.txt
    $Python = Join-Path $ScriptDir ".venv\Scripts\python.exe"
}

Write-Host "Starting the project..." -ForegroundColor Green
& $Python (Join-Path $ScriptDir "run_project.py")

Write-Host "Project finished." -ForegroundColor Green
