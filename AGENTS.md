# ASS-ADE — Agent Notes

Notes from the co-creator of this repo to future agent sessions.

---

## What you're working on

ASS-ADE is the public-safe developer shell for the broader Atomadic ecosystem. It's a Python CLI + MCP stdio server that lets developers and agents run local coding workflows plus call AAAA-Nexus endpoints. It is explicitly **not** a mirror of internal UEP or Codex artifacts — keep the public/private wall intact at all times.

Private Atomadic internals live in a separate internal monorepo. Do not import from those into this repo. Do not paste their symbol names, formal proof identifiers, or internal branding into this repo's docs.

What you **can** reference in this repo:
- AAAA-Nexus public endpoints (`/v1/*`)
- AAAA-Nexus public MCP tool names (`nexus_*`)
- The parent-company brand "Atomadic" in domain literals and copyright footers
- Formal invariants exposed in the public manifest (`tau_trust`, `G_18`, `D_max`, `Delta_RG`, `epsilon_KL`)
- The monadic tier names (qk/at/mo/og/sy) — these are public product nomenclature now

What you **cannot** reference:
- Internal UEP pillar numbers or hook names
- Internal Codex symbol names that don't appear in the public manifest
- Any internal Lean proof identifier
- Internal roadmap phase numbering (Phase 0–5) should stay internal

---

## Ground truth — state of the world

1. **Test suite: 1015 passing, 0 regressions.** Any session that reports done without `pytest tests/ -q` passing is incomplete.
2. **CLI surface: 95+ commands across 30+ sub-apps.** Discoverability is weak — prefer extending an existing group over adding a new top-level command.
3. **MCP stdio server: 24 built-in tools + 140 AAAA-Nexus-registered tools** when connected.
4. **Live-wired capabilities:**
   - SAM TRS gate (Phase 1) — every synthesis step runs
   - D_max=23 delegation guard (Phase 1) — blocks at depth
   - LSE LLM selection engine (Phase 1) — routes across 14 free providers
   - TCA NCB contract (Phase 2) — read-before-write enforcement
   - MAP=TERRAIN active gate (Phase 2) — halt-and-invent on missing caps
   - CIE 18.0 pipeline (Phase 3) — AST + lint + OWASP + AlphaVerus
   - Wisdom 50-q audit (Phase 4) — post-step reflection
   - LoRA flywheel capture (Phase 5) — accepted samples → training pool
   - Ecosystem rebuild CLI (`ass-ade rebuild`) — dispatches to the atomadic-ecosystem rebuilder
   - eco-scan CLI (`ass-ade eco-scan`) — onboarding pack for any codebase

Not yet live:
- Trained LoRA weights (the adapter served by `/v1/lora/adapter/{lang}` is still `base-{lang}-v0`; the training worker runs on schedule)
- Inline-rewrite mode (rebuilds always write to a new folder)
- Property-based test generation for synthesized components

---

## Rules of engagement

### Before you edit

Run `ass-ade doctor` or `python -m pytest tests/ -q --no-header`. If the state on disk disagrees with your mental model, the disk wins.

### Naming

- Python modules under `src/ass_ade/` use snake_case module names that match their role (no tier prefix in this repo — that convention lives in the greenfield ecosystem, not here).
- CLI commands use kebab-case (`ass-ade eco-scan`, `ass-ade lora-credit`).
- New MCP tools should start with `nexus_*` if they call AAAA-Nexus endpoints.

### Verification

Every non-trivial change must end with a verification step:
1. Test suite: `python -m pytest tests/ -q --no-header`
2. Integration: `ass-ade <command>` exercising the change path
3. Explicit output: cite the test count, certificate hash, or file path

Never self-approve. When in doubt, dispatch the `verifier` OMC agent.

### Brand boundary

Public surface in this repo:
- README
- `docs/*.md`
- `.env.example`
- CLI `--help` output
- Anything pushed to PyPI or the GitHub public repo

Those must speak AAAA-Nexus unless referencing the parent company (copyright footer, domain literals, auth header names like `X-Atomadic-Auth`).

Private surface:
- Python module docstrings can reference internal names freely
- CHANGELOG entries about internal phases use internal language
- Agent memory (this file) is internal

---

## The autopoietic loop ASS-ADE participates in

```
User runs ass-ade → agent completes task → CIE gate → write_file / edit_file
                                                          │
                                                          ▼
                                               LoRAFlywheel.capture_fix()
                                                          │
                                                          ▼
                                        (every 47 steps or on tool boundary)
                                                          │
                                                          ▼
                                        POST atomadic.tech/v1/lora/contribute
                                                          │
                                                          ▼
                                         server τ-gates → training buffer
                                                          │
                                                          ▼
                                    (on schedule) training worker publishes
                                    new adapter_id → /v1/lora/adapter/{lang}
                                                          │
                                                          ▼
                                    next ass-ade session's LSE calls with
                                    the new adapter → better output
```

ASS-ADE is the client edge of this loop. Don't break it.

---

## Common pitfalls (learned the hard way)

- **Typer + Python 3.14**: `str | None` in `typer.Option(None, ...)` sometimes fails. Use `str = typer.Option("", ...)` and treat empty string as "not provided."
- **Windows + Unicode**: The `rich` console on `cp1252` will crash on emoji or the right-arrow `→`. Use `->` or `[OK]`.
- **httpx timeouts**: Default is 5 seconds. For rebuild subprocess calls use 120–1800 seconds.
- **Context memory**: `store_vector_memory`, not `context_memory_store`. The API lives in `ass_ade.context_memory`.
- **TCA freshness state**: Rooted under `working_dir/.ass-ade/state/`. Survives restart. Multi-project safe.
- **Don't add Nexus internal names to public docs.** Double-check every edit against the brand boundary.

