# ASS-ADE — goal pipeline (reference for “finished” product)

This document is the **canonical checklist** for turning orphaned/sibling repos into **one shippable, CNA/monadic, Atomadic-structured** ASS-ADE. Each block lists **intent**, **what exists today** (paths / commands), **gaps**, and **how to implement** the missing pieces.

Related docs: [`docs/ATOMADIC_SWARM_SURFACE_AUDIT.md`](docs/ATOMADIC_SWARM_SURFACE_AUDIT.md) (swarm surfaces), [`ASS_ADE_SHIP_PLAN.md`](ASS_ADE_SHIP_PLAN.md) (**phased execution roadmap**), [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md), [`docs/ASS_ADE_SPINE_RFC.md`](docs/ASS_ADE_SPINE_RFC.md), [`docs/ASS_ADE_FORGE_CLI.md`](docs/ASS_ADE_FORGE_CLI.md), [`ASS_ADE_MATRIX.md`](ASS_ADE_MATRIX.md), [`ASS_ADE_INVENTORY.md`](ASS_ADE_INVENTORY.md).

---

## Legend

| Tag | Meaning |
|-----|---------|
| **HAVE** | Implemented and usable in-repo (may need polish). |
| **PARTIAL** | Exists but incomplete, wrong UX, or not wired as default. |
| **GAP** | Not implemented; needs design + code. |

### Workspace truth — Atomadic umbrella (`!atomadic`, 2026-04)

Edits below call out **this checkout** where it differs from older authoring. **Canonical code paths:** monadic package `ass_ade_v11` under `ass-ade-v1.1/src/`; **editable install + `[tool.importlinter]` + `[tool.pytest.ini_options]`** live in the **repository root** `pyproject.toml` (T12). **`ass-ade-v1.1/pyproject.toml`** is a pointer stub only (no `[project]`). CI: `.github/workflows/ass-ade-ship.yml` (golden assimilate, `lint-imports`, pytest `-m "not dogfood"`, `ass-ade-v11 synth-tests --check`). Policy/plan: `.ass-ade/specs/*.schema.json`, bundled wheel copies under `ass_ade_v11/_bundled_ade_specs/`, CLI `--policy` / `--plan-out`, fail-closed `--also` when `CI` or `ASS_ADE_ASSIMILATE_REQUIRE_POLICY=1`.

---


## Live terrain (auto-generated)

<!-- ASS_ADE_AUTOGEN:BEGIN -->
_Terrain refresh: **2026-04-22 22:51 UTC** — [`ASS_ADE_SUITE_SNAPSHOT.md`](ASS_ADE_SUITE_SNAPSHOT.md) has the full machine snapshot._

- **Repo root:** `C:/!atomadic`
- **Umbrella git (short):** `—`
- **`ass-ade*` dirs at root:** 8
- **`tier-map.json` files:** 11 (5 ephemeral / under tmp or backup paths)
- **Spine hint:** ass_ade_v11 under ass-ade-v1.1/src/ (T12 root pyproject)

**Subtrees (name → git short):**

- `ass-ade` → `1eca9b9`
- `ass-ade-v1` → `883a2dc`
- `ass-ade-v1-test` → `—`
- `ass-ade-v1-test-backup-20260421-134252` → `—`
- `ass-ade-v1-test-backup-20260421-155054` → `—`
- `ass-ade-v1-test-bridges` → `—`
- `ass-ade-v1-test-selfcheck` → `—`
- `ass-ade-v1.1` → `—`

**Other tier-mapped repo-root siblings:**
- `!atomadic-uep` → `b317051`

<!-- ASS_ADE_AUTOGEN:END -->

## Track P — Product preflight (before any ingest)

### P1 — Assimilation contract (scope, merge law, licenses)

| Item | Intent |
|------|--------|
| **P1** | Define *what* may merge automatically, *what* requires human sign-off, license compatibility (GPL vs proprietary), and the **single primary** MAP root. |

