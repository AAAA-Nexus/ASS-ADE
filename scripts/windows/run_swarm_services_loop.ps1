# Long-running swarm automation (PowerShell) — run from repo root.
# Stops on Ctrl+C. For a detached process, use Task Scheduler or `Start-Process`.
$ErrorActionPreference = "Stop"
$repo = if ($args[0]) { $args[0] } else { (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path }
Set-Location $repo
$env:ATOMADIC_WORKSPACE = $repo
# Optional overrides:
# $env:SWARM_TICK_SEC = "180"
# $env:SWARM_REGEN_DOCS = "1"
# $env:SWARM_BROADCAST_READY = "0"
& python (Join-Path $repo "scripts\run_swarm_services.py") @("run")
