# Monadic Development — ASS-ADE Standard

Copy this into any agent context to enforce monadic composition across Atomadic projects.

---

## The Core Idea

Code is organized in **5 strict tiers**. Each tier has one job. Tiers compose upward — never downward. A pure function never depends on a stateful class. A CLI command orchestrates everything below it but invents nothing new.

This isn't style. It's **the law** that keeps 500+ tests passing across a growing ecosystem.

---

## Tier Map

| Tier | Directory | What lives here | Allowed imports |
|------|-----------|-----------------|-----------------|
| **a0** | `a0_qk_constants/` | Constants, enums, TypedDicts, config dataclasses. **Zero logic.** | Nothing |
| **a1** | `a1_at_functions/` | Pure stateless functions — validators, parsers, formatters | a0 only |
| **a2** | `a2_mo_composites/` | Stateful classes, clients, registries, repositories | a0, a1 |
| **a3** | `a3_og_features/` | Feature modules combining composites into capabilities | a0, a1, a2 |
| **a4** | `a4_sy_orchestration/` | CLI commands, entry points, top-level orchestrators | a0–a3 |

---

## Hard Rules

1. **One tier per file.** A pure function → a1. A class with state → a2. A CLI entry point → a4. Split if in doubt.

2. **Never import upward.** `a1` cannot import from `a2`–`a4`. `a0` cannot import from anything. Circular imports are always wrong.

3. **Compose, don't rewrite.** Before writing new logic, check whether the building block already exists. If it does, import it. If it doesn't, create it in the right tier first, *then* compose.

4. **Check the tier map first.** Run `cat .ass-ade/tier-map.json` or read it. Know where existing files live before creating new ones.

5. **New features use separate tier files:**
   ```
   a0_qk_constants/my_feature_config.py   ← enums, defaults, TypedDicts
   a1_at_functions/my_feature_utils.py    ← pure helpers
   a2_mo_composites/my_feature_core.py    ← stateful class
   a3_og_features/my_feature.py           ← feature assembly
   a4_sy_orchestration/my_feature_cmd.py  ← CLI command
   ```
   Only create the tiers that are actually needed. Don't create empty stubs.

6. **Small, focused files.** One responsibility per file. If a file is growing large, split it — but keep the split within the same tier.

7. **Every new file gets a module docstring:**
   ```python
   """Tier a1 — pure helpers for <feature>."""
   ```

---

## File Naming Conventions

| Tier | Naming pattern |
|------|---------------|
| a0 | `*_config.py`, `*_constants.py`, `*_types.py`, `*_enums.py` |
| a1 | `*_utils.py`, `*_helpers.py`, `*_validators.py`, `*_parsers.py` |
| a2 | `*_client.py`, `*_core.py`, `*_store.py`, `*_registry.py` |
| a3 | `*_feature.py`, `*_service.py`, `*_pipeline.py`, `*_gate.py` |
| a4 | `*_cmd.py`, `*_cli.py`, `*_runner.py`, `*_main.py` |

---

## Verification Gate

Before claiming a task complete:

```bash
python -m pytest           # must pass (currently 501 tests)
python -m ass_ade --help   # must print without error
```

And confirm no upward imports were introduced.

---

## Building Blocks → Features (The Core Philosophy)

The reason this structure works is that **each lower tier is a verified building block** for everything above it. This is the monadic property: a function applied to a correct value produces a correct value.

```
a0  ←  pure data, zero logic, instantly testable
 ↓
a1  ←  pure functions on a0 data, no hidden state
 ↓
a2  ←  stateful classes wrapping verified a1 logic
 ↓
a3  ←  features assembled from verified a2 composites
 ↓
a4  ←  orchestrators wiring verified a3 features to the world
```

The discipline: **you never write logic at a4 that belongs in a1.** If you do, you've created untestable, un-reusable code that only works in one context. You've also made the next feature harder — because the building block you needed is buried in the wrong tier.

When a new feature is needed:
1. Identify what building blocks it needs (types, helpers, clients).
2. Check which tier each belongs to.
3. If a building block is missing, create it in the right tier first.
4. Compose those building blocks in a3 (or a4 for CLI).
5. Test each tier before moving to the next.

The result is that 500+ tests stay green across a growing multi-repo ecosystem because every layer was correct before the next layer was built. There is no heroic maintenance — just composition.

---

## Why This Matters

Break the law once and the tests will tell you. Break it quietly and you've introduced hidden coupling that costs hours to untangle later.

The goal isn't bureaucracy. It's that **every building block you write once becomes permanently available to everything above it** — with no duplication, no drift, no "which version of this function is the right one?"

---

## Applying This to Any Agent

When giving this file to any agent (Claude, Copilot, Gemini, Cursor, etc.), prepend:

> "You are working in an Atomadic project. Follow the monadic composition law in this file exactly. Before creating any new file, check `.ass-ade/tier-map.json`. Before writing any new logic, verify the building block does not already exist. Never import upward. Run `python -m pytest` before claiming done."

---

*This file lives at `C:\Users\atoma\.ass-ade\MONADIC_DEVELOPMENT.md`. Copy it to any project or agent context to propagate the standard.*
