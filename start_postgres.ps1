# Запускає окремий кластер PostgreSQL для ЛР 14-15 (без Docker).
# Кластер лежить у .pgdata, порт 5433, користувач user / пароль password (як у методичці).
# Службу postgresql-x64-18 і її базу скрипт не чіпає.
#
# Запуск:  powershell -ExecutionPolicy Bypass -File start_postgres.ps1
# Зупинка: powershell -ExecutionPolicy Bypass -File start_postgres.ps1 -Stop

param([switch]$Stop)

$PgBin = "D:\PostgreSQL\18\bin"          # змініть, якщо PostgreSQL встановлено деінде
$Data  = Join-Path $PSScriptRoot ".pgdata"
$Port  = 5433
$env:PGPASSWORD = "password"

if ($Stop) {
    & "$PgBin\pg_ctl.exe" -D $Data stop
    return
}

if (-not (Test-Path "$Data\PG_VERSION")) {
    Write-Host "Створюю кластер у $Data ..."
    $pw = New-TemporaryFile
    Set-Content -Path $pw -Value "password" -NoNewline -Encoding ascii
    & "$PgBin\initdb.exe" -D $Data -U user --pwfile=$pw --auth=scram-sha-256 -E UTF8 --locale=C
    Remove-Item $pw
}

& "$PgBin\pg_isready.exe" -h localhost -p $Port | Out-Null
if ($LASTEXITCODE -ne 0) {
    # Start-Process, щоб сервер працював у фоні й не тримав це вікно
    Start-Process -FilePath "$PgBin\pg_ctl.exe" -WindowStyle Hidden `
        -ArgumentList @("-D", "`"$Data`"", "-o", "`"-p $Port`"", "-l", "`"$Data\server.log`"", "start")
    for ($i = 0; $i -lt 30; $i++) {
        Start-Sleep -Milliseconds 500
        & "$PgBin\pg_isready.exe" -h localhost -p $Port | Out-Null
        if ($LASTEXITCODE -eq 0) { break }
    }
}

foreach ($db in @("booksdb", "booksdb_fk")) {
    $exists = & "$PgBin\psql.exe" -h localhost -p $Port -U user -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$db'"
    if ($exists -ne "1") { & "$PgBin\psql.exe" -h localhost -p $Port -U user -d postgres -c "CREATE DATABASE $db;" }
}
Write-Host "PostgreSQL працює: postgresql://user:password@localhost:$Port (бази booksdb, booksdb_fk)"
