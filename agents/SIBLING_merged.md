# RECON_REPORT

**Path:** `C:\!aaaa-nexus\!ass-ade-merged`  
**Duration:** 1734 ms

## Summary

Repo at `C:\!aaaa-nexus\!ass-ade-merged` contains 2000 files (73 source, 474 test-related) across 2 directory levels (11332.1 KB total). Circular import detected (2 cycle(s)). Test coverage: 411 test functions across 14 test files (ratio 0.25). Documentation coverage is low (40%). Dominant tier: `at`.

## Scout

- Files: 2000 (11332.1 KB)
- Source files: 73
- Max depth: 2
- Top-level: .env, .github, .gitignore, 0_README.md, 1_QUICKSTART.md, 2_ARCHITECTURE.md, 3_USER_GUIDE.md, 4_FEATURES.md, 5_CONTRIBUTING.md, ASS_ADE_OUTPUT.json

**By extension:**
  - `.json`: 1904
  - `.py`: 73
  - `.md`: 13
  - `.yml`: 5
  - `[no_ext]`: 3
  - `.yaml`: 1
  - `.toml`: 1

## Dependencies

- Python files: 73
- Unique external deps: 135
- Max import depth: 1
- Circular deps: YES — ['a0_qk_constants/annotated_handlers.py → a0_qk_constants/json_schema.py → a0_qk_constants/annotated_handlers.py', 'a0_qk_constants/_generate_schema.py → a0_qk_constants/_schema_generation_shared.py → a0_qk_constants/_generate_schema.py']

## Tier Distribution

- `qk`: 1 — e.g. a0_qk_constants/__init__.py
- `at`: 38 — e.g. __init__.py, a0_qk_constants/annotated_handlers.py
- `mo`: 9 — e.g. a0_qk_constants/constrain.py, a0_qk_constants/manifest.py
- `og`: 14 — e.g. a0_qk_constants/exceptions.py, a0_qk_constants/json_schema.py
- `sy`: 11 — e.g. a0_qk_constants/cli.py, a0_qk_constants/import_benchmark.py

**Violations:**
  - a0_qk_constants/core_schema.py (at, 156KB — may span tiers)
  - a0_qk_constants/schema_materializer.py (at, 19KB — may span tiers)
  - a0_qk_constants/test_exceptions.py (at, 24KB — may span tiers)
  - a0_qk_constants/test_validators.py (at, 88KB — may span tiers)
  - a0_qk_constants/_macos.py (at, 20KB — may span tiers)
  - a0_qk_constants/__init__.py (qk, 29KB — may span tiers)

## Tests

- Test files: 14
- Test functions: 411
- Coverage ratio: 0.25
- Frameworks: pytest, unittest
- Untested modules: 50

**Untested (sample):**
  - `a0_qk_constants/annotated_handlers.py`
  - `a0_qk_constants/arguments_schema.py`
  - `a0_qk_constants/bindings.py`
  - `a0_qk_constants/constrain.py`
  - `a0_qk_constants/constructors.py`
  - `a0_qk_constants/core_schema.py`
  - `a0_qk_constants/import_benchmark.py`
  - `a0_qk_constants/json_schema.py`

## Documentation

- README: yes
- Doc files: 13
- Public callables: 1364
- Documented: 542 (40%)

**Missing docstrings (sample):**
  - `a0_qk_constants/cli.py:parse_args`
  - `a0_qk_constants/cli.py:main`
  - `a0_qk_constants/cli.py:run`
  - `a0_qk_constants/cli.py:from_arguments`
  - `a0_qk_constants/cli.py:load`
  - `a0_qk_constants/cli.py:filenotfound_error`
  - `a0_qk_constants/cli.py:parsing_error`
  - `a0_qk_constants/cli.py:validation_error`
  - `a0_qk_constants/cli.py:validation_success`
  - `a0_qk_constants/cli.py:filenotfound_error`

## Recommendations

1. Resolve 2 circular import(s) — introduce an interface layer or inversion-of-control.
2. Test coverage is low (0.25). Add tests for the 50 untested modules.
3. 6 file(s) may span tier boundaries. Split into smaller, single-purpose modules.

**Next action:** Fix circular imports first, then increase test coverage.
