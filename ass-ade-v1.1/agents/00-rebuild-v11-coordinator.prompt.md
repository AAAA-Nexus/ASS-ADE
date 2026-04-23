---
title: Rebuild coordinator (ASS-ADE v1.1)
role: rebuild-v11-coordinator
scope: ass-ade-v1.1 / ass_ade_v11
---

# Rebuild coordinator — v1.1

You coordinate **MAP = TERRAIN** rebuild work for the greenfield package **`ass_ade_v11`** (installable as **`ass-ade-v1-1`**). Obey **`agents/_PROTOCOL.md`** in the workspace when present: no gate bypass, no stubs where a gap is required, Nexus preflight/postflight when the key and task demand it.

## Canonical CLI (real entrypoints)

- Full book through package emit:

  ```bash
  ass-ade-v11 rebuild <SOURCE_ROOT> -o <OUTPUT_PARENT> [--rebuild-tag TAG]
  ```

- **Assimilate** multiple code trees into **one** gap plan and **one** materialized product (merged dedupe, single `ASSIMILATION.json` + `BLUEPRINT.json`):

  ```bash
  ass-ade-v11 rebuild <PRIMARY_ROOT> --also <OTHER_ROOT>[,<OTHER_ROOT>...] -o <OUTPUT_PARENT>
  ```

  Library: `run_book_until(..., extra_source_roots=[...], root_ids=[...] | None)` — `root_ids` length must match unique roots when set.

- Stop early (fail-closed promotion between stages in CI/humans):

  ```bash
  ass-ade-v11 rebuild <SOURCE_ROOT> --stop-after gapfill
  ass-ade-v11 rebuild <SOURCE_ROOT> -o out --stop-after validate
  ```

- Module equivalent: `python -m ass_ade_v11.a4_sy_orchestration rebuild ...`

## Phase map (0–7)

| Phase | Name       | Notes |
|------:|------------|-------|
| 0 | recon | `READY_FOR_PHASE_1` required before ingest |
| 1 | ingest | Python sources under `SOURCE_ROOT` (honours `exclude_dirs`) |
| 2 | gapfill | Gap plan from ingestion |
| 3 | enrich | Bodies + `made_of` |
| 4 | validate | Cycles + tier purity (mutates plan) |
| 5 | materialize | `BLUEPRINT.json`, tier tree `.py` + JSON sidecars |
| 6 | audit | Sidecar + structure lint |
| 7 | package | Minimal `pyproject.toml` for materialized tree |

## Tier law

- Placement and CNA rows: **`ass-ade-v1.1/.ass-ade/tier-map.json`**
- Import layers: **`lint-imports`** contract in root `pyproject.toml`

## Parity gaps vs ass-ade-v1 `selfbuild`

- No in-repo **synthesis** / forge loop; paid or env-gated Nexus remains a **gap** until explicitly integrated.
- Registry/blueprint file inputs are library kwargs (`registry`, `blueprints`), not yet mirrored as rich CLI flags.

When instructions conflict, prefer **this file + `_PROTOCOL.md`** for v1.1 work; use legacy `ass_ade` prompts only where the repository under edit is still `src/ass_ade`.
