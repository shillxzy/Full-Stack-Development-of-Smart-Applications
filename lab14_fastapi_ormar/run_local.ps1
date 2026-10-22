# ЛР 14 без Docker: локальний PostgreSQL (start_postgres.ps1) + uvicorn.
# Запуск: powershell -ExecutionPolicy Bypass -File run_local.ps1   ->  http://localhost:8000/docs
& (Join-Path $PSScriptRoot "..\start_postgres.ps1")
$env:DATABASE_URL = "postgresql://user:password@localhost:5433/booksdb"
Set-Location $PSScriptRoot
& "..\.venv-fastapi\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000
