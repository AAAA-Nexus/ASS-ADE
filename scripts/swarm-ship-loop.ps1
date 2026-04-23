<#
.SYNOPSIS
  Repeat ASS-ADE ship gates until green (stop with Ctrl+C).

.DESCRIPTION
  Reruns scripts/ship_readiness_audit.py (doctor, lint-imports, pytest,
  synth-tests, golden assimilate, optional studio chat smoke). Same gates as CI.

  IP: never runs git push from C:\!atomadic. On success, prints staging for
  C:\!aaaa-nexus and push from that checkout only.

.PARAMETER UntilGreen
  Loop on failure until audit exits 0, or until Ctrl+C.

.PARAMETER MaxRounds
  Safety cap (0 = unlimited when -UntilGreen).

.PARAMETER SleepSec
  Seconds to wait between failed rounds.

.PARAMETER OneShot
  Single audit round then exit (no loop).
#>
param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [switch]$UntilGreen,
    [int]$MaxRounds = 0,
    [int]$SleepSec = 45,
    [switch]$OneShot
)

$ErrorActionPreference = "Stop"
$logDir = Join-Path $RepoRoot "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$logFile = Join-Path $logDir "swarm-ship-loop.log"
$py = Join-Path $RepoRoot "scripts\ship_readiness_audit.py"

if (-not (Test-Path $py)) {
    Write-Error "Missing $py"
    exit 2
}

function Write-Log([string]$msg) {
    $line = "$(Get-Date -Format o) $msg"
    Add-Content -Path $logFile -Value $line
    Write-Host $line
}

Write-Log "START repo=$RepoRoot UntilGreen=$UntilGreen OneShot=$OneShot MaxRounds=$MaxRounds SleepSec=$SleepSec"

$round = 0
do {
    $round++
    if ($MaxRounds -gt 0 -and $round -gt $MaxRounds) {
        Write-Log "STOP max_rounds=$MaxRounds"
        exit 3
    }

    $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $json = Join-Path $logDir "audit_$stamp.json"
    $env:SHIP_AUDIT_JSON = $json
    $env:PYTHONUTF8 = "1"
    $env:PYTHONPATH = ""

    Push-Location $RepoRoot
    try {
        & python $py
        $code = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    Write-Log "ROUND=$round EXIT=$code SHIP_AUDIT_JSON=$json"

    if ($code -eq 0) {
        Copy-Item -Force $json (Join-Path $logDir "LAST_GREEN.json")
        Write-Host ""
        Write-Host "=== SHIP GATES GREEN ===" -ForegroundColor Green
        Write-Host "Evidence: $json and logs/LAST_GREEN.json"
        Write-Host ""
        Write-Host "IP / next human steps (required for public ship):" -ForegroundColor Cyan
        Write-Host "  1. Stream B scrub: copy production-ready ASS-ADE into C:\!aaaa-nexus\ (approved layout)."
        Write-Host "  2. Run: ass-ade-unified ade ship-audit --staging-root C:\!aaaa-nexus\!ass-ade"
        Write-Host "  3. git push ONLY from that C:\!aaaa-nexus checkout - NEVER push all of C:\!atomadic."
        Write-Host "  4. Confirm GitHub Actions green on the merge SHA."
        Write-Host ""
        exit 0
    }

    if ($OneShot) {
        exit $code
    }
    if (-not $UntilGreen) {
        exit $code
    }

    Write-Log ('RETRY in ' + $SleepSec + ' sec (Ctrl+C to stop)')
    Start-Sleep -Seconds $SleepSec
} while ($true)
