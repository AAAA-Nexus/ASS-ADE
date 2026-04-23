# ASS-ADE feature inventory (single trunk `C:\!aaaa-nexus\!ass-ade`)

**Purpose:** MAP = TERRAIN for *where capabilities live* before and during **multi-root assimilate**. This is deeper than [`ASS_ADE_MATRIX.md`](../ASS_ADE_MATRIX.md) (dist/CLI matrix): here we map **features** to **paths** and **entrypoints** so operators can wire one working tree without guessing.

**Refresh:** bump the date when you change sibling layout or add a major surface. The current source-of-truth roles are also summarized in [`ONE_WORKING_PRODUCT.md`](ONE_WORKING_PRODUCT.md).

---

## 1. Operator CLI (united spine)

| Feature | Location | How to run |
|--------|----------|------------|
| **`ass-ade`** Typer root | [`ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/unified_cli.py`](../ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/unified_cli.py) | `ass-ade doctor` |
| **Atomadic engine shell** | [`atomadic-engine/src/ass_ade/cli.py`](../atomadic-engine/src/ass_ade/cli.py) | `ass-ade rebuild --help`, `atomadic --help` |
| **`book`** (phases 0–7) | [`cli.py`](../ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/cli.py) | `ass-ade book rebuild ...` |
| **One-shot `assimilate`** | `unified_cli.py` (`assimilate` command) | `ass-ade assimilate PRIMARY OUT [--also ...] [--policy ...]` |
| **`ade`** (materialize, doctor) | [`ass_ade_v11/ade/cli.py`](../ass-ade-v1.1/src/ass_ade_v11/ade/cli.py) | `ass-ade ade materialize` |
| **`synth-tests`** manifest | [`cli.py`](../ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/cli.py) | `ass-ade book synth-tests --check --repo ass-ade-v1.1` |
| **Install / scripts** | Root [`pyproject.toml`](../pyproject.toml) `[project.scripts]` | `pip install -e ".[dev]"` from umbrella root |

---

## 2. Monadic pipeline (book engine)

| Phase | Role | Primary implementation |
|------|------|-------------------------|
| 0 | Multi-root recon | [`phase0_recon_multi.py`](../ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase0_recon_multi.py) |
| 1 | Ingest | [`phase1_ingest.py`](../ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase1_ingest.py), `run_phase1_ingest_multi` |
| 2 | Gapfill | [`phase2_gapfill.py`](../ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase2_gapfill.py) |
| 3–7 | Enrich → package | [`pipeline_book.py`](../ass-ade-v1.1/src/ass_ade_v11/a3_og_features/pipeline_book.py) |
| **Orchestrator** | `run_book_until` | `pipeline_book.py` |

**Law:** [`tier-map.json`](../ass-ade-v1.1/.ass-ade/tier-map.json) + root [`pyproject.toml`](../pyproject.toml) `[tool.importlinter]`.

---

## 3. Multi-root policy & plan (S2 / Phase 2)

