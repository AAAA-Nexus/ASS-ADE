<pre>
    ___   _____ _____       ___   ____  ___
   /   | / ___// ___/      /   | / __ \/ __/
  / /| | \__ \ \__ \______/ /| |/ / / / /_ 
 / ___ |___/ /___/ /_____/ ___ / /_/ / __/ 
/_/  |_/____//____/     /_/  |_|\____/_/   

  Autonomous Sovereign System — Atomadic Development Environment
  Blueprint is truth. Code is artifact.
</pre>

[![Version](https://img.shields.io/badge/version-1.1.0a1-blue)](pyproject.toml)
[![License](https://img.shields.io/badge/license-Proprietary-orange)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](pyproject.toml)

> **This is the public staging release of ASS-ADE v1.1.0a1.**
> 
> - All code, docs, and CI are scrubbed and verified for public release.
> - The canonical source and blueprint remain in the private Atomadic workspace.
> - See below for install, usage, and architecture.

---

# Atomadic workspace (`c:\!atomadic`)

This directory is the **private development sandbox** for Atomadic IDE / ASS-ADE,
ASS-CLAW, and related evolution trees. It is **not** always a single Git
repository: many subfolders are independent trees or backups. Treat
**`ass-ade\`** as the canonical ASS-ADE source home for shipping work.

## ASS-ADE ship track (CI + install)

- **Local “run until green” loop (no Cursor required):** double-click [`ENTER-SHIP-LOOP.cmd`](ENTER-SHIP-LOOP.cmd) (or run `scripts\swarm-ship-loop.ps1 -UntilGreen`). Logs under `logs/`; does **not** `git push` — see IP wall below for `!aaaa-nexus` staging.
- **Single editable install (spine):** from this directory, `pip install -e ".[dev]"` (see root `pyproject.toml` and [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/README.ship.md`](.ato-plans/active/ass-ade-ship-nexus-github-20260422/README.ship.md)).
- **CI:** [`.github/workflows/ass-ade-ship.yml`](.github/workflows/ass-ade-ship.yml) — `lint-imports`, `pytest ass-ade-v1.1/tests -m "not dogfood"`, golden `assimilate` on `minimal_pkg` with **`book.json` + `ASSIMILATE_PLAN.json`** artifacts (Ubuntu, Python 3.12).
- **Staging handoff gate:** `ass-ade-unified ade ship-audit --staging-root C:\!aaaa-nexus\!ass-ade` verifies the scrubbed checkout is git-backed, clean, and still mirrors the private ship surface before any public push.
- **Copilot / VS Code control surfaces:** [`.github/copilot-instructions.md`](.github/copilot-instructions.md), [`.github/agents/`](.github/agents), and [`.github/skills/ass-ade-ship-control/`](.github/skills/ass-ade-ship-control) keep repo-side agents aligned with the active ASS-ADE ship plan.
- **Hygiene:** [`CONTRIBUTING.md`](CONTRIBUTING.md) (temp dirs, backups, install).
- **Full ship plan:** [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/plan.md`](.ato-plans/active/ass-ade-ship-nexus-github-20260422/plan.md). Public GitHub org target is **QUARANTINE** until credentials are verified ([`research.md`](.ato-plans/active/ass-ade-ship-nexus-github-20260422/research.md) `[Q-GH-1]`).

## Start here

| Document | Purpose |
|----------|---------|
| [`RULES.md`](RULES.md) | Axiom 0 + MAP = TERRAIN (global) |
| [`ass-ade/README.md`](ass-ade/README.md) | ASS-ADE setup, tests, CLI entrypoint |
| [`.ato-plans/assclaw-v1/RULES.md`](.ato-plans/assclaw-v1/RULES.md) | Plan-specific rules for ASS-CLAW v1 |
| [`.ato-plans/assclaw-v1/PRODUCTION-ORCHESTRATION.md`](.ato-plans/assclaw-v1/PRODUCTION-ORCHESTRATION.md) | **Release playbook:** polish → docs → GitHub → branches → live tests → ASS-CLAW merge |
| [`.ato-plans/assclaw-v1/TASK-INDEX.md`](.ato-plans/assclaw-v1/TASK-INDEX.md) | Live task matrix |

## Git and GitHub

Initialize or use a **dedicated clone** of the target GitHub repo (e.g. ASS-ADE
on the org remote). This workspace root often has **no `.git`**; branch hygiene
and release tags are applied **inside that clone**. See
`PRODUCTION-ORCHESTRATION.md` §5 and `tools/git-evolution-branches.ps1`.

### IP wall — **`C:\!atomadic` is private dev only**

- **`C:\!atomadic`** — IP-sensitive Atomadic **development** workspace. **Never** treat this tree as the thing you `git push` to a public GitHub remote.
- **`C:\!aaaa-nexus`** — **Public** staging home: scrubbed, shippable artifacts (e.g. completed ASS-ADE) live here before publication.
- **Ship flow:** finish and verify ASS-ADE under `!atomadic` → **move** (export/copy per Stream B scrub policy) the production-ready tree into the correct path under **`!aaaa-nexus`** → run **`git push` to GitHub only from that `!aaaa-nexus` checkout**, never from `!atomadic`.

Details: [`ass-ade/README.md`](ass-ade/README.md) §IP rules and Stream B export pipeline.

## License

Proprietary unless a subfolder states otherwise. Public surfaces follow the
**`!aaaa-nexus`** staging rule above (see `ass-ade/README.md` IP section).
