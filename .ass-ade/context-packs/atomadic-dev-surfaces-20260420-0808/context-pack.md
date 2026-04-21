# Context pack — Atomadic dev surfaces (memory + evolution + sync)

**Pack:** `.ass-ade/context-packs/atomadic-dev-surfaces-20260420-0808/`  
**Repo root:** `C:/!aaaa-nexus/!ass-ade`  
**Generated:** 2026-04-20 UTC (no trailing user intent after `/context-pack`; scope inferred from recent work).

## Intent

Ship and operate **MAP = TERRAIN**-faithful dev tooling: **trust-scored local vector recall**, **GitHub evolution caps**, **Cursor ↔ Claude two-way suite sync**, without treating roadmap prose as runtime truth.

**Deliverables**

1. Keep `query_vector_memory` **min_score** / `ASS_ADE_MEMORY_MIN_SCORE` behavior tested and MCP/CLI-exposed.  
2. Keep `github_evolution_control.py` + `github-evolution-control.json` aligned with lane workflows.  
3. Re-run `setup_cursor_atomadic.py --two-way` when `atomadic-suite-manifest.json` changes.  
4. Either **add** `scripts/context_pack_gate.py` or **trim** docs that reference it—today the scripts tree has no such file.

## Repo map (Lane L)

- **Tier law:** `.ass-ade/tier-map.json` — `a0` constants through `a4` orchestration; new modules go under `src/ass_ade/` paths registered there.  
- **Context + memory:** `src/ass_ade/context_memory.py` — deterministic hashing vectors; **trust floor** on query; JSONL under `.ass-ade/vector-memory/`.  
- **MCP surface:** `src/ass_ade/mcp/server.py` — `context_memory_query` accepts optional `min_score`.  
- **CLI:** `src/ass_ade/cli.py` — `ass-ade context query … --min-score`.  
- **Evolution gate:** `scripts/github_evolution_control.py`, `.ass-ade/github-evolution-control.json`, `.github/workflows/auto-evolve-cycle.yml` (gate job + evolve job).  
- **Governance handoff:** `.github/workflows/evolution-orchestrate.yml`, `src/ass_ade/local/uep_evolution_orchestrate.py` (neutral naming in artifacts).

**Tests to run before edits**

- `pytest tests/test_recon_context.py`  
- `pytest tests/test_github_evolution_control.py`

## Web research (Lane W)

- **CAG vs RAG (bounded KB):** arXiv **2412.15605** — *Don't Do RAG: When Cache-Augmented Generation Is All You Need for Knowledge Tasks* — use as **design analogy** for “preload stable ASS-ADE slices” vs “vector index for volatile docs”; not a license to stuff entire monorepo into one prompt.  
- **MCP contracts:** Official MCP **2025-11-25** tools spec for JSON-RPC shapes when extending tools.

## Tech docs (Lane T)

- **Pydantic v2** — `VectorMemoryQueryResult` extensions.  
- **Typer** — optional float CLI options.  
- Pin versions from `pyproject.toml` (`pydantic>=2.11,<3`, `typer>=0.15,<1`).

## Risks / gaps

| Risk | Mitigation |
|------|------------|
| Missing `context_pack_gate.py` vs hook docs | Add minimal gate or fix AGENTS/command references. |
| Over-tight `min_score` with hashing vectors | Default `0.0`; use env for machine-wide floor; document. |
| External Cursor sync script | Record path `~/.cursor/atomadic/setup_cursor_atomadic.py` in runbooks. |

## Next edits (suggested order)

1. Confirm whether **Write hook** for context packs is required; if yes, **scaffold** `scripts/context_pack_gate.py` + test.  
2. Any change to **MCP tool schema** → update `tests/test_mcp_*` + `map_terrain` inventory if listed.  
3. After manifest edits outside repo, run **`py -3 %USERPROFILE%\.cursor\atomadic\setup_cursor_atomadic.py --two-way`** and re-open Cursor.

## Pack verdict

**REFINE** — repo terrain is strong for memory + evolution; **documentation / hook parity** for `context_pack_gate` is the gating gap before claiming full `/context-pack` automation.
