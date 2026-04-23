# Atomadic workspace (`C:\!atomadic`) — agent map

## Read first

1. [`ASS_ADE_SHIP_PLAN.md`](ASS_ADE_SHIP_PLAN.md) — **execution roadmap**: Phase 0–6, exit criteria, anti-patterns, first 48h.  
2. [`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) — **technical checklist**: preflight, book 0–7, v1 parity, ship; HAVE / GAP / IMPLEMENT per track.  
3. [`docs/ATOMADIC_SWARM_SURFACE_AUDIT.md`](docs/ATOMADIC_SWARM_SURFACE_AUDIT.md) — **Cursor / hooks / agents / VS Code** surfaces aligned to the ship plan.  
4. [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) — **single ASS-ADE** goal, CNA/monadic target, `ass-ade-unified`, merge phases.  

5. [`docs/ASS_ADE_SPINE_RFC.md`](docs/ASS_ADE_SPINE_RFC.md) — interim terrain (v1 engine vs v1.1 spine vs distribution), ephemeral dirs.  
6. [`ASS_ADE_MATRIX.md`](ASS_ADE_MATRIX.md) — versions, CLIs, capabilities per tree.  
7. [`ASS_ADE_INVENTORY.md`](ASS_ADE_INVENTORY.md) — fingerprint of `ass-ade*` dirs (re-run: `python scripts/regenerate_ass_ade_docs.py` or `scripts/inventory_ass_ade.ps1`). [`ASS_ADE_SUITE_SNAPSHOT.md`](ASS_ADE_SUITE_SNAPSHOT.md) — full machine snapshot from the same script.  
8. [`agents/ATOMADIC_PATH_BINDINGS.md`](agents/ATOMADIC_PATH_BINDINGS.md) — `ATOMADIC_WORKSPACE` / `ATOMADIC_NEXUS_WORKSPACE` placeholders.  
9. **Persistent swarm automation (optional):** `python scripts/run_swarm_services.py` — long-running heartbeat + `tasks.json` nudges; see [`.cursor/hooks/README.md`](.cursor/hooks/README.md) § *Persistent Python services*.  
10. **Ship ADE to any workspace:** `ass-ade-unified ade materialize` — populates **`.ade/`** (hooks, automation, harness refs) from this monorepo; see [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) § *ADE / Atomadic operator stack*.  
11. **One-paste swarm (all IDEs):** [`SWARM-ONE-PROMPT.md`](SWARM-ONE-PROMPT.md) — host prep + single boxed prompt for Cursor, VS Code Copilot, and Codex. Quick prep: `powershell -NoProfile -File scripts/ensure_dev_session.ps1` from repo root.  
12. **Cross-IDE control surfaces:** [`.github/copilot-instructions.md`](.github/copilot-instructions.md), [`.github/agents/`](.github/agents), and [`.github/skills/ass-ade-ship-control/`](.github/skills/ass-ade-ship-control) mirror the active ship plan for Copilot / VS Code custom agents.  
13. **Nexus MCP + LoRA dev corpus:** [`agents/NEXUS_SWARM_MCP.md`](agents/NEXUS_SWARM_MCP.md) §9 — `AAAA_NEXUS_API_KEY` in `.env`, `python scripts/nexus_env_smoke.py`, full §11 tool chain when the key is live; corpus `python scripts/collect_ass_ade_dev_corpus.py`; local LoRA `pip install -e ".[lora]"` then `python scripts/train_lora_local.py`.  
14. **Pre-push staging proof:** `ass-ade-unified ade ship-audit --staging-root C:\!aaaa-nexus\!ass-ade` — blocks on dirty git state, missing remotes, or ship-surface drift between private and public trees.

## Do not edit as product code

- `ass-ade-v1/.pytest_tmp/**`
- Dated `ass-ade-v1-test-backup-*` (archive policy TBD)
- Large `[rebuild-outputs](rebuild-outputs)` unless intentionally curating examples

## ASS-ADE agent swarm

Canonical pipeline prompts live under [`agents/`](agents) (`INDEX.md`, `_PROTOCOL.md`). **Alignment brief (CNA / MAP = TERRAIN / Nexus / T12 / global bridges):** [`agents/ATO_DEV_ENVIRONMENT.md`](agents/ATO_DEV_ENVIRONMENT.md). After prompt or protocol edits: `python agents/sync_build_swarm_to_cursor.py` (from repo root). Verify anchors: `python agents/check_swarm_prompt_alignment.py`.

Keep the root `AGENTS.md`, [`.github/copilot-instructions.md`](.github/copilot-instructions.md), [`.github/agents/`](.github/agents), and [`.github/skills/ass-ade-ship-control/`](.github/skills/ass-ade-ship-control) aligned so Cursor, Copilot, and in-repo agents operate from the same living plan and release-gate truth.

**ADE strict harness (duplicate swarm):** [`ADE/HARNESS_README.md`](ADE/HARNESS_README.md) — hook gate, `ade-*` Cursor bridges, sentinel agent 25. Sync: `scripts/sync_agents_to_ade.ps1` · verify: `python ADE/harness/verify_ade_harness.py` · bridges: `python ADE/sync_ade_swarm_to_cursor.py`.

## “One command” roadmap

See [`docs/ASS_ADE_FORGE_CLI.md`](docs/ASS_ADE_FORGE_CLI.md) — dispatcher sketch (`atomadic forge`) over today’s `ass-ade rebuild` / `ass-ade-v11` CLIs.

## United CLI (one venv, co-install)

```text
pip install -e .[dev]     # from repository root; spine is defined in root pyproject.toml
pip install -e ./ass-ade-v1
ass-ade-unified doctor
ass-ade-unified assimilate PRIMARY_REPO OUTPUT_PARENT --also SIBLING1 --also SIBLING2
ass-ade-unified book rebuild …
ass-ade-unified studio …
```

[`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md)
