# Atomadic dev environment — swarm + global agents

This file is the **single alignment brief** for:

- **In-repo pipeline agents** — `agents/*-*.prompt.md` (00–24) and `INDEX.md`
- **Global Cursor bridges** — `~/.cursor/agents/ass-ade-*.md` (generated; not committed)
- **Host tooling** — inventory, CI, ASS-ADE install (T12)

## Authority stack (never invert)

1. `<ATOMADIC_WORKSPACE>/RULES.md` and the active plan `RULES.md` (when present)
2. `agents/_PROTOCOL.md` — envelopes §1–§2, status §9, **§11 AAAA-Nexus** preflight/postflight
3. `agents/ASS_ADE_MONADIC_CODING.md` — CNA, five-tier vocabulary, import law, `ass_ade` paths (`src/ass_ade/`)
4. `agents/NEXUS_SWARM_MCP.md` — MCP tool names, RatchetGate, Aegis, drift, receipts
5. The agent’s own `.prompt.md` (identity + task schema)

**MAP = TERRAIN:** no stubs, no fake completions, no undocumented `engine/` drops. **Gap-file or refuse** per `_PROTOCOL.md` §4.

## ASS-ADE product paths (T12)

- **Install:** `pip install -e ".[dev]"` from the **monorepo root** (`pyproject.toml` is canonical `[project]`).
- **Monadic package:** canonical source path `src/ass_ade/` — tiers `a0_qk_constants` ... `a4_sy_orchestration`.
- **Product assimilate:** `ass-ade assimilate ...` (see `docs/ASS_ADE_UNIFICATION.md`).

When a handoff says “edit `ass_ade`”, the canonical package is `ass_ade` under `src/ass_ade/` in the ASS-ADE-SEED repo.

## Global Cursor agents (bridges)

Canonical prompts stay **in this repo** under `agents/`. Cursor discovers **short** bridge files under **`%USERPROFILE%\.cursor\agents\`** (Linux/macOS: `~/.cursor/agents/`).

After **any** change to `agents/*.prompt.md`, `agents/_PROTOCOL.md`, `agents/NEXUS_SWARM_MCP.md`, or `agents/ASS_ADE_MONADIC_CODING.md`:

```bash
python agents/sync_build_swarm_to_cursor.py
```

That regenerates `ass-ade-00-interpreter.md` … `ass-ade-24-genesis-recorder.md` and `ass-ade-pipeline-orchestrator.md` with up-to-date absolute paths to this workspace.

## Copilot / VS Code surfaces

Keep these repo-side surfaces aligned with the active ship plan and root `AGENTS.md`:

- `.github/copilot-instructions.md`
- `.github/agents/`
- `.github/skills/ass-ade-ship-control/`

Release truth still comes from the same gates regardless of host:

- Private spine gate: `python scripts/ship_readiness_audit.py`
- Public staging gate: `ass-ade ade ship-audit --staging-root <ATOMADIC_NEXUS_WORKSPACE>/!ass-ade`

## Verification (CI + local)

```bash
python agents/check_swarm_prompt_alignment.py
```

Fails if any pipeline `.prompt.md` is missing required protocol anchors (`_PROTOCOL.md`, `MAP = TERRAIN`, `ATOMADIC_WORKSPACE`, `## Protocol`).

## Terrain inventory (disk)

**Cross-platform (repo-local scan, path-agnostic):**

```bash
python scripts/regenerate_ass_ade_docs.py
```

Refreshes `ASS_ADE_INVENTORY.md`, `ASS_ADE_INVENTORY.paths.json`, `ASS_ADE_SUITE_SNAPSHOT.md`, and the bounded `<!-- ASS_ADE_AUTOGEN -->` blocks in `ASS_ADE_MATRIX.md`, `ASS_ADE_SHIP_PLAN.md`, and `ASS_ADE_GOAL_PIPELINE.md`.

**Windows-wide fingerprint (optional; scans extra drives):**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/inventory_ass_ade.ps1
```

Refreshes `ASS_ADE_INVENTORY.md` / `ASS_ADE_INVENTORY.paths.json` only (does not update the other ASS_ADE\* suite files).

## ASS-ADE matrix (versions + git heads)

`ASS_ADE_MATRIX.md` — refresh the **Git (short)** column per subtree with:

```bash
git -C ass-ade rev-parse --short HEAD
git -C "!atomadic-uep" rev-parse --short HEAD
```

The canonical ASS-ADE source is `src/ass_ade/` in the ASS-ADE-SEED repo. Historical `ass-ade-v1.1` paths are deprecated — use `src/ass_ade/` for all new work.

## Related

- [`INDEX.md`](INDEX.md) — chain diagram, envelopes, invocation
- [`ATOMADIC_PATH_BINDINGS.md`](ATOMADIC_PATH_BINDINGS.md) — placeholders
- [`docs/ATOMADIC_SWARM_SURFACE_AUDIT.md`](../docs/ATOMADIC_SWARM_SURFACE_AUDIT.md) — Cursor / hooks / VS Code surfaces
