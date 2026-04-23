# Swarm Signal Bus — Cursor Hook Layer

**One-paste (all IDEs + persistent orchestrator):** see repo root [`SWARM-ONE-PROMPT.md`](../../SWARM-ONE-PROMPT.md) and run `scripts/ensure_dev_session.ps1` before pasting.

This directory wires a filesystem-backed signal bus into the Cursor hook chain
so the orchestrator can broadcast reroutes, halts, and informational updates
to every agent in the swarm **between** their tool calls. The agent doesn't
have to remember to check for messages — the hook injects them automatically
as `additional_context` after every tool use.

## Files

| Path | Purpose |
|---|---|
| `.cursor/hooks.json` | Registers `check` on `sessionStart`, `postToolUse`, `subagentStart`. |
| `.cursor/hooks/swarm_signal.py` | Stdlib-only CLI + hook entry point; also merges **`ADE/harness/ade_hook_gate.py context`** into `additional_context` (disable with `ADE_HARNESS=0`). |
| `ADE/harness/ade_hook_gate.py` | Strict harness: RULES, ADE protocol files, prompt alignment; warns if `cna-seed.yaml` / `symbols.txt` missing unless `ADE_VERIFY_STRICT=1`. |
| `.cursor/hooks/swarm_scribe.py` | **Automated scribe** — hook lines + **messenger** (unread inbox snapshot) + `COORDINATION-PULSE.md` + `MASTER-SCRIBE-INDEX.md` refresh. |
| `.ato-plans/assclaw-v1/signals/` | Shared on-disk message store. |

The full-featured runtime companion (same on-disk format) may live under the
**ASS-ADE v1** tree (`ass-ade-v1/src/ass_ade/…`) as product code evolves; this
`.cursor/hooks` copy stays **stdlib-only** and workspace-local. Both agree on
the signal file format so the bootstrap swarm and the shipped product can
share the same wire protocol.

**Ship alignment:** [`ASS_ADE_SHIP_PLAN.md`](../../ASS_ADE_SHIP_PLAN.md),
[`docs/ATOMADIC_SWARM_SURFACE_AUDIT.md`](../../docs/ATOMADIC_SWARM_SURFACE_AUDIT.md).

## Per-tab setup (do this once when you open a Cursor tab)

In PowerShell:

```powershell
$env:SWARM_AGENT = "stream-A"        # or stream-B / stream-C / stream-D /
                                      # orchestrator / enhancement-planner /
                                      # parent
```

In bash (for anyone on WSL):

```bash
export SWARM_AGENT=stream-A
```

If unset, the hook reports signals as agent `anonymous`. Signals are still
delivered; per-agent delivery tracking just uses the slug `anonymous/`.

## Automated scribe (hook-driven)

Every hook invocation also runs `swarm_scribe.append_hook_event` with the same
stdin JSON Cursor sent. You get an append-only log at:

`.ato-plans/assclaw-v1/stream-reports/scribe/SCRIBE-<SWARM_AGENT>.md`

Mute scribe only: `$env:SWARM_SCRIBE_SILENT = "1"`.

### Manual digest (agent-authored)

Pipe markdown (or plain text) into the scribe without waiting for a hook:

```powershell
$env:SWARM_AGENT = "stream-C"
@'
## What we shipped today
- ...
'@ | python .cursor/hooks/swarm_scribe.py digest
```

This calls `append_manual_digest`, prefixes a `### Manual digest — <UTC>` heading,
appends to `SCRIBE-stream-C.md`, and triggers a master-index refresh (same
throttle rules as the automated refresh).

## CLI stdout encoding (Windows)

`swarm_signal.py` reconfigures **stdout/stderr to UTF-8** at the start of every
CLI run so `inbox` bodies with Unicode punctuation do not crash **cp1252**
consoles. No need to set `PYTHONUTF8=1` for swarm CLI commands.

## What agents see

After every tool call, if there are unread signals for `$SWARM_AGENT`, Cursor
surfaces something like:

```
[SWARM SIGNAL BUS] 1 unread signal for agent 'stream-A'

---  20260421T042127Z-P1-reroute-absorb-reranker-hook  (P1-reroute)  ---
  issued_by: orchestrator
  issued_at: 2026-04-21T04:21:27Z
  subject: Absorb T-A+3 reranker hook into A-03
  routes: ['stream-A']
  ack_required: True

A-03 must expose `binder._rerank(candidates, plan)` so Lane W's T-A+3
lands as a single-file additive PR ...

  >> ACK REQUIRED: run  python .cursor/hooks/swarm_signal.py ack --signal
     20260421T042127Z-P1-reroute-absorb-reranker-hook --note '<your note>'
```

A second tool call in the same turn returns `{}` (already delivered).

## Priorities

- **P0-halt** — stop current atom immediately, ack, wait for orchestrator.
- **P1-reroute** — new terrain; fold into current atom or start over with
  the updated plan. Ack required by convention.
