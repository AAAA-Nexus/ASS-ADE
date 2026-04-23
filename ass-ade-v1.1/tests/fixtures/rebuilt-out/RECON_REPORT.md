# RECON_REPORT

**Path:** `C:\!atomadic\ass-ade-v1.1\tests\fixtures\rebuilt-out`  
**Duration:** 63 ms

## Summary

Repo at `C:\!atomadic\ass-ade-v1.1\tests\fixtures\rebuilt-out` contains 71 files (31 source, 71 test-related) across 6 directory levels (50.2 KB total). Test coverage: 13 test functions across 2 test files (ratio 1.0). Documentation coverage: 100%. Dominant tier: `at`. CNA compatibility is clean across 10 tier file(s).

## Scout

- Files: 71 (50.2 KB)
- Source files: 31
- Max depth: 6
- Top-level: API_INVENTORY.md, BLUEPRINT.json, BLUEPRINT.plan.json, CERTIFICATE.json, DOC_COVERAGE.md, MANIFEST.json, MULTILANG_BRIDGES.md, PROVENANCE.json, TEST_COVERAGE.md, VERSION

**By extension:**
  - `.json`: 16
  - `.py`: 13
  - `.rs`: 11
  - `.swift`: 7
  - `.ts`: 7
  - `.kt`: 6
  - `.md`: 5
  - `.toml`: 2

## Dependencies

- Python files: 13
- Unique external deps: 9
- Max import depth: 0
- Circular deps: none

## Tier Distribution

- `qk`: 0
- `at`: 13 — e.g. __init__.py, a1_at_functions/a1_compile_python_compile.py
- `mo`: 0
- `og`: 0
- `sy`: 0

## CNA Compatibility

- Status: compatible
- Tier dirs found: a1_at_functions, a2_mo_composites
- Files checked: 10
- Python atom files: 5
- JSON atom files: 5
- Current ids: 5
- Legacy ids: 0
- Invalid ids: 0
- Filename issues: 0
- Id/stem mismatches: 0
- Paired file mismatches: 0
- Tier mismatches: 0

## Tests

- Test files: 2
- Test functions: 13
- Coverage ratio: 1.0
- Frameworks: pytest, generated-baseline
- Untested modules: 0

## Documentation

- README: yes
- Doc files: 5
- Public callables: 31
- Documented: 31 (100%)

**Missing docstrings (sample):**
  - `example_pkg/core.py:pure_helper`
  - `example_pkg/core.py:run`
  - `tests/test_generated_multilang_bridges.py:test_multilang_bridge_artifacts_exist`
  - `tests/test_generated_multilang_bridges.py:test_multilang_bridge_manifest_is_consistent`
  - `tests/test_generated_multilang_bridges.py:test_multilang_bridge_report_exists`
  - `tests/test_generated_multilang_bridges.py:test_typescript_bridge_compiles_when_tsc_present`
  - `tests/test_generated_multilang_bridges.py:test_typescript_bridge_smoke_when_node_present`
  - `tests/test_generated_multilang_bridges.py:test_rust_bridge_compiles_when_cargo_present`
  - `tests/test_generated_multilang_bridges.py:test_kotlin_bridge_runs_when_gradle_present`
  - `tests/test_generated_multilang_bridges.py:test_swift_bridge_builds_when_swift_present`

## Recommendations

1. Repo looks healthy. Run `ass-ade certify` to produce a signed certificate.

**Next action:** Run `ass-ade lint` for detailed style and security findings.
