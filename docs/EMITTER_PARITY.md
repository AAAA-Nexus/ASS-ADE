# Emitter parity (v1 `ass_ade.engine.rebuild` → v1.1 `ass_ade_v11`)

Tracks which v1 `engine/rebuild/` emitters have been ported to v1.1 monadic
tiers (a0/a1/a3), with byte-for-byte parity where practical (golden diffable).

## Tiering convention for ports

- Pure deterministic renderers → `a1_at_functions/*_emit.py`
- Stateful / path-writing wrappers → `a3_og_features/emit_*.py`
- Constants / schema IDs → `a0_qk_constants`

Default stance: **port the pure renderer first**, then the thin writer, then
the pipeline hookup. Goldens are snapshot tests under `ass-ade-v1.1/tests`.

## Status table

| v1 module                                          | v1.1 port                                                                                           | Status   | Notes                                                                        |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------- |
| `engine/rebuild/coverage_emitter._build_api_inventory` | `a1_at_functions/api_inventory_emit.build_api_inventory_markdown` + `a3_og_features/emit_api_inventory.emit_api_inventory` | **Ported (v1.1a1 Slice D)** | Pure renderer + thin writer; covered by `tests/test_emitter_parity_api_inventory.py`. |
| `engine/rebuild/coverage_emitter` (remainder)      | —                                                                                                   | Planned  | Test coverage manifest + generated integrity tests; depends on `coverage_manifest` port. |
| `engine/rebuild/coverage_manifest`                 | —                                                                                                   | Planned  | `.ass-ade/coverage/{test,docs}_coverage.json` paths + loaders.               |
| `engine/rebuild/bridge_emitter`                    | —                                                                                                   | Planned  | Cross-tier bridge manifests.                                                 |
| `engine/rebuild/bridge_manifest`                   | —                                                                                                   | Planned  | Bridge schema IDs + loaders.                                                 |
| `engine/rebuild/version_tracker`                   | —                                                                                                   | Planned  | `VERSION.json` emitter (may be redundant with v11 pipeline book).            |
| `engine/rebuild/tier_purity`                       | `a1_at_functions/*purity*` (existing coverage in phase4_validate) | **Covered (equivalent)** | v1.1 enforces purity in phase 4 via `run_phase4_validate(enforce_purity=True)`. |
| `engine/rebuild/cycle_detector`                    | `a1_at_functions/conflict_detector` (related) / phase4                                              | Partial  | Cycle break covered by `break_cycles_if_found` in phase 4.                   |
| `engine/rebuild/synthesis`                         | `a3_og_features/phase2_gapfill`                                                                     | Covered  | Gap-fill + synthesis already native in v1.1 pipeline.                        |
| `engine/rebuild/forge` / `orchestrator` / `finish` | `a3_og_features/pipeline_book` (`run_book_until`)                                                   | Covered  | End-to-end pipeline driver superseded by `pipeline_book`.                    |
| `engine/rebuild/package_emitter`                   | `a3_og_features/phase5_materialize` + `phase7_package`                                              | Covered  | Materialize + package stages land emitted trees.                             |
| `engine/rebuild/import_rewriter`                   | `a3_og_features/phase5_materialize` (via `rewrite_imports=True`) and CNA machinery | Covered  | Import rewriting honored by phase 5 + tested in `test_cna_import_rewrite`.   |
| `engine/rebuild/schema_materializer`               | `a0_qk_constants/schemas` + `a1_at_functions/assimilate_plan_emit`                                  | Covered  | Schema emission lives in a0 / a1 emitters.                                   |
| `engine/rebuild/body_extractor`                    | `a1_at_functions/body_extractor`                                                                    | Covered  | Already ported.                                                              |
| `engine/rebuild/tiers`                             | `a0_qk_constants/tier_names`                                                                        | Covered  | Tier constants live in a0.                                                   |
| `engine/rebuild/project_parser` / `nexus_parse`    | `a1_at_functions/ingest` + `a3_og_features/phase1_ingest`                                           | Covered  | Project ingest is the v1.1 entry path.                                       |
| `engine/rebuild/autopoiesis_*`                     | —                                                                                                   | Not planned | v20 IP-leak territory; intentionally left out of public v1.1 surface.    |
| `engine/rebuild/gap_filler`                        | `a3_og_features/phase2_gapfill`                                                                     | Covered  | Gap filler is the gapfill phase.                                             |
| `engine/rebuild/feature` / `epiphany_cycle`        | —                                                                                                   | Not planned | Internal orchestration constructs not part of the v1.1 shipping surface. |

## Golden diff policy

- Renderers marked **Ported** must produce byte-identical Markdown against the
  v1 implementation when fed equivalent inputs (same resolved symbols).
- The v1.1 test suite does not import `ass_ade` (v1) — parity is asserted via
  snapshot text anchored to the v1 format, re-derivable by re-reading
  `ass_ade/engine/rebuild/coverage_emitter.py` at the commit noted inline.
- When v1 deprecates or alters a renderer, update both the v1.1 port and the
  anchored snapshot in a single atomic slice.

## How to port the next one

1. Copy the pure rendering helper into `a1_at_functions/<name>_emit.py`
   verbatim, preserving whitespace and output order (sorted keys / files).
2. If it reads the filesystem, split into `collect_*` (pure, reads only) and
   `build_*_markdown` (pure, no I/O).
3. Create `a3_og_features/emit_<name>.py` as the thin writer (boundary
   check + `write_text`).
4. Add snapshot + symbol-equivalence tests; mark `usecase` so CI runs them in
   the fast operator slice.
5. Flip the row above from "Planned" to "Ported (v1.1a1 Slice <N>)".
