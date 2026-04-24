# ASS-ADE one command - dispatcher contract

The plan splits concerns into **(A) multi-tree assimilation** and **(B) single-spine ship/rebuild**. A single UX can wrap both.

## Today (merged CLI)


| CLI | Project | Notes |
| --- | ------- | ----- |
| `ass-ade` | root [`pyproject.toml`](../pyproject.toml) | Product CLI: Atomadic engine commands plus `book`, `assimilate`, `ade`, `doctor`. |
| `atomadic` | root [`pyproject.toml`](../pyproject.toml) | Alias to the same merged CLI. |


Primary **rebuild** implementation lives under the restored engine in [`atomadic-engine/src/ass_ade/engine/rebuild`](../atomadic-engine/src/ass_ade/engine/rebuild).

## Recommended dispatcher: `ass-ade forge` (future)

Subcommands (sketch — implement by delegating to existing modules, not rewriting engines):


| Subcommand        | Purpose                                     | Delegates to                                                                       |
| ----------------- | ------------------------------------------- | ---------------------------------------------------------------------------------- |
| `forge inventory` | Re-run fingerprint scan                     | `[scripts/inventory_ass_ade.ps1](../scripts/inventory_ass_ade.ps1)` or Python port |
| `forge plan`      | Diff N roots → merge plan (dry-run default) | New thin planner; inputs from `ASS_ADE_INVENTORY.paths.json`                       |
| `forge apply`     | Execute approved plan                       | git / patch application + policy hooks                                             |
| `forge rebuild`   | Single-spine emit                           | `ass-ade rebuild ...`                                                              |
| `forge ship`      | Docs + tests + receipts                     | wrap `_generate_rebuild_docs` / package emitter pipeline                           |


**Default safety:** `forge` with no args prints help; destructive steps require `--i-understand` or `--yes`.

## One command mapping

- **User phrase**: “assimilate everything”  
**Actual chain**: `forge inventory` → `forge plan --roots ...` → human review → `forge apply` → `forge rebuild` on spine → `forge ship`.
- **User phrase**: “ship this repo”  
**Actual chain**: `forge rebuild` only (single tree).

## Until dispatcher exists

Documented two-step manual:

```text
# Engine rebuild
ass-ade rebuild <source> --output <output>

# Monadic book / gates
ass-ade book rebuild <source> --output <output>

# Multi-root assimilate
ass-ade assimilate PRIMARY OUT --also SIBLING --policy POLICY.yaml
```

Run `ass-ade --help` after install for the full merged surface.

## Inventory script

Bounded scan: `[scripts/inventory_ass_ade.ps1](../scripts/inventory_ass_ade.ps1)` → writes `[ASS_ADE_INVENTORY.md](../ASS_ADE_INVENTORY.md)`.
