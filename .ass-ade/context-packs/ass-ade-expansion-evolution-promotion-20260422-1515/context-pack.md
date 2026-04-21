# Context pack — ASS-ADE expansion / evolution / promotion

## Intent

Support **bounded** enhancement of ASS-ADE through three coordinated lanes—**expansion** (technical surface under monadic + MCP parity law), **evolution** (roadmap, logs, governance), and **promotion** (contributor and public narrative grounded in tests and CI). This pack was assembled for the user request combined with `/ato-plan` and `/context-pack` command structure.

## Repo map summary (Lane L)

- **Monadic law:** `.ass-ade/tier-map.json` classifies `src/ass_ade/` modules into `a0`–`a4`; new code must extend this map, not bypass it.
- **MAP = TERRAIN index:** `.ass-ade/terrain-index.v0.json` lists canonical artifacts (MCP manifest, autonomous graphs, context-pack gate, demos).
- **MCP surface:** `mcp/server.json` is the public contract; `tests/test_mcp_manifest_parity.py` prevents registry drift.
- **Local preflight:** `scripts/atomadic_dev_harness.py` (`--quick` / `--full`) and `AGENTS.md` pointers.
- **Pre-write gate:** `scripts/context_pack_gate.py` (see `terrain-index`).

## Web research summary (Lane W)

- **MCP specification (latest):** JSON-RPC-based protocol; servers expose **tools**, **resources**, and **prompts**; hosts must obtain consent before tool invocation; tool descriptions from untrusted servers should be treated as untrusted. Source: [modelcontextprotocol.io/specification/latest](https://modelcontextprotocol.io/specification/latest).
- **Hop 1b — corpus / governance motivation:** arXiv:2603.23802 analyzes a large sample of public MCP tools and highlights growth in **action** tools and regulatory relevance at the **tool layer**. Use for **risk framing**, not as reproduced in-repo statistics. Source: [arxiv.org/abs/2603.23802](https://arxiv.org/abs/2603.23802).

## Tech docs summary (Lane T)

- **Project:** `ass-ade` Python package, `requires-python >= 3.11`, Typer CLI, Pydantic v2, httpx — see `pyproject.toml` in repo root.
- **Testing:** `pytest` with `dev` optional extras.

## Risks and gaps

- Confirm **which repository** hosts canonical GitHub Actions before embedding run URLs in outward copy.
- Roadmap phase **hosted MCP parity** remains aspirational until smoke evidence exists.

## Next edits (for dev agent)

1. Execute **ato-plan `T1`** (`@recon-swarm-orchestrator`): refresh gap list against `mcp/server.json` and `tests/test_mcp_extended.py` tool names.
2. Pick **one** expansion slice (E1) with manifest + tests in a single PR.
3. Append **roadmap `growthNotes`** only with a path or CI reference.
4. Run `python scripts/atomadic_dev_harness.py --quick` before handoff.

## Handoff

Attach this file and `context-pack.json` to implementation tasks. For monadic implementation after coding starts, prefer **`/ass`** mode per project norms.

## Pack verdict

**PASS** — pack is internally consistent, repo-anchored, and cites retrieved external sources without claiming unverified benchmark numbers.
