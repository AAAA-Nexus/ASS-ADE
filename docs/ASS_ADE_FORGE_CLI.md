# ASS-ADE “one command” — dispatcher contract

The plan splits concerns into **(A) multi-tree assimilation** and **(B) single-spine ship/rebuild**. A single UX can wrap both.

## Today (existing CLIs)


| CLI                                   | Project                           | Notes                                                                                                                                                         |
| ------------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `**ass-ade-unified`**                 | **[repo root `pyproject.toml`](../pyproject.toml)** (T12; sources in `ass-ade-v1.1/src/`) | `**assimilate**` = multi-root → monadic book (one command); `book`, `studio` (optional v1), `doctor`. See [`ASS_ADE_UNIFICATION.md`](ASS_ADE_UNIFICATION.md). |
| `ass-ade` / `atomadic` / `controller` | `[ass-ade-v1](../ass-ade-v1)`     | Typer `ass_ade.cli:app` — rebuild, recon, marketplace forge, Nexus families, etc.                                                                             |
| `ass-ade` / `atomadic`                | `[ass-ade](../ass-ade)`           | Click `ass_ade.cli.__main__:main` — overlapping name; different stack                                                                                         |
| `ass-ade-v11`                         | Same install as **`ass-ade-unified`** (root `pyproject.toml`) | Monadic pipeline only; prefer `ass-ade-unified book` for the single-product path                                                                              |


Primary **rebuild** implementation lives under `**ass-ade-v1`** (`ass_ade.engine.rebuild` per `[ass-ade-v1/.ass-ade/tier-map.json](../ass-ade-v1/.ass-ade/tier-map.json)`).

## Recommended dispatcher: `atomadic forge` (future)

Subcommands (sketch — implement by delegating to existing modules, not rewriting engines):


| Subcommand        | Purpose                                     | Delegates to                                                                       |
| ----------------- | ------------------------------------------- | ---------------------------------------------------------------------------------- |
| `forge inventory` | Re-run fingerprint scan                     | `[scripts/inventory_ass_ade.ps1](../scripts/inventory_ass_ade.ps1)` or Python port |
| `forge plan`      | Diff N roots → merge plan (dry-run default) | New thin planner; inputs from `ASS_ADE_INVENTORY.paths.json`                       |
| `forge apply`     | Execute approved plan                       | git / patch application + policy hooks                                             |
| `forge rebuild`   | Single-spine emit                           | `ass-ade rebuild …` from `**ass-ade-v1`** venv                                     |
| `forge ship`      | Docs + tests + receipts                     | wrap `_generate_rebuild_docs` / package emitter pipeline                           |


**Default safety:** `forge` with no args prints help; destructive steps require `--i-understand` or `--yes`.

## “One command” mapping

- **User phrase**: “assimilate everything”  
**Actual chain**: `forge inventory` → `forge plan --roots ...` → human review → `forge apply` → `forge rebuild` on spine → `forge ship`.
- **User phrase**: “ship this repo”  
**Actual chain**: `forge rebuild` only (single tree).

## Until dispatcher exists

Documented two-step manual:

```text
# (1) sibling → monadic emit (from ass-ade-v1 install)
ass-ade rebuild <source> <output>

# (2) v1.1 book / gates (unified or standalone)
ass-ade-unified book rebuild …
# or: ass-ade-v11 …
```

Exact v1.1 subcommands are defined in `ass_ade_v11.a4_sy_orchestration.cli` — run `ass-ade-v11 --help` after install.

## Inventory script

Bounded scan: `[scripts/inventory_ass_ade.ps1](../scripts/inventory_ass_ade.ps1)` → writes `[ASS_ADE_INVENTORY.md](../ASS_ADE_INVENTORY.md)`.