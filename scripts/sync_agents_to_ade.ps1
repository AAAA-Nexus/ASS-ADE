# Sync canonical agents/ into ADE/ (preserve ADE harness + ADE-only files).
# Run from repo root: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_agents_to_ade.ps1
$ErrorActionPreference = 'Stop'
$root = Resolve-Path (Join-Path $PSScriptRoot '..')
$src = Join-Path $root 'agents'
$dst = Join-Path $root 'ADE'
if (-not (Test-Path -LiteralPath $src)) { throw "missing agents/: $src" }
if (-not (Test-Path -LiteralPath $dst)) { New-Item -ItemType Directory -Path $dst | Out-Null }

$preserve = @(
    'harness',
    'HARNESS_README.md',
    'sync_ade_swarm_to_cursor.py',
    '25-ade-harness-sentinel.prompt.md'
)

Get-ChildItem -LiteralPath $src -File | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $dst $_.Name) -Force
}

Write-Host "Synced agents/* files into ADE/. Preserved: $($preserve -join ', ')"
