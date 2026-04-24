# RECON_REPORT

**Path:** `C:\!aaaa-nexus\!ass-ade-cursor-dev-20260420-1710`  
**Duration:** 6312 ms

## Summary

Repo at `C:\!aaaa-nexus\!ass-ade-cursor-dev-20260420-1710` contains 2000 files (365 source, 82 test-related) across 6 directory levels (12315.7 KB total). Test coverage: 1074 test functions across 67 test files (ratio 0.25). Documentation coverage is low (46%). Dominant tier: `at`.

## Scout

- Files: 2000 (12315.7 KB)
- Source files: 365
- Max depth: 6
- Top-level: candidates, claw-handoff, merged, primary, reports

**By extension:**
  - `.json`: 1535
  - `.py`: 364
  - `.md`: 75
  - `.yml`: 12
  - `[no_ext]`: 5
  - `.mmd`: 3
  - `.toml`: 2
  - `.ipynb`: 2

## Dependencies

- Python files: 364
- Unique external deps: 61
- Max import depth: 0
- Circular deps: none

## Tier Distribution

- `qk`: 21 — e.g. candidates/ass-ade-fix/a0_qk_constants/__init__.py, candidates/ass-ade-fix/a1_at_functions/__init__.py
- `at`: 203 — e.g. candidates/ass-ade-fix/a0_qk_constants/schema_materializer.py, candidates/ass-ade-fix/a0_qk_constants/tokens.py
- `mo`: 60 — e.g. candidates/ass-ade-fix/a0_qk_constants/proofbridge.py, candidates/ass-ade-fix/a1_at_functions/bas.py
- `og`: 29 — e.g. candidates/ass-ade-fix/a1_at_functions/dgm_h.py, candidates/ass-ade-fix/a1_at_functions/plan.py
- `sy`: 51 — e.g. candidates/ass-ade-fix/a1_at_functions/cli.py, candidates/ass-ade-fix/a1_at_functions/golden_runner.py

**Violations:**
  - candidates/ass-ade-fix/a0_qk_constants/schema_materializer.py (at, 20KB — may span tiers)
  - candidates/ass-ade-fix/a1_at_functions/capabilities.py (at, 21KB — may span tiers)
  - candidates/ass-ade-fix/a1_at_functions/evolution.py (at, 27KB — may span tiers)
  - candidates/ass-ade-fix/a1_at_functions/interpreter.py (at, 91KB — may span tiers)
  - candidates/ass-ade-fix/a2_mo_composites/map_terrain.py (at, 46KB — may span tiers)
  - candidates/ass-ade-fix/a2_mo_composites/models.py (at, 38KB — may span tiers)
  - candidates/ass-ade-fix/a2_mo_composites/recon.py (at, 31KB — may span tiers)
  - candidates/ass-ade-fix/src/ass_ade/interpreter.py (at, 91KB — may span tiers)
  - candidates/ass-ade-fix/src/ass_ade/map_terrain.py (at, 45KB — may span tiers)
  - candidates/ass-ade-fix/src/ass_ade/recon.py (at, 30KB — may span tiers)

## Tests

- Test files: 67
- Test functions: 1074
- Coverage ratio: 0.25
- Frameworks: pytest, unittest
- Untested modules: 201

**Untested (sample):**
  - `candidates/ass-ade-fix/a0_qk_constants/proofbridge.py`
  - `candidates/ass-ade-fix/a0_qk_constants/schema_materializer.py`
  - `candidates/ass-ade-fix/a1_at_functions/bas.py`
  - `candidates/ass-ade-fix/a1_at_functions/conversation.py`
  - `candidates/ass-ade-fix/a1_at_functions/cycle.py`
  - `candidates/ass-ade-fix/a1_at_functions/dgm_h.py`
  - `candidates/ass-ade-fix/a1_at_functions/evolution.py`
  - `candidates/ass-ade-fix/a1_at_functions/golden_runner.py`

## Documentation

- README: yes
- Doc files: 76
- Public callables: 4433
- Documented: 2036 (46%)

**Missing docstrings (sample):**
  - `candidates/ass-ade-fix/a0_qk_constants/proofbridge.py:Lean4Spec`
  - `candidates/ass-ade-fix/a0_qk_constants/proofbridge.py:ProofBridge`
  - `candidates/ass-ade-fix/a0_qk_constants/proofbridge.py:translate`
  - `candidates/ass-ade-fix/a0_qk_constants/proofbridge.py:run`
  - `candidates/ass-ade-fix/a0_qk_constants/proofbridge.py:report`
  - `candidates/ass-ade-fix/a0_qk_constants/tokens.py:for_model`
  - `candidates/ass-ade-fix/a1_at_functions/bas.py:Alert`
  - `candidates/ass-ade-fix/a1_at_functions/bas.py:BAS`
  - `candidates/ass-ade-fix/a1_at_functions/bas.py:subscribe`
  - `candidates/ass-ade-fix/a1_at_functions/bas.py:alert`

## Recommendations

1. Test coverage is low (0.25). Add tests for the 201 untested modules.
2. 10 file(s) may span tier boundaries. Split into smaller, single-purpose modules.

**Next action:** Run `ass-ade lint` for detailed style and security findings.
