# ASS-ADE comparison matrix

**Direction:** one shippable ASS-ADE under CNA/monadic law — interim united CLI **`ass-ade-unified`**. See [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md).

Auto-derived from `pyproject.toml`, package layout, and inventory ([`ASS_ADE_INVENTORY.md`](ASS_ADE_INVENTORY.md)). Git heads are per-folder `.git` when present (this umbrella folder is not always a single git root).

**Git column last refreshed:** 2026-04-22 — `git rev-parse --short HEAD` in each subtree that has a `.git` directory (re-run when cutting a release).

| Path                                                     | Dist name         | Version            | Python pkg                    | CLI entrypoints                                         | tier-map                          | Rebuild engine (`engine/rebuild`)                                    | v1.1 pipeline (`pipeline_book`)    | Tests (`pytest`)         | Git (short)                                   |
| -------------------------------------------------------- | ----------------- | ------------------ | ----------------------------- | ------------------------------------------------------- | --------------------------------- | -------------------------------------------------------------------- | ---------------------------------- | ------------------------ | --------------------------------------------- |
| `[ass-ade](ass-ade)`                                     | `ass-ade`         | 1.0.0              | `ass_ade` (setuptools)        | `atomadic`, `ass-ade` → `ass_ade.cli.__main__:main`     | No (uses `.ass-ade/` for genesis) | Partial / CLI reclaim paths                                          | No                                 | `tests/`                 | `1eca9b9`                                     |
| `[ass-ade-v1](ass-ade-v1)`                               | `ass-ade`         | 0.9.0              | `ass_ade`                     | `controller`, `ass-ade`, `atomadic` → `ass_ade.cli:app` | Yes                               | **Yes** — primary `src/ass_ade/engine/rebuild/`*                     | No                                 | Typer app + pytest       | `883a2dc`                                     |
| [`ass-ade-v1.1`](ass-ade-v1.1)                           | `ass-ade-v1-1`    | 1.1.0a1            | `ass_ade_v11`                 | `ass-ade-v11`, **`ass-ade-unified`**                    | Yes                               | Tier-mapped a1 rebuild helpers; not same tree as v1 `engine/rebuild` | **Yes** `pipeline_book` phases 0–7 | `tests/` + import-linter | (no `.git` here; may track with sibling repo) |
| `[ass-ade-v1-test](ass-ade-v1-test)`                     | `ass_ade_rebuild` | 0.1.0.dev0         | emitted `ass_ade` + tier pkgs | same as v1 Typer                                        | Yes                               | Copy/slice of v1 rebuild                                             | No                                 | `tests/`                 | —                                             |
| `[ass-ade-v1-test-bridges](ass-ade-v1-test-bridges)`     | `ass_ade_rebuild` | 0.1.0.dev0         | emitted `a0`+`a1` only        | `controller` / `ass-ade` / `atomadic`                   | No                                | partial emit                                                         | No                                 | `tests/`                 | —                                             |
| `[ass-ade-v1-test-selfcheck](ass-ade-v1-test-selfcheck)` | `ass_ade_rebuild` | 0.1.0.dev0         | emitted `a0`+`a1` only        | same                                                    | No                                | partial emit                                                         | No                                 | `tests/`                 | —                                             |
| `ass-ade-v1-test-backup-`*                               | `ass_ade_rebuild` | dev                | emitted layout                | Typer                                                   | Yes                               | sandbox                                                              | No                                 | yes                      | —                                             |
| `[!atomadic-uep](!atomadic-uep)`                         | `atomadic-uep`    | 0.12.0-integration | tier dirs `a0`…`a4`           | `atomadic-uep`                                          | Yes                               | Imports `**ass-ade`** dep; composition layer                         | No                                 | `tests/`                 | `b317051`                                     |
| `C:\Users\...\ass-ade-nexus-enforcer`                    | —                 | —                  | prompts only                  | —                                                       | —                                 | —                                                                    | —                                  | —                        | —                                             |
| `C:\Users\...\.cursor\skills\ass-ade-autopoiesis`        | —                 | —                  | skill doc                     | —                                                       | —                                 | —                                                                    | —                                  | —                        | —                                             |



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

## Interpretation

- **T12 (Atomadic umbrella):** **`[project]` for `ass-ade-v1-1`** and **`import-linter` / pytest config** live in the **[repo-root `pyproject.toml`](pyproject.toml)**; run **`pip install -e ".[dev]"`** from the monorepo root. Sources stay under **`ass-ade-v1.1/src/`**; **`ass-ade-v1.1/pyproject.toml`** is a **pointer stub** only. CI: `.github/workflows/ass-ade-ship.yml`.
- **Rebuild / “assimilate sprawl → monadic package”** gravity is on `**ass-ade-v1`** (`ass-ade rebuild`, `engine/rebuild`, `.pytest_tmp` proof runs).
- **Monadic law + phased book** gravity is on **[`ass-ade-v1.1`](ass-ade-v1.1)** (`ass_ade_v11`, `ass-ade-v11` / **`ass-ade-unified book`**).
- **Published-style 1.0.0 line** lives in `**[ass-ade](ass-ade)`** with Click and different CLI entry — reconcile before calling it *the* installable.
- `**ass-ade-v1-test`*** trees are **emit / harness / backup** artifacts — treat as **inputs or archives**, not competing product truths.
- `**!atomadic-uep`** depends on `**ass-ade`** package name per its `pyproject.toml`; keep dependency edges aligned with whichever spine ships.

See `[docs/ASS_ADE_SPINE_RFC.md](docs/ASS_ADE_SPINE_RFC.md)` for the recommended convergence roles.