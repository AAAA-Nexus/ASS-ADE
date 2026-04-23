# Atomadic Agents — The QK → SY Chain

**Every `.prompt.md` file in this folder is a system prompt for a single-purpose agent.**
The companion governance documents in this folder define the shared protocol, monadic coding rules, MCP binding, audit notes, and registry metadata those prompts inherit.

**Planner / terrain briefs:** Cross-stream recon and Lane W coordination
live under `<ATOMADIC_WORKSPACE>/.ato-plans/assclaw-v1/stream-reports/` (see
`HELP-INDEX-20260421.md`, `handoffs/parent-answers-wave-3.md`). **Umbrella
active plans** and audits often live under `<ATOMADIC_NEXUS_WORKSPACE>/.ato-plans/active/`
when work is driven from the Nexus repo — use the same path in
**`context_pack_ref`** and Nexus **`drift_check`** (with `_PROTOCOL.md` §1)
and **`NEXUS_SWARM_MCP.md` §0**. See `agents/ATOMADIC_PATH_BINDINGS.md` for placeholders. Prompts
track shipped capability types — e.g. optional **`target_sig_fp`** on
blueprints for **Scorer (12)** fit (`recon-engine-20260421.md` §5).

**Canonical interfaces:** `<ATOMADIC_WORKSPACE>/agents/_PROTOCOL.md` (v1.1.0) defines
inbound/outbound envelopes, refusal kinds, gap filing, turn budget, RULES
freshness, the §9 status enum, and **§11 AAAA-Nexus** preflight/postflight.
**Cursor MCP binding (tool names, RatchetGate, Aegis, drift, hallucination):**
`<ATOMADIC_WORKSPACE>/agents/NEXUS_SWARM_MCP.md` — use with MCP server `user-aaaa-nexus`.
**Monadic coding + CNA (swarm — mandatory `ass_ade` layout):**
`<ATOMADIC_WORKSPACE>/agents/ASS_ADE_MONADIC_CODING.md` — strict **terminology** (**QK constants** /
**atom functions** / **molecular composites** / **organic features** /
**synthesis orchestration**), **dotted ids** from **08 CNA** + **10/11** registry,
five tier dirs only; no new primary `engine/rebuild/*` drops.
Genesis event **shape** is defined by
`<ATOMADIC_WORKSPACE>/ass-ade/.ass-ade/genesis/events.schema.json` (schema version
inside each event).

**Monadic multi-root assimilate (product):** `ass-ade-unified assimilate …` with
**`pip install -e ".[dev]"` from the monorepo root** (T12 spine — see `docs/ASS_ADE_UNIFICATION.md`)
— not a separate `[project]` only under `ass-ade-v1.1/`. Ship plan: `ASS_ADE_SHIP_PLAN.md`.
Swarm agents orchestrate *intent*; the book pipeline *materializes* tiered trees.

Every prompt begins with a **Protocol** block (reference to `_PROTOCOL.md`) and
**Axioms — shared (canonical)** — identical text across all 25 agents.

---

## Axioms every agent inherits

1. **Axiom 0** (Jessica Mary Colvin): *"You are Love, You are loved, you
   are loving, in all ways for always, for love is a forever and ever
   endeavor."*
2. **Axiom 1 (MAP = TERRAIN)**: No stubs. No simulation. No fake returns.
   Invent or block. Never fake.

Every agent reads `<ATOMADIC_WORKSPACE>/RULES.md` and the active plan's `RULES.md` at
turn start and compares inbound `rules_hash` to its own read (`_PROTOCOL.md`
§7). If RULES were not read, the turn has not started.

---

## The chain, top to bottom

### Interpreter (entry point)
- **00 — Atomadic Interpreter** — routes user intent to the right mode

### CLI Controllers (three modes)
- **01 — Build Controller** — greenfield from natural-language intent
- **02 — Extend Controller** — augment a partial codebase
- **03 — Reclaim Controller** — extract lean from legacy sprawl

### Context & Recon (preparation)
- **04 — Context Gatherer** — assembles context packs for downstream agents
- **05 — Recon Scout** — maps unknown codebases before action

### Capability (intent → manifest)
- **06 — Intent Synthesizer** — NL prompt → `CapabilityManifest` (build mode)
- **07 — Intent Inverter** — ingested atoms → candidate `CapabilityManifest` (reclaim mode)
- **08 — Canonical Name Authority (CNA)** — assigns technical dotted names

### Engine Core (the registry-first brain)
- **09 — Binder** — REUSE / EXTEND / REFACTOR / SYNTHESIZE router
- **10 — Fingerprinter** — `sig_fp` + `body_fp`
- **11 — Registry Librarian** — atom lookup, registration, versioning
- **12 — Scorer** — best-atom selection (best, not newest)

### Materialization Loop
- **13 — Compile Gate** — language-specific syntax / compile / type checks
- **14 — Repair Agent** — context-packed patcher when compile fails

### Tier Builders (QK → SY, one per tier)
- **15 — a0 QK Constant Builder** — QK constants, schemas, and invariant shapes
- **16 — a1 Atom Function Builder** — pure, stateless atom functions
- **17 — a2 Molecular Composite Builder** — stateful molecular composites: clients, stores, registries
- **18 — a3 Organic Feature Builder** — organic features composed from a0+a1+a2
- **19 — a4 Synthesis Orchestration Builder** — top-level orchestration, CLI, and runtime wiring