- **HAVE:** Narrative merge roles in [`docs/ASS_ADE_SPINE_RFC.md`](docs/ASS_ADE_SPINE_RFC.md) and sibling policy; multi-root **primary wins** on duplicate symbols in [`ass-ade-v1.1/src/ass_ade_v11/a3_og_features/pipeline_book.py`](ass-ade-v1.1/src/ass_ade_v11/a3_og_features/pipeline_book.py) (`run_book_until` docstring).
- **HAVE (CLI gate):** Machine-readable policy YAML validated against [`ass-ade-v1.1/.ass-ade/specs/assimilate-policy.schema.json`](ass-ade-v1.1/.ass-ade/specs/assimilate-policy.schema.json); `ass-ade-unified assimilate --policy …`; fail-closed when `--also` is used under **`CI`** or **`ASS_ADE_ASSIMILATE_REQUIRE_POLICY=1`** (see [`ass-ade-v1.1/src/ass_ade_v11/a1_at_functions/assimilate_policy_gate.py`](ass-ade-v1.1/src/ass_ade_v11/a1_at_functions/assimilate_policy_gate.py) and unified CLI tests).
- **PARTIAL:** Phase engines do not yet consume **every** policy row for automated refuse/allow beyond the CLI gate (deep semantic enforcement).
- **IMPLEMENT:** Thread validated policy into `run_phase0_recon_multi` / ingest for root-specific allowlists and asset rules; keep YAML + schema as source of truth.

### P2 — Terrain inventory (find siblings / orphans)

| Item | Intent |
|------|--------|
| **P2** | Enumerate candidate repos on disk (fingerprints: `pyproject`, `tier-map`, `ass-ade*`). |

- **HAVE:** [`scripts/regenerate_ass_ade_docs.py`](scripts/regenerate_ass_ade_docs.py) (cross-platform, repo-local) and [`scripts/inventory_ass_ade.ps1`](scripts/inventory_ass_ade.ps1) (Windows-wide) → [`ASS_ADE_INVENTORY.md`](ASS_ADE_INVENTORY.md), `ASS_ADE_INVENTORY.paths.json`, plus [`ASS_ADE_SUITE_SNAPSHOT.md`](ASS_ADE_SUITE_SNAPSHOT.md) and autogen terrain blocks in matrix / ship / goal docs (Python only).
- **PARTIAL:** Not invoked by default from CLI; [`docs/ASS_ADE_FORGE_CLI.md`](docs/ASS_ADE_FORGE_CLI.md) sketches `forge inventory`.
- **IMPLEMENT:** Port inventory to a **Python module** under `ass_ade_v11.a1_at_functions` (pure) + thin `ass-ade-unified` subcommand, or call the script via subprocess from [`ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/unified_cli.py`](ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/unified_cli.py).

### P3 — Operator / trust gates (optional but “Atomadic”)

| Item | Intent |
|------|--------|
| **P3** | Session, spend caps, drift, injection bounds, receipts for paid or sensitive runs. |

- **HAVE:** Agent protocol §11 + [`agents/NEXUS_SWARM_MCP.md`](agents/NEXUS_SWARM_MCP.md); v1 Typer apps under [`ass-ade-v1/src/ass_ade/cli.py`](ass-ade-v1/src/ass_ade/cli.py) (Nexus-related typers).
- **GAP:** No automatic **pipeline-attached** preflight for `assimilate` / `book` (swarm docs ≠ product enforcement).
- **IMPLEMENT:** Add optional `--nexus-preflight` to `assimilate` / `book rebuild` that runs a **minimal** contract (or records `SKIPPED` with reason) and writes receipt JSON next to output; keep default local/offline for open-source runs.

---

## Track B — Monadic “book” (phases 0–7) — core ingest → emit

Implementation spine: [`ass-ade-v1.1/src/ass_ade_v11/a3_og_features/pipeline_book.py`](ass-ade-v1.1/src/ass_ade_v11/a3_og_features/pipeline_book.py) (`run_book_until`, `STOP_AFTER_PHASE`). CLI: `ass-ade-v11 …`, `ass-ade-unified book …`, **`ass-ade-unified assimilate`** ([`ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/unified_cli.py`](ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/unified_cli.py)).

### Phase 0 — `recon` (multi-root terrain)

