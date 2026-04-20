# ASS-ADE release checklist

Use this before tagging a release or publishing a milestone. All commands assume repository root `!ass-ade`.

## Pre-release (verified locally)

1. `python -m pip install -e ".[dev]"`
2. `python scripts/atomadic_dev_harness.py --full`  
   - Or minimal: `python scripts/atomadic_dev_harness.py --quick` plus the subset you changed.
3. `python scripts/check_evolution_context.py --roadmap .ass-ade/ass-ade-suite-roadmap.json`  
   - On a PR branch, pass `--git-range base...head` as in `.github/workflows/epiphany-cycle.yml`.
4. `python -m pytest tests/ -q --tb=line` for a full ship candidate.

## Version and changelog

1. Bump `version` in `pyproject.toml` per semver policy.
2. Summarize user-visible changes (CLI, MCP tools, Nexus behavior, CI) in `CHANGELOG.md` if the repo keeps one; otherwise use the GitHub **Releases** notes only.

## Promotion hygiene

1. Re-read `README.md` and `CONTRIBUTING.md` for stale commands.
2. Ensure `docs/demos/` demo files still carry `**Status:** PASS ✓` if demos are part of the release story (`tests/test_demos_and_import_budget.py`).

## Post-release

1. Append a **path-only** line to `.ass-ade/ass-ade-suite-roadmap.json` `growthNotes` describing what shipped.
2. Open a follow-up issue for any **DEFER** items (hosted MCP, benchmark baselines) with an owner.
