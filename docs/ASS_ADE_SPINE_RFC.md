# ASS-ADE spine RFC (workspace convergence)

> **Current trunk:** This checkout now ships the monadic spine under `ass-ade-v1.1/` **and** the restored Atomadic engine under `atomadic-engine/`. Rows that point to folders outside `C:\!aaaa-nexus\!ass-ade` are donor/archive context, not alternate product roots.

Status: **Accepted for coordination** — interim roles across checkouts until **one** CNA/monadic product ships. Operator entry: **`ass-ade`** ([`docs/ASS_ADE_UNIFICATION.md`](ASS_ADE_UNIFICATION.md)).

## Problem

Multiple trees still **build** different slices of ASS-ADE: rebuild engine, monadic pipeline, marketing `1.0.0` line, UEP composition, and many **test / backup / pytest_tmp** clones. Agents drift when hard-coded paths or “the” checkout move. **Product intent** is a **single** ASS-ADE; the repo layout is catching up.

## Recommended roles (MAP = TERRAIN)


| Role                                | Path                                                              | Owns                                                                                                                    |
| ----------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Product trunk**                   | [`..`](..)                                                        | Root `pyproject.toml`, `ass_ade_v11` spine, restored `atomadic-engine/src/ass_ade`, one install                         |
| **Restored rebuild / assimilation engine** | [`../atomadic-engine`](../atomadic-engine)                   | `ass-ade rebuild`, `src/ass_ade/engine/rebuild/*`, sibling scanning, emitted packages                                  |
| **Monadic vNext + import law**      | `[ass-ade-v1.1](../ass-ade-v1.1)`                                 | `ass_ade_v11`, `pipeline_book` phases 0–7, `import-linter`, MAP=TERRAIN notes vs `ass-ade-v1*`                          |
| **Distribution / site-facing line** | `[ass-ade](../ass-ade)`                                           | Version **1.0.0**, Click CLI, x402 stack — **merge target for public install** once feature parity is decided           |
| **Composition / private UEP**       | `[!atomadic-uep](../!atomadic-uep)`                               | Binds `ass-ade` + private engines; **not** the ASS-ADE core spine                                                       |
| **Harness / backup / emit**         | `ass-ade-v1-test*`, dated backups                                 | **Archive or read-only inputs** — never the default edit surface                                                        |
| **Ephemeral**                       | `ass-ade-v1/.pytest_tmp`, `[rebuild-outputs](../rebuild-outputs)` | **Do not hand-edit**; safe to delete per hygiene policy                                                                 |


## Spine choice (operational default)

For the current `C:\!aaaa-nexus\!ass-ade` trunk, use:

1. **CNA / monadic law + phased book**: [`ass-ade-v1.1/src/ass_ade_v11`](../ass-ade-v1.1/src/ass_ade_v11).
2. **Restored engine + broad CLI**: [`atomadic-engine/src/ass_ade`](../atomadic-engine/src/ass_ade).
3. **Generated outputs and quarantine folders**: evidence only; see [`ONE_WORKING_PRODUCT.md`](ONE_WORKING_PRODUCT.md).

Until **physical** merge into one `src/` tree:

1. **CNA / monadic law + phased book** — design authority: **[`ass-ade-v1.1`](../ass-ade-v1.1)** (`ass_ade_v11`, `pipeline_book`). **Import law (`import-linter`)** is enforced via **[repo-root `pyproject.toml`](../pyproject.toml)** (T12); install with `pip install -e ".[dev]"` from the umbrella root (not a separate `[project]` only under `ass-ade-v1.1/`).
2. **Rebuild engine + broad Typer shell** — restored under **[`atomadic-engine`](../atomadic-engine)** (`ass_ade`) and flattened into **`ass-ade`**.
3. **Genesis JSON schema** today: under **[`ass-ade/.ass-ade/genesis/`](../ass-ade/.ass-ade/genesis)** (v1.1 also carries a copy; keep **one** canonical).

**Target:** one package, one CLI — phases in [`docs/ASS_ADE_UNIFICATION.md`](ASS_ADE_UNIFICATION.md).

## Sibling policy

- **Input**: feature branches and `ass-ade-v1-test*` → cherry-pick or re-emit via rebuild into the spine.
- **Archive**: dated `*-backup-*` → zip or move to `archive/` outside hot path.
- **Delete**: `pytest_tmp` trees on a schedule after CI green.

## Agent rule (one sentence)

If a task says “edit ASS-ADE” without a path: **new monadic / CNA work** -> **`ass-ade-v1.1/src/ass_ade_v11/`**; **Atomadic shell / rebuild engine** -> **`atomadic-engine/src/ass_ade/`**. Consult [`ASS_ADE_MATRIX.md`](../ASS_ADE_MATRIX.md) and [`docs/ASS_ADE_UNIFICATION.md`](ASS_ADE_UNIFICATION.md) before touching any sibling tree.

## Next decisions (human)

1. Publish target and version cadence for the `ass-ade` distribution.
2. Whether `atomadic` remains a long-term alias after `ass-ade` is fully established.
3. **Hygiene**: gitignore / CI policy for `.pytest_tmp` and `rebuild-outputs`.

## References

- `[ASS_ADE_INVENTORY.md](../ASS_ADE_INVENTORY.md)` — discovered paths  
- `[ASS_ADE_MATRIX.md](../ASS_ADE_MATRIX.md)` — capability matrix  
- [`docs/ASS_ADE_UNIFICATION.md`](ASS_ADE_UNIFICATION.md) — single-product merge plan + `ass-ade`  
- `[docs/ASS_ADE_FORGE_CLI.md](ASS_ADE_FORGE_CLI.md)` — one-command dispatcher sketch  
- `[agents/ATOMADIC_PATH_BINDINGS.md](../agents/ATOMADIC_PATH_BINDINGS.md)` — path placeholder for prompts
