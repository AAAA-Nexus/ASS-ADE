# RECON_REPORT

**Path:** `C:\!aaaa-nexus\!ass-ade\src\ass_ade`  
**Duration:** 2328 ms

## Summary

Repo at `C:\!aaaa-nexus\!ass-ade\src\ass_ade` contains 137 files (134 source, 0 test-related) across 2 directory levels (1522.5 KB total). Test coverage: 0 test functions across 0 test files (ratio 0.0). Documentation coverage: 63%. Dominant tier: `at`.

## Scout

- Files: 137 (1522.5 KB)
- Source files: 134
- Max depth: 2
- Top-level: README.md, RECON_REPORT.md, __init__.py, __main__.py, a0_qk_constants, a1_at_functions, a2_mo_composites, a2a, a3_og_features, agent

**By extension:**
  - `.py`: 134
  - `.md`: 3

## Dependencies

- Python files: 134
- Unique external deps: 48
- Max import depth: 0
- Circular deps: none

## Tier Distribution

- `qk`: 9 — e.g. __init__.py, agent/__init__.py
- `at`: 81 — e.g. config.py, context_memory.py
- `mo`: 23 — e.g. agent/atlas.py, agent/bas.py
- `og`: 12 — e.g. a3_og_features/auth_gate.py, agent/alphaverus.py
- `sy`: 9 — e.g. cli.py, pipeline.py

**Violations:**
  - interpreter.py (at, 100KB — may span tiers)
  - map_terrain.py (at, 45KB — may span tiers)
  - recon.py (at, 30KB — may span tiers)
  - agent/capabilities.py (at, 35KB — may span tiers)
  - engine/rebuild/forge.py (at, 26KB — may span tiers)
  - engine/rebuild/schema_materializer.py (at, 19KB — may span tiers)
  - nexus/models.py (at, 38KB — may span tiers)
  - protocol/evolution.py (at, 26KB — may span tiers)

## Tests

- Test files: 0
- Test functions: 0
- Coverage ratio: 0.0
- Frameworks: none detected
- Untested modules: 116

**Untested (sample):**
  - `cli.py`
  - `config.py`
  - `context_memory.py`
  - `interpreter.py`
  - `map_terrain.py`
  - `pipeline.py`
  - `prompt_toolkit.py`
  - `recon.py`

## Documentation

- README: yes
- Doc files: 3
- Public callables: 1261
- Documented: 792 (63%)

**Missing docstrings (sample):**
  - `cli.py:init`
  - `cli.py:doctor`
  - `cli.py:plan`
  - `cli.py:full_cycle`
  - `cli.py:repo_summary`
  - `cli.py:protocol_run`
  - `cli.py:nexus_health`
  - `cli.py:nexus_agent_card`
  - `cli.py:nexus_mcp_manifest`
  - `cli.py:nexus_overview`

## Recommendations

1. Test coverage is low (0.0). Add tests for the 116 untested modules.
2. 8 file(s) may span tier boundaries. Split into smaller, single-purpose modules.

**Next action:** Run `ass-ade lint` for detailed style and security findings.
