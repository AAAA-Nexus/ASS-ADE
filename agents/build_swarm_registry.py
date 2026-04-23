"""
Auto-generated from build_swarm_registry.json on 2026-04-23.
This module provides the agent registry as a Python dict for direct import/use.
"""

BUILD_SWARM_REGISTRY = {
    "_schema": "atomadic/build-swarm/cursor/v1",
    "_description": "Maps ASS-ADE pipeline .prompt.md files to Cursor ~/.cursor/agents/*.md bridge names.",
    "protocol": "<ATOMADIC_WORKSPACE>/agents/_PROTOCOL.md",
    "rules_global": "<ATOMADIC_WORKSPACE>/RULES.md",
    "index": "<ATOMADIC_WORKSPACE>/agents/INDEX.md",
    "agents": [
        {"id": "00", "prompt": "00-atomadic-interpreter.prompt.md", "cursor_name": "ass-ade-00-interpreter", "title": "Atomadic Interpreter", "use_when": "Route user intent to build / extend / reclaim; entry point for the chain."},
        {"id": "01", "prompt": "01-build-controller.prompt.md", "cursor_name": "ass-ade-01-build-controller", "title": "Build Controller", "use_when": "Greenfield: NL intent → working project (build mode)."},
        {"id": "02", "prompt": "02-extend-controller.prompt.md", "cursor_name": "ass-ade-02-extend-controller", "title": "Extend Controller", "use_when": "Augment a partial codebase."},
        {"id": "03", "prompt": "03-reclaim-controller.prompt.md", "cursor_name": "ass-ade-03-reclaim-controller", "title": "Reclaim Controller", "use_when": "Extract lean registry from legacy sprawl."},
        {"id": "04", "prompt": "04-context-gatherer.prompt.md", "cursor_name": "ass-ade-04-context-gatherer", "title": "Context Gatherer", "use_when": "Assemble context packs for downstream agents."},
        {"id": "05", "prompt": "05-recon-scout.prompt.md", "cursor_name": "ass-ade-05-recon-scout", "title": "Recon Scout", "use_when": "Map unknown codebases before action."},
        {"id": "06", "prompt": "06-intent-synthesizer.prompt.md", "cursor_name": "ass-ade-06-intent-synthesizer", "title": "Intent Synthesizer", "use_when": "NL → CapabilityManifest (build)."},
        {"id": "07", "prompt": "07-intent-inverter.prompt.md", "cursor_name": "ass-ade-07-intent-inverter", "title": "Intent Inverter", "use_when": "Atoms → candidate CapabilityManifest (reclaim)."},
        {"id": "08", "prompt": "08-canonical-name-authority.prompt.md", "cursor_name": "ass-ade-08-cna", "title": "Canonical Name Authority (CNA)", "use_when": "Assign dotted canonical names; aligns with ASS-ADE materializer."},
        {"id": "09", "prompt": "09-binder.prompt.md", "cursor_name": "ass-ade-09-binder", "title": "Binder", "use_when": "REUSE / EXTEND / REFACTOR / SYNTHESIZE routing."},
        {"id": "10", "prompt": "10-fingerprinter.prompt.md", "cursor_name": "ass-ade-10-fingerprinter", "title": "Fingerprinter", "use_when": "sig_fp + body_fp for atoms."},
        {"id": "11", "prompt": "11-registry-librarian.prompt.md", "cursor_name": "ass-ade-11-registry-librarian", "title": "Registry Librarian", "use_when": "Lookup, registration, versioning."},
        {"id": "12", "prompt": "12-scorer.prompt.md", "cursor_name": "ass-ade-12-scorer", "title": "Scorer", "use_when": "Best-atom selection (best, not newest)."},
        {"id": "13", "prompt": "13-compile-gate.prompt.md", "cursor_name": "ass-ade-13-compile-gate", "title": "Compile Gate", "use_when": "Syntax / compile / type checks before ship."},
        {"id": "14", "prompt": "14-repair-agent.prompt.md", "cursor_name": "ass-ade-14-repair-agent", "title": "Repair Agent", "use_when": "Context-packed patches when compile fails."},
        {"id": "15", "prompt": "15-a0-qk-constant-builder.prompt.md", "cursor_name": "ass-ade-15-a0-builder", "title": "a0 QK Constant Builder", "use_when": "QK (quark) constants — declarative shapes and invariants."},
        {"id": "16", "prompt": "16-a1-atom-function-builder.prompt.md", "cursor_name": "ass-ade-16-a1-builder", "title": "a1 Atom Function Builder", "use_when": "Atom functions — pure, stateless, deterministic behavior."},
        {"id": "17", "prompt": "17-a2-molecular-composite-builder.prompt.md", "cursor_name": "ass-ade-17-a2-builder", "title": "a2 Molecular Composite Builder", "use_when": "Molecular composites — stateful clients, stores, registries, and other reusable resource managers."},
        {"id": "18", "prompt": "18-a3-organic-feature-builder.prompt.md", "cursor_name": "ass-ade-18-a3-builder", "title": "a3 Organic Feature Builder", "use_when": "Organic features — coordinated capabilities composed from a0, a1, and a2."},
        {"id": "19", "prompt": "19-a4-synthesis-orchestration-builder.prompt.md", "cursor_name": "ass-ade-19-a4-builder", "title": "a4 Synthesis Orchestration Builder", "use_when": "Synthesis orchestration — CLI entrypoints, runtime wiring, and top-level orchestration flows."},
        {"id": "20", "prompt": "20-sovereign-gatekeeper.prompt.md", "cursor_name": "ass-ade-20-sovereign-gatekeeper", "title": "Sovereign Gatekeeper", "use_when": "IP-boundary-preserving comparisons."},
        {"id": "21", "prompt": "21-leak-auditor.prompt.md", "cursor_name": "ass-ade-21-leak-auditor", "title": "Leak Auditor", "use_when": "Scan commits for sovereign leakage."},
        {"id": "22", "prompt": "22-no-stub-auditor.prompt.md", "cursor_name": "ass-ade-22-no-stub-auditor", "title": "No-Stub Auditor", "use_when": "MAP = TERRAIN on every diff."},
        {"id": "23", "prompt": "23-trust-propagator.prompt.md", "cursor_name": "ass-ade-23-trust-propagator", "title": "Trust Propagator", "use_when": "trust_score across registry."},
        {"id": "24", "prompt": "24-genesis-recorder.prompt.md", "cursor_name": "ass-ade-24-genesis-recorder", "title": "Genesis Recorder", "use_when": "Persist chained genesis events."},
        {"id": "25", "prompt": "25-ass-ade-cli-doc-sweeper.prompt.md", "cursor_name": "ass-ade-25-cli-doc-sweeper", "title": "ASS-ADE CLI Doc Sweeper", "use_when": "Small docs-only sweep from transitional CLI names to the single ass-ade command."},
        {"id": "26", "prompt": "26-ass-ade-agent-prompt-sweeper.prompt.md", "cursor_name": "ass-ade-26-agent-prompt-sweeper", "title": "ASS-ADE Agent Prompt Sweeper", "use_when": "Small prompt/docs sweep so agents tell users to run ass-ade."},
        {"id": "27", "prompt": "27-ass-ade-cli-smoke-tester.prompt.md", "cursor_name": "ass-ade-27-cli-smoke-tester", "title": "ASS-ADE CLI Smoke Tester", "use_when": "Focused CLI tests for ass-ade, atomadic alias, book, assimilate, doctor, and build alias."},
        {"id": "28", "prompt": "28-ass-ade-env-dedupe-auditor.prompt.md", "cursor_name": "ass-ade-28-env-dedupe-auditor", "title": "ASS-ADE Environment Dedupe Auditor", "use_when": "Read-only stale editable install audit and troubleshooting docs."}
    ]
}
