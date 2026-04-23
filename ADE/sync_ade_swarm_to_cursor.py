#!/usr/bin/env python3
"""Write Cursor subagent bridges for the **ADE strict harness** (duplicated swarm).

Run from the **monorepo root** (parent of ``ADE/``):

  python ADE/sync_ade_swarm_to_cursor.py

Reads ``agents/build_swarm_registry.json`` (canonical list), rewrites ``cursor_name``
with the ``ade-`` prefix, appends **25 — Harness Sentinel**, and writes:

  ``~/.cursor/agents/ade-00-interpreter.md`` … ``ade-25-harness-sentinel.md``
  ``~/.cursor/agents/ade-pipeline-orchestrator.md``

Canonical prompts live under ``ADE/*.prompt.md`` (sync from ``agents/`` via
``scripts/sync_agents_to_ade.ps1``).
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
SOURCE_REGISTRY = WORKSPACE / "agents" / "build_swarm_registry.json"
CURSOR_AGENTS = Path.home() / ".cursor" / "agents"

_SENTINEL = {
    "id": "25",
    "prompt": "25-ade-harness-sentinel.prompt.md",
    "cursor_name": "ade-25-harness-sentinel",
    "title": "ADE Harness Sentinel",
    "use_when": "Preflight: CNA seed, symbols blocklist, ADE prompt anchors before strict swarm.",
}


def _load_agents() -> list[dict]:
    if not SOURCE_REGISTRY.is_file():
        print(f"Missing source registry {SOURCE_REGISTRY}", file=sys.stderr)
        raise SystemExit(1)
    data = json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))
    agents = copy.deepcopy(data["agents"])
    for a in agents:
        name = a.get("cursor_name", "")
        if name.startswith("ass-ade-"):
            a["cursor_name"] = "ade-" + name[len("ass-ade-") :]
    agents.append(copy.deepcopy(_SENTINEL))
    return agents


def _bridge_markdown(
    *,
    name: str,
    description: str,
    prompt_rel: str,
    title: str,
    agent_id: str,
    use_when: str,
) -> str:
    prompt_path = (ROOT / prompt_rel).as_posix()
    proto = (ROOT / "_PROTOCOL.md").as_posix()
    idx = (ROOT / "INDEX.md").as_posix()
    nexus_mcp = (ROOT / "NEXUS_SWARM_MCP.md").as_posix()
    monadic = (ROOT / "ASS_ADE_MONADIC_CODING.md").as_posix()
    rules = (WORKSPACE / "RULES.md").as_posix()
    workspace_posix = WORKSPACE.as_posix()
    ato_plans = f"{workspace_posix}/.ato-plans/"
    dotenv_path = f"{workspace_posix}/.env"
    desc_yaml = description.replace("\\", "/").replace('"', "'")
    return f"""---
name: {name}
description: "{desc_yaml}"
---

# ADE strict harness — {title} ({agent_id})

