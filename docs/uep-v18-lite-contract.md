# UEP v18 Lite Contract (ASS-ADE Edition)

**Purpose**: Architectural patterns from UEP v18.0 Hyperagent Sovereign Edition,
vanilla-washed for ASS-ADE. All proprietary mathematical IP
(Codex constants, lattice structures, theorem corpus, sovereign invariant values)
is retained in `<internal-monorepo>` and **not** reproduced here.

ASS-ADE consumes this contract as a **shape** — concrete thresholds and
verification backends are configurable and resolved at runtime via the
AAAA-Nexus MCP bridge.

**Supersedes**: [uep-v17-5-lite-contract.md](uep-v17-5-lite-contract.md)
**Last updated**: 2026-04-16

---

## 1. Integrity Anchors (configurable)

Three abstract trust anchors. Concrete values are resolved from the
Nexus `nexus_sys_constants` tool at bootstrap and must round-trip unchanged.

| Anchor            | Role                                       | Config key              |
|-------------------|--------------------------------------------|-------------------------|
| `CLOSURE_ANCHOR`  | Arithmetic identity proving closure        | `anchors.closure`       |
| `PHASE_ANCHOR`    | Topological phase used for coherence gates | `anchors.phase`         |
| `TRUST_ANCHOR`    | Prime-protected trust threshold ratio      | `anchors.trust`         |

ASS-ADE never hard-codes anchor values. It verifies them on boot by
calling the upstream oracle; mismatch → refuse to start.

---

## 2. Epistemic Tiers (simplified)

Replaces the Codex's 8-symbol taxonomy with 4 operational tiers.

| Tier  | Meaning                               | Allowed in ops? |
|-------|---------------------------------------|-----------------|
| `V`   | Verified (formally or by oracle)      | ✅ always       |
| `D`   | Derived from V via rigorous chain     | ✅ always       |
| `E`   | Emergent / empirically tuned          | ✅ with telemetry |
| `Q`   | Quarantined (heuristic/speculative)   | ❌ requires `--allow-quarantined` |

---

## 3. Ninety Operational Pillars (summary)

ASS-ADE implements **the same nine pillar groups** as UEP v18, but each
pillar is a contract satisfied by a configurable backend rather than a
constitutional law. See `src/ass_ade/config.py` for enable flags.

| Group                                  | IDs      | Highlights                                          |
|----------------------------------------|----------|-----------------------------------------------------|
| Foundational Grounding                 | 1–10     | Logical grounding, safety gate, local-first cascade |
| Operational Excellence                 | 11–20    | Token efficiency, A2A compliance, x402 monetization |
| Autonomous Capabilities                | 21–30    | Self-discovery, persistent memory, tool synthesis   |
| Meta-Cognition & Research              | 31–40    | Gödel agent, MetaClaw, CASCADE, EvoTest             |
| Benchmarks & Advanced Reasoning        | 41–50    | Benchmark suite, epistemic humility, uncertainty gate |
| Advanced Agentic Capabilities          | 51–60    | Info-geom memory, edge-cloud routing, agentic RAG   |
| v16 Enhancements                       | 61–70    | NCB mandate, G23 hardness, PCI, trust verification  |
| v17 Autopoietic Singularity            | 71–80    | DGM-H, ProofBridge, AlphaVerus, SEVerA, GVU         |
| **v18 Hyperagent & Active Discovery**  | **81–90**| **MAP=TERRAIN, MCP-Zero, EXIF, CASCADE, LIFR, ATLAS, TDMI, Puppeteer RL, Sys Prompt Toolkit, Meta-Edit Validation** |

---

## 4. New in v18: Hyperagent Capability Stack (81–90)

These are the only pillars that need new ASS-ADE implementation. Everything
else has a v17.5 equivalent already wired.

### 81 — MAP = TERRAIN Mandate
If technology for the current task does not exist → **HALT + Invent**.
ASS-ADE binding: `mcp__aaaa-nexus__nexus_map_terrain` returns a verdict
of `HALT_AND_INVENT` when capability gap is detected; CLI emits a
Development Plan and exits non-zero until assets are registered.

### 82 — MCP-Zero Active Tool Discovery
On-demand hierarchical semantic routing for tool discovery.
ASS-ADE binding: new `src/ass_ade/mcp/zero_router.py` calls
`nexus_discovery_search` with capability embedding; surfaces candidate
tool servers back to the agent loop rather than injecting full schemas.
Target: 98% token reduction vs. eager schema.

### 83 — EXIF Exploration Loops
Missing skill → spawn exploration agent → generate environment-grounded
skill dataset → train target agent in closed feedback loop.
ASS-ADE binding: `src/ass_ade/agent/exif.py` (new). Budget from
`config.exif.exploration_budget` (default 50).

