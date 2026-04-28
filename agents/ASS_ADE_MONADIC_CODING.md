# ASS-ADE dev swarm — monadic layout (MANDATORY for all `ass_ade` work)

**Authority order:** `<ATOMADIC_WORKSPACE>/RULES.md` → `<ATOMADIC_WORKSPACE>/agents/_PROTOCOL.md` → this file → each agent’s `.prompt.md` → `<ATOMADIC_WORKSPACE>/agents/INDEX.md`.

If anything conflicts, **RULES** and **\_PROTOCOL** win.

## 0. Standardized terminology (use these words — not ad-hoc synonyms)

These terms are **normative** across specs, registry rows, and code review. They map 1:1 to monadic tiers so **constants**, **functions**, and **composites** stay **composable, swappable, and future-proof** when a3 **organic features** and a4 **synthesis orchestration** are built on top.

| Term | Tier | Meaning |
|------|------|---------|
| **QK (quark) constants** | a0 | Immutable values, enums, type aliases, static configuration shapes — **no** executable logic, **no** I/O |
| **Atom functions** | a1 | Pure, stateless, deterministic **atoms** of behavior: same inputs → same outputs; testable in isolation |
| **Molecular composites** | a2 | **Stateful** building blocks: clients, registries, caches, sessions — **composable** behind explicit interfaces; **no** end-user “feature” surface and **no** CLI |
| **Organic features** | a3 | **Feature**: a coordinated capability built from atoms + molecules (library / domain API), still **not** a process entrypoint |
| **Synthesis orchestration** | a4 | **Orchestration** entry: CLI, long-running loop, or top-level orchestration that wires a3 and below |

**Do not** mix vocabulary (e.g. do not call an a2 class a “service object” in one file and “composite” in another — use **molecular composite** or the concrete type name). **Do not** use marketing or product names inside canonical ids (CNA).
These exact labels must appear in agent titles, registry metadata, bridge descriptions, review notes, and generated build reports whenever they refer to a0-a4. Singular builder forms that preserve the same tier label, such as `a1 Atom Function Builder` or `a2 Molecular Composite Builder`, are conformant; casual substitutes are not. If you touch a legacy surface that still says `stateful service`, `feature builder`, or `orchestrator builder`, normalize it to the fixed tier label for that tier in the same change.

## 0.1 CNA (Canonical Name Authority) — every swappable unit is named

**CNA** (agent **08**; inputs from **06/07**; checks with **11** Registry Librarian) assigns **dotted technical names** that are **stable forever** at the semantic level: `a0.*`, `a1.*`, `a2.*`, `a3.*`, `a4.*` with a fixed grammar (see **08** prompt, `cna-seed.yaml`, `RULES.md`).

- **No placeholder ids** in shipped code: never `a1.tmp.foo`, `a1.TODO`, or untyped `utils` as a permanent public surface.
- **Module path ↔ id:** Public modules under `src/ass_ade/<tier>_*/` must be **registrable** with a **canonical id** in the same tier. File layout should mirror the **domain.segments** of the id (e.g. `a1.text.parse.line_count` → `a1_at_functions/text/parse/line_count.py` or a single module named by the leaf segment, per repo convention — but **one** id per public atom, not one-off names).
- **Registry alignment:** If an atom is published to the plan/registry (**11**), the **dotted name**, **version**, and **sig_fp** / **body_fp** (**10**) are the source of truth; code changes without registry updates = **drift** (refuse or **gap_filed**).
- **Sovereign / blocklist:** CNA + Gatekeeper rules apply to names; never encode sovereign literals or forbidden domains (**08**, `symbols.txt`).

**Swappability:** Two **a2** implementations of the same **Protocol** (or explicit abstract type) for the same **capability** must share a **stable CNA id** for the *capability*; version bodies via registry, not ad-hoc forks of filenames.

## 1. All new code uses the five tier directories

**Spine package:** `ass_ade` under **`src/ass_ade/`** (tiers `a0_qk_constants` … `a4_sy_orchestration`). This is the canonical ASS-ADE-SEED layout. The table below uses the `ass_ade.*` import root.

Any **new** or **rewritten** Python for ASS-ADE in a greenfield or rebuild must live under the spine `src/` tree in **exactly** these packages (CNA + materializer target layout):

