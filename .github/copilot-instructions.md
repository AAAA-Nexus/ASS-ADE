# ASS-ADE repository instructions

Use this file as the repo-wide orientation layer. The canonical agent brief is [`AGENTS.md`](../AGENTS.md), and the active execution plan lives in [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/`](../.ato-plans/active/ass-ade-ship-nexus-github-20260422/).

## Read first

- [`AGENTS.md`](../AGENTS.md)
- [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/plan.md`](../.ato-plans/active/ass-ade-ship-nexus-github-20260422/plan.md)
- [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/tasks.json`](../.ato-plans/active/ass-ade-ship-nexus-github-20260422/tasks.json)
- [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/research.md`](../.ato-plans/active/ass-ade-ship-nexus-github-20260422/research.md)
- [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/evolution.log`](../.ato-plans/active/ass-ade-ship-nexus-github-20260422/evolution.log)
- [`ASS_ADE_SHIP_PLAN.md`](../ASS_ADE_SHIP_PLAN.md)
- [`ASS_ADE_GOAL_PIPELINE.md`](../ASS_ADE_GOAL_PIPELINE.md)
- [`SWARM-ONE-PROMPT.md`](../SWARM-ONE-PROMPT.md)
- [`agents/_PROTOCOL.md`](../agents/_PROTOCOL.md)
- [`agents/ASS_ADE_MONADIC_CODING.md`](../agents/ASS_ADE_MONADIC_CODING.md)
- [`agents/ATO_DEV_ENVIRONMENT.md`](../agents/ATO_DEV_ENVIRONMENT.md)

## Non-negotiables

- MAP = TERRAIN. Do not claim a pass, push, or integration that was not verified.
- New monadic Python work belongs under the ASS-ADE monadic source path `ass-ade-v1.1/src/ass_ade_v11/` unless the task is explicitly engine work.
- `C:\!atomadic` is private development terrain. Do not treat it as the public push surface.
- Public release readiness requires both the private spine gate and the public staging gate.
- Whenever project state changes materially, update `plan.md`, `tasks.json`, `research.md`, and `evolution.log` together.
- For unstable or current facts, use official primary documentation and quarantine anything unverified.
- Respect the source-of-truth order from `SWARM-ONE-PROMPT.md`: `swarm_task_state.json` + `tasks.json`, then `plan.md`, then `evolution.log`, then the ship plan, then automation pulse/signals.

## Current operator split

- Copilot owns the **living-plan lane** for this phase: keep `plan.md`, `tasks.json`, `research.md`, `swarm-execution.md`, and `evolution.log` truthful and aligned.
- Codex owns the **development lane** for this phase: product changes, staging alignment work, and transcript-backed CLI UX dogfood execution.
- If a task mixes both lanes, keep Copilot on planning truth and hand implementation or runtime evidence capture back to Codex.

## Verification commands

```bash
ass-ade doctor
python scripts/ship_readiness_audit.py
lint-imports
ass-ade book synth-tests --check --repo ass-ade-v1.1
python -m pytest ass-ade-v1.1/tests -m "not dogfood" -q
ass-ade ade ship-audit --staging-root C:\!aaaa-nexus\!ass-ade
```

## Alignment rule

Keep this file, [`.github/agents/`](./agents/), [`.github/skills/ass-ade-ship-control/`](./skills/ass-ade-ship-control/), [`AGENTS.md`](../AGENTS.md), and [`agents/ATO_DEV_ENVIRONMENT.md`](../agents/ATO_DEV_ENVIRONMENT.md) aligned with the active plan.
