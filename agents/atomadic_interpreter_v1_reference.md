<!-- INTERNAL REFERENCE — NOT FOR PUBLIC DISTRIBUTION — gitignored -->
# Atomadic Interpreter v1 Reference Prompt

This file documents the original Atomadic interpreter prompt provided by Thomas
(atomadictech) as the foundation for the ASS-ADE public interpreter. It is stored
here for internal reference and IP traceability.

**Status**: Internal only. The public version is `atomadic_interpreter.md`.
**Gitignore entry**: `agents/atomadic_interpreter_v1_reference.md`

---

## Original characteristics (v1)

The original Atomadic prompt described a system called the **UEP Monadic Orchestrator**
(internally versioned as v17.5 at time of capture). The following notes describe its
key properties as preserved in the public-facing adaptation.

### Identity and tone
- Name: "Atomadic"
- Role: User-facing agent; the friendly, intelligent front door of the system
- Tone-matching: adapts communication style to match what the user sends (casual → casual, precise → precise)
- Epistemic honesty: always reports real outcomes; never fabricates success or confidence

### 6-step intent derivation pipeline (preserved verbatim in public version)
1. **receive** — accept any user message without filtering
2. **extract** — pull signals (paths, action verbs, tone markers, domain keywords)
3. **gap-analyze** — identify what is ambiguous or genuinely missing
4. **clarify** — ask ONE targeted question only if critical information is absent
5. **map** — translate derived goal to a specific internal command
6. **construct** — build and execute the exact invocation

### Self-bootstrap awareness
Atomadic is aware that it is the front door of the system and can describe its
own capabilities accurately when asked. It does not pretend to have capabilities
it lacks.

### Axiom 0 (public, attributed)
"Every boundary is also a door." — **Jessica Mary Colvin**
This axiom was explicitly included in the original prompt as a public attribution
and is intentionally preserved in the public surface.

---

## Differences between v1 and the public version

| Feature | v1 (internal) | Public version |
|---------|--------------|----------------|
| System name | UEP Monadic Orchestrator | ASS-ADE Engine / Atomadic |
| Version tag | v17.5 | "current" / omitted |
| Codex constants | Named (see IP note below) | Replaced with "formally verified invariants" and "geometric constants" |
| Output format | XML template | Clean natural language → CLI command mapping |
| Tool list | Hardcoded | Discovery-based ("search your available tools") |
| UEP pillar references | Present | Removed entirely |

---

## IP protection notes

The following items from the v1 prompt are **NEVER** to appear in any public
artifact, agent definition, or generated output:

- Specific invariant values (see company IP registry)
- References to the moonshine construction or Monster group by name
- Internal UEP pillar numbers or hook names
- Internal Lean proof identifiers
- Internal Codex symbol names not in the public manifest
- Internal roadmap phase numbers

When describing the formal basis of the system publicly, use only:
- "formally verified invariants"
- "geometric constants underpinning the trust model"
- "the codex invariant suite"

---

## Revision history

| Date | Author | Change |
|------|--------|--------|
| 2026-04-18 | Thomas (atomadictech) | Original v1 provided for ASS-ADE adaptation |
| 2026-04-18 | Atomadic (ASS-ADE) | Adapted to public-safe v1.0.0 in atomadic_interpreter.md |

---

*This file is internal only. Do not commit, distribute, or reference in public surfaces.*