| Feature | Location |
|--------|----------|
| Policy YAML schema | [`ass-ade-v1.1/.ass-ade/specs/assimilate-policy.schema.json`](../ass-ade-v1.1/.ass-ade/specs/assimilate-policy.schema.json) |
| Plan JSON schema | [`assimilate-plan.schema.json`](../ass-ade-v1.1/.ass-ade/specs/assimilate-plan.schema.json) |
| Policy parse / gate | [`assimilate_policy_gate.py`](../ass-ade-v1.1/src/ass_ade_v11/a1_at_functions/assimilate_policy_gate.py) |
| Plan emit | [`assimilate_plan_emit.py`](../ass-ade-v1.1/src/ass_ade_v11/a1_at_functions/assimilate_plan_emit.py) |
| CI fixture policy | [`tests/fixtures/multi_root_policy.yaml`](../ass-ade-v1.1/tests/fixtures/multi_root_policy.yaml) |
| **Umbrella PoC policy** | [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/policies/umbrella_ass_ade_roots.yaml`](../.ato-plans/active/ass-ade-ship-nexus-github-20260422/policies/umbrella_ass_ade_roots.yaml) |

---

## 4. Runtime trees in the single trunk

| Path | Package / role | Rebuild engine | Monadic pipeline | Notes |
|------|----------------|----------------|------------------|-------|
| **`ass-ade-v1.1/`** | `ass_ade_v11` - **MAP / spine** | a1-tier helpers, not v1 `engine/rebuild` | **Yes** `pipeline_book` | Design authority for assimilate primary root |
| **`atomadic-engine/`** | `ass_ade` - restored Atomadic engine | **Yes** `engine/rebuild` | No | Runtime compatibility surface and broad CLI |
| **`ADE/`** | harness | No | No | Strict prompt/hook harness used by ship checks |
| **`agents/`** | prompt chain | No | No | Pipeline prompts and swarm protocol |

## 4b. External folders in `C:\!aaaa-nexus`

| Path | Role | Merge posture |
|------|------|---------------|
| `ass-ade-fix/` | clean donor | Already copied into `atomadic-engine`; use only for diff/reference. |
| `QUARANTINE_IP_LEAK_v20/` | quarantine donor | Compare only; no direct copy until IP/scrub review. |
| `ass-ade-final-release*`, `assimilated_ade/` | generated outputs | Evidence only until imports/tests pass. |
| `ASS-CLAW*`, `ass-claw-repos/` | separate product inputs | Do not merge into ASS-ADE core automatically. |
| `!ass-ade-control/`, `!ass-ade-cursor-dev-*` | audit/staging records | Useful history; not runtime source. |

---

## 5. IDE / materializer / hooks

| Feature | Location |
|--------|----------|
| **Materialize** | [`materialize.py`](../ass-ade-v1.1/src/ass_ade_v11/ade/materialize.py) |
| **Discover monorepo** | [`discover.py`](../ass-ade-v1.1/src/ass_ade_v11/ade/discover.py) |
| Bundled Cursor hook templates | `ass_ade_v11/ade/cursor_hooks_bundled/` (package data; **not** import-graph modules) |
| Cross-IDE samples | `ass_ade_v11/ade/cross_ide_bundled/` |
| Cursor hooks (dev) | [`hooks/`](../hooks) and ADE materialized copies |
| **ADE harness (CI)** | [`ADE/harness/`](../ADE/harness) |

---

## 6. Swarm & governance (agents)

| Feature | Location |
|--------|----------|
| Pipeline prompts `00–24` | [`agents/*.prompt.md`](../agents) |
| Protocol | [`agents/_PROTOCOL.md`](../agents/_PROTOCOL.md), [`agents/INDEX.md`](../agents/INDEX.md) |
| Ship plan (phased) | [`ASS_ADE_SHIP_PLAN.md`](../ASS_ADE_SHIP_PLAN.md) |
| Active Cursor plan | [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/`](../.ato-plans/active/ass-ade-ship-nexus-github-20260422) |
| Task DAG | [`tasks.json`](../.ato-plans/active/ass-ade-ship-nexus-github-20260422/tasks.json) |
| Swarm services (private) | [`scripts/run_swarm_services.py`](../scripts/run_swarm_services.py) |

---

## 7. CI / quality

| Feature | Location |
|--------|----------|
| Ship workflow | [`.github/workflows/ass-ade-ship.yml`](../.github/workflows/ass-ade-ship.yml) |
| Import law | `lint-imports` + `pyproject.toml` |
| Golden assimilate | workflow: `minimal_pkg` + optional multi-root job |

---

## 8. Trunk self-assimilate (PoC) — intent

**Goal:** Prove ASS-ADE on its own current trunk: primary = **`ass-ade-v1.1`**, sibling = **`atomadic-engine`**, with a checked policy and artifacts under **`_unified_assimilate_poc/`** (gitignored).

**Commands and escalation** (recon → ingest → gapfill → …) live in [`swarm-execution.md`](../.ato-plans/active/ass-ade-ship-nexus-github-20260422/swarm-execution.md) § *Umbrella self-assimilate (PoC)*.

**Honesty:** generated final-release folders are not accepted as product source until they import and pass smoke tests. They remain evidence for parity and regression fixtures.

---

*Inventory version: 2026-04-23 — single-trunk consolidation pass.*