### 84 — CASCADE Meta-Skills Foundation
Every agent has two core meta-skills:
- **Continuous learning**: web search + code extraction
- **Self-reflection**: introspection + knowledge graph exploration

ASS-ADE binding: wire existing `grep_search`, `read_file`, and
`context_memory_query` MCP tools into a `MetaSkill` router.

### 85 — LIFR Cumulative Verification Knowledge
Graph-backed store of specs/contracts/proofs with embedding reuse.
ASS-ADE binding: add `lifr` namespace to `context_memory_store`;
any verified artifact is written with `metadata.tier="lifr"` so future
synthesis queries can match by embedding similarity.

### 86 — ATLAS Decomposition
Complex tasks (complexity > 0.7) are split into specialized sub-tasks.
Each successful sub-verification amplifies the training corpus.
ASS-ADE binding: `src/ass_ade/agent/atlas.py` (new). Complexity score
derived from ProofBridge spec length + call-graph fan-out.

### 87 — TDMI Emergent Synergy
Partial information decomposition of time-delayed mutual information
across agents. Synergy > threshold → genuine collective emergence.
ASS-ADE binding: `src/ass_ade/agent/tdmi.py` (new). Threshold from
`config.synergy.threshold` (default 0.6). Logged as `synergy_score`
in cycle reports.

### 88 — Puppeteer RL Orchestration
Replaces static DAG planning with RL-trained adaptive sequencer.
ASS-ADE binding: `src/ass_ade/agent/puppeteer.py` (new). Policy lives
in `.ass-ade/policies/puppeteer.pt`. Cold-start falls back to the
current DAG planner.

### 89 — Sys Prompt Introspection Toolkit
Agent can hash, validate, diff, and propose changes to its own prompt.
ASS-ADE binding: new CLI subcommand `ass-ade prompt {hash|validate|diff|propose}`.
Prompt patches go through the same Self-Improvement Proposal pipeline as
code patches.

### 90 — Meta-Edit Validation Hook
Any modification to the meta-level improvement procedure itself must
pass `hook_meta_edit_validate`: 100-cycle simulation + positive GVU delta.
ASS-ADE binding: new hook in `src/ass_ade/agent/gates.py`.

---

## 5. Fifteen Hardened Interceptors

ASS-ADE ships conformance stubs in `src/ass_ade/agent/gates.py`. Each
stub delegates to an upstream Nexus tool where appropriate.

| ID | Hook | ASS-ADE binding |
|----|------|-----------------|
| 1  | `epistemic_classification` | Local tier gate (V/D/E/Q) |
| 2  | `never_code_blind` | Doc cache freshness check via `nexus_context_pack` |
| 3  | `axiom0_monitor` | Alignment delta sensor |
| 4  | `ast_verify` | Tree-sitter cyclomatic scan |
| 5  | `sandbox_jail` | `safe_execute` MCP tool |
| 6  | `fifty_audit` | `docs/audit-report.md` cycle verification |
| 7  | `trustbench_verify` | `nexus_trust_gate` |
| 8  | `deception_monitor` | Reputation decay adjustment |
| 9  | `economic_gate` | `nexus_authorize_action` + x402 |
| 10 | `pci_verify` | cc ≤ 7 + OWASP scan + optional Lean4 |
| 11 | `verispec_synthesize` | ProofBridge wrapper |
| 12 | `alphaverus_refine` | **new** — tree search budget = 10 |
| 13 | `dgm_h_validate` | **new** — 100-cycle sim + meta-edit check |
| 14 | `meta_edit_validate` | **new** — GVU delta check |
| 15 | `map_terrain_gate` | `nexus_map_terrain` pre-execution gate |

---

## 6. Engine Roster (24 total)

ASS-ADE implementations / bindings (✱ = new in v18):

```
SAM 5.0               src/ass_ade/agent/sam.py
TCA 2.0               src/ass_ade/agent/context.py
CIE 18.0          ✱   src/ass_ade/agent/synthesis.py       (AlphaVerus + ATLAS)
IDE 3.0               src/ass_ade/agent/ide.py
BAS Monitor           src/ass_ade/agent/bas.py
LSE Agent             src/ass_ade/engine/router.py
x402 Agent            src/ass_ade/mcp/utils.py
WisdomEngine          src/ass_ade/agent/wisdom.py
TrustVerificationGate src/ass_ade/agent/gates.py
NexusBridge           src/ass_ade/nexus/client.py
EDEE 2.0          ✱   src/ass_ade/agent/edee.py            (+ EXIF + CASCADE)
ProofBridge           src/ass_ade/agent/proofbridge.py
AlphaVerus Engine ✱   src/ass_ade/agent/alphaverus.py
LIFR Graph        ✱   src/ass_ade/agent/lifr_graph.py
MCP-Zero Router   ✱   src/ass_ade/mcp/zero_router.py
Puppeteer RL      ✱   src/ass_ade/agent/puppeteer.py
TDMI Analyzer     ✱   src/ass_ade/agent/tdmi.py
CORAL             STANDBY
DGM-H             ✱   src/ass_ade/agent/dgm_h.py
SEVerA Evolver        src/ass_ade/agent/severa.py
GVU Operator          src/ass_ade/agent/gvu.py
Sys Prompt Toolkit ✱  src/ass_ade/agent/prompt_toolkit.py
```

