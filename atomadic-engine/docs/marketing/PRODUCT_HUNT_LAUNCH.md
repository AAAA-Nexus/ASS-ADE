# Product Hunt Launch — ASS-ADE v0.0.1

---

## Listing Details

**Name:** ASS-ADE

**Tagline:** The software engine that rebuilds itself — blueprint-driven synthesis with SHA-256 certified output

**Short Description (under 150 chars):**
Blueprint-driven synthesis engine. Rebuilt 2,195 components at 100% conformance in 75.7s on launch day. pip install ass-ade.

---

## Full Description

ASS-ADE is a software synthesis engine that treats your codebase as an artifact of a blueprint — not the other way around.

Most codebases drift. The architecture diagram says one thing; the running system does another. Teams patch around it, document around it, and eventually live with it. ASS-ADE closes the gap structurally.

**How it works:**

You describe what your codebase should be — its modules, tiers, dependency contracts, semantic versions — in a blueprint. ASS-ADE synthesizes the codebase from that blueprint, verifies every component against its specification, and produces a signed certificate. The blueprint is the canonical truth. The code is the artifact.

**On launch day, ASS-ADE rebuilt its own codebase:**
- 2,195 components synthesized
- 100% blueprint conformance
- 75.7 seconds end-to-end
- SHA-256 verified on every output

This is what we mean by "autopoietic" — the system produces and maintains itself.

**Five-tier monadic architecture:**
- a0: Constants (invariant anchors)
- a1: Functions (pure transforms)
- a2: Composites (assembled behavior)
- a3: Features (domain logic)
- a4: Orchestration (system synthesis)

Dependencies flow strictly downward. Every module is independently versioned. You can synthesize a single tier without touching the others.

**Key capabilities:**
- Blueprint-driven synthesis with per-synthesis MANIFEST and CERTIFICATE
- Split/merge evolution branches (parallel architectural experiments, merge the winner)
- LoRA training flywheel (developer corrections improve synthesis quality over time)
- IP Guard for enterprise (tenant-isolated blueprints and training)
- Full MCP integration for Claude Code and VS Code

**The file count question:** On small clean codebases, synthesis decomposes code into more independently-versioned components (95 files → 2,195 components). On large, messy codebases, it compresses — duplicate utilities collapse into reusable tier-1 functions, copy-pasted code consolidates. The messier the input, the bigger the cleanup. ASS-ADE's value scales with codebase complexity.

**Install:** `pip install ass-ade`

**Pricing:**
- Starter: $29/month
- Pro: $99/month
- Enterprise: $499/month
- Blueprint Bundle: $19 one-time (try blueprints before subscribing)
- Prompt Pack: $9 one-time

Open source under BSL 1.1.

---

## Gallery / Media Captions

**Image 1 (hero):** "Maiden rebuild: 2,195 components · 100% conformance · 75.7 seconds"
Caption: The ASS-ADE engine rebuilt its own codebase on launch day. Every output SHA-256 verified.

**Image 2 (architecture diagram):** "Five-tier monadic architecture"
Caption: a0→a1→a2→a3→a4. Dependencies flow downward. Each module independently versioned.

**Image 3 (certificate):** "Every synthesis produces a certificate"
Caption: MANIFEST + CERTIFICATE + conformance report. Blueprint-to-code provenance on every run.

**Image 4 (MCP integration):** "Native tools in Claude Code and VS Code"
Caption: Full MCP server. synthesis capabilities in your editor.

**Image 5 (evolution branches):** "Split/merge evolution"
Caption: Open parallel blueprint paths. Synthesize both. Merge the winner.

---

## Maker Comment

Hi Product Hunt 👋

I'm Thomas from Atomadic Tech. We shipped ASS-ADE today — and I want to be direct about what it actually is, because the name and the concept are both a bit unusual.

**What it is:** A software synthesis engine. You describe what your codebase should be in a blueprint. It builds the codebase from that blueprint, certifies the output, and tracks every change. Blueprint is truth. Code is artifact.

**Why we built it:** Architecture drift is one of the most expensive problems in software engineering that nobody measures. Teams spend enormous amounts of time understanding why code is the way it is before they can change it. We think that's a tooling problem, not a people problem.

**The maiden rebuild:** We ran the engine on itself on launch day. 2,195 components, 100% conformance, 75.7 seconds. Every output SHA-256 verified. We have the certificate. This is the benchmark we hold ourselves to.

**The file count thing:** This will probably come up — when you run synthesis on a small, clean project, you get more files (each component independently versioned). On a large, messy codebase, you get fewer — duplicates collapse, utilities consolidate. We designed it for the latter: large, drifted codebases where the cleanup is worth the decomposition overhead.

**MCP integration:** If you use Claude Code or VS Code with Cline, ASS-ADE plugs in as a native toolset. Blueprint ops without leaving your editor.

Happy to answer any questions about the architecture, the synthesis approach, the LoRA flywheel, or why we called it what we called it. All fair game.

— Thomas
atomadic.tech/ass-ade

---

## FAQ

**Q: What's "autopoietic" mean?**
The biological term for a system that produces and maintains itself. A cell continuously rebuilds its components. ASS-ADE does the same for software — synthesis from blueprint, verification, certification, on every run. The name is intentional.

**Q: Is this just another code generator?**
Code generators produce output once. ASS-ADE produces output continuously, tracks it, certifies it, and evolves it. The difference is provenance: every synthesis event is tied to a specific blueprint version, a specific set of components, a specific conformance score. You can audit the history. You can diff any two builds. You can roll back.

**Q: 95 files → 2,195 components sounds like bloat. What gives?**
For small, clean codebases, synthesis decomposes into more independently-versioned components (that's the point — each module is independently versioned and tracked). For large, messy codebases, the direction inverts: duplicate functions collapse, copy-pasted helpers consolidate, tangled dependencies get resolved into clean tier relationships. ASS-ADE's value scales with codebase complexity. If your codebase has 10,000+ files with significant duplication, expect fewer components out, not more.

**Q: What does "blueprint conformance 100%" mean exactly?**
Each synthesized component is evaluated against its blueprint specification — type contracts, dependency declarations, tier constraints, version constraints. Conformance measures how many components met all their specifications. 100% means every one of the 2,195 components passed all checks — zero deviations. The full audit log is in REBUILD_REPORT.md in the repository.

**Q: Is the source code available?**
Yes — github.com/AAAA-Nexus/ASS-ADE under BSL 1.1. BSL means it's source-available and free for individual and internal use; commercial resale or hosting-as-a-service requires a commercial license.

**Q: What's IP Guard?**
Enterprise tenants get blueprint artifact isolation, LoRA adaptor isolation, and audit logging. Your synthesis patterns — including what the LoRA flywheel learns from your corrections — stay in your tenant namespace. No cross-contamination between organizations.

**Q: Does it work with any programming language?**
The synthesis engine is language-agnostic at the blueprint level. Current synthesis backends target Python; additional language backends are on the roadmap.

**Q: What's the LoRA flywheel?**
Every correction a developer makes during synthesis review gets captured as a training signal. Over time, the synthesis engine improves against your specific codebase's patterns and domain vocabulary. This is per-tenant on the Pro and Enterprise tiers.

**Q: What's the Blueprint Bundle?**
A $19 one-time purchase of the blueprint toolkit — lets you design and test blueprints without committing to a subscription. Good for evaluating whether the blueprint format works for your codebase before going further.

**Q: Can this run in CI?**
Yes. The synthesis and certification pipeline is fully CLI-driven. You can gate CI on conformance score — require ≥99% conformance before a build passes. This is one of the target use cases.

---
