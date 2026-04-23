# Sync scrubbed ASS-ADE ship surface from private !atomadic to public staging (!aaaa-nexus\!ass-ade).
# Requires: git, robocopy. Run from repo root:  powershell -NoProfile -File scripts/sync_public_ass_ade_staging.ps1
# Review `git status` in staging before committing.

param(
    [string]$PrivateRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
    [string]$StagingRoot = "C:\!aaaa-nexus\!ass-ade"
)

$ErrorActionPreference = "Stop"
if (-not (Test-Path -LiteralPath $StagingRoot)) {
    Write-Error "Staging root not found: $StagingRoot"
}
if (-not (Test-Path -LiteralPath (Join-Path $PrivateRoot "pyproject.toml"))) {
    Write-Error "Private root missing pyproject.toml: $PrivateRoot"
}

Push-Location -LiteralPath $StagingRoot
try {
    $legacy = @(
        "benchmarks", "examples", "hooks", "mcp", "prompts", "skills", "tools",
        "src", "tests", "scripts"
    )
    foreach ($d in $legacy) {
        if (Test-Path -LiteralPath $d) {
            git rm -r -f --ignore-unmatch $d 2>$null
        }
    }
} finally {
    Pop-Location
}

# Untracked junk
$junk = @(
    (Join-Path $StagingRoot ".pytest_tmp"),
    (Join-Path $StagingRoot ".claude"),
    (Join-Path $StagingRoot "rebuilt_test"),
    (Join-Path $StagingRoot "ass-ade-v1.1\\.import_linter_cache"),
    (Join-Path $StagingRoot "ass-ade-v1.1\\.pytest_cache"),
    (Join-Path $StagingRoot "ass-ade-v1.1\\_cov_tmp_out"),
    (Join-Path $StagingRoot "ass-ade-v1.1\\_cov_tmp_out2"),
    (Join-Path $StagingRoot "ass-ade-v1.1\\cov_annot"),
    (Join-Path $StagingRoot "ass-ade-v1.1\\.coverage")
)
foreach ($j in $junk) {
    if (Test-Path -LiteralPath $j) {
        Remove-Item -LiteralPath $j -Recurse -Force -ErrorAction SilentlyContinue
    }
}

$excludeDirs = @(
    ".pytest_cache",
    "__pycache__",
    ".pytest_tmp",
    ".ruff_cache",
    ".import_linter_cache",
    "_cov_tmp_out",
    "_cov_tmp_out2",
    "cov_annot"
)
$excludeFiles = @(".coverage")

$rcArgs = @(
    (Join-Path $PrivateRoot "ass-ade-v1.1"),
    (Join-Path $StagingRoot "ass-ade-v1.1"),
    "/MIR",
    "/XD"
) + $excludeDirs + @(
    "/XF"
) + $excludeFiles + @(
    "/NFL", "/NDL", "/NJH", "/NJS"
)
& robocopy @rcArgs
if ($LASTEXITCODE -ge 8) { throw "robocopy ass-ade-v1.1 failed: $LASTEXITCODE" }

foreach ($pair in @(
    @( "docs", "docs" ),
    @( ".github", ".github" ),
    @( "agents", "agents" ),
    @( "scripts", "scripts" )
)) {
    $src = Join-Path $PrivateRoot $pair[0]
    $dst = Join-Path $StagingRoot $pair[1]
    if (-not (Test-Path -LiteralPath $src)) { continue }
    $r = @($src, $dst, "/MIR", "/XD") + $excludeDirs + @("/XF") + $excludeFiles + @("/NFL", "/NDL", "/NJH", "/NJS")
    & robocopy @r
    if ($LASTEXITCODE -ge 8) { throw "robocopy $($pair[0]) failed: $LASTEXITCODE" }
}

$rootFiles = @(
    "pyproject.toml", "LICENSE", "CONTRIBUTING.md", "SECURITY.md", "AGENTS.md",
    "ASS_ADE_SHIP_PLAN.md", "ASS_ADE_GOAL_PIPELINE.md", "ASS_ADE_MATRIX.md",
    "ENTER-SHIP-LOOP.cmd", "RULES.md"
)
foreach ($f in $rootFiles) {
    $from = Join-Path $PrivateRoot $f
    $to = Join-Path $StagingRoot $f
    if (Test-Path -LiteralPath $from) {
        Copy-Item -LiteralPath $from -Destination $to -Force
    }
}

$pubReadme = Join-Path $PrivateRoot "docs\PUBLIC_SHOWCASE_README.md"
$stagingReadme = Join-Path $StagingRoot "README.md"
if (Test-Path -LiteralPath $pubReadme) {
    Copy-Item -LiteralPath $pubReadme -Destination $stagingReadme -Force
}
$dup = Join-Path $StagingRoot "docs\PUBLIC_SHOWCASE_README.md"
if (Test-Path -LiteralPath $dup) {
    Remove-Item -LiteralPath $dup -Force
}

# Ensure staging ignores local pytest temp
$gitignore = Join-Path $StagingRoot ".gitignore"
if (Test-Path -LiteralPath $gitignore) {
    $gi = Get-Content -LiteralPath $gitignore -Raw
    if ($gi -notmatch '(?m)^\.pytest_tmp/') {
        Add-Content -LiteralPath $gitignore -Value "`n.pytest_tmp/`n"
    }
}

Write-Host "Done. Next: cd `"$StagingRoot`"; git status; ass-ade-unified ade ship-audit --staging-root `"$StagingRoot`""
