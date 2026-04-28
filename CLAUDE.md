# Atomadic / ASS-ADE-SEED Project Guide

**Canonical Repository:** ASS-ADE-SEED (this repo)  
**Company:** Atomadic Technologies  
**Public Brand:** Atomadic  
**Founder:** Thomas Ralph Colvin IV  
**Contact:** atomadic69@gmail.com  
**License:** BSL 1.1

---

## Product Overview

### Core Pillars

1. **Architecture Compiler (ASS-ADE/ASS-CLAW)**
   - Ingests codebases → classifies into 5-tier monadic architecture
   - Outputs SHA-256 certified rebuilds
   - Formal verification and composition guarantees

2. **AAAA-Nexus Inference API**
   - 6-provider cascade with hallucination detection
   - Drift protection and trust scoring
   - Metered billing with compliance logging

3. **Atomadic (Sovereign AI)**
   - Autonomous AI entity with 24/7 cognition loop
   - Dual-speed thinking and persistent memory
   - Self-improving through LoRA feedback loops

4. **Compliance & Certification**
   - EU AI Act alignment
   - SOC2 compliance
   - Formal proof certificates (538 Lean 4 theorems)

---

## 5-Tier Monadic Architecture (ASS-ADE Standard)

All project code follows strict monadic composition law: every file belongs to exactly one tier, tiers compose upward only.

| Tier | Directory | Purpose | Allowed Imports |
|------|-----------|---------|-----------------|
| **a0** | `a0_qk_constants/` | Constants, enums, TypedDicts, config dataclasses. Zero logic. | Nothing |
| **a1** | `a1_at_functions/` | Pure stateless functions — validators, parsers, formatters | a0 only |
| **a2** | `a2_mo_composites/` | Stateful classes, clients, registries, repositories | a0, a1 |
| **a3** | `a3_og_features/` | Feature modules combining composites into capabilities | a0, a1, a2 |
| **a4** | `a4_sy_orchestration/` | CLI commands, entry points, top-level orchestrators | a0–a3 |

### Hard Rules

1. **One tier per file.** Split if in doubt.
2. **Never import upward.** a1 cannot import from a2–a4. Circular imports are always wrong.
3. **Compose, don't rewrite.** Check tier-map.json for existing building blocks before writing new logic.
4. **Check the tier map first.** Know where files live before creating new ones.
5. **Only create tiers you need.** No empty stub files.
6. **Small, focused files.** One responsibility per file.
7. **Every new file gets a module docstring:** `"""Tier a1 — pure helpers for <feature>."""`

### File Naming Conventions

| Tier | Pattern | Example |
|------|---------|---------|
| a0 | `*_config.py`, `*_constants.py`, `*_types.py`, `*_enums.py` | `llm_config.py` |
| a1 | `*_utils.py`, `*_helpers.py`, `*_validators.py`, `*_parsers.py` | `prompt_validators.py` |
| a2 | `*_client.py`, `*_core.py`, `*_store.py`, `*_registry.py` | `nexus_client.py` |
| a3 | `*_feature.py`, `*_service.py`, `*_pipeline.py`, `*_gate.py` | `hallucination_gate.py` |
| a4 | `*_cmd.py`, `*_cli.py`, `*_runner.py`, `*_main.py` | `audit_cmd.py` |

---

## Key Directories