| Item | Intent |
|------|--------|
| **B0** | Every source root must look like a valid ingest target (e.g. at least one `.py` after exclusions); produce `READY_FOR_PHASE_1` or stop. |

- **HAVE:** `run_phase0_recon_multi` via [`ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase0_recon_multi.py`](ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase0_recon_multi.py); v1 parity command `ass-ade recon` in [`ass-ade-v1`](ass-ade-v1).
- **GAP:** Non-Python-heavy repos (games, mixed stacks) may fail recon; exclusions may need per-product tuning.
- **IMPLEMENT:** Extend exclusion tables in a0 constants and recon rules; add **language plugins** only after Python path is stable (new a1 classifiers, CNA ids).

### Phase 1 — `ingest` (symbols, multi-root merge)

| Item | Intent |
|------|--------|
| **B1** | Build ingestions; multi-root uses `run_phase1_ingest_multi` + `detect_namespace_conflicts`. |

- **HAVE:** [`ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase1_ingest.py`](ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase1_ingest.py), [`ass-ade-v1.1/src/ass_ade_v11/a1_at_functions/conflict_detector.py`](ass-ade-v1.1/src/ass_ade_v11/a1_at_functions/conflict_detector.py).
- **HAVE (JSON plan):** `ASSIMILATE_PLAN` object validated against [`assimilate-plan.schema.json`](ass-ade-v1.1/.ass-ade/specs/assimilate-plan.schema.json); merged into book JSON; **`--plan-out`** writes sidecar file (see [`assimilate_plan_emit.py`](ass-ade-v1.1/src/ass_ade_v11/a1_at_functions/assimilate_plan_emit.py)).
- **PARTIAL:** Optional companion **`ASSIMILATE_PLAN.md`** prose artifact for operators (if not emitted by default).
- **IMPLEMENT:** Emit markdown plan alongside JSON when product needs human-only review surfaces; keep JSON as contract for CI and tooling.

### Phase 2 — `gapfill` (plan missing / stub / tier work)

| Item | Intent |
|------|--------|
| **B2** | Turn ingestions into a gap plan (what must be created or fixed for monadic/CNA compliance). |

- **HAVE:** `run_phase2_gapfill` — [`ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase2_gapfill.py`](ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase2_gapfill.py).
- **GAP:** “Auto-write missing logic at production quality” is **not** a single switch; gapfill plans may still need LLM or human execution with gates.
- **IMPLEMENT:** Define **tiered automation**: (1) deterministic fixes only in CI, (2) optional `--enrich-with-nexus` for paid enrichment, (3) always attach diff size + risk score to plan artifact.

### Phase 3 — `enrich` (attach bodies / evidence)

| Item | Intent |
|------|--------|
| **B3** | Attach bodies / caps to gap plan for downstream validate/materialize. |

- **HAVE:** `run_phase3_enrich` — [`ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase3_enrich.py`](ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase3_enrich.py).
- **GAP:** Large monorepos may hit `max_body_chars` defaults; quality varies by source.
- **IMPLEMENT:** Tunable limits per policy file; streaming/chunked enrich for huge files (a2 composite “session” + a1 pure chunkers).

### Phase 4 — `validate` (cycles, tier purity, import law prep)

| Item | Intent |
|------|--------|
| **B4** | Enforce acyclicity (optional break), tier-purity edges, validation gates before emit. |

- **HAVE:** `run_phase4_validate` — [`ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase4_validate.py`](ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase4_validate.py); **`import-linter`** contract in **[repository root `pyproject.toml`](pyproject.toml)** (`[tool.importlinter]`, `root_package = "ass_ade_v11"`). *(Legacy pointer: `ass-ade-v1.1/pyproject.toml` defers to root — do not duplicate `[project]`.)*
- **PARTIAL:** Emitted tree may still need **post-hoc** import-linter until package layout matches `root_package` expectations.
- **IMPLEMENT:** Run `lint-imports` (or equivalent) as **phase 4.5** or part of phase 7 packaging script; fail build on contract break.

### Phase 5 — `materialize` (write tier tree)

| Item | Intent |
|------|--------|
| **B5** | Write monadic directory layout under `output_parent` / `rebuild_tag`; record `assimilation_meta` for multi-root. |

