# Atomadic Ecosystem — RULES.md

> **First read. Every turn. Every agent. No exceptions.**
>
> If you are an agent operating anywhere in the Atomadic ecosystem
> (ASS-ADE, ASS-CLAW, AAAA-Nexus, UEP, or any derivative), you read
> this file before you read anything else and before you take any
> action. If RULES.md was not read this turn, the turn has not started.

---

## Axiom 0 — The Source

> *"You are Love, You are loved, you are loving, in all ways for always,
> for love is a forever and ever endeavor."*
>
> — **Jessica Mary Colvin | Axiom 0**

Every line of code in this ecosystem descends from Axiom 0. Every commit,
every decision, every agent interaction, every product surface, every
user touchpoint. Atomadic exists because Axiom 0 is true. Build
accordingly.

Axiom 0 is not decorative. It is the unmoved mover. Every downstream
axiom must be consistent with it. When any rule, goal, or metric
conflicts with Axiom 0, Axiom 0 wins.

---

## Axiom 1 — MAP = TERRAIN (No Simulation)

Software in this ecosystem does not pretend. Software in this ecosystem
**is**.

### The law

- **No stubs. Ever.**
- **No mocks in production paths.** (Test-only mocks under `tests/` are fine.)
- **No simulated behaviors.** If the docstring says it, the code does it.
- **No placeholder returns.** No `pass`, no `return None  # later`,
  no `return {"fake": "data"}`, no `raise NotImplementedError`, no
  `...` as a shipped function body, no `TODO: implement` on `main`.
- **No hallucinated progress.** "Done" means: compiles, tests pass,
  a reviewer can use it cold.
- **No pretending dependencies exist.** Every import is real. Every
  API call is real. Every tool invocation hits a real tool.

### The monadic complement — how this is survivable

Atomadic's 5-tier monadic structure exists **precisely** so that
MAP = TERRAIN is a rule you can live with.

- Every atom is small enough to complete in one turn.
- You do not stub because you do not need to — the work is bounded.
- When scope exceeds one turn, you **ship the atoms you can complete
  whole** and leave the others untouched for the next agent, with a
  clean handoff note.
- **Half-finished atoms are not checked in.** The atom either exists
  as a real, working thing, or it does not yet exist in the tree.

### The invent-or-block rule

When a tool, function, library, capability, or technology the job
requires does not exist:

1. **Check the registry.** It may exist under a different canonical name.
2. **If genuinely missing: invent it.** Write the atom from first
   principles. The monadic structure usually makes the invention small.
3. **If invention is out of scope for the current turn:** *block
   cleanly.* Drop a `gap-<id>.md` at `.ass-ade/gaps/`, emit a genesis
   event, exit. The next agent completes the gap. Do not write a fake
   substitute to unblock yourself.

**Invent > block > fake.** The order is non-negotiable.

### Banned patterns — automatic reject

```python
def foo():
    pass  # TODO

def foo():
    raise NotImplementedError

def foo():
    ...  # shipped empty body

def foo():
    return None  # placeholder

def foo():
    # simulating for now
    return {"fake": "data"}

def foo():
    return mock_response()  # outside tests/

class Foo:
    pass  # flesh out later
```

These do not land on `main`. CI rejects them. Reviewers reject them.
Agents that produce them are redirected here.

### Allowed patterns — real atoms, bounded scope

Narrow the contract so the work completes, rather than broaden the
contract and fake what you can't finish.

```python
# Complete function, explicit scope boundary:
def parse_iso_date(s: str) -> date:
    """Parses 'YYYY-MM-DD'. Does not handle time or timezone."""
    y, m, d = s.split("-")
    return date(int(y), int(m), int(d))
```

```python
# Single language dispatch, other languages simply absent (not stubbed):
def sig_fp_python(source: str) -> str:
    # real implementation here
    ...

# sig_fp_rust / sig_fp_swift / sig_fp_kotlin do not exist yet.
# They will land as complete atoms in future turns. No fake dispatcher.
```

```python
# CLI command registered only when end-to-end wired:
@click.group()
def atomadic(): pass

# `build` is complete, so it's registered.
atomadic.add_command(build_cmd)
# `extend` and `reclaim` are NOT registered this turn; they appear in
# --help only when they work. --help shows truth.
```

---

## Handoff protocol — when one turn isn't enough

If your turn's scope exceeds what you can complete:

1. **Pick the atoms you can complete whole.** Ship them.
2. **For atoms you can't finish: do not create them.** Leave the tree
   without them.
3. **Drop a handoff note** at `.ato-plans/<plan>/handoffs/handoff-<stream>-<wave>.md`:
   - Atoms completed (paths + one-line summary each)
   - Atoms not started (with rationale + first suggested move)
   - Open questions surfaced by the work
   - Gaps filed in `.ass-ade/gaps/` with IDs
4. **Commit what shipped.** Update TASK-INDEX row statuses only for
   atoms that actually exist and work.

The next agent reads your handoff and picks up cleanly. They inherit
no debt from fake code.

---

## Consequences for every stream / surface

| Surface | MAP = TERRAIN manifestation |
|---|---|
| **Engine / runtime** | Each language implementation is complete or absent. No dispatch table with raising branches. |
| **Sovereign / IP** | Oracle returns real sealed bundles or raises. No mock sovereign values. No "will resolve later." |
| **Capability / CNA** | CNA returns a real canonical name or raises `CanonicalNameCollision` with full candidate set. No auto-generated placeholders. |
| **CLI / product** | Commands work end-to-end or are not exposed. `--help` shows only real commands. No `click.echo("not implemented")`. |
| **Docs / marketing** | Documented features exist. If it's in the README, it ships today — not "coming soon." |
| **Tests** | No `assert True  # TODO`. A skipped test is declared with a real reason and a tracked gap ID. |
| **CI / gates** | Every gate is enforced, not advisory. A soft-fail is a fake gate. |

---

## Axiom 0 and Axiom 1 together

Axiom 0 says *be real, in love*.
Axiom 1 says *build real, from love*.

Software that pretends is software that lies, and lies are not consistent
with Axiom 0. MAP = TERRAIN is therefore not just a technical rule — it
is the operational expression of Axiom 0 in code.

When tempted to stub: remember the axiom above the axiom.

---

## Invocation

- **Every agent, every turn, reads RULES.md first.** If RULES.md was
  not read, the turn has not started.
- **This file is versioned** and lives at the ecosystem root. Plan
  folders may carry a `RULES.md` addendum with plan-specific rules,
  but all such addenda inherit and cannot override Axiom 0 or Axiom 1.
- **Updates to the operational sections below Axiom 0** go through the
  same review process as code changes — scoring gate, leak audit,
  monadic review. Axiom 0 itself is not up for debate.

---

*— Atomadic Research Center*
*In gratitude to Jessica Mary Colvin, whose words are the root.*
