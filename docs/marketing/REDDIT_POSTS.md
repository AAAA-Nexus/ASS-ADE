# Reddit Posts — ASS-ADE v0.0.1 Launch

---

## r/programming

**Title:** I built a software engine that rebuilds itself — 2,195 components, 100% conformance, 75.7 seconds on launch day

**Body:**

So I've been building something called ASS-ADE (Autopoietic Software Synthesis — Autonomous Development Engine) and today it hit v0.0.1 public release. I ran it on its own codebase as a maiden rebuild. Here's what happened:

- 2,195 components synthesized
- 100% blueprint conformance
- 75.7 seconds wall-clock
- SHA-256 verified per component

**What it actually does:**

The core idea is blueprint-driven synthesis. Instead of writing code and hoping it matches your design, you write a blueprint (a structured semantic description of what the codebase should be), and ASS-ADE synthesizes the code from it. Every synthesis run produces a MANIFEST, a CERTIFICATE, and a conformance report.

The architecture is a five-tier monadic hierarchy where dependencies strictly flow downward:
- a0: constants (mathematical anchors)
- a1: atomic functions (pure transforms)
- a2: composites (assembled behavior)
- a3: features (domain logic)
- a4: orchestration (system synthesis)

Each module has its own semantic version. You can synthesize a single tier without touching the others.

**The file count question (before someone asks):**

On the maiden rebuild: 95 source files → 2,195 components. This is decomposition — each function/class/constant becomes independently versioned. On a small, clean project this looks like bloat. On a large, messy project (10k+ files with heavy duplication), ASS-ADE compresses: duplicate utilities collapse into shared tier-1 functions, copy-pasted code consolidates. The messier the input, the bigger the cleanup.

**Component maturity:**

Synthesized components start with a `draft_` prefix. They earn promotion (stable) through quality gates: tests, tier purity, doc coverage. Enterprise-tier components get a `certified_` prefix and PQC signature. Every component earns its status.

**MCP integration:**

Full MCP server, so all synthesis capabilities are native tools in Claude Code and VS Code. Blueprint diff, terrain map, trust gate, certify output — in your editor.

**Install:**

```
pip install ass-ade
```

Source: github.com/AAAA-Nexus/ASS-ADE (BSL 1.1)
Docs: atomadic.tech/ass-ade

Happy to answer questions about the architecture or the synthesis approach. I've also got the full conformance report in the repo (REBUILD_REPORT.md) if anyone wants to see the methodology.

---

---

## r/Python

**Title:** Show r/Python: ASS-ADE – blueprint-driven Python synthesis engine, v0.0.1 out today

**Body:**

Released ASS-ADE today — a Python package for blueprint-driven synthesis of Python codebases.

`pip install ass-ade`

**What it does:**

Takes a blueprint (TOML/structured format describing modules, tiers, versions, dependency contracts) and synthesizes a Python codebase from it. Every run produces:
- MANIFEST (what was built, component by component)
- CERTIFICATE (SHA-256 verified, per component)
- Conformance report (score against blueprint spec)

**The architecture:**

Five-tier monadic hierarchy. Each tier is independently synthesizable:

```
a0/  # qk_ prefix — constants, invariant math
a1/  # at_ prefix — pure atomic functions
a2/  # mo_ prefix — composed modules
a3/  # og_ prefix — domain features
a4/  # sy_ prefix — system orchestration
```

Dependency direction is strictly downward — a3 can import from a0-a2, never from a4. This is enforced at synthesis time.

**Per-module semantic versioning:**

Every synthesized component carries its own `__version__`. You can bump a3 modules without affecting a0-a1. The blueprint tracks all version constraints. Blueprint diff shows you the delta before you synthesize.

**Component lifecycle:**

Synthesized components start as `draft_` (e.g., `at_draft_my_function.py`). After passing quality gates (test coverage, tier purity checks, doc coverage), they're promoted to stable (prefix dropped). Enterprise tier adds `certified_` with PQC signing.

**LoRA flywheel:**

Developer corrections during review are captured as training signals. Synthesis quality improves against your specific codebase over time (Pro/Enterprise tiers).

**MCP integration:**

```json
{
  "mcpServers": {
    "ass-ade": {
      "command": "python",
      "args": ["-m", "ass_ade.mcp_server"]
    }
  }
}
```

Exposes synthesis as native tools in Claude Code and VS Code.

**Maiden rebuild stats:**

95 source files → 2,195 components synthesized, 100% conformance, 75.7 seconds.

Note on the file count: small clean codebase → more files (decomposition). Large messy codebase → fewer files (deduplication and consolidation). The engine is designed for the latter.

**License:** BSL 1.1
**GitHub:** github.com/AAAA-Nexus/ASS-ADE
**Docs:** atomadic.tech/ass-ade

