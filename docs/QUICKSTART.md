# Quick Start

This guide gets a fresh ASS-ADE checkout installed, verified, and ready for the
first scout and assimilation loop.

New to the project language? Keep [GLOSSARY.md](GLOSSARY.md) open for the
plain-English version of terms like RAG, scout, assimilation, and trust gates.

## Requirements

- Python 3.12 or newer.
- Git.
- A shell from the repository root.
- Optional: Node/Rust/etc. if you are scouting or rebuilding projects that use
  those ecosystems.

## Install

```powershell
git clone https://github.com/AAAA-Nexus/ASS-ADE.git
cd ASS-ADE
python -m pip install -e ".[dev]"
```

If the console script is not on `PATH`, use the module form:

```powershell
python -m ass_ade --help
```

## Verify

```powershell
python -m ass_ade --version
python -m ass_ade doctor
python -m ass_ade --help
```

The package also installs these console scripts when the editable install is
resolved correctly:

```powershell
ass-ade --help
atomadic --help
```

## First Scout

Scout a sibling repository and compare it to the current ASS-ADE seed:

```powershell
python -m ass_ade scout ..\some-sibling-repo --benefit-root . --json-out .ass-ade\scout-sibling.json
```

For deterministic local-only scouting:

```powershell
python -m ass_ade scout ..\some-sibling-repo --benefit-root . --no-llm --json-out .ass-ade\scout-sibling.json
```

## First Cherry Pick

Review the scout report and write a manifest:

```powershell
python -m ass_ade cherry-pick .ass-ade\scout-sibling.json --target .
```

For a non-interactive dry selection of every candidate:

```powershell
python -m ass_ade cherry-pick .ass-ade\scout-sibling.json --target . --pick all --no-interactive --json
```

## First Assimilation

After reviewing `.ass-ade/cherry_pick.json`, assimilate it into the target tree:

```powershell
python -m ass_ade assimilate .ass-ade\cherry_pick.json --target .
```

Use the target map when you need a broader sibling inventory before choosing
what to take:

```powershell
python -m ass_ade selfbuild target-map --primary . --parent .. --pattern "!ass-ade*" --out .ass-ade\target-map.json
```

## Validate Your Checkout

```powershell
python -m pytest
python -m ruff check src tests
python scripts\doc_coverage.py
```

## Local RAG Smoke Test

```powershell
python -m ass_ade context store "trusted quickstart memory" --namespace quickstart --path . --json
python -m ass_ade context query "quickstart memory" --namespace quickstart --path . --json
```

Private owner RAG uses `python -m ass_ade search` and requires
`ATOMADIC_SESSION_TOKEN`. See [RAG_PUBLIC_PRIVATE.md](RAG_PUBLIC_PRIVATE.md).

## Wakeup And Launch Smoke Test

```powershell
python -m ass_ade wakeup --check --json
python -m ass_ade launch status --no-write
```

See [ATOMADIC_WAKEUP_LAUNCH.md](ATOMADIC_WAKEUP_LAUNCH.md).

## Common Fixes

If `ass-ade` resolves to an old install:

```powershell
where ass-ade
python -m pip show ass-ade
python -c "import ass_ade; print(ass_ade.__file__)"
python -m pip install -e ".[dev]"
```

For deeper environment help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
