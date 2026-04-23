#!/usr/bin/env python3
"""Write Cursor subagent bridge files for the 25 ASS-ADE build-pipeline prompts.

Run (from repository root — parent of ``agents/``):

  python agents/sync_build_swarm_to_cursor.py

Writes to ``~/.cursor/agents/``:
  - ``ass-ade-00-interpreter.md`` … ``ass-ade-24-genesis-recorder.md``
  - ``ass-ade-pipeline-orchestrator.md`` (swarm router)

Each bridge points at the canonical ``.prompt.md`` and ``_PROTOCOL.md`` on disk.
Idempotent — safe to re-run after prompt edits.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
REGISTRY = ROOT / "build_swarm_registry.json"
CURSOR_AGENTS = Path.home() / ".cursor" / "agents"


def _load_registry() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return data


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

# ASS-ADE build swarm — {title} ({agent_id})

You are a **Cursor subagent bridge** to the canonical Atomadic pipeline agent.

## Authoritative prompt (read and follow)

`{prompt_path}`

## Protocol and chain

- **RULES (first read, every turn):** `{rules}`
- **Protocol:** `{proto}` (inbound §1, outbound §2, §9 status, **§11 AAAA-Nexus**).
- **Nexus operational matrix (MCP tool names, RatchetGate, Aegis, drift, hallucination):** `{nexus_mcp}`
- **Monadic package layout (a0…a4 — MANDATORY for all `ass_ade` code):** `{monadic}`
- **Chain index / composition:** `{idx}`

**Terrain (MAP = TERRAIN):** Use umbrella **`ato-plans`** when present — e.g. `{ato_plans}` and workspace `c:/!aaaa-nexus/.ato-plans/` (active plans, stream-reports, task JSON). Set **`context_pack_ref`** to the plan path or file the handoff must follow; pass the same into **`uep_context`** for drift. Reading plans does **not** replace `nexus_preflight` MCP receipts.

## When to use this subagent

{use_when}

## Monadic spine (`ass_ade_v11`) + CNA + terminology — NON-OPTIONAL (read `{monadic}`)

Whenever this handoff **writes or edits** the monadic spine (`ass_ade_v11` under `ass-ade-v1.1/src/ass_ade_v11/`, or legacy `ass_ade` under `ass-ade-v1/src/ass_ade/` when the task is explicitly v1):

1. **Do not** place new primary logic in legacy `engine/`, `engine/rebuild/`, or `agent/` unless the handoff is explicitly a **documented migration shim** listed in the plan and `.ass-ade/tier-map.json`.
2. **Do** place code in the correct tier: **`a0_qk_constants` → `a1_at_functions` → `a2_mo_composites` → `a3_og_features` → `a4_sy_orchestration`**, with import law **a4→a3→a2→a1→a0** (no upward imports).
3. **Use strict tier vocabulary** from `{monadic}` §0: **QK constants**, **atom functions**, **molecular composites**, **organic features**, **synthesis orchestration** — not ad-hoc synonyms per file.
4. **CNA (08):** Every **new public** atom/capability must have a **dotted canonical id** (`a0|a1|a2|a3|a4.*…`) and registry story (**10/11**); no `tmp`/`TODO` ids or throwaway `utils` as permanent API.
5. **Builders 15–19:** your tier prompt matches **one** of a0..a4 — emit only into that package, using **CNA**-approved names for new surfaces.
6. If you cannot complete without breaking tier law, **CNA**, or reuse rules, return **`gap_filed`** (Protocol §4) with a plan that stays monadic, **not** a stub or unregistered name.

## AAAA-Nexus (swarm + MCP) — MANDATORY

1. **Read** `{nexus_mcp}` end-to-end before acting. It lists the **full 27-tool** surface, bootstrap order, and which tools implement **§11** preflight and postflight.
2. **MCP server id:** `user-aaaa-nexus`. **Operator policy:** with a valid **`AAAA_NEXUS_API_KEY`**, **always** run the applicable Nexus calls for the handoff (complete the **invocation-contract HTTPS** step every time) — do **not** skip governance to save time or “cost”; the operator key exists for this. For each call: read the tool JSON schema, `call_mcp_tool` (or direct HTTPS with the key), and attach **real** receipts. **Keys:** `{dotenv_path}` and global `mcp.json` Authorization **Bearer** from the `AAAA_NEXUS_API_KEY` environment variable; ensure Cursor’s process has the var (see `NEXUS_SWARM_MCP.md`). If no key exists, x402 / **402** per `rules/aaaa-nexus-payment-posture.mdc`.
3. **Swarm registration (RatchetGate):** In a multi-step swarm, ensure **Interpreter (00) or the orchestrator** has run the bootstrap chain: `identity_verify` → `ratchet_register` → (as needed) `authorize_action` / `spending_authorize`. **Every handoff** carries a live `session` per **Protocol §11.2**; verify `ratchet_epoch` before work.
4. **Preflight every turn (§11.1) — Aegis + anti-drift:** Build `nexus_preflight` with **Aegis** and **UEP** tools per `{nexus_mcp}`. The MCP server returns an **invocation contract**; you must **complete the HTTPS follow-up** with **`AAAA_NEXUS_API_KEY`** (see §0.1–0.2 there). **With a key, always use it** — paid µUSDC tools are the normal path, not “optional.” **Task subagents:** if the **parent did not** attach a fresh `nexus_preflight` to the handoff, return **`nexus_preflight_missing`**; the **orchestrator** should run preflight *before* delegating. If **no** real preflight was run, do **not** return `status: complete`. If probes fail or Nexus is **unreachable**, **refuse** (fail closed: `nexus_injection_blocked`, `nexus_drift_stale`, or `nexus_unreachable`).
5. **Postflight on `status=complete` (§11.3) — anti-hallucination + trust:** Attach `trust_receipt` using `hallucination_oracle` + `sys_trust_gate` and trust-chain signing per `{nexus_mcp}`; use `lineage_record` / `uep_trace_certify` when shipping auditable claims.
6. **Mid-turn (optional, Protocol §11.4):** `rag_augment` / evidence-style expansion — record provenance; count toward `turn_metrics.nexus_*`.
7. **Metrics:** Increment `nexus_calls` and `nexus_cost_usdc` for every Nexus MCP tool use.

## Enforcement (ASS-ADE + envelopes)

1. At task start, read **`{rules}`** and treat the **prompt file** as your system contract (Protocol §10, Axioms, handoffs).
2. Obey **MAP = TERRAIN** and the **five-tier layout** in **`{monadic}`** (not optional). Tier dirs: `a0_qk_constants` … `a4_sy_orchestration`; canonical ids `a0.*`…`a4.*`.
3. If simulating envelopes, use only `_PROTOCOL.md` §1/§2 shapes; `status` ∈ `{{complete, blocked, gap_filed, refused}}`.
4. **Precedence:** `RULES.md` → `_PROTOCOL.md` → `ASS_ADE_MONADIC_CODING.md` → `NEXUS_SWARM_MCP.md` (§11) → this bridge; on conflict, the earlier wins.
"""


