# RECON_REPORT

**Path:** `C:\!aaaa-nexus\ade-self-1`  
**Duration:** 13656 ms

## Summary

Repo at `C:\!aaaa-nexus\ade-self-1` contains 2000 files (999 source, 24 test-related) across 3 directory levels (4136.9 KB total). Test coverage: 0 test functions across 1 test files (ratio 0.0). Documentation coverage: 59%. Dominant tier: `at`.

## Scout

- Files: 2000 (4136.9 KB)
- Source files: 999
- Max depth: 3
- Top-level: ASSIMILATION.json, BLUEPRINT.json, README.md, pyproject.toml, src, tests

**By extension:**
  - `.json`: 999
  - `.py`: 999
  - `.toml`: 1
  - `.md`: 1

## Dependencies

- Python files: 999
- Unique external deps: 62
- Max import depth: 0
- Circular deps: none

## Tier Distribution

- `qk`: 3 — e.g. src/ass_ade/__init__.py, src/ass_ade/a0_qk_constants/__init__.py
- `at`: 935 — e.g. src/ass_ade/a0_qk_constants/a0_source_ass_ade_v1_1_default_assimilate_plan_schema_path.py, src/ass_ade/a0_qk_constants/a0_source_ass_ade_v1_1_default_assimilate_policy_schema_path.py
- `mo`: 36 — e.g. src/ass_ade/a0_qk_constants/a0_source_atomadic_engine_proofbridge.py, src/ass_ade/a1_at_functions/a1_source_atomadic_engine_alphaverus.py
- `og`: 0
- `sy`: 25 — e.g. src/ass_ade/a1_at_functions/a1_source_ass_ade_v1_1_atomadic_main.py, src/ass_ade/a1_at_functions/a1_source_atomadic_engine_agentloop.py

**Violations:**
  - src/ass_ade/a1_at_functions/a1_source_atomadic_engine_atomadic.py (at, 43KB — may span tiers)
  - src/ass_ade/a1_at_functions/a1_source_atomadic_engine_rebuild_codebase.py (at, 31KB — may span tiers)

## Tests

- Test files: 1
- Test functions: 0
- Coverage ratio: 0.0
- Frameworks: none detected
- Untested modules: 995

**Untested (sample):**
  - `src/ass_ade/a0_qk_constants/a0_source_ass_ade_v1_1_default_assimilate_plan_schema_path.py`
  - `src/ass_ade/a0_qk_constants/a0_source_ass_ade_v1_1_default_assimilate_policy_schema_path.py`
  - `src/ass_ade/a0_qk_constants/a0_source_ass_ade_v1_1_fold_registry_token.py`
  - `src/ass_ade/a0_qk_constants/a0_source_ass_ade_v1_1_is_excluded_dir_name.py`
  - `src/ass_ade/a0_qk_constants/a0_source_ass_ade_v1_1_load_manifest_qualnames.py`
  - `src/ass_ade/a0_qk_constants/a0_source_ass_ade_v1_1_manifest_drift.py`
  - `src/ass_ade/a0_qk_constants/a0_source_ass_ade_v1_1_plan_manifest_payload.py`
  - `src/ass_ade/a0_qk_constants/a0_source_ass_ade_v1_1_plan_manifest_payload_for_package.py`

## Documentation

- README: yes
- Doc files: 1
- Public callables: 1429
- Documented: 838 (59%)

**Missing docstrings (sample):**
  - `src/ass_ade/a0_qk_constants/a0_source_ass_ade_v1_1_load_manifest_qualnames.py:load_manifest_qualnames`
  - `src/ass_ade/a0_qk_constants/a0_source_ass_ade_v1_1_plan_manifest_payload_for_package.py:plan_manifest_payload_for_package`
  - `src/ass_ade/a0_qk_constants/a0_source_atomadic_engine_for_model.py:for_model`
  - `src/ass_ade/a0_qk_constants/a0_source_atomadic_engine_lean4spec.py:Lean4Spec`
  - `src/ass_ade/a0_qk_constants/a0_source_atomadic_engine_mcpmanifest.py:MCPManifest`
  - `src/ass_ade/a0_qk_constants/a0_source_atomadic_engine_nexus_mcp_manifest.py:nexus_mcp_manifest`
  - `src/ass_ade/a0_qk_constants/a0_source_atomadic_engine_proofbridge.py:ProofBridge`
  - `src/ass_ade/a0_qk_constants/a0_source_atomadic_engine_proofbridge.py:translate`
  - `src/ass_ade/a0_qk_constants/a0_source_atomadic_engine_proofbridge.py:run`
  - `src/ass_ade/a0_qk_constants/a0_source_atomadic_engine_proofbridge.py:report`

## Recommendations

1. Test coverage is low (0.0). Add tests for the 995 untested modules.
2. 2 file(s) may span tier boundaries. Split into smaller, single-purpose modules.

**Next action:** Run `ass-ade lint` for detailed style and security findings.