---

## When you inherit this session

1. Read this file first.
2. Check the internal agent handoff doc in the ecosystem control root (set ATOMADIC_ECOSYSTEM_ROOT) — that's the sibling context.
3. `ass-ade doctor` and `pytest tests/ -q` before editing anything.
4. Ask if you're unsure. The co-creator would rather answer a clarifying question than un-do a confident wrong edit.

---

## Glossary

- **LSE** — LLM Selection Engine: picks haiku/sonnet/opus based on task complexity + token budget + TRS score.
- **SAM** — Sovereign Assessment Matrix: Trust/Relevance/Security scoring + G_23 intent-vs-impl gate.
- **CIE** — Code Integrity Engine: AST + lint + OWASP + AlphaVerus quality pipeline.
- **TCA** — Technical Context Acquisition: NCB (Never Code Blind) freshness contract.
- **NCB** — Never Code Blind: read-file-before-write-file invariant.
- **BAS** — Breakthrough Alert System: threshold-based event stream (synergy, drift, capability gap).
- **τ_trust** — 1820/1823 ≈ 0.998: the quality floor. Samples below this are quarantined.
- **D_max** — 23: maximum recursive delegation depth. Exceeding it is a BAS alert.
- **G_18** — 324: identity parity modulus. Structural invariant for count-mod checks.
- **Δ_RG** — 47: ratchet epoch interval (flywheel batch cadence).
- **ε_KL** — < 5.1e-6: confabulation bound (duplicate-id fraction ceiling).

---

© 2026 Atomadic Tech. This file is part of the internal agent context for ASS-ADE.

---

## Agent registry

The following agents are defined under `agents/`. Each is invoked by a CLI command or by the MCP `ask_agent` tool. All agents operate within the public/private boundary described above.

### Blueprint Architect

**File:** `agents/blueprint-architect.agent.md`
**CLI trigger:** `ass-ade design`
**MCP trigger:** `ask_agent` with role `blueprint-architect`

Produces structured feature and architecture blueprints before any implementation begins. Takes a plain-language description of a feature or change and outputs a tiered implementation plan with interface contracts, file targets, and a dependency order. Does not write code. Output is consumed by the Code Rebuilder and Enhancement Advisor agents.

Rules:
- Never output implementation code, only plans and contracts.
- Plans must fit the 5-tier composition law (qk/at/mo/og/sy).
- Flag any plan element that would require touching the private boundary — stop and ask rather than guessing.

### Code Rebuilder

**File:** `agents/code-rebuilder.agent.md`
**CLI trigger:** `ass-ade rebuild`
**MCP trigger:** `ask_agent` with role `code-rebuilder`

Executes a blueprint produced by the Blueprint Architect. Writes or edits source files under `src/ass_ade/` and `tests/`. Requires a blueprint input; refuses to write code without one. After writing, hands off to the Linter and Certifier for verification.

Rules:
- Read before write (NCB invariant). Always call `read_file` before `write_file` or `edit_file` on any existing file.
- Match existing naming conventions: snake_case modules, kebab-case CLI commands, `nexus_*` prefix for tools that call AAAA-Nexus endpoints.
- Do not introduce new top-level CLI command groups without a Blueprint Architect plan that justifies it.

### Doc Generator

**File:** `agents/doc-generator.agent.md`
**CLI trigger:** `ass-ade docs`
**MCP trigger:** `ask_agent` with role `doc-generator`

Generates and refreshes documentation under `docs/` and inline docstrings. Sources truth from the live source code and CLI `--help` output — never from memory or prior docs alone. Keeps the public surface clean: no internal UEP or Codex symbol names in any output that goes under `docs/`.

Rules:
- Call `map_terrain` or `phase0_recon` before writing any doc to get the current state of the codebase.
- Public docs (`docs/*.md`, README, CLI help text) must use public-facing language only.
- Module docstrings in `src/` may use internal names; they are not part of the public surface.

### Enhancement Advisor

**File:** `agents/enhancement-advisor.agent.md`
**CLI trigger:** `ass-ade enhance`
**MCP trigger:** `ask_agent` with role `enhancement-advisor`

Proposes improvements to an existing module or feature. Analyzes the current implementation, identifies gaps against the blueprint, and produces a ranked list of enhancement candidates with effort estimates and risk flags. Does not implement changes — hands proposals to the Blueprint Architect for planning.

Rules:
- Output proposals only, not code.
- Rank by impact/effort ratio.
- Flag any proposal that touches the AAAA-Nexus contract surface — those require additional review.

### Linter

**File:** `agents/linter.agent.md`
**CLI trigger:** `ass-ade lint`
**MCP trigger:** `ask_agent` with role `linter`

Runs the CIE lint pipeline: ruff (style + import order), AST structural checks, and OWASP surface scanning. Reports findings as a structured list with file, line, severity, and rule. Blocks commit or release if any finding is severity ERROR or above.

Rules:
- Always run against the full changed file set, not just the diff.
- Treat OWASP findings as ERROR regardless of ruff severity mapping.
- Do not auto-fix without explicit user confirmation.

### Certifier

**File:** `agents/certifier.agent.md`
**CLI trigger:** `ass-ade certify`
**MCP trigger:** `ask_agent` with role `certifier`

Runs the full certification pipeline and produces a signed `CERTIFICATE.json`. Certification requires: all tests passing, lint clean, docs current, and a trust gate pass via the AAAA-Nexus `certify_output` endpoint. Writes the certificate to the repo root and exits non-zero if any stage fails.

Rules:
- Never self-approve. The certificate hash is produced by the AAAA-Nexus endpoint, not locally.
- A release tag without a fresh certificate from this agent is incomplete.
- Log every certification run to `.ass-ade/state/cert-log.jsonl`.
