# ASS-ADE product trunk (`C:\!aaaa-nexus\!ass-ade`) - agent map

This checkout is the product trunk. Do not treat sibling folders under
`C:\!aaaa-nexus` as alternate products unless [`docs/ONE_WORKING_PRODUCT.md`](docs/ONE_WORKING_PRODUCT.md)
is updated first.

## Read first

1. [`docs/ONE_WORKING_PRODUCT.md`](docs/ONE_WORKING_PRODUCT.md) - **current trunk decision**: product, donor, quarantine, archive.
2. [`ASS_ADE_SHIP_PLAN.md`](ASS_ADE_SHIP_PLAN.md) — **execution roadmap**: Phase 0–6, exit criteria, anti-patterns, first 48h.  
3. [`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) — **technical checklist**: preflight, book 0–7, engine parity, ship; HAVE / GAP / IMPLEMENT per track.  
4. [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) — **single ASS-ADE** goal, CNA/monadic target, `ass-ade`, merge phases.  
5. [`docs/ASS_ADE_FEATURE_INVENTORY.md`](docs/ASS_ADE_FEATURE_INVENTORY.md) — current feature locations in `ass-ade-v1.1/` and `atomadic-engine/`.
6. [`docs/CURSOR_AGENT_LANES.md`](docs/CURSOR_AGENT_LANES.md) — four tiny Cursor-safe lanes for docs, prompts, smoke tests, and duplicate-install notes.
7. [`docs/ATOMADIC_SWARM_SURFACE_AUDIT.md`](docs/ATOMADIC_SWARM_SURFACE_AUDIT.md) — **Cursor / hooks / agents / VS Code** surfaces aligned to the ship plan.  
8. [`docs/ASS_ADE_SPINE_RFC.md`](docs/ASS_ADE_SPINE_RFC.md) — interim terrain and archive policy.  
9. [`ASS_ADE_MATRIX.md`](ASS_ADE_MATRIX.md) — versions, CLIs, capabilities per tree.  
10. [`agents/ATOMADIC_PATH_BINDINGS.md`](agents/ATOMADIC_PATH_BINDINGS.md) — `ATOMADIC_WORKSPACE` / `ATOMADIC_NEXUS_WORKSPACE` placeholders.  
11. **Persistent swarm automation (optional):** `python scripts/run_swarm_services.py` — long-running heartbeat + task nudges.  
12. **Ship ADE to any workspace:** `ass-ade ade materialize` — populates **`.ade/`** (hooks, automation, harness refs) from this monorepo; see [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) § *ADE / Atomadic operator stack*.  
13. **One-paste swarm (all IDEs):** [`SWARM-ONE-PROMPT.md`](SWARM-ONE-PROMPT.md) — host prep + single boxed prompt for Cursor, VS Code Copilot, and Codex. Quick prep: `powershell -NoProfile -File scripts/ensure_dev_session.ps1` from repo root.  
14. **Nexus MCP + LoRA dev corpus:** [`agents/NEXUS_SWARM_MCP.md`](agents/NEXUS_SWARM_MCP.md) §9 — `AAAA_NEXUS_API_KEY` in `.env`, `python scripts/nexus_env_smoke.py`, full §11 tool chain when the key is live; corpus `python scripts/collect_ass_ade_dev_corpus.py`; local LoRA `pip install -e ".[lora]"` then `python scripts/train_lora_local.py`.  
15. **Pre-push staging proof:** `ass-ade ade ship-audit --staging-root C:\!aaaa-nexus\!ass-ade` — blocks on dirty git state, missing remotes, or ship-surface drift.

## Default edit rule

- ASS-ADE monadic pipeline, policy, plan, import-law, ADE: edit internal source path `ass-ade-v1.1/src/ass_ade_v11/`.
- ASS-ADE Atomadic shell, broad CLI, local rebuild, Nexus, MCP, A2A, agent loop: edit internal source path `atomadic-engine/src/ass_ade/`.
- Quarantine comparison: read `QUARANTINE_IP_LEAK_v20/`, but do not copy from it without scrub review.

## Do not edit as product code

- `ass-ade-v1/.pytest_tmp/**`
- Dated `ass-ade-v1-test-backup-*` (archive policy TBD)
- Large `[rebuild-outputs](rebuild-outputs)` unless intentionally curating examples
- `ass-ade-final-release*`, `assimilated_ade/`, `ASS-CLAW*` unless explicitly converting them into fixtures.

## ASS-ADE agent swarm

Canonical pipeline prompts live under [`agents/`](agents) (`INDEX.md`, `_PROTOCOL.md`). **Alignment brief (CNA / MAP = TERRAIN / Nexus / T12 / global bridges):** [`agents/ATO_DEV_ENVIRONMENT.md`](agents/ATO_DEV_ENVIRONMENT.md). After prompt or protocol edits: `python agents/sync_build_swarm_to_cursor.py` (from repo root). Verify anchors: `python agents/check_swarm_prompt_alignment.py`.

Keep the root `AGENTS.md`, [`.github/copilot-instructions.md`](.github/copilot-instructions.md), [`.github/agents/`](.github/agents), and [`.github/skills/ass-ade-ship-control/`](.github/skills/ass-ade-ship-control) aligned so Cursor, Copilot, and in-repo agents operate from the same living plan and release-gate truth.

**ADE strict harness (duplicate swarm):** [`ADE/HARNESS_README.md`](ADE/HARNESS_README.md) — hook gate, `ade-*` Cursor bridges, sentinel agent 25. Sync: `scripts/sync_agents_to_ade.ps1` · verify: `python ADE/harness/verify_ade_harness.py` · bridges: `python ADE/sync_ade_swarm_to_cursor.py`.

## “One command” roadmap

See [`docs/ASS_ADE_FORGE_CLI.md`](docs/ASS_ADE_FORGE_CLI.md) — dispatcher sketch over the merged `ass-ade` CLI.

## United CLI (one venv, co-install)

```text
pip install -e .[dev]     # from repository root; spine is defined in root pyproject.toml
ass-ade doctor
ass-ade assimilate PRIMARY_REPO OUTPUT_PARENT --also SIBLING1 --also SIBLING2
ass-ade book rebuild ...
ass-ade --help
atomadic --help
```

[`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md)
