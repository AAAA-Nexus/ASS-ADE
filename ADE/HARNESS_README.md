# ADE strict harness

The `ADE/` tree is a **hardened duplicate** of the canonical `agents/` swarm for stricter Cursor integration.

## What is wired

| Piece | Role |
|-------|------|
| [`harness/ade_hook_gate.py`](harness/ade_hook_gate.py) | CNA seed, `symbols.txt`, RULES, prompt-anchor checks; `context` / `verify` |
| [`.cursor/hooks/swarm_signal.py`](../../.cursor/hooks/swarm_signal.py) | Merges `ade_hook_gate.py context` into hook `additional_context` (unless `ADE_HARNESS=0`) |
| [`sync_ade_swarm_to_cursor.py`](sync_ade_swarm_to_cursor.py) | Writes `ade-*` bridges + `ade-pipeline-orchestrator.md` under `~/.cursor/agents/` |
| [`25-ade-harness-sentinel.prompt.md`](25-ade-harness-sentinel.prompt.md) | Extra agent **25** — preflight narration |
| [../../.cursor/rules/ade-harness.mdc](../../.cursor/rules/ade-harness.mdc) | Cursor rule when editing `ADE/**` |
| [../../.cursor/skills/ade-harness/SKILL.md](../../.cursor/skills/ade-harness/SKILL.md) | Operator skill |

## Commands

```bash
python ADE/harness/verify_ade_harness.py    # CI / gate — exit 1 on failure
python ADE/sync_ade_swarm_to_cursor.py      # refresh ~/.cursor/agents/ade-*.md
powershell -File scripts/sync_agents_to_ade.ps1   # copy agents/ → ADE/ (keeps harness/)
```

## Disable (emergency)

- `ADE_HARNESS=0` — skips ADE block in swarm hook (not for production lanes).