| Tier | Directory | Import root (today → target) | Canonical id prefix | What belongs here |
|------|------------|--------------------------------|---------------------|-------------------|
| **a0** | `a0_qk_constants` | `ass_ade.a0_qk_constants` | `a0.*` | Constants, enums, type aliases, config dataclasses — **no runtime logic** |
| **a1** | `a1_at_functions` | `ass_ade.a1_at_functions` | `a1.*` | **Pure** stateless functions — deterministic, no I/O, no class state |
| **a2** | `a2_mo_composites` | `ass_ade.a2_mo_composites` | `a2.*` | **Stateful** services, clients, registries — no user-facing “feature” and **no** CLI/entrypoint |
| **a3** | `a3_og_features` | `ass_ade.a3_og_features` | `a3.*` | **Features** composed from a1+a2 — still no process-level CLI entry (library-level API) |
| **a4** | `a4_sy_orchestration` | `ass_ade.a4_sy_orchestration` | `a4.*` | **Synthesis orchestration:** Typer/CLI, main loops, app entry, top-level orchestration composition |

**Forbidden for new work (unless an approved migration step says otherwise):**

- Dropping new first-class modules under legacy paths such as `engine/`, `engine/rebuild/`, `agent/`, `commands/` as the **permanent** home of new logic.
- “Hidden” `utils.py` at repo root for production behavior — use a1.
- Stubs, `pass`, or fake returns in production modules (Axiom 1, MAP = TERRAIN).

**Migration shims** (re-exporting from a tier to an old import path) are allowed only when explicitly in the plan; they must re-export **tier-resident** implementations.

## 2. Import law (5-tier, no upward edges)

- **a0** imports: stdlib, third-party only. **Not** a1+.
- **a1** imports: a0, stdlib, third-party.
- **a2** imports: a0, a1, stdlib, third-party.
- **a3** imports: a0, a1, a2, stdlib, third-party.
- **a4** imports: a0…a3, stdlib, third-party.

**Never** import “upward” (e.g. a1 must not import a2). **Never** import a3/a4 from a0–a2.

## 3. Reuse, contracts, and future-proofing

- **a0 (QK):** One **semantic constant**, one name — no duplicate literals scattered across a1+.
- **a1 (atom):** Functions are **side-effect free** and **type-stable**; document inputs/outputs; they are the **reusable** core for every higher tier.
- **a2 (molecular):** Expose **state** only through a **narrow API**; prefer `typing.Protocol` or an ABC for **swap-in** implementations (e.g. another storage backend). **Do not** reach into globals from a1.
- **a3 (organic):** A **feature** depends on a1/a2 only via **constructors** or **injected** interfaces — not hidden singletons — so **features** can be rearranged and tested.
- **a4 (synthesis):** **Orchestrates** only; keeps **wiring** thin so a3 features remain **portable** to other entrypoints (HTTP worker, test harness).

## 4. Repository artifacts

- **`.ass-ade/tier-map.json`:** Every shipped module under the spine `src/ass_ade/**` must be listed with correct tier, reason, and (when applicable) **canonical id** or pointer to the registry row.
- **CNA + registry (08 / 10 / 11):** Dotted ids are assigned under **CNA**; **Fingerprinter** and **Librarian** materialize the registry view. This doc does not duplicate the full grammar; **08** + `cna-seed.yaml` do.

## 5. How pipeline agents use this

- **00–14:** Recon, manifests, plans — outputs must name **CNA targets** (dotted id + tier + file path), not vague paths.
- **08 (CNA):** Assigns the canonical name; no shipping without it for new public surfaces.
- **09–12:** Bind / score using registry identity — **reusability** is impossible without stable names and **fingerprints**.
- **15–19 (builders):** Emit code **only** into the tier package for the handoff, using **CNA** output for public identifiers.
- **20–24:** Enforce: no **placeholder** names; no stubs; tier-map and registry **consistent**.

## 6. Swarm (Cursor) behavior

- **Every** `ass-ade-*` subagent with a handoff that touches `ass_ade` must treat this file as **binding** for **layout + terminology + CNA alignment**.
- If the only way to “finish” is to violate a tier rule, **CNA**, or reuse rules, return **`gap_filed`** (Protocol §4) and describe the **smallest** follow-up, not a stub or throwaway name.

— Atomadic ASS-ADE governance