- **P2-inform** — heads-up, no action required.
- **P3-fyi** — low-signal background noise.

Inbox ordering is strict by priority then signal id, so a P0 always renders
first.

## Publishing a signal (orchestrator only)

```powershell
$env:SWARM_AGENT = "orchestrator"

python .cursor/hooks/swarm_signal.py broadcast `
  --priority P1-reroute `
  --subject "Absorb T-A+3 reranker hook into A-03" `
  --routes "stream-A" `
  --ack-required `
  --body-file .\message.md
```

Body can be supplied three ways (first hit wins):
1. `--body-file PATH` — markdown file,
2. `--body "..."` — inline,
3. stdin (pipe when TTY is not a TTY).

Routing:
- `*` or `all` — everyone.
- Comma list, e.g. `stream-A,stream-B,enhancement-planner`.
- Exact, case-sensitive.

## Acknowledging

```powershell
python .cursor/hooks/swarm_signal.py ack `
  --signal 20260421T042127Z-P1-reroute-absorb-reranker-hook `
  --note "binder._rerank stub landed in commit 3f2a1; test green"
```

## Viewing state

```powershell
python .cursor/hooks/swarm_signal.py list    # every signal in the inbox
python .cursor/hooks/swarm_signal.py inbox   # unread for $SWARM_AGENT
Get-Content .ato-plans/assclaw-v1/signals/broadcast.log.jsonl | Select-Object -Last 20
```

## Debugging

- Hook failing closed? It doesn't — `check` swallows all exceptions and emits
  `{}` so the agent never gets bricked by a bus bug. Errors go to stderr and
  to the Cursor **Hooks** output channel.
- Temporarily mute the bus: set `$env:SWARM_HOOK_SILENT = "1"`. `check` emits
  `{}` regardless of inbox contents.
- Point at a different bus root: `$env:SWARM_SIGNAL_ROOT = "C:\path\to\dir"`.

## Safety posture

- Hooks fail **open** (exit 0, empty `{}` on any error). No bus failure can
  block a tool call.
- `broadcast` writes atomically (`write + os.replace`) so a partial file
  never appears in `inbox/`.
- Digest field in every signal is a short sha256 over `signal_id + subject +
  body + issued_by`. `parse_envelope` rejects mismatches — not cryptographic
  defense against a malicious orchestrator, but makes accidental corruption
  loud.
- Authentication: none in v1. `issued_by` is self-asserted. Internal swarm
  discipline is the source of trust. If we need real auth (to bridge public
  Cursor tabs and a CI runner), the Sovereign layer's session module is
  already specced — wire that in before shipping the bus externally.

## Persistent Python services (heartbeat + planner)

A **long-running** companion (stdlib-only) keeps terrain fresh, tracks
`tasks.json` completion, and can emit **P3-fyi** nudges on the same signal bus
hooks read every tool call:

| Command | Purpose |
|--------|---------|
| `python scripts/run_swarm_services.py run` | Loop until Ctrl+C: tick every `SWARM_TICK_SEC` (default 120s) |
| `python scripts/run_swarm_services.py once` | Single tick (cron / Task Scheduler) |
| `python scripts/run_swarm_services.py status` | Show nodes + which are **READY** (deps met, not done) |
| `python scripts/run_swarm_services.py task mark T3 done --note "…"` | Update `swarm_task_state.json` + append `evolution.log` |

**State files:**  
`.ato-plans/assclaw-v1/swarm_services/daemon_state.json` (tick / nudge dedup),  
`AUTOMATION-PULSE.md` (append-only log), and per-plan `swarm_task_state.json` next to `tasks.json`.

**Env (optional):** `SWARM_PLAN_DIR` (default `active/ass-ade-ship-nexus-github-20260422`), `SWARM_REGEN_DOCS` (1 = run `regenerate_ass_ade_docs` on interval), `SWARM_DOC_REGEN_SEC` (default 86400), `SWARM_BROADCAST_READY` (1 = P3 nudge for first **ready** node; cooldown `SWARM_NUDGE_COOLDOWN_SEC` per node), `SWARM_NUDGE_ROUTES` (default `orchestrator,parent`), `ATOMADIC_WORKSPACE` or `--repo`.

**Windows:** `powershell -NoProfile -File scripts/windows/run_swarm_services_loop.ps1` from repo root (or pass repo path as first arg).

Nudges are **P3** by default and respect a daily cap — they **do not** block work; for halts use `broadcast` with **P0** / **P1** as before.

## When the bus becomes ASS-ADE

The controller for `atomadic build/extend/reclaim` / unified CLI should call
the same coordinator between subagent batches; the hook UX the bootstrap swarm
sees here is what ASS-ADE operators should get at runtime. Track implementation
against `ASS_ADE_GOAL_PIPELINE.md` (Track P / governance hooks).