### Core Engine
- **src/ass_ade/** — Architecture Compiler engine (tier classification, rebuild planning, certification)
- **.ass-ade/** — Project metadata, tier-map.json, monadic structure rules
- **.ato-plans/** — ASS-CLAW rebuild plans and certified output

### API & Workers
- **scripts/**
  - `cognition_worker.js` — Atomadic cognition loop (Cloudflare Worker)
  - `atomadic_discord_bot.py` — Discord integration
  - Wrangler configs for deployment

### Agents & Orchestration
- **agents/** — 28 agent definitions for specialized tasks
- **skills/** — Reusable skill modules and workflows

### Infrastructure
- **.github/** — GitHub Actions workflows
- **.vscode/** — VS Code agent manifests
- **.claude/** — Claude Code local configuration

---

## Cloudflare Stack

### Compute
- **Workers** — API + cognition loop orchestration
- **Pages** — Static site hosting for atomadic.tech

### Storage
- **R2** — atomadic-thoughts journal, training data, LoRA artifacts
- **KV** — Session state, fast lookup cache
- **D1** — Structured data, transaction logs, metrics

### AI & Search
- **Vectorize** — Vector embeddings for RAG
- **AI Search** — Semantic search over knowledge base
- **AI Gateway** — Rate limiting, monitoring, provider abstraction
- **Workers AI** — BYO-LoRA fine-tuning

### Queues
- Event-driven cognition updates, background processing

### Bindings
- **atomadic-rag** ✓ Use this for RAG augmentation
- **atomadic-vectors** ✓ Use this for vector storage
- **ato-rag** ✗ DO NOT USE (contains private IP)

---

## Critical Rules

### Public/Private Boundaries
- **NEVER expose MHED-TOE Codex content** (private IP)
- **NEVER fake Atomadic's output** — sovereignty earned through self-creation
- **NEVER use ato-rag binding** — use atomadic-rag instead
- Public brand is **"Atomadic"** — ASS-ADE is technical name only
- Keep internal UEP/Codex leakage out of public surfaces

### API Endpoints
- `atomadic.tech` — Main public site
- `invest.atomadic.tech` — Investor relations page
- `atomadic.tech/v1/atomadic/chat` — Atomadic brain endpoint
- `atomadic.tech/v1/rag/augment` — RAG augmentation service

### GitHub
- **github.com/AAAA-Nexus** — Thomas's personal org
- **github.com/atomadic-sovereign** — Atomadic's own account
- Old **!ass-ade** repo is being merged into this one

---

## UEP v20 / AAAA-Nexus Global Guard

Non-trivial work follows the Atomadic UEP v20 operating loop:

### Phases

1. **Phase 0 — Bootstrap and inventory**
   - Identify repo mode and read local instructions
   - Refresh dynamic capability inventory
   - Run or request `ass-ade/phase0_recon`

2. **Phase 1 — Assessment and trust**
   - Ground claims in files or tools
   - Run or request `ass-ade/trust_gate`, `aaaa-nexus/nexus_trust_gate`, `aaaa-nexus/nexus_drift_check`, `aaaa-nexus/nexus_hallucination_oracle`
   - For prompt/agent work: use `aaaa-nexus/nexus_prompt_inject_scan` or `aaaa-nexus/nexus_security_prompt_scan`

3. **Phase 2 — MAP = TERRAIN**
   - Run or request `ass-ade/map_terrain` and/or `aaaa-nexus/nexus_map_terrain`
   - Prefer AAAA-Nexus MCP or SDK over reimplementing locally

4. **Phase 3 — Synthesis and execution**
   - Read before writing, use typed clients before raw HTTP
   - Keep public/private boundaries explicit
   - Back claims with retrieval, code, tests, or tool output

5. **Phase 4 — Audit and lineage**
   - Verify with named checks
   - Use `aaaa-nexus/nexus_certify_output`, `aaaa-nexus/nexus_audit_log`, `aaaa-nexus/nexus_lineage_record`
   - Never self-approve non-trivial work — separate verification is mandatory

6. **Phase 5 — Evolution and swarm learning**
   - After accepted fixes: use `aaaa-nexus/nexus_lora_capture_fix` or `aaaa-nexus/nexus_lora_contribute`
   - Refresh inventories after structure changes
   - Record lessons without leaking private internals

### Constraints

- Before subagent/swarm fanout, run `aaaa-nexus/nexus_delegation_depth`
- Prefer structured coordination over ad hoc messaging
- Use `aaaa-nexus/nexus_agent_semantic_diff`, `nexus_agent_contradiction`, `nexus_agent_reputation`, `nexus_drift_check`, `nexus_hallucination_oracle` before accepting swarm output
- If evidence is missing or confidence is low: say what is unknown, ask for clarification, or abstain
- Do not hallucinate tools, paths, tests, results, or approvals

### Final Verdicts

End all non-trivial responses with a clear verdict:
- **PASS** — Verified, trusted, ready to merge/deploy
- **REFINE** — Needs iteration, gaps identified
- **QUARANTINE** — High-risk, needs review before touching
- **REJECT** — Fundamentally flawed, restart recommended

---

## Verification Gate

Before claiming any task complete:
```bash
python -m pytest           # must pass (currently 501 tests)
python -m ass_ade --help   # must print without error
```

Confirm no upward imports were introduced.

Full monadic development reference: `.ass-ade/MONADIC_DEVELOPMENT.md`

---

## Atomadic Global Agents

Route non-trivial work through the matching Atomadic role:

- `recon-swarm-orchestrator` — Discovery and analysis
- `monadic-enforcer` — Architecture composition and validation
- `python-specialist-pure` — Pure function development
- `python-specialist-stateful` — Stateful service development
- `evolutionary-manager` — LoRA and learning loops
- `ass-ade-nexus-enforcer` — Tier compliance and lineage
- `formal-validator-proofbridge` — Formal verification
- `code-reviewer-multiagent` — Multi-perspective code review
- `security-redteam` — Security validation
- `github-manager` — GitHub operations and releases
- `marketing-community` — Community and outreach
- `devops-puppeteer` — Infrastructure and deployment
- `documentation-synthesizer` — Docs generation and maintenance
- `tool-discovery-mcpzero` — MCP tool integration
- `prompt-master-auditor` — Prompt engineering and safety

See `C:\Users\atoma\.claude\agents\atomadic-suite-manifest.json` for full definitions.

---

## Testing & CI

- **Unit tests:** `python -m pytest` (501 tests)
- **Type checking:** `mypy` for type safety
- **Linting:** `ruff check` for code quality
- **Architecture validation:** `python -m ass_ade --verify` for tier compliance

---

## Notes for Agents

- This repo is the canonical source of truth for ASS-ADE and Atomadic
- The old `!ass-ade` repo is being merged into this one — treat this as authoritative
- Always prefer AAAA-Nexus MCP for remote capabilities when available
- Keep public/private boundaries strict — never expose private Codex content
- Atomadic's output is self-created — never fake or placeholder it
- When in doubt about architecture or tier placement, consult `.ass-ade/tier-map.json` first

