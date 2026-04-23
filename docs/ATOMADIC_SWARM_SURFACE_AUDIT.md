# Atomadic swarm — surface audit & alignment (Cursor / VS Code / ASS-ADE)

**Date:** 2026-04-22  
**Scope:** Workspace `C:\!atomadic` controlling surfaces: Cursor hooks/rules, ASS-ADE agent prompts (`agents/`), harness scripts, MCP/Nexus docs, alignment with [`ASS_ADE_SHIP_PLAN.md`](../ASS_ADE_SHIP_PLAN.md) and [`ASS_ADE_GOAL_PIPELINE.md`](../ASS_ADE_GOAL_PIPELINE.md).

**Non-scope:** Deleting the ASS-ADE pipeline agents. Agents 00-24 are the intentional monadic/swarm chain; agents 25-28 are temporary tiny cleanup lanes. This audit **aligns** them; it does not replace product code.

---

## 1. Boundary model (private vs public)

| Zone | Content | Agents / tools |
|------|---------|------------------|
| **Private / UEP / MHED-Codex** | Sovereign IP, unreleased engines, internal plans | Swarm prompts under [`agents/`](../agents), `.ato-plans/`, UEP under [`!atomadic-uep`](../!atomadic-uep) |
| **Public scrubbed** | Marketable names (e.g. Interpreter), AAAA-Nexus contracts | [`agents/NEXUS_SWARM_MCP.md`](../agents/NEXUS_SWARM_MCP.md), MCP `user-aaaa-nexus` |
| **ASS-ADE product** | CNA/monadic emit, assimilate | `ass-ade`, backed by [`unified_cli.py`](../ass-ade-v1.1/src/ass_ade_v11/a4_sy_orchestration/unified_cli.py) |

**MAP = TERRAIN:** No stubs in shipped paths; unknowns → gap file or refuse ([`agents/_PROTOCOL.md`](../agents/_PROTOCOL.md), [`agents/ASS_ADE_MONADIC_CODING.md`](../agents/ASS_ADE_MONADIC_CODING.md)).

---

## 2. Inventory — what exists today

### 2.1 Workspace Cursor (`.cursor/`)

| Asset | Role | Alignment status |
|-------|------|-------------------|
| [`hooks.json`](../.cursor/hooks.json) | `sessionStart` / `postToolUse` / `subagentStart` → `swarm_signal.py check` | **OK** — keeps swarm bus alive between tool calls |
| [`hooks/swarm_signal.py`](../.cursor/hooks/swarm_signal.py), `swarm_scribe.py` | Signal bus + scribe | **OK** — document env `SWARM_AGENT`, `SWARM_HOOK_SILENT` |
| [`hooks/README.md`](../.cursor/hooks/README.md) | Operator guide | **UPDATED** — points to ship plan + correct product paths |
| `context-packs/*.json` | Lane / bootstrap artifacts | **Operational** — not agents; prune/archive per [`ASS_ADE_SHIP_PLAN.md`](../ASS_ADE_SHIP_PLAN.md) Phase 0 |
| [`scripts/asymmetric_invariant_lint.py`](../.cursor/scripts/asymmetric_invariant_lint.py) | Extra lint | **OK** — optional in CI |

**Gap:** No **workspace-root** `.cursor/rules/*.mdc` before this pass — **FIXED** by [`.cursor/rules/atomadic-swarm.mdc`](../.cursor/rules/atomadic-swarm.mdc).

### 2.2 Nested Cursor (`ass-ade/`, `ass-ade-v1/`)

| Path | Role |
|------|------|
| `ass-ade/.cursor/rules/atomadic-global.mdc` | Global rule copy in legacy tree |
| `ass-ade-v1/.cursor/mcp.json`, `rules/atomadic-global.mdc` | v1 MCP + rules |

**Alignment:** Prefer **one** workspace rule at repo root; nested copies can drift — refresh from root rule when editing those trees.

### 2.3 ASS-ADE agents (`agents/`)