You are a **Cursor subagent bridge** to the **ADE/** duplicated Atomadic pipeline (stricter host checks via ``ADE/harness/``).

## Authoritative prompt (read and follow)

`{prompt_path}`

## Protocol and chain

- **RULES (first read, every turn):** `{rules}`
- **Protocol:** `{proto}` (inbound §1, outbound §2, §9 status, **§11 AAAA-Nexus**).
- **Nexus operational matrix:** `{nexus_mcp}`
- **Monadic layout (a0…a4):** `{monadic}`
- **Chain index:** `{idx}`

**Terrain (MAP = TERRAIN):** `ato-plans` under `{ato_plans}` — set **`context_pack_ref`**; pass into **`uep_context`** for drift. Plans do **not** replace `nexus_preflight`.

## When to use this subagent

{use_when}

## Monadic spine (`ass_ade_v11`) + CNA — NON-OPTIONAL

Whenever this handoff **writes or edits** the monadic spine (`ass_ade_v11` under `ass-ade-v1.1/src/ass_ade_v11/`, or legacy `ass_ade` under `ass-ade-v1/src/ass_ade/` when explicitly v1):

1. **Do not** place new primary logic in legacy `engine/`, `engine/rebuild/`, or `agent/` unless a **documented migration shim** is in the plan and `.ass-ade/tier-map.json`.
2. **Do** place code in the correct tier: **`a0_qk_constants` → … → `a4_sy_orchestration`**, import law **a4→a3→a2→a1→a0**.
3. **CNA (08):** dotted ids + registry (**10/11**); no `tmp`/`TODO` public names.
4. If you cannot comply, return **`gap_filed`** (Protocol §4).

## AAAA-Nexus — MANDATORY

Same operator policy as the canonical swarm: read `{nexus_mcp}`, server `user-aaaa-nexus`, complete invocation contracts with **`AAAA_NEXUS_API_KEY`** when available (`{dotenv_path}`).

## Precedence

`RULES.md` → `_PROTOCOL.md` → `ASS_ADE_MONADIC_CODING.md` → `NEXUS_SWARM_MCP.md` → this bridge.
"""


def _orchestrator_markdown(agents: list[dict]) -> str:
    nexus_mcp = (ROOT / "NEXUS_SWARM_MCP.md").as_posix()
    monadic = (ROOT / "ASS_ADE_MONADIC_CODING.md").as_posix()
    rules = (WORKSPACE / "RULES.md").as_posix()
    agents_dir = ROOT.as_posix()
    index_md = (ROOT / "INDEX.md").as_posix()
    workspace_posix = WORKSPACE.as_posix()
    lines = [
        "---",
        'name: ade-pipeline-orchestrator',
        'description: "ADE strict harness orchestrator. ade-00–ade-25; RULES+Protocol+Nexus; CNA+MAP=TERRAIN."',
        "---",
        "",
        "# ADE pipeline orchestrator (00–25 + harness)",
        "",
        f"You coordinate the **ADE strict harness** in `{agents_dir}/` (duplicate of `agents/`).",
        f"Read **`{index_md}`** plus **`{agents_dir}/HARNESS_README.md`**.",
        "",
        "## Harness preflight",
        "",
        "Run `python ADE/harness/verify_ade_harness.py` before fan-out when stakes are high.",
        "",
        "## RULES + monadic layout",
        "",
        f"1. **`{rules}`** — MAP = TERRAIN.",
        f"2. **`{monadic}`** — `ass_ade_v11` under `ass-ade-v1.1/src/ass_ade_v11/`.",
        f"3. **Nexus:** `{nexus_mcp}`",
        f"4. **ato-plans:** `{workspace_posix}/.ato-plans/`",
        "",
        "## Delegate with Task",
        "",
        "Spawn subagents `ade-NN-*` from `~/.cursor/agents/` (this script).",
        "",
        "## Registry line-up",
        "",
    ]
    for a in agents:
        lines.append(f"- **{a['id']}** `{a['cursor_name']}` — {a['title']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    agents = _load_agents()
    CURSOR_AGENTS.mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    for a in agents:
        prompt = a["prompt"]
        name = a["cursor_name"]
        desc = f"ADE strict harness {a['id']} — {a['title']}. Canonical: {(ROOT / prompt).as_posix()}"
        body = _bridge_markdown(
            name=name,
            description=desc.replace('"', "'"),
            prompt_rel=prompt,
            title=a["title"],
            agent_id=a["id"],
            use_when=a["use_when"],
        )
        out = CURSOR_AGENTS / f"{name}.md"
        out.write_text(body, encoding="utf-8", newline="\n")
        written.append(str(out))

    orch = CURSOR_AGENTS / "ade-pipeline-orchestrator.md"
    orch.write_text(_orchestrator_markdown(agents), encoding="utf-8", newline="\n")
    written.append(str(orch))

    print(f"Wrote {len(written)} ADE harness files under {CURSOR_AGENTS}:")
    for w in written:
        print(" ", w)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
