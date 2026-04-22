# ASS-ADE — phased ship plan (spaghetti → shippable)

This is the **execution roadmap**: ordered work you can assign, schedule, and verify. It turns the technical truth in [`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) into **week-sized phases** with **exit criteria**. The “cure” for spaghetti is **repeatable law** (CNA + monadic tiers + CI + one CLI), not a one-off rewrite.

**Companion docs:** [`docs/ATOMADIC_SWARM_SURFACE_AUDIT.md`](docs/ATOMADIC_SWARM_SURFACE_AUDIT.md) (Cursor / hooks / agents alignment), [`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) (HAVE/GAP per track), [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md), [`docs/ASS_ADE_SPINE_RFC.md`](docs/ASS_ADE_SPINE_RFC.md), [`ASS_ADE_MATRIX.md`](ASS_ADE_MATRIX.md).

---

## How to use this plan

1. **Do phases in order** unless explicitly marked “parallel.” Skipping phases creates fake progress (green demos, red production).
2. For each phase, tick **exit criteria** before starting the next. If an exit criterion fails, **stop** and file a gap in [`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) under the right track.
3. **Default spine for new work:** monadic package [`ass-ade-v1.1`](ass-ade-v1.1) (`ass_ade_v11`); operator entry [`ass-ade-unified`](ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/unified_cli.py). v1 is **input engine + studio** until merged.

---

## Success definition (what “shippable” means)

| # | Criterion | Verifiable by |
|---|-----------|----------------|
| S1 | One documented **golden assimilate** (multi-root → monadic tree → tests pass) | CI job + README section |
| S2 | **Assimilation policy** exists as data (not prose only) and is enforced on multi-root runs | Failing CI when policy missing or violated |
| S3 | **No accidental edit** of ephemeral dirs (`pytest_tmp`, stale backups) | `.gitignore` / CONTRIBUTING + optional pre-commit |
| S4 | **Import law** holds on emitted + spine packages | `import-linter` (or equivalent) in CI |
| S5 | **Single install story** documented for your first external user | Fresh venv + copy-paste from README works |
| S6 | **Roadmap to one `pyproject`** is either done or time-boxed with next milestone | [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) updated |

“Cures future spaghetti” means **the same pipeline runs on the next messy repo** without inventing new steps—only tuning policy and fixtures.

### Atomadic workspace — evidence vs this table (2026-04)

Use this as a **MAP = TERRAIN** snapshot for the `!atomadic` umbrella; it does **not** replace ticking exit criteria when your fork differs.

| Criterion | In this workspace |
|-----------|---------------------|
| **S1** | **HAVE:** `.github/workflows/ass-ade-ship.yml` golden assimilate on `ass-ade-v1.1/tests/fixtures/minimal_pkg` (single-root); root `README.md` documents install + assimilate. **PARTIAL:** CI does not yet run a **public multi-root** trio with `--also` (covered in pytest / `-m usecase`, not the default CI assimilate step). |
| **S2** | **HAVE (CLI + schema):** `--policy` YAML + JSON Schema; fail-closed `--also` under `CI` / `ASS_ADE_ASSIMILATE_REQUIRE_POLICY`; `--plan-out` + book `ASSIMILATE_PLAN`. **PARTIAL:** Phase engines do not yet enforce every policy row beyond the CLI gate. |
| **S3** | **HAVE:** `CONTRIBUTING.md` hygiene; `.gitignore` patterns on subtrees. |
| **S4** | **HAVE:** `lint-imports` in `ass-ade-ship` workflow; contract in root `pyproject.toml`. |
| **S5** | **HAVE:** Root `README.md` + [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) copy-paste venv path. |
| **S6** | **HAVE (spine):** One **`[project]`** for `ass-ade-v1-1` at **repo root** `pyproject.toml` (T12); `ass-ade-v1.1/pyproject.toml` is pointer-only. **GAP (target doc):** Legacy sibling distributions (`ass-ade`, `ass-ade-v1`) still carry their own `pyproject.toml` until full product merge. |

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