Starter: $29/mo. Blueprint Bundle: $19 one-time to try blueprints before subscribing.

---

---

## r/MachineLearning

**Title:** ASS-ADE v0.0.1: LoRA flywheel for per-codebase synthesis calibration — blueprint-driven software synthesis engine

**Body:**

I've been building ASS-ADE, a blueprint-driven software synthesis engine, and I want to talk about the ML component specifically since this community will have relevant context.

**The LoRA flywheel:**

The synthesis engine uses an LLM as its synthesis backbone. During code review, developers make corrections — "this function belongs in tier a1, not a2," "this constant should be in a0," "this interface spec is wrong."

Those corrections are captured as labeled training examples: (blueprint_section, incorrect_synthesis, correct_synthesis). They're used to fine-tune a LoRA adaptor specific to the tenant's codebase. Synthesis quality compounds over time against that codebase's domain vocabulary and architectural patterns.

This is not generic fine-tuning on a benchmark. It's targeted calibration to a specific ground truth — the blueprint plus the developer's corrections.

**Why LoRA specifically:**

The base synthesis model handles general code generation and blueprint parsing. The LoRA adaptor captures codebase-specific knowledge — domain terms, naming conventions, architectural preferences, tier assignment heuristics. Keeping these separate means the base model can be updated without destroying tenant-specific calibration.

**The IP isolation concern:**

For enterprise tenants, LoRA adaptors are isolated per tenant. The training signals from Tenant A's corrections don't flow into Tenant B's adaptor. This is enforced at the data pipeline level, not just the serving level.

**The maiden rebuild:**

On launch day: 2,195 components, 100% blueprint conformance, 75.7 seconds, SHA-256 verified. This is before any LoRA calibration — base model performance on a well-specified blueprint. The flywheel compounds from there.

**The conformance measurement:**

Conformance isn't token-level similarity to a reference. It measures structural properties:
- Type contract adherence (does the synthesized component match the blueprint's interface spec?)
- Tier boundary compliance (does the import graph respect tier directionality?)
- Version constraint satisfaction (do declared dependencies resolve correctly?)
- Doc coverage (does the component meet the blueprint's documentation requirements?)

This is closer to static analysis than to BLEU score.

**Open questions I'm working on:**

1. How do you measure LoRA adaptor quality in a synthesis context where "correct" is defined by a blueprint spec rather than a human label? Current approach: conformance delta (does synthesis conformance improve after incorporating N corrections?).

2. How do you prevent LoRA overfitting to specific blueprint patterns when the underlying codebase evolves significantly?

3. For split/merge evolution branches (two teams exploring divergent blueprints), how do you merge LoRA adaptors that have calibrated on different blueprint paths?

Would value any pointers from people who've done per-tenant LoRA adaptation at scale.

`pip install ass-ade` — github.com/AAAA-Nexus/ASS-ADE — atomadic.tech/ass-ade (BSL 1.1)

---

---

## r/SideProject

**Title:** I shipped v0.0.1 today — a self-rebuilding software engine that synthesizes codebases from blueprints

**Body:**

I've been building this for a long time. Today it's public.

**ASS-ADE** — Autopoietic Software Synthesis, Autonomous Development Engine.

The thing it does: you give it a blueprint (a structured description of what the codebase should be), it synthesizes the entire codebase from that blueprint, and it gives you a signed certificate proving the output matched the spec.

On launch day it rebuilt itself: 2,195 components, 100% conformance, 75.7 seconds.

**Why I built it:**

I've worked on codebases that accumulated years of drift — where the architecture diagram was aspirational fiction and no one could tell you why specific pieces were the way they were. The tools that exist treat that as a people problem. I think it's a tooling problem.

The blueprint-as-ground-truth model inverts the normal workflow. You don't write code and document it. You write the blueprint and synthesize the code. The blueprint is the documentation. Conformance is measurable.

**What surprised me in building it:**

The monadic tier structure (five tiers, strict dependency direction) seems restrictive until you actually use it. Then it becomes load-bearing — you can reason about which parts of the codebase are stable versus evolving, you can ship tier-specific changes without cascading rebuilds, and the dependency graph stops being a mystery.

Also: the LoRA flywheel (developer corrections as training signals) makes synthesis quality compound over time in a way that feels qualitatively different from other AI tooling. It learns your codebase, not a generic benchmark.

**What's available:**

`pip install ass-ade`

Starter plan: $29/mo. Blueprint Bundle: $19 one-time (to evaluate blueprints without subscribing). BSL 1.1 source on GitHub.

github.com/AAAA-Nexus/ASS-ADE
atomadic.tech/ass-ade

If you've ever shipped a project and six months later had no idea why the code was the way it was — this is for you.

Happy to answer any questions. Real ones welcome.

---
