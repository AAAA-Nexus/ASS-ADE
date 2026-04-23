# RECON_REPORT

**Path:** `C:\!atomadic\ass-ade-v1.1\tests\fixtures\minimal_pkg`  
**Duration:** 0 ms

## Summary

Repo at `C:\!atomadic\ass-ade-v1.1\tests\fixtures\minimal_pkg` contains 4 files (2 source, 4 test-related) across 1 directory levels (2.3 KB total). Test coverage: 0 test functions across 0 test files (ratio 0.0). Documentation coverage: 60%. Dominant tier: `at`.

## Scout

- Files: 4 (2.3 KB)
- Source files: 2
- Max depth: 1
- Top-level: RECON_REPORT.md, example_pkg, pyproject.toml

**By extension:**
  - `.py`: 2
  - `.toml`: 1
  - `.md`: 1

## Dependencies

- Python files: 2
- Unique external deps: 0
- Max import depth: 0
- Circular deps: none

## Tier Distribution

- `qk`: 0
- `at`: 2 — e.g. example_pkg/core.py, example_pkg/__init__.py
- `mo`: 0
- `og`: 0
- `sy`: 0

## CNA Compatibility

- Status: not_applicable
- Tier dirs found: none
- Files checked: 0
- Python atom files: 0
- JSON atom files: 0
- Current ids: 0
- Legacy ids: 0
- Invalid ids: 0
- Filename issues: 0
- Id/stem mismatches: 0
- Paired file mismatches: 0
- Tier mismatches: 0

## Tests

- Test files: 0
- Test functions: 0
- Coverage ratio: 0.0
- Frameworks: none detected
- Untested modules: 1

- Note: No monadic tier directories found at the scan root.

**Untested (sample):**
  - `example_pkg/core.py`

## Documentation

- README: MISSING
- Doc files: 1
- Public callables: 5
- Documented: 3 (60%)

**Missing docstrings (sample):**
  - `example_pkg/core.py:pure_helper`
  - `example_pkg/core.py:run`

## Recommendations

1. Test coverage is low (0.0). Add tests for the 1 untested modules.
2. No README.md found. Add one for onboarding context.

**Next action:** Run `ass-ade lint` for detailed style and security findings.