- **HAVE:** `run_phase5_materialize` — [`ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase5_materialize.py`](ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase5_materialize.py).
- **GAP:** Parity with **v1** `engine/rebuild` emit (docs bridges, coverage sidecars, etc.) may differ; two engines until unification completes.
- **IMPLEMENT:** Per [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md), port missing emitters from [`ass-ade-v1/src/ass_ade/engine/rebuild/`](ass-ade-v1/src/ass_ade/engine/rebuild/) into `ass_ade_v11` a2/a3 with CNA ids; add golden **fixture diff tests** v1 vs v11 on same input.

### Phase 6 — `audit` (structure conformant)

| Item | Intent |
|------|--------|
| **B6** | Audit materialized tree; `structure_conformant` gate. |

- **HAVE:** `run_phase6_audit`, CLI `book certify` — [`ass-ade-v1.1/src/ass_ade_v11/a1_at_functions/audit_rebuild.py`](ass-ade-v1.1/src/ass_ade_v11/a1_at_functions/audit_rebuild.py) (validate path used by CLI).
- **GAP:** None critical for MVP; extend audit rules as new tier violations are discovered.
- **IMPLEMENT:** Add audit checks for **CNA id presence** on public modules (read `.ass-ade/tier-map.json` in emitted tree).

### Phase 7 — `package` (wheel / pyproject emit)

| Item | Intent |
|------|--------|
| **B7** | Emit installable metadata (`distribution_name`, etc.). |

