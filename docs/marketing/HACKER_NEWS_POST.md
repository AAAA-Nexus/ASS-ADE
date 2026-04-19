# Hacker News — ASS-ADE v0.0.1 Launch

---

## Show HN Post

**Title:**
Show HN: ASS-ADE – a software engine that rebuilds itself (2,139 components, 99.8% conformance, 75.7s)

**Body:**

ASS-ADE (Autopoietic Software Synthesis – Autonomous Development Engine) is a blueprint-driven synthesis engine I've been building. Today it rebuilt its own codebase on launch day: 2,139 components, 99.8% blueprint conformance, 75.7 seconds, SHA-256 verified per component.

The core idea: the blueprint is the canonical truth, the code is a synthesized artifact. Every synthesis run produces a MANIFEST (what was built), a CERTIFICATE (cryptographic proof), and a conformance score. You can diff two blueprints before synthesizing. You can roll back to any prior blueprint state. You can open parallel evolution branches, synthesize both, and merge the winner.

Architecture is a five-tier monadic hierarchy: a0 (constants) → a1 (functions) → a2 (composites) → a3 (features) → a4 (orchestration). Dependencies flow strictly downward. Each module carries its own semantic version. You can synthesize one tier without touching the others.

Two things that surprised me in practice:

1. For small, clean codebases, synthesis decomposes into more files (each component is independently versioned). For large, messy codebases, it compresses — duplicate utilities collapse, copy-pasted code consolidates into reusable tier-1 components. The rebuild of our small source (95 files) produced 2,139 components. The same engine on a 10,000-file enterprise codebase tends to produce fewer, cleaner components.

2. The `draft_` prefix in synthesized components is intentional — first-generation components earn promotion to stable and eventually `certified_` through quality gates (tests, tier purity, doc coverage). Every component earns its status through the pipeline.

There's a full MCP server, so synthesis capabilities are native tools in Claude Code and VS Code. A LoRA flywheel captures developer corrections as training signals; synthesis quality compounds over time against your specific codebase.

BSL 1.1. Install: `pip install ass-ade`. GitHub: github.com/AAAA-Nexus/ASS-ADE. Docs: atomadic.tech/ass-ade.

Happy to answer questions about the architecture, the synthesis approach, the conformance measurement methodology, or the failure cases.

---

## Prepared Responses

---

### Response to: "What does 'autopoietic' mean here?"

Autopoiesis is the biological property of self-producing, self-maintaining systems. A cell doesn't just exist — it continuously reconstructs its own components and maintains its structural integrity.

Applied to software: ASS-ADE can reconstruct the full codebase from its blueprint without any component persisting from a prior run. The output on run N doesn't depend on the output from run N-1 — it depends only on the blueprint. Conformance is measured by comparing the synthesis output to the blueprint spec, not to prior runs.

This is meaningful for two reasons: drift detection (you can tell if a manually-edited file has diverged from blueprint) and reproducibility (given the same blueprint version, you get the same certified output).

---

### Response to: "95 files → 2,139 components sounds like decomposition bloat"

This is the right question to ask.

The decomposition effect is by design: every function, class, and constant becomes its own independently versioned module. For a small, clean codebase, the overhead outweighs the benefit — you get more files, each tracked separately.

For a large, messy codebase — 10,000+ files with significant duplication, utilities that live in 12 different places, copy-pasted helpers everywhere — the direction inverts. Duplicate functions collapse into single shared tier-1 components. Copy-pasted code consolidates. What was 10,000 messy files becomes 3,000 clean, properly-tiered components.

ASS-ADE's value scales with codebase complexity. The maiden rebuild was a proof of mechanism on a small input. The target use case is the large, drifted enterprise codebase.

---

### Response to: "What's the difference between this and LLM code generation?"

Code generators produce output once. They don't track it, don't certify it, and don't maintain a relationship between the output and a persistent specification.

ASS-ADE has a different model: every synthesis event is tied to a blueprint version. You can see what changed between blueprints, what components were affected, and what the conformance delta was. The output isn't just code — it's a certified artifact with provenance.

