# Remove orphaned pip/uninstall folders (names starting with "~") under site-packages.
# These cause "Ignoring invalid distribution ~..." warnings and can confuse imports.
# Safe to run; only deletes directories whose names start with "~".
# Usage: pwsh -File scripts/repair_pip_corruption.ps1
#        (optional) $env:PYTHON_SITE_PACKAGES = "C:\...\site-packages"

$ErrorActionPreference = "Stop"
if (-not $env:PYTHON_SITE_PACKAGES) {
    $sp = python -c "import site; print(site.getsitepackages()[0])" 2>$null
    if (-not $sp) { throw "Could not resolve site-packages; set PYTHON_SITE_PACKAGES." }
} else {
    $sp = $env:PYTHON_SITE_PACKAGES
}
$removed = @()
Get-ChildItem -LiteralPath $sp -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -like '~*' } |
    ForEach-Object {
        Remove-Item -LiteralPath $_.FullName -Recurse -Force
        $removed += $_.Name
    }
if ($removed.Count -eq 0) {
    Write-Host "No tilde-prefixed junk in $sp"
} else {
    Write-Host "Removed from site-packages:"
    $removed | ForEach-Object { Write-Host "  $_" }
}
