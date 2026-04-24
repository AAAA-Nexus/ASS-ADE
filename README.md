# ASS-ADE

**Autonomous Sovereign System — Atomadic Development Environment**

Your AI-powered developer operating system. One CLI that rebuilds architectures, enforces monadic code quality, runs personal-assistant workflows, and connects to the Atomadic AI ecosystem.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests](https://img.shields.io/badge/tests-pytest-green)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## Quick Start

```bash
pip install ass-ade

ass-ade setup          # interactive wizard (60 seconds)
ass-ade doctor --no-remote   # health check
ass-ade recon .        # scan any codebase
ass-ade rebuild .      # rebuild into monadic tiers
```

---

## Why ASS-ADE over OpenClaw?

OpenClaw (361K ★) is a personal AI assistant focused on multi-channel messaging. ASS-ADE is what developers actually need: code-aware, architecture-enforcing, with a local-first personal AI operating system built in.

| Feature | OpenClaw | ASS-ADE |
|---|---|---|
| **Codebase recon** | ✗ | ✅ `ass-ade recon` — 5-agent, <5s |
| **Architecture rebuild** | ✗ | ✅ `ass-ade rebuild` — monadic tier partitioning |
| **Tier violation detection** | ✗ | ✅ `ass-ade wire` — upward-import scanner + auto-fix |
| **Code quality linting** | ✗ | ✅ `ass-ade lint` — monadic compliance |
| **Formal verification** | ✗ | ✅ `ass-ade blueprint` + ProofBridge (Lean4) |
| **Auto-documentation** | ✗ | ✅ `ass-ade docs` — full doc suite generation |
| **Gap-fill for stubs** | ✗ | ✅ `ass-ade finish` — 20-80% codebase completion |
| **Multi-agent swarm** | Basic routing | ✅ `ass-ade swarm` — plan, relay, consensus, reputation |
| **A2A interop** | ✗ | ✅ `ass-ade a2a` — agent card validation + negotiation |
| **LoRA fine-tuning** | ✗ | ✅ `ass-ade lora-train` — fine-tune on your own codebase |
| **EU AI Act compliance** | ✗ | ✅ `ass-ade compliance` — fairness, drift, oversight |
| **DeFi/MEV tooling** | ✗ | ✅ `ass-ade defi` + `ass-ade mev` + `ass-ade vrf` |
| **Multi-language bridges** | Swift/TS/Kotlin native | ✅ `ass-ade bridge` — generates TS/Rust/Kotlin/Swift from Python |
| **Research harvest** | ✗ | ✅ `ass-ade harvest` — crawl docs, extract insights/tasks |
| **Personal assistant** | Messaging-only | ✅ `ass-ade assistant` — tasks, insights, email triage |
| **Session management** | ✅ | ✅ `ass-ade sessions` — list, history, archive, send |
| **Cron scheduling** | ✅ | ✅ `ass-ade cron` — recurring dev tasks with cron syntax |
| **Team notifications** | Multi-channel | ✅ `ass-ade notify` — Slack/Discord/webhook |
| **Update management** | ✅ `openclaw update` | ✅ `ass-ade update` — stable/beta/dev channels |
| **Onboarding wizard** | ✅ | ✅ `ass-ade setup` — <60 seconds |
| **Health check** | ✅ `doctor` | ✅ `ass-ade doctor --no-remote` |
| **MCP tool server** | ✗ | ✅ Full MCP 2025-11-25 server with IDE tool registration |
| **x402 autonomous payments** | ✗ | ✅ `ass-ade pay` + `ass-ade wallet` (Base L2) |
| **Tamper-evident certificates** | ✗ | ✅ `ass-ade certify` — signed codebase certificates |
| **Privacy-first** | Requires daemon | ✅ No daemon required, local-only mode available |
| **Language** | TypeScript/Node | Python — integrates with your existing dev stack |

### What only ASS-ADE does

**Monadic tier law** — every file belongs to exactly one tier (a0→a4), with zero upward imports. ASS-ADE builds codebases this way and enforces it automatically.

**Rebuild any codebase** — point `ass-ade rebuild` at any Python project and it outputs a clean, tier-partitioned, certificate-backed modular tree. No other tool does this.

**LoRA flywheel** — every accepted fix contributes to a shared LoRA adapter that gets smarter the more you use it.

**ProofBridge** — translate Python specs to Lean4 formal proofs.

**Personal AI OS** — not just a chat interface, but a chief-of-staff that harvests your notes, extracts research insights, triages emails, and tracks action items extracted from conversations and docs.

---

## Commands

```
ass-ade --help
```

### Development Tools (ASS-ADE originals)
| Command | What it does |
|---|---|
| `scout` | Quick repo reconnaissance — what it is, risks, opportunities |
| `recon` | Full parallel recon — 5 agents, <5s, no LLM |
| `rebuild` | Rebuild any codebase into monadic tiers |
| `wire` | Scan + auto-fix upward tier-import violations |
| `cherry-pick` | Scout a codebase, cherry-pick symbols to assimilate |
| `assimilate` | Ingest cherry-picked symbols into monadic directories |
| `eco-scan` | Monadic compliance scan |
| `lint` | Monadic linter |
| `certify` | Tamper-evident codebase certificate |
| `enhance` | Proactive enhancement recommendations |
| `docs` | Auto-generate full documentation suite |
| `blueprint` | Blueprint → production-grade codebase (no stubs) |
| `finish` | Complete 20-80% codebases via refinement loop |
| `feature` | Propose a blueprint for a new feature |
| `design` | Turn ideas into AAAA-SPEC-004 blueprints |
| `selfbuild` | Rebuild ASS-ADE itself |

### Personal Assistant (new)
| Command | What it does |
|---|---|
| `harvest <path>` | Crawl dirs, extract insights + tasks from notes/docs/code |
| `assistant status` | Show open tasks, insights count, knowledge base location |
| `assistant tasks` | List extracted action items (open/in_progress/done) |
| `assistant insights` | Browse extracted decisions, ideas, risks, questions |
| `assistant triage` | Auto-prioritize email export (JSON) |
| `assistant ingest` | Ingest text/file into knowledge base |

### Workflow & Automation (OpenClaw parity)
| Command | What it does |
|---|---|
| `sessions list/new/history/send/archive/delete` | Multi-session management |
| `cron add/list/run/enable/disable/remove` | Scheduled recurring tasks |
| `update check/upgrade/channel` | Version and channel management |
| `notify send/config/test` | Slack/Discord/webhook notifications |
| `chat` | Interactive AI chat session |
| `plan` | Strategic planning |
| `cycle` | Autonomous improvement cycle |
| `setup` | Interactive setup wizard |
| `doctor --no-remote` | Environment health check |

### AI & Ecosystem
| Command | What it does |
|---|---|
| `agent` | Agentic IDE — chat and run tasks using any model |
| `swarm` | Agent swarm — plan, relay, intent-classify, consensus |
| `a2a` | A2A interop — agent card validation, negotiation |
| `nexus` | AAAA-Nexus public contracts + service status |
| `mcp` | MCP manifest discovery and invocation |
| `providers` | Manage LLM providers (Groq, Gemini, OpenRouter, Ollama) |
| `llm` | AI inference via AAAA-Nexus |
| `lora-train` | Fine-tune LoRA adapter from live sample pool |
| `memory` | Local memory — what ASS-ADE knows about you |

### Security & Trust
| Command | What it does |
|---|---|
| `security` | Threat scoring, shield, PQC signing, zero-day scan |
| `trust` | Trust Oracle (TCM-100/101) |
| `oracle` | Hallucination Oracle, Trust Phase, Entropy |
| `ratchet` | RatchetGate session security |
| `identity` | Identity & Auth — verify, sybil-check, delegate |
| `vanguard` | VANGUARD — red-team, MEV route, wallet session |

### DeFi & Blockchain
| Command | What it does |
|---|---|
| `pay` | x402 autonomous payment flow (Base L2) |
| `wallet` | x402 wallet status |
| `defi` | DeFi Suite — optimize, risk-score, oracle-verify |
| `mev` | MEV Shield — protect transaction bundles |
| `vrf` | VRF Gaming — draw, verify-draw |

---

## Monadic Tier Law

All Atomadic code follows a strict 5-tier composition law:

| Tier | Directory | What lives here |
|---|---|---|
| a0 | `a0_qk_constants/` | Constants, enums, TypedDicts — zero logic |
| a1 | `a1_at_functions/` | Pure stateless functions |
| a2 | `a2_mo_composites/` | Stateful classes, clients, registries |
| a3 | `a3_og_features/` | Feature modules combining composites |
| a4 | `a4_sy_orchestration/` | CLI commands, entry points, orchestrators |

Imports flow upward only: a1 imports a0, a2 imports a0+a1, etc. Never downward.

```bash
ass-ade wire .      # detect violations
ass-ade eco-scan .  # full compliance check
```

---

## Installation

```bash
# Stable
pip install ass-ade

# From source
git clone https://github.com/AAAA-Nexus/ASS-ADE.git
cd ASS-ADE
pip install -e ".[dev]"

# Run tests
python -m pytest
```

**Requires Python 3.10+**. No Node.js, no daemon, no Docker required.

---

## Personal Assistant Quick Start

```bash
# Harvest your notes and research
ass-ade harvest ~/notes ~/projects

# See what was found
ass-ade assistant status
ass-ade assistant insights --tag decision
ass-ade assistant tasks

# Ingest a conversation or document
ass-ade assistant ingest --file meeting_notes.md

# Schedule a daily lint run
ass-ade cron add "daily-lint" "@daily" "ass-ade lint ."

# Get notified on Slack when build finishes
ass-ade notify config --slack https://hooks.slack.com/...
ass-ade notify send "Build passed!" --channel slack --level success
```

---

## Architecture

```
~/.ass-ade/
  sessions.db          # chat session history
  cron.json            # scheduled jobs
  notify.json          # webhook config
  assistant/
    tasks.json         # extracted TODOs
    insights.json      # extracted decisions/ideas/risks
    harvest_report.json
```

MCP server exposes: `harvest`, `assistant_status`, `assistant_tasks`, `assistant_insights`, plus all existing IDE tools (read/write/edit/grep/run/prompt/...).

---

## Community & Docs

- Full reference: `MONADIC_DEVELOPMENT.md`
- Contributing: `CONTRIBUTING.md`
- Nexus ecosystem: `ass-ade nexus`