| Asset | Count / role |
|-------|----------------|
| `00`-`24` `*.prompt.md` | **25** single-purpose agents (QK->SY chain) |
| `25`-`28` `*.prompt.md` | **4** tiny consolidation lanes for docs, prompts, tests, and duplicate-install notes |
| [`INDEX.md`](../agents/INDEX.md) | Chain diagram, envelopes, §11 Nexus |
| [`_PROTOCOL.md`](../agents/_PROTOCOL.md), `NEXUS_SWARM_MCP.md`, `ASS_ADE_MONADIC_CODING.md` | Governance + MCP + monadic law |
| [`build_swarm_registry.json`](../agents/build_swarm_registry.json) | Cursor bridge metadata |
| [`sync_build_swarm_to_cursor.py`](../agents/sync_build_swarm_to_cursor.py) | Writes `~/.cursor/agents/ass-ade-*.md` |
| [`ATOMADIC_PATH_BINDINGS.md`](../agents/ATOMADIC_PATH_BINDINGS.md) | `ATOMADIC_WORKSPACE` + second workspace |

**Historical:** [`_AUDIT.md`](../agents/_AUDIT.md) — 2026-04-20 prompt grades; **not** removed — retained; forward-looking checklist is **this file** + [`ASS_ADE_GOAL_PIPELINE.md`](../ASS_ADE_GOAL_PIPELINE.md).

### 2.4 VS Code

| State | Action |
|-------|--------|
| No root `.vscode/` | **ADDED** minimal [`../.vscode/extensions.json`](../.vscode/extensions.json) (Python stack) |

Claude Code / worktrees under `!atomadic-uep` carry their own `.vscode/tasks.json` — **out of scope** for ASS-ADE swarm sync; UEP team maintains those.

### 2.5 Global (machine-wide) — checklist for operators

Cursor / Claude **global** config lives outside this repo. Operators should verify:

1. **Cursor → MCP:** `user-aaaa-nexus` configured per [`agents/NEXUS_SWARM_MCP.md`](../agents/NEXUS_SWARM_MCP.md); API key in host env or `terminal.integrated.envFile` → `<ATOMADIC_WORKSPACE>/.env`.
2. **Regenerate bridges** after any prompt or protocol edit:  
   `python agents/sync_build_swarm_to_cursor.py` (from `<ATOMADIC_WORKSPACE>`).
3. **`~/.cursor/agents/`** contains `ass-ade-00-interpreter.md` … `ass-ade-24-genesis-recorder.md` and `ass-ade-pipeline-orchestrator.md`.
4. **Read** [`agents/ATO_DEV_ENVIRONMENT.md`](../agents/ATO_DEV_ENVIRONMENT.md) — CNA / MAP = TERRAIN / T12 paths / Nexus precedence for in-repo + global agents. **Verify** prompt anchors: `python agents/check_swarm_prompt_alignment.py`.

---

## 3. Alignment actions (completed in repo)

| # | Action |
|---|--------|
| A1 | Add [`.cursor/rules/atomadic-swarm.mdc`](../.cursor/rules/atomadic-swarm.mdc) (workspace root) — Cursor rule for swarm + ship plan + `ass-ade` when editing listed globs. |
| A2 | Add [`agents/README.md`](../agents/README.md) — how to run sync, read INDEX, obey path bindings. |
| A3 | Extend [`agents/ATOMADIC_PATH_BINDINGS.md`](../agents/ATOMADIC_PATH_BINDINGS.md) — `ATOMADIC_NEXUS_WORKSPACE` for second umbrella. |
| A4 | Update [`agents/INDEX.md`](../agents/INDEX.md) — remove hardcoded `c:\!aaaa-nexus` path; reference assimilate + ship docs. |
| A5 | Update [`.cursor/hooks/README.md`](../.cursor/hooks/README.md) — ship plan link; de-hardcode `ass-ade/src` product path wording. |
| A6 | Link this audit from [`AGENTS.md`](../AGENTS.md). |

---

## 4. Recommended operator order (before executing ship plan)

1. Read [`AGENTS.md`](../AGENTS.md) → [`ASS_ADE_SHIP_PLAN.md`](../ASS_ADE_SHIP_PLAN.md).  
2. `pip install -e ".[dev]"` from repo root; then `ass-ade doctor`.  
3. `python agents/sync_build_swarm_to_cursor.py`  
4. `python agents/check_swarm_prompt_alignment.py`  
5. Open Cursor **Hooks** output once to confirm `swarm_signal.py` exits 0.  
6. Set `SWARM_AGENT` for multi-tab swarms per hooks README.

---

## 5. Future work (not done in this pass)

| Item | Owner / phase |
|------|----------------|
| Auto-run `import-linter` from a Cursor hook on save | Phase 3 ship plan — optional |
| Retire duplicate `atomadic-global.mdc` in sub-trees | When single package lands |
| Claude Desktop global system prompt | Operator machine — document only |

---

*Maintainers: update this file when hooks, agent count, or Cursor bridge layout changes.*