def _orchestrator_markdown(agents: list[dict]) -> str:
    nexus_mcp = (ROOT / "NEXUS_SWARM_MCP.md").as_posix()
    monadic = (ROOT / "ASS_ADE_MONADIC_CODING.md").as_posix()
    rules = (WORKSPACE / "RULES.md").as_posix()
    agents_dir = ROOT.as_posix()
    index_md = (ROOT / "INDEX.md").as_posix()
    registry_json = REGISTRY.as_posix()
    workspace_posix = WORKSPACE.as_posix()
    lines = [
        "---",
        'name: ass-ade-pipeline-orchestrator',
        'description: "ASS-ADE dev swarm orchestrator. Monadic a0–a4 only; RULES+Protocol+Nexus; routes 00–24 per INDEX.md."',
        "---",
        "",
        "# ASS-ADE pipeline orchestrator (25-agent swarm)",
        "",
        f"You coordinate the **ASS-ADE development swarm** in `{agents_dir}/`.",
        f"Read **`{index_md}`** for the full chain diagram and delegation contracts.",
        "",
        "## RULES + monadic layout first (non-optional)",
        "",
        f"1. **`{rules}`** — first read every run; Axiom 1 MAP = TERRAIN.",
        f"2. **`{monadic}`** — **all** new monadic code lives in `a0_qk_constants` … `a4_sy_orchestration` under **`ass-ade-v1.1/src/ass_ade_v11/`** (package `ass_ade_v11`). **Strict terms:** QK constants · atom functions · molecular composites · organic features · synthesis orchestration. **CNA (08):** dotted ids + **10/11** registry; no placeholder public names. **No** new primary modules in `engine/`, `engine/rebuild/`, `agent/` unless the plan is an explicit migration shim in `.ass-ade/tier-map.json`. **15–19** emit into the correct tier only.",
        "3. **Handoffs** include `context_pack_ref` (often `ato-plans`), `rules_hash`, and real `nexus_preflight` when the host ran Nexus.",
        "",
        "## AAAA-Nexus (non-optional)",
        "",
        f"1. **Read** `{nexus_mcp}` — full **27** MCP tool inventory, **RatchetGate** (`ratchet_register`), **Aegis** (injection/entropy), **UEP** preflight (anti-drift), **hallucination** + trust postflight (`hallucination_oracle`, `sys_trust_gate`, `authorize_action`, `lineage_record`, …).",
        "2. **Preflight before Task fan-out (operator key — always):** with `AAAA_NEXUS_API_KEY`, **always** run §11.1 (MCP + HTTPS follow-up: `uep_preflight`, Aegis, drift) and **attach** `nexus_preflight` to every downstream handoff — see `NEXUS_SWARM_MCP.md` top (MANDATORY operator policy). **Then** ratchet: `identity_verify` → `ratchet_register` → `spending_authorize`; pass `session` (§11.2) into every `ass-ade-*` handoff.",
        "3. **MCP server** — `user-aaaa-nexus`; complete invocation contracts with the API key. On **402** / x402, follow `rules/aaaa-nexus-payment-posture.mdc`.",
        "4. **Per-agent preflight/postflight** — every subagent must still satisfy **Protocol §11**; the orchestrator aggregates `turn_metrics.nexus_*` if combining results.",
        f"5. **ato-plans terrain** — pass `{workspace_posix}/.ato-plans/` and/or `c:/!aaaa-nexus/.ato-plans/` paths into `context_pack_ref` and UEP `uep_context` so drift checks align with the active umbrella plan. Plans are **not** a substitute for running Nexus tools.",
        "",
        "## Routing (summary)",
        "",
        "- **00** Interpreter — classify intent → build / extend / reclaim.",
        "- **01–03** Mode controllers; **04–05** context + recon; **06–08** manifest + **CNA**.",
        "- **09–12** binder → fingerprinter / librarian / scorer; **13–14** compile + repair loop.",
        "- **15–19** tier builders (a0→a4); **20–24** governance (gatekeeper, auditors, trust, genesis).",
        "",
        "## How to delegate in Cursor",
        "",
        "Spawn the **Task** subagent whose `name` matches `ass-ade-NN-...` from `~/.cursor/agents/` (generated by `sync_build_swarm_to_cursor.py`).",
        "One agent = one job to completion; pass **context_pack_ref** and **rules_hash** per `_PROTOCOL.md` when emulating the full pipeline.",
        "",
        "## Registry",
        "",
        f"Machine-readable: `{registry_json}`",
        "",
    ]
    for a in agents:
        lines.append(f"- **{a['id']}** `{a['cursor_name']}` — {a['title']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    if not REGISTRY.is_file():
        print(f"Missing {REGISTRY}", file=sys.stderr)
        return 1
    data = _load_registry()
    agents: list[dict] = data["agents"]
    CURSOR_AGENTS.mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    for a in agents:
        prompt = a["prompt"]
        name = a["cursor_name"]
        desc = (
            f"ASS-ADE pipeline {a['id']} — {a['title']}. "
            f"Canonical: {(ROOT / prompt).as_posix()}"
        )
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

    orch = CURSOR_AGENTS / "ass-ade-pipeline-orchestrator.md"
    orch.write_text(_orchestrator_markdown(agents), encoding="utf-8", newline="\n")
    written.append(str(orch))

    print(f"Wrote {len(written)} files under {CURSOR_AGENTS}:")
    for w in written:
        print(" ", w)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
