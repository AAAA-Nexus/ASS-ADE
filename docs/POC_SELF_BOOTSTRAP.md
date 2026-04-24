# PoC: ASS-ADE Self-Bootstrap

Status as of 2026-04-23: first structural self-assimilation completed, with one clear remaining blocker before the emitted tree can replace trunk product source wholesale.

## Goal

Take the current ASS-ADE trunk, run `assimilate` against its own real roots, and emit a clean monadic package under `src/ass_ade/` instead of the older flat tier layout.

## What changed

1. Added a checked policy at `.ass-ade/policies/self-assimilate.yaml` for the roots that actually exist in this checkout:
   - primary: `ass-ade-v1.1`
   - sibling: `atomadic-engine`
2. Hardened source walking so recon/ingest/conflict scans ignore:
   - `*.egg-info`
   - `*-backup-*`
   - `ass-ade-v1-test*`
   - `.pytest_basetemp`
   - `rebuild-outputs`
3. Fixed policy glob handling so patterns like `**/tests/**` also match a root-level `tests/` directory.
4. Extended CNA import rewrite to:
   - search `src/` roots
   - optionally prefix emitted imports with a package root like `ass_ade`
   - preserve original module imports needed by extracted symbol bodies
5. Extended materialize/package so phase 5/7 can emit:
   - `src/ass_ade/<tier>/...`
   - root `src/ass_ade/__init__.py`
   - generated smoke-test manifest under `tests/generated_smoke/`
   - emitted `pyproject.toml` with `package-dir = {"" = "src"}` and import-linter root `ass_ade`
6. Taught the emitted `pyproject.toml` to inherit dependencies from the source project, including dev extras needed by currently imported runtime surfaces such as `jsonschema`.

## Command used

From `C:\!aaaa-nexus\!ass-ade`:

```powershell
ass-ade assimilate ass-ade-v1.1 .. `
  --also atomadic-engine `
  --policy .ass-ade\policies\self-assimilate.yaml `
  --output-package-name ass_ade `
  --distribution-name ass-ade `
  --rebuild-tag ade-self-1 `
  --plan-out ..\ade-self-1-plan.json `
  --json-out ..\ade-self-1-book.json
```

## What succeeded

- The real trunk self-assimilation completed through phase 7.
- Output landed at `C:\!aaaa-nexus\ade-self-1`.
- Audit was clean:
  - `structure_conformant = true`
  - `findings_total = 0`
- The emitted package list is:
  - `ass_ade`
  - `ass_ade.a0_qk_constants`
  - `ass_ade.a1_at_functions`
  - `ass_ade.a2_mo_composites`
  - `ass_ade.a3_og_features`
  - `ass_ade.a4_sy_orchestration`
- The run produced:
  - `ASSIMILATION.json`
  - `BLUEPRINT.json`
  - `pyproject.toml`
  - generated smoke manifest and smoke test

## Current blocker

The emitted tree is now structurally correct, but it is not yet fully self-hosting as an importable product package.

The next blocker is not packaging anymore. It is the symbol model:

- Phase 1/3 still primarily assimilates function/class bodies, not full source modules.
- Some emitted components preserve imports that refer to module-level constants or assignment-driven surfaces from the original source package.
- Example observed during emitted-tree import checks:
  - emitted module imports `ass_ade_v11.a0_qk_constants.schemas.COMPONENT_SCHEMA_V11`
  - but the emitted tree does not contain a module-level `schemas` surface compatible with that import
  - because those constants/module surfaces are not yet assimilated as first-class emitted components

That means the PoC has crossed the “clean package layout” barrier, but not yet the “product built itself and imports cleanly end-to-end” barrier.

## Verification results

Local targeted tests added for this PoC passed:

- `test_a0_surface.py`
- `test_cna_import_rewrite.py`
- `test_policy_engine_deep.py`
- `test_self_bootstrap_layout.py`

Real trunk run summary from `ade-self-1-book.json`:

- phase 1 sources: `2`
- phase 1 symbols: `2097`
- phase 2 proposed components: `1172`
- phase 6 structure conformant: `true`

Emitted-tree editable install succeeded, but import smoke still fails on unresolved legacy/module-surface expectations after dependency hydration.

## Next steps

1. Teach ingest/enrich to assimilate top-level assignment and constant surfaces, not only function/class bodies.
2. Add a module-surface strategy for preserved imports that currently reference original package modules such as `ass_ade_v11.*`.
3. Re-run the same self-assimilate command and require:
   - `import ass_ade`
   - generated smoke imports
   - emitted-tree pytest green
4. Only after that should `ade-self-1` be considered a candidate to replace trunk product source.