- **HAVE:** `run_phase7_package` — [`ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase7_package.py`](ass-ade-v1.1/src/ass_ade_v11/a3_og_features/phase7_package.py).
- **GAP:** Final **product name** may still be `ass-ade-v1-1` / `ass-ade-assimilated` until single-package rename; optional deps (x402) not merged from [`ass-ade`](ass-ade).
- **IMPLEMENT:** Template `pyproject` from policy; merge **optional extras** from v1/legacy Click package in unification phase ([`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) §Target architecture).

---

## Track R — v1 “rebuild engine” parity (legacy spine, high capability)

| Item | Intent |
|------|--------|
| **R1** | `ass-ade rebuild` for sibling sprawl → rich emitted package (docs, bridges, coverage manifests in many flows). |

- **HAVE:** [`ass-ade-v1/src/ass_ade/engine/rebuild/`](ass-ade-v1/src/ass_ade/engine/rebuild/), CLI `ass-ade rebuild` in [`ass-ade-v1/src/ass_ade/cli.py`](ass-ade-v1/src/ass_ade/cli.py).
- **GAP:** Not the same code path as v1.1 **book**; operators must choose until merge ([`ASS_ADE_MATRIX.md`](ASS_ADE_MATRIX.md)).
- **IMPLEMENT:** Either (a) call v1 rebuild as a **phase** behind a feature flag, or (b) port emitters into v1.1 materialize (preferred for single product).

---

## Track S — Post-emit “ship” (prove + document + distribute)

### S1 — Tests on emitted tree

| Item | Intent |
|------|--------|
| **S1** | `pytest` (and synth import smoke) on assimilated output. |

- **HAVE:** `ass-ade-unified book synth-tests`, `--check` mode — [`ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/cli.py`](ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/cli.py); generated smoke tests under `ass-ade-v1.1/tests/`. Same command is available as `ass-ade-v11 synth-tests` (standalone) or nested under `ass-ade-unified book …`.
- **HAVE (CI slice):** [`.github/workflows/ass-ade-ship.yml`](.github/workflows/ass-ade-ship.yml) runs pytest on `ass-ade-v1.1/tests` (excluding `dogfood`), `synth-tests --check`, and a **single-root** golden assimilate fixture (see [`ASS_ADE_SHIP_PLAN.md`](ASS_ADE_SHIP_PLAN.md) workspace notes).
- **GAP:** No single **`assimilate && test`** wrapper; CI does not yet run a **checked-in multi-root** golden trio (policy + `--also` is covered in pytest / `pytest -m usecase`, not the default CI assimilate step).
- **IMPLEMENT:** Add `ass-ade-unified assimilate … --then pytest` (subprocess) or `tox`-like mini harness; optional second CI job with synthetic multi-root fixture + `--policy`.

### S2 — Documentation and API inventory

| Item | Intent |
|------|--------|
| **S2** | Auto docs / API inventory for shippable artifact. |

- **HAVE:** v1 rebuild doc generation paths (referenced from rebuild flows and pytest temp outputs under `ass-ade-v1/.pytest_tmp` / [`rebuild-outputs`](rebuild-outputs)).
- **GAP:** Not unified as **phase 8** of book; quality varies by emitter used (R vs B track).
- **IMPLEMENT:** Add optional `phase8_docs` or post-step in assimilate that invokes shared **a3** doc emitter with CNA-tagged sections.

### S3 — Single installable + CLI collapse

| Item | Intent |
|------|--------|
| **S3** | One `pip install ass-ade`, one `atomadic` / `ass-ade` entry, `import ass_ade` only. |

- **HAVE:** [`ass-ade-unified`](ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/unified_cli.py) unifies **UX** for book + assimilate + optional v1 `studio`.
- **PARTIAL:** **Spine distribution** is merged to **one** `[project]` at **[repository root `pyproject.toml`](pyproject.toml)** (T12) with sources under `ass-ade-v1.1/src/`; **sibling** distributions remain for [`ass-ade-v1`](ass-ade-v1), [`ass-ade`](ass-ade), and harness trees ([`ASS_ADE_MATRIX.md`](ASS_ADE_MATRIX.md)).
- **GAP:** Physical **single import namespace** (`ass_ade_v11` → `ass_ade`) and retiring duplicate sibling `pyproject.toml` **products** per [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) target architecture.
- **IMPLEMENT:** Execute unification phases 1–5 there; bump major version; migration guide for imports `ass_ade_v11` → `ass_ade`.

---

## One-command operator map (today vs target)

| Goal | Today | Target |
|------|--------|--------|
| Multi-root → monadic emit | `ass-ade-unified assimilate PRIMARY OUT [--also …]` | Same, but policy + plan artifacts + CI green without manual flags |
| Full v1 IDE/Nexus surface | `ass-ade-unified studio …` (needs `pip install -e ass-ade-v1`) | Flattened under top-level CLI (no `studio` group) |
| Disk inventory | `scripts/inventory_ass_ade.ps1` | `ass-ade-unified inventory` (or `forge inventory`) |
| Merge plan / apply | **GAP** | `forge plan` / `forge apply` per [`docs/ASS_ADE_FORGE_CLI.md`](docs/ASS_ADE_FORGE_CLI.md) |

---

## Suggested execution order (for contributors)

1. Run **P2** inventory; pick **P1** primary + policy stub.
2. Run **`ass-ade-unified assimilate`** with `--stop-after gapfill`, review plan; iterate exclusions.
3. Run **full book** to `package` (B0–B7); run **S1** tests on output.
4. For parity with legacy emitters, execute **R1** compare or port (**IMPLEMENT** under B5/R1).
5. When stable, execute **S3** unification doc phases (single tree).

---

## CNA / monadic discipline (cross-cutting)

- **HAVE:** [`ass-ade-v1.1/.ass-ade/tier-map.json`](ass-ade-v1.1/.ass-ade/tier-map.json), import-linter config, builder prompts under [`agents/`](agents), [`agents/ASS_ADE_MONADIC_CODING.md`](agents/ASS_ADE_MONADIC_CODING.md).
- **GAP:** v1 `ass_ade` tree still mixes legacy `engine/` layout ([`ass-ade-v1/.ass-ade/tier-map.json`](ass-ade-v1/.ass-ade/tier-map.json)) — migration shims must stay explicit in tier-map.
- **IMPLEMENT:** Any new automation lives in **`ass_ade_v11.a0…a4`** (or post-rename `ass_ade`) only; no silent new logic in `engine/` without tier-map migration row.

---

*Last aligned to repo layout, root `pyproject.toml` (T12), `ass-ade-ship` CI, policy/plan CLI gates, and `pipeline_book` phases (2026-04). Update when phases or CLIs change.*
