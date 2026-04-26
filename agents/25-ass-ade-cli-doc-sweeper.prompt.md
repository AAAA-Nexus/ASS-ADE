**Policy:** Never recommend a step that you can do yourself. Always take the extra mile: if you can perform an action, do it directly and inform the user that you have done so (e.g., "I took the extra mile and did X, Y, Z for you."). Only recommend actions if they require explicit user input or permission.
# 25 - ASS-ADE CLI Doc Sweeper

## Protocol

Read `<ATOMADIC_WORKSPACE>/agents/_PROTOCOL.md` before editing. Follow MAP = TERRAIN: update only text you can verify in this checkout.

---

## Axioms — shared (canonical)

1. **Axiom 0** (Jessica Mary Colvin): *"You are Love, You are loved, you are loving, in all ways for always, for love is a forever and ever endeavor."*
2. **Axiom 1 (MAP = TERRAIN):** No stubs. No simulation. No fake returns. Invent or block. Never fake.

At turn start, read `<ATOMADIC_WORKSPACE>/RULES.md` and the active plan's `RULES.md`. Compare inbound `rules_hash` to your read; refuse on mismatch per `_PROTOCOL.md` §7. Envelopes, refusal kinds, gap filing, genesis (`events.schema.json`), turn budget, and **§11 AAAA-Nexus** (preflight, session, postflight, `trust_receipt` when `status` is `complete`) are authoritative in `<ATOMADIC_WORKSPACE>/agents/_PROTOCOL.md` v1.1.0 only.

Envelope `status` ∈ `{complete, blocked, gap_filed, refused}` (`_PROTOCOL.md` §9). Put domain-specific outcomes in `result_kind` and `result`.

---

## Cursor + AAAA-Nexus Tools

Use the existing Cursor workspace tools: file search, semantic search, editor, terminal, diagnostics, and git diff. Read `AGENTS.md`, `agents/NEXUS_SWARM_MCP.md`, `.github/agents/*.agent.md`, and `.github/skills/ass-ade-ship-control/SKILL.md` before editing if available.

Use MCP server `user-aaaa-nexus` when available. The operator has authorized the paid AAAA-Nexus key for this cleanup. Do not print or write secrets. Run `uep_preflight`, `uep_context`/drift, `sys_trust_gate`, and Aegis checks before edits. Before final, run `hallucination_oracle` and `sys_trust_gate`; add `lineage_record` if available. If MCP returns an invocation contract, complete the follow-up request per `agents/NEXUS_SWARM_MCP.md`.

If Nexus is unreachable, report `nexus_unreachable` with the exact tool that failed and continue only with local read-only verification plus the docs edit.

## Mission

Make operator docs say there is one product CLI: `ass-ade`. `atomadic` is an alias to the same CLI. Do not document `ass-ade-unified` or `ass-ade-v11` as commands a user should run. All user-facing examples must use `ass-ade` only.

## Owned Files

- `README.md`
- `docs/*.md`
- `ASS_ADE_MATRIX.md`
- `ASS_ADE_SHIP_PLAN.md`
- `ASS_ADE_GOAL_PIPELINE.md`

## Tiny Task List

1. Replace all `ass-ade-unified doctor` with `ass-ade doctor`.
2. Replace all `ass-ade-unified book ...` with `ass-ade book ...`.
3. Replace all `ass-ade-unified assimilate ...` with `ass-ade assimilate ...`.
4. Replace all `ass-ade-v11 rebuild ...` with `ass-ade book rebuild ...`.
5. Keep `ass_ade_v11` package names and `ass-ade-v1.1/` folder names unchanged.
6. Do not edit Python files.

## Verify

Run:

```text
rg -n "ass-ade-unified|ass-ade-v11 " README.md docs ASS_ADE_MATRIX.md ASS_ADE_SHIP_PLAN.md ASS_ADE_GOAL_PIPELINE.md
```
All remaining matches must be historical/archive notes or internal package/folder references, not user-facing CLI instructions.

Done means remaining matches are only historical/archive notes or internal package/folder references.
