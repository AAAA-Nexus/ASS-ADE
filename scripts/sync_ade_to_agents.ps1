# Copy ADE/ refinements into canonical agents/ (reverse of sync_agents_to_ade.ps1).
# Skips ADE-only harness files. Run from repo root:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_ade_to_agents.ps1
$ErrorActionPreference = 'Stop'
$root = Resolve-Path (Join-Path $PSScriptRoot '..')
$src = Join-Path $root 'ADE'
$dst = Join-Path $root 'agents'
if (-not (Test-Path -LiteralPath $src)) { throw "missing ADE/: $src" }
if (-not (Test-Path -LiteralPath $dst)) { throw "missing agents/: $dst" }

# ADE-only: not mirrored under agents/
$adeOnly = @(
    '25-ade-harness-sentinel.prompt.md',
    'sync_ade_swarm_to_cursor.py',
    'HARNESS_README.md'
)

$copied = New-Object System.Collections.Generic.List[string]
Get-ChildItem -LiteralPath $src -File | ForEach-Object {
    if ($adeOnly -contains $_.Name) { return }
    $target = Join-Path $dst $_.Name
    if (Test-Path -LiteralPath $target) {
        Copy-Item -LiteralPath $_.FullName -Destination $target -Force
        $null = $copied.Add($_.Name)
    }
}

Write-Host "Synced ADE/* -> agents/ for $($copied.Count) files (ADE-only files skipped)."
