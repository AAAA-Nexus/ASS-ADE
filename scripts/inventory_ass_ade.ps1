# Bounded ASS-ADE fingerprint discovery (Windows).
# Writes: ASS_ADE_INVENTORY.paths.json, ASS_ADE_INVENTORY.md
# For the full ASS_ADE* doc suite (inventory + snapshot + matrix/ship/goal autogen blocks), use:
#   python scripts/regenerate_ass_ade_docs.py
$ErrorActionPreference = 'SilentlyContinue'
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
Set-Location $repoRoot

function Add-Row {
    param([string]$Path, [string]$Kind, [hashtable]$Extra = @{})
    $row = @{ path = $Path; kind = $Kind }
    foreach ($k in $Extra.Keys) { $row[$k] = $Extra[$k] }
    [pscustomobject]$row
}

$hits = [System.Collections.Generic.List[object]]::new()
$seenDirs = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)

function Try-AddDir {
    param([string]$FullPath)
    if ([string]::IsNullOrWhiteSpace($FullPath)) { return }
    if (-not (Test-Path -LiteralPath $FullPath)) { return }
    $null = $seenDirs.Add($FullPath)
}

# 1) Top-level C:\ and C:\!atomadic: directories named ass-ade*
foreach ($root in @('C:\', 'C:\!atomadic')) {
    if (-not (Test-Path -LiteralPath $root)) { continue }
    Get-ChildItem -LiteralPath $root -Directory -Filter 'ass-ade*' -ErrorAction SilentlyContinue | ForEach-Object {
        Try-AddDir $_.FullName
    }
}

# 2) Under %USERPROFILE% depth 6 (worktrees, source trees)
$user = $env:USERPROFILE
if (Test-Path -LiteralPath $user) {
    Get-ChildItem -LiteralPath $user -Directory -Filter 'ass-ade*' -Recurse -Depth 6 -ErrorAction SilentlyContinue | ForEach-Object {
        Try-AddDir $_.FullName
    }
}

# 3) Common dev roots
foreach ($extra in @('C:\dev', 'C:\src', 'C:\projects', 'C:\code', 'C:\git', 'C:\workspace')) {
    if (-not (Test-Path -LiteralPath $extra)) { continue }
    Get-ChildItem -LiteralPath $extra -Directory -Filter 'ass-ade*' -Recurse -Depth 5 -ErrorAction SilentlyContinue | ForEach-Object {
        Try-AddDir $_.FullName
    }
}

$v11Pointer = Join-Path $repoRoot 'ass-ade-v1.1\pyproject.toml'
$v11PointerFull = $null
if (Test-Path -LiteralPath $v11Pointer) {
    $v11PointerFull = [System.IO.Path]::GetFullPath($v11Pointer)
}

foreach ($d in $seenDirs) {
    $hits.Add((Add-Row -Path $d -Kind 'dir_ass_ade_star'))
    $tier = Join-Path $d '.ass-ade\tier-map.json'
    if (Test-Path -LiteralPath $tier) {
        $hits.Add((Add-Row -Path $tier -Kind 'tier_map'))
    }
    $py = Join-Path $d 'pyproject.toml'
    if (Test-Path -LiteralPath $py) {
        $pyFull = [System.IO.Path]::GetFullPath($py)
        if ($null -eq $v11PointerFull -or -not [string]::Equals($pyFull, $v11PointerFull, [StringComparison]::OrdinalIgnoreCase)) {
            $hits.Add((Add-Row -Path $py -Kind 'pyproject'))
        }
    }
}

# Umbrella monorepo root — ships `ass-ade-v1-1` / `ass-ade-unified` (T12); not under `ass-ade*` name.
$rootPy = Join-Path $repoRoot 'pyproject.toml'
if (Test-Path -LiteralPath $rootPy) {
    $hits.Add((Add-Row -Path $rootPy -Kind 'pyproject_root_spine'))
}

# T12 pointer under v1.1 tree (comments only; no `[project]`) — listed here instead of "next to roots".
if ($null -ne $v11PointerFull) {
    $hits.Add((Add-Row -Path $v11Pointer -Kind 'pyproject_v11_pointer'))
}

# 4) tier-map.json anywhere under C:\!atomadic (workspace) — catches !atomadic-uep etc.
if (Test-Path -LiteralPath 'C:\!atomadic') {
    Get-ChildItem -LiteralPath 'C:\!atomadic' -Filter 'tier-map.json' -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
        $hits.Add((Add-Row -Path $_.FullName -Kind 'tier_map_workspace'))
    }
}

$hits | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $repoRoot 'ASS_ADE_INVENTORY.paths.json') -Encoding utf8

$md = @()
$md += '# ASS-ADE inventory (auto-generated)'
$md += ''
$md += 'Fingerprint scan: directories `ass-ade*`, `.ass-ade/tier-map.json`, `pyproject.toml` under selected roots.'
$md += ''
$md += '## Directory roots (`ass-ade*`)'
$md += ''
foreach ($d in ($hits | Where-Object { $_.kind -eq 'dir_ass_ade_star' } | Sort-Object path)) {
    $md += "- ``$($d.path)``"
}
$md += ''
$md += '## tier-map.json hits'
$md += ''
foreach ($t in ($hits | Where-Object { $_.kind -like 'tier_map*' } | Sort-Object path -Unique)) {
    $md += "- ``$($t.path)``"
}
$md += ''
$md += '## pyproject.toml next to ass-ade roots'
$md += ''
foreach ($p in ($hits | Where-Object { $_.kind -eq 'pyproject' } | Sort-Object path)) {
    $md += "- ``$($p.path)``"
}
$md += ''
$md += '## Spine distribution (`pyproject.toml` at repo root, T12)'
$md += ''
foreach ($p in ($hits | Where-Object { $_.kind -eq 'pyproject_root_spine' } | Sort-Object path)) {
    $md += "- ``$($p.path)`` - canonical ``pip install -e .`` / ``ass-ade-unified`` metadata; sources under ``ass-ade-v1.1/src/``"
}
$md += ''
$md += '## v1.1 pointer stub (no `[project]`)'
$md += ''
$md += '- `ass-ade-v1.1/pyproject.toml` (relative to repo root) - T12 pointer only; canonical `[project]` lives in root `pyproject.toml`.'
if ($null -ne $v11PointerFull) {
    foreach ($p in ($hits | Where-Object { $_.kind -eq 'pyproject_v11_pointer' } | Sort-Object path)) {
        $md += "- Resolved on this host: ``$($p.path)``"
    }
}
$md += ''
$md | Set-Content -LiteralPath (Join-Path $repoRoot 'ASS_ADE_INVENTORY.md') -Encoding utf8

Write-Host "Dirs: $($seenDirs.Count) Hits written: $($hits.Count)"