The LLM-generated output problem in production is precisely this: you have code, but you don't know its relationship to intent. ASS-ADE tries to make that relationship explicit and measurable.

---

### Response to: "What's BSL 1.1? Is this open source?"

BSL 1.1 (Business Source License) is source-available but not open source by the OSI definition.

The source is public and readable. Use for personal projects, internal tooling, and evaluation is free. Commercial use in hosted services or resale requires a commercial license (that's the paid tier).

The conversion clause: BSL 1.1 includes a provision where the code converts to a permissive open-source license after a specified period. Our conversion is to Apache 2.0.

---

### Response to: "What does 99.8% conformance actually measure?"

Each synthesized component is evaluated against its blueprint specification along four axes:

1. **Type contracts** — does the component expose the interface the blueprint declares?
2. **Dependency constraints** — does the component's import graph respect tier boundaries?
3. **Version constraints** — does the component version satisfy declared dependencies?
4. **Doc coverage** — does the component meet the blueprint's documentation requirements?

Conformance = (components passing all four checks) / (total components). 99.8% on 2,139 components means approximately 4-5 components had minor spec deviations — these are logged in the conformance report with their specific failure reasons.

The full conformance report is in REBUILD_REPORT.md in the repository if you want to see the actual methodology.

---

### Response to: "Why not just use contract testing or property-based testing?"

These are complementary, not alternatives.

Contract testing verifies behavioral contracts at runtime. Property-based testing explores behavioral edge cases. Both are excellent and we use both.

ASS-ADE addresses structural conformance — whether the codebase *is* what the design says it should be, independent of behavior. A component can pass all its tests and still violate tier boundaries, import from a higher tier, or carry a version that doesn't satisfy its declared dependency contract.

You can have 100% test coverage on a codebase that's completely drifted from its architectural intent. ASS-ADE closes that gap.

---

### Response to: "What's the LoRA flywheel?"

During synthesis review, developers make corrections — "this function should be in a1, not a2," "this constant belongs in a0," "this interface is wrong." Those corrections get captured as labeled training examples.

Over time, the synthesis engine is fine-tuned on those corrections for your specific codebase. Quality compounds — not on generic benchmarks, but against your domain vocabulary and your architectural patterns.

This is per-tenant on Pro and Enterprise tiers. The fine-tuning stays in your environment.

---

### Response to: "What's the `draft_` prefix?"

First-generation components from synthesis carry a `draft_` prefix — e.g., `draft_rebuild_codebase.py`. This is intentional.

Components earn promotion through quality gates: test coverage, tier purity checks, doc coverage. A `draft_` component is functional but hasn't passed the full gate yet. Promoted components lose the prefix and become stable. Enterprise-certified components get a `certified_` prefix and carry a PQC signature.

This gives users a clear signal of maturity level at the file name. If you see `draft_`, you know it's first-generation synthesis output. If you see the bare name, it's been verified. If you see `certified_`, it's been through the enterprise compliance pipeline.

---

### Response to: "How does the trust gate work for the community tier?"

The community tier is a blueprint-sharing network gated by reputation score.

Score is earned through: synthesis runs (proof of use), contributions that others certify as high-conformance, corrections that improve community blueprints. It's not purchasable.

Why gate it: blueprints are operational artifacts. A low-quality blueprint will produce low-quality synthesis. The gate ensures that shared blueprints carry signal about their author's synthesis track record.

Early members get founding-cohort status, which means their verification history counts double for 90 days. This is how we seed the reputation pool without requiring years of activity.

---

### Response to: "What's the IP Guard?"

For enterprise tenants, IP Guard provides three guarantees:

1. Blueprint artifacts are stored in a tenant-isolated namespace — no blueprint content crosses organizational boundaries
2. LoRA adaptors are trained per-tenant — your corrections don't improve synthesis for other customers
3. Every synthesis event is logged with input blueprint hash, output component hashes, and conformance score — full audit trail

The concern IP Guard addresses: "if my team uses AI synthesis, does my proprietary code end up improving the model for competitors?" The answer with IP Guard is no.

---
