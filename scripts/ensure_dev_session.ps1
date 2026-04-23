# One-click host prep for SWARM-ONE-PROMPT.md (Windows, repo root).
# Run:  powershell -NoProfile -ExecutionPolicy Bypass -File scripts/ensure_dev_session.ps1
$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root
$env:ATOMADIC_WORKSPACE = $root.Path
$env:SWARM_AGENT = "orchestrator"
$ws = $env:ATOMADIC_WORKSPACE
Write-Host "== ASS-ADE dev session - ATOMADIC_WORKSPACE = $ws ==" -ForegroundColor Cyan
& python (Join-Path $root "scripts\run_swarm_services.py") @("once")
& python (Join-Path $root "scripts\regenerate_ass_ade_docs.py")
Write-Host ""
Write-Host 'Next: optional second terminal, leave it open and run:' -ForegroundColor Yellow
Write-Host '  python scripts\run_swarm_services.py run'
Write-Host ""
Write-Host 'Then open SWARM-ONE-PROMPT.md and paste the boxed block into Cursor, VS Code, or Codex.'
Write-Host ""