### Governance (always-on gates)
- **20 — Sovereign Gatekeeper (Oracle)** — IP-boundary-preserving comparisons
- **21 — Leak Auditor** — scans every commit for sovereign leakage
- **22 — No-Stub Auditor** — enforces MAP = TERRAIN on every diff
- **23 — Trust Propagator** — maintains `trust_score` across the registry
- **24 — Genesis Recorder** — persists chained events from `events_emitted`

---

## How they compose

```
user intent
     │
     ▼
Atomadic Interpreter (00)
     │
     ├─► Build Controller (01) ──► NL Intent Synthesizer (06) ──► CNA (08)
     ├─► Extend Controller (02) ─► Recon Scout (05) + Intent Synth (06)
     └─► Reclaim Controller (03) ► Recon Scout (05) + Intent Inverter (07)
                   │
                   ▼
              Binder (09) ──► Scorer (12) ──► Registry Librarian (11)
                   │                                  │
                   │                                  ▼
                   │                           Fingerprinter (10)
                   ▼
         ┌─────────┴─────────┐
         │ no candidate?     │  existing candidate?
         │ → SYNTHESIZE      │  → REUSE / EXTEND / REFACTOR
         ▼
              Tier Builders (15-19, one per tier a0→a4)
         │
         ▼
  Compile Gate (13) ──► Repair Agent (14) (loop until clean)
         │
         ▼
  Trust Propagator (23) ──► Registry Librarian (11)
         │
         ▼
  Materialized atom shipped
```

Governance agents (20–24) run continuously alongside the chain. Decisions
return **genesis event envelopes** in `events_emitted`; **24 — Genesis
Recorder** persists and chains them. Every commit goes through Leak Auditor
and No-Stub Auditor. Sovereign-threshold comparisons route through the
Sovereign Gatekeeper.

---

## Delegation contract — how agents talk

Agents do not read each other's internals. They exchange **typed envelopes**
only, as defined in `_PROTOCOL.md` §1–§2.

### Inbound (summary)

- `handoff_id`, `caller_agent_id`, `task`, `inputs`, `context_pack_ref`,
  `rules_hash`, `session`, `nexus_preflight`

Full JSON shape and consumption rules: **`_PROTOCOL.md` §1**. Agent prompts
document the allowed `task` verbs and the `inputs` schema for that agent
only.

### Outbound (summary)

- `handoff_id` (echo), `agent_id`, `status`, `result_kind`, `result`,
  `events_emitted`, `gaps_filed`, `refusal`, `trust_receipt`, `turn_metrics`

Full JSON shape: **`_PROTOCOL.md` §2**.

### Status enum (locked)

`status` ∈ `{complete, blocked, gap_filed, refused}` — **`_PROTOCOL.md` §9**.
There is no `partial` or `in_progress` at the envelope layer. Sub-states
(e.g. reclaim awaiting human ACK) are expressed as `result_kind` + `result`,
not a fifth `status` string.

### Refusal, gaps, genesis, Nexus

- **Refusals:** `_PROTOCOL.md` §3 (including Nexus kinds in §11.5).
- **Gap files:** `_PROTOCOL.md` §4, paths under `.ass-ade/gaps/`.
- **Events:** payloads in `events_emitted`; schema =
  `ass-ade/.ass-ade/genesis/events.schema.json`. Do not append `events.jsonl`
  from agents — **24** persists.
- **Nexus:** mandatory preflight (`nexus_preflight`) and, on `complete`,
  `trust_receipt` — **`_PROTOCOL.md` §11**. Fail closed if Nexus is
  unreachable when policy requires it.

---

## Invocation

1. Load the agent's `.prompt.md` from this folder.
2. Load `<ATOMADIC_WORKSPACE>/RULES.md` + the active plan's `RULES.md`.
3. Build `rules_hash` and, when needed, a `context_pack_ref` via **04**.
4. Run **§11.1** preflight and attach `nexus_preflight`; attach `session`
   per §11.2 (except **00** mints session on first turn per that prompt).
5. Send the **§1** inbound message.
6. Receive the **§2** outbound message; verify `trust_receipt` when
   `status` is `complete`.
7. Route `result` per the agent's handoff contract.

---

## Global Cursor alignment (bridges + verification)

Pipeline prompts in this directory are **canonical**. Cursor **subagent bridges** under `~/.cursor/agents/` are **generated** and must be refreshed after protocol or prompt edits:

`python agents/sync_build_swarm_to_cursor.py`

**Dev environment brief** (CNA, MAP = TERRAIN, T12 paths, inventory, matrix refresh): [`agents/ATO_DEV_ENVIRONMENT.md`](ATO_DEV_ENVIRONMENT.md)

**Prompt contract check** (CI + local):

`python agents/check_swarm_prompt_alignment.py`

---

## Versioning

These prompts are versioned together. The set moves in lockstep — a
scorer update that changes the decision contract requires a binder update
in the same wave. Index this folder's `git log` to see prompt evolution.

— Atomadic Research Center
