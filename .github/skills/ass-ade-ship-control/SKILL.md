---
name: ass-ade-ship-control
description: Maintain the ASS-ADE living plan, integrate research and dev breakthroughs, and run truthful private/public release gates.
argument-hint: "[breakthrough, blocker, research finding, or gate to update]"
---

# ASS-ADE Ship Control

Use this skill when the goal is to keep the ASS-ADE execution plan current, synthesize new evidence, or verify whether the system is actually ready to ship.

## Read first

- [`AGENTS.md`](../../../AGENTS.md)
- [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/plan.md`](../../../.ato-plans/active/ass-ade-ship-nexus-github-20260422/plan.md)
- [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/tasks.json`](../../../.ato-plans/active/ass-ade-ship-nexus-github-20260422/tasks.json)
- [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/research.md`](../../../.ato-plans/active/ass-ade-ship-nexus-github-20260422/research.md)
- [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/evolution.log`](../../../.ato-plans/active/ass-ade-ship-nexus-github-20260422/evolution.log)
- [`.ato-plans/active/ass-ade-ship-nexus-github-20260422/swarm-execution.md`](../../../.ato-plans/active/ass-ade-ship-nexus-github-20260422/swarm-execution.md)
- [`ASS_ADE_SHIP_PLAN.md`](../../../ASS_ADE_SHIP_PLAN.md)
- [`agents/ATO_DEV_ENVIRONMENT.md`](../../../agents/ATO_DEV_ENVIRONMENT.md)

## Procedure

1. Reconstruct the current state from repo evidence before making new claims.
2. For current or unstable facts, use official or primary sources and record the implication in `research.md`.
3. Update `plan.md`, `tasks.json`, `research.md`, and `evolution.log` together so the plan stays internally consistent.
4. Run truthful release gates instead of assuming green status from earlier work.
5. Keep `.github/copilot-instructions.md`, `.github/agents/`, `.github/skills/ass-ade-ship-control/`, `AGENTS.md`, and `agents/ATO_DEV_ENVIRONMENT.md` aligned.
6. Quarantine any unverified public claim, remote access assumption, or privileged MCP attachment.

## Verification commands

```bash
ass-ade doctor
python scripts/ship_readiness_audit.py
lint-imports
ass-ade book synth-tests --check --repo ass-ade-v1.1
python -m pytest ass-ade-v1.1/tests -m "not dogfood" -q
ass-ade ade ship-audit --staging-root C:\!aaaa-nexus\!ass-ade
```

## Expected outputs

- Updated living plan artifacts with an honest current verdict
- Any new research folded into `research.md`
- A clear next step for build, gate, or human follow-through