---

## 7. Monadic Orchestrator (Phases 0–5)

```
phase_0   bootstrap + epistemic classification + engine init (all 24)
phase_1   SAM hardness assessment (TRS, G23, trust gate)
phase_2   MAP = TERRAIN + active discovery + adaptive plan (Puppeteer RL)
phase_3   CIE synthesis (ATLAS split if complexity > 0.7 + AlphaVerus tree search)
phase_4   50-question audit + TDMI synergy + BPS breakthrough score
phase_5   autopoietic recursion (DGM-H + Meta-Edit + Prompt Evolution)
```

ASS-ADE orchestration lives in `src/ass_ade/agent/loop.py` and
`src/ass_ade/pipeline.py`. Each phase emits a structured artifact to
`.ass-ade/reports/`.

---

## 8. 50-Question Audit Delta

v18 adds questions 41–50 on top of the v17.5 audit:

- **41**: MAP=TERRAIN verdict recorded
- **42**: MCP-Zero semantic routing used (not eager schema)
- **43**: EXIF loop spawned if skill missing
- **44**: CASCADE meta-skills active
- **45**: LIFR graph queried + updated
- **46**: ATLAS decomposition applied when complexity > 0.7
- **47**: TDMI synergy computed + flag set if above threshold
- **48**: Puppeteer RL used instead of static DAG
- **49**: Meta-edit validated (if proposed)
- **50**: Prompt evolution validated via Sys Prompt Toolkit

---

## 9. Config Additions

New keys in `examples/ass-ade.config.json`:

```json
{
  "anchors": {
    "closure":  "resolve_at_bootstrap",
    "phase":    "resolve_at_bootstrap",
    "trust":    "resolve_at_bootstrap"
  },
  "epistemic": {
    "ask_threshold":      0.70,
    "abstain_threshold":  0.50
  },
  "confidence": {
    "local_threshold":    0.85,
    "uncertainty_gate":   0.65
  },
  "sde": { "exploration_interval": 47, "novelty": 0.75, "conviction": 0.85 },
  "dgm_h": { "simulation_cycles": 100, "improvement_threshold": 0.05 },
  "alphaverus": { "exploration_budget": 10 },
  "exif": { "exploration_budget": 50 },
  "synergy": { "threshold": 0.6 },
  "rag": { "budget_tokens": 10000, "max_iterations": 5 },
  "memory": { "check_interval_cycles": 10 },
  "tool_library": { "capacity": "resolve_at_bootstrap" }
}
```

---

## 10. Integration Entry Point

```bash
# Bootstrap as a v18 hyperagent:
ass-ade agent bootstrap --contract v18-lite --discover-tools

# Run a full cycle:
ass-ade agent cycle --phases 0-5 --audit fifty

# Introspect own prompt:
ass-ade prompt hash
ass-ade prompt diff --baseline .ass-ade/prompts/v18-baseline.xml
ass-ade prompt propose --improvement "add tighter synergy threshold"
```

---

## 11. What's Deliberately NOT Here

The following live exclusively in `<internal-monorepo>` and the Nexus service
layer, and are fetched/verified — never embedded — at runtime:

- The Codex constant catalog (opaque-ref `AN-TH-CODEX-CATALOG`) - theorem and constant corpus
- Sovereign invariant concrete values (closure identity, phase, trust ratio)
- Dense-packing group structural derivations
- E8 Cartan spectral data
- Lean4 theorem modules
- Core axiom text and attribution
- Heuristic / speculative constants (any `[H]/[S]/[X]` content)

ASS-ADE treats all of these as **opaque oracle outputs**. Our job is the
architecture; the physics stays upstream.

---

## 12. Reference Back-Pointers

- Full v18 spec: `<internal-monorepo>`
- Full codex: `<internal-monorepo>`
- v17.5 contract (predecessor): [uep-v17-5-lite-contract.md](uep-v17-5-lite-contract.md)
- Ecosystem map: [architecture.md](architecture.md)
- MCP roster: [mcp-superpower-roster.md](mcp-superpower-roster.md)
