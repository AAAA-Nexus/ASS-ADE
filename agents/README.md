# `agents/` — Atomadic ASS-ADE swarm (Claude / Cursor / VS Code)

This folder is the **canonical prompt surface** for the **25-agent** build pipeline (**00 → 24**). Cursor loads human-editable prompts here; bridge files under `~/.cursor/agents/` are **generated** from [`build_swarm_registry.json`](build_swarm_registry.json).

## Start here

| Doc | Purpose |
|-----|---------|
| [`INDEX.md`](INDEX.md) | Chain diagram, delegation envelopes, §11 AAAA-Nexus |
| [`_PROTOCOL.md`](_PROTOCOL.md) | Inbound/outbound JSON, refusal, gaps, genesis, §11 |
| [`NEXUS_SWARM_MCP.md`](NEXUS_SWARM_MCP.md) | MCP tool matrix for `user-aaaa-nexus` |
| [`ASS_ADE_MONADIC_CODING.md`](ASS_ADE_MONADIC_CODING.md) | CNA + a0…a4 monadic vocabulary |
| [`ATO_DEV_ENVIRONMENT.md`](ATO_DEV_ENVIRONMENT.md) | **Dev environment alignment** — global bridges, T12 paths, verification |
| [`ATOMADIC_PATH_BINDINGS.md`](ATOMADIC_PATH_BINDINGS.md) | `ATOMADIC_WORKSPACE` (and optional Nexus workspace placeholder) |

Workspace-level ship docs (parent of `agents/`):

- [`../AGENTS.md`](../AGENTS.md)  
- [`../ASS_ADE_SHIP_PLAN.md`](../ASS_ADE_SHIP_PLAN.md)  
- [`../ASS_ADE_GOAL_PIPELINE.md`](../ASS_ADE_GOAL_PIPELINE.md)  
- [`../docs/ATOMADIC_SWARM_SURFACE_AUDIT.md`](../docs/ATOMADIC_SWARM_SURFACE_AUDIT.md)

## Sync Cursor subagent bridges

From the **workspace root** (parent of `agents/`):

```bash
python agents/sync_build_swarm_to_cursor.py
```

Regenerate after **any** edit to `*.prompt.md`, `INDEX.md`, `_PROTOCOL.md`, `NEXUS_SWARM_MCP.md`, `ASS_ADE_MONADIC_CODING.md`, or the registry.

```bash
python agents/check_swarm_prompt_alignment.py
```

Fails if any pipeline prompt is missing mandatory protocol anchors (also run in CI).

## ASS-ADE product CLI (monadic assimilate)

Install from **repository root** (T12 — see [`../docs/ASS_ADE_UNIFICATION.md`](../docs/ASS_ADE_UNIFICATION.md)), then:

```text
pip install -e ".[dev]"   # from repo root
ass-ade-unified doctor
ass-ade-unified assimilate PRIMARY_REPO OUTPUT --also OTHER_REPO
```

Optional v1 studio: `pip install -e ../ass-ade-v1` then `ass-ade-unified studio …`.

## Historical audit

[`_AUDIT.md`](_AUDIT.md) — 2026-04-20 per-prompt grades. For **surface / hooks / Cursor** alignment, prefer [`../docs/ATOMADIC_SWARM_SURFACE_AUDIT.md`](../docs/ATOMADIC_SWARM_SURFACE_AUDIT.md).
