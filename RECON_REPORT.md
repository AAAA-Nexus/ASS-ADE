# RECON_REPORT

**Path:** `C:\!aaaa-nexus\!ass-ade`  
**Duration:** 5234 ms

## Summary

Repo at `C:\!aaaa-nexus\!ass-ade` contains 396 files (229 source, 87 test-related) across 4 directory levels (2854.0 KB total). Test coverage: 1081 test functions across 70 test files (ratio 0.5). Documentation coverage is low (38%). Dominant tier: `at`.

## Scout

- Files: 396 (2854.0 KB)
- Source files: 229
- Max depth: 4
- Top-level: .claude, .cursor, .env, .github, .vscode, .wrangler, AGENTS.md, CONTRIBUTING.md, README.md, RECON_REPORT.md

**By extension:**
  - `.py`: 227
  - `.md`: 91
  - `.json`: 55
  - `.yml`: 8
  - `.txt`: 6
  - `[no_ext]`: 2
  - `.js`: 2
  - `.ipynb`: 2

## Dependencies

- Python files: 227
- Unique external deps: 61
- Max import depth: 0
- Circular deps: none

## Tier Distribution

- `qk`: 13 — e.g. scripts/fix_a2a_and_pipeline.py, scripts/fix_annotated.py
- `at`: 131 — e.g. scripts/__init__.py, scripts/lora_training/__init__.py
- `mo`: 25 — e.g. src/ass_ade/agent/atlas.py, src/ass_ade/agent/bas.py
- `og`: 12 — e.g. src/ass_ade/agent/alphaverus.py, src/ass_ade/agent/dgm_h.py
- `sy`: 46 — e.g. hooks/post_rebuild.py, hooks/post_rebuild_collect_training.py

**Violations:**
  - src/ass_ade/interpreter.py (at, 100KB — may span tiers)
  - src/ass_ade/map_terrain.py (at, 45KB — may span tiers)
  - src/ass_ade/recon.py (at, 30KB — may span tiers)
  - src/ass_ade/agent/capabilities.py (at, 35KB — may span tiers)
  - src/ass_ade/engine/rebuild/forge.py (at, 25KB — may span tiers)
  - src/ass_ade/engine/rebuild/schema_materializer.py (at, 19KB — may span tiers)
  - src/ass_ade/nexus/models.py (at, 38KB — may span tiers)
  - src/ass_ade/protocol/evolution.py (at, 26KB — may span tiers)
  - tests/test_free_providers.py (at, 32KB — may span tiers)
  - tests/test_new_commands.py (at, 39KB — may span tiers)

## Tests

- Test files: 70
- Test functions: 1081
- Coverage ratio: 0.5
- Frameworks: pytest, unittest
- Untested modules: 108

**Untested (sample):**
  - `hooks/post_rebuild.py`
  - `hooks/post_rebuild_collect_training.py`
  - `hooks/post_rebuild_context_load.py`
  - `hooks/post_rebuild_docs.py`
  - `hooks/post_rebuild_eco_scan.py`
  - `hooks/pre_prompt_governance.py`
  - `hooks/pre_rebuild.py`
  - `hooks/pre_rebuild_validate.py`

## Documentation

- README: yes
- Doc files: 97
- Public callables: 2637
- Documented: 995 (38%)

**Missing docstrings (sample):**
  - `scripts/atomadic_dev_harness.py:main`
  - `scripts/check_evolution_context.py:main`
  - `scripts/cli.py:cmd_recon`
  - `scripts/cli.py:cmd_enhance`
  - `scripts/cli.py:cmd_rebuild`
  - `scripts/cli.py:main`
  - `scripts/epiphany_breakthrough_local.py:main`
  - `scripts/github_evolution_control.py:cmd_gate`
  - `scripts/github_evolution_control.py:main`
  - `scripts/lora_train.py:main`

## Recommendations

1. Docstring coverage is 38%. Add docstrings to public functions and classes.
2. 10 file(s) may span tier boundaries. Split into smaller, single-purpose modules.

**Next action:** Run `ass-ade lint` for detailed style and security findings.
