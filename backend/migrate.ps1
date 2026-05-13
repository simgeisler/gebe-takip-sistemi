# Alembic: PATH'te "alembic" olmasa da calisir. Klasorde: .\migrate.ps1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$candidates = @(
    @{ Name = ".venv"; Exe = Join-Path $PSScriptRoot ".venv\Scripts\python.exe" }
    @{ Name = "venv";  Exe = Join-Path $PSScriptRoot "venv\Scripts\python.exe" }
)

$python = $null
foreach ($c in $candidates) {
    if (Test-Path $c.Exe) {
        $python = $c.Exe
        Write-Host "Kullanilan Python: $($c.Name) -> $python"
        break
    }
}

if (-not $python) {
    $pyCmd = Get-Command python -ErrorAction SilentlyContinue
    if ($pyCmd -and (Test-Path $pyCmd.Source)) {
        $python = $pyCmd.Source
        Write-Host "Kullanilan Python: PATH -> $python"
    }
}

if (-not $python) {
    Write-Host @"
Python bulunamadi.

1) Python 3.12+ kur: https://www.python.org/downloads/ (kurulumda "Add python.exe to PATH" sec)
2) Bu klasorde sanal ortam olustur:
   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
3) Sonra tekrar: .\migrate.ps1
"@
    exit 1
}

& $python -m pip show alembic *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "alembic yuklu degil; yukleniyor..."
    & $python -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")
}

Write-Host "alembic upgrade head calistiriliyor..."
& $python -m alembic upgrade head
Write-Host "Bitti (exit $LASTEXITCODE)."
