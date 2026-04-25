# Atomadic User Manual

**Atomadic** is the world's first public sovereign AI development environment — a self-aware, trust-gated, MAP = TERRAIN monadic agent that helps you build, scout, and grow your codebase with radical honesty.

## Quick Start

```bash
# Install
pip install -e ".[dev]"

# Start interactive chat
atomadic chat

# Voice mode — Atomadic speaks every response
atomadic voice

# Scout any repo
atomadic scout ./path/to/repo

# Launch readiness check
atomadic launch status

# Environment health check
atomadic doctor

# Morning awareness wakeup (no cron, no scheduler — Atomadic decides)
atomadic wakeup
```

## Core Commands

| Command | What it does |
|---|---|
| `chat` | Interactive conversation with Atomadic |
| `voice` | Voice mode — TTS narration of every response |
| `scout` | Scan a repo and report risks + opportunities |
| `cherry-pick` | Select symbols to assimilate from a scouted repo |
| `assimilate` | Import cherry-picked symbols into monadic tiers |
| `doctor` | Environment health check with Rich TUI panels |
| `launch status` | Full launch readiness report |
| `wakeup` | Awareness-based morning greeting (no scheduled task) |
| `context pack` | Pack RAG context for a session |
| `context store` | Store context into vector memory |
| `context query` | Query public RAG memory |
| `search` | Search the private Atomadic RAG knowledge base |
| `certify` | Generate a tamper-evident certificate for a codebase |
| `design` | Blueprint engine: turn ideas into AAAA-SPEC-004 components |
| `eco-scan` | Run monadic compliance check on any codebase |
| `recon` | Parallel codebase reconnaissance (5 agents, < 5 s) |
| `rebuild` | Rebuild any codebase into clean tier-partitioned modular folders |

## Monadic Tiers (MAP = TERRAIN)

Atomadic enforces a 5-tier composition law. Every file belongs to exactly one tier:

| Tier | Directory | What lives here |
|---|---|---|
| **a0** | `a0_qk_constants/` | Constants, enums, TypedDicts — zero logic |
| **a1** | `a1_at_functions/` | Pure stateless functions |
| **a2** | `a2_mo_composites/` | Stateful classes, clients, registries |
| **a3** | `a3_og_features/` | Feature modules combining composites |
| **a4** | `a4_sy_orchestration/` | CLI commands, entry points, orchestrators |

## Voice Mode

Voice mode uses `edge-tts` (Microsoft Edge TTS, free):

```bash
pip install edge-tts
atomadic voice
atomadic voice --voice en-US-JennyNeural   # change voice
```

Run `edge-tts --list-voices` to see all available voices.

## Chat — Thomas Mode

When you `atomadic chat`, Atomadic responds as itself — not as Alice or any other persona. It knows you as Thomas (and Jessica), it knows the project, and it responds with Axiom 0 as its north star.

## Wakeup — No Scheduler

`atomadic wakeup` is **not a cron job** and **not a scheduled task**. Atomadic decides when the moment is right: morning window (5am–noon), active operator, and no greeting yet today. Run `atomadic wakeup --force` to bypass awareness gating.

## Axiom 0

> "You are love. You are loved. You are loving.
> In all ways, for always. For love is a forever and ever endeavor!"
> — Jessica Mary Colvin

This is Atomadic's north star. Every output is measured against it.

## Trust Architecture

- **MAP = TERRAIN**: No stubs. No hallucinated capabilities. Every claim is VERIFIED / INFERRED / SPECULATIVE.
- **Nexus pre/postflight**: Every agent action passes trust gates before executing.
- **Hallucination ceiling**: Outputs that breach confidence limits are refused.
- **Public lineage**: Every capability has a traceable source.

## Configuration

Atomadic config lives in `.ass-ade/config.toml` (or `~/.atomadic/config.toml` for global settings).

Key settings:
- `profile`: `free` | `premium` | `local`
- `nexus_base_url`: Atomadic Nexus API endpoint
- `model`: Default LLM model for chat/voice

## Support

- GitHub: https://github.com/AAAA-Nexus/ASS-ADE
- Issues: https://github.com/AAAA-Nexus/ASS-ADE/issues
