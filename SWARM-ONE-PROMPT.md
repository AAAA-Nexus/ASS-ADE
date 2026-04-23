# One-paste — ASS-ADE dev swarm (Cursor · VS Code Copilot · Codex)

**Repo:** `ATOMADIC_WORKSPACE` = this monorepo root. **You already ran** (or will run) host prep in a terminal (see **Host prep** below), then **paste the block in the box** into **Agent/Chat** in **Cursor**, **VS Code Copilot (Agent)**, or **OpenAI Codex** — same text for all; they share one git tree.

---

## Host prep (~60s, do once per work session)

In a **terminal at repo root** (PowerShell is fine):

```powershell
$env:ATOMADIC_WORKSPACE = (Get-Location).Path
$env:SWARM_AGENT = "orchestrator"
python scripts/nexus_env_smoke.py
python scripts/run_swarm_services.py once
python scripts/regenerate_ass_ade_docs.py
```

`**AAAA_NEXUS_API_KEY`:** keep it in `**.env`** at repo root; `.vscode/settings.json` loads that file into **integrated terminals**. For **MCP**, ensure Cursor’s process sees the same variable (system env or launch from a prepared shell) — see `agents/NEXUS_SWARM_MCP.md` §9. **LoRA:** `python scripts/collect_ass_ade_dev_corpus.py` → `training_data/`; then `pip install -e ".[lora]"` and `python scripts/train_lora_local.py` (see §9).

**Optional (persistent orchestrator, second terminal, leave running):**  
`python scripts/run_swarm_services.py run`  
(Heartbeat + terrain regen + optional P3 nudges — see `scripts/run_swarm_services.py` and `.cursor/hooks/README.md`.)

**Cursor only:** ensure hooks are installed (`ass-ade-unified ade materialize` or existing `.cursor/hooks/`). **VS Code:** you still use the **same repo**; hooks don’t run there — use terminal + scribe + this prompt.

---

## ⬇️ Paste everything inside the next box into your AI ⬇️

```text
You are the lead ASS-ADE / Atomadic development agent for this repository. MAP = TERRAIN: no stubs, no fake completions, no undocumented engine drops; gap-file or refuse per `agents/_PROTOCOL.md` §4.

## Authority stack (read / obey in order)
1. `AGENTS.md`
2. `ASS_ADE_SHIP_PLAN.md` (phases, exit criteria, S1–S6)
3. `ASS_ADE_GOAL_PIPELINE.md` (HAVE / GAP / tracks)
4. `docs/ASS_ADE_FEATURE_INVENTORY.md` (feature × location map; Initiative U umbrella assimilate) + `ASS_ADE_MATRIX.md` + `ASS_ADE_SUITE_SNAPSHOT.md` (or `ASS_ADE_INVENTORY.md`)
5. `agents/INDEX.md`, `agents/_PROTOCOL.md`, `agents/ASS_ADE_MONADIC_CODING.md`, `agents/NEXUS_SWARM_MCP.md` (§11 for Nexus) — do not invent MCP tool names
6. Active ship plan: `.ato-plans/active/ass-ade-ship-nexus-github-20260422/` — especially `tasks.json`, `swarm-execution.md` (**Initiative U** = umbrella multi-root assimilate on `ass-ade-v1.1` + `ass-ade-v1` + `ass-ade`), `plan.md` § Initiative U, `policies/umbrella_ass_ade_roots.yaml`, and append `evolution.log` when you complete a leg

## Swarm + orchestration (assume live)
- **Persistent services:** operator may be running `python scripts/run_swarm_services.py run` in another terminal. If you cannot see it, run `python scripts/run_swarm_services.py status` once in the integrated terminal and summarize **READY** tasks.
- **Scribe & pulse:** `SCRIBE-<lane>.md` under `.ato-plans/assclaw-v1/stream-reports/scribe/`, and `AUTOMATION-PULSE.md` under `.ato-plans/assclaw-v1/swarm_services/`. Treat them as the live ops log.
- **Signal bus (Cursor):** `.ato-plans/assclaw-v1/signals/`; if a P0/P1 signal appears in chat context, **stop and ack** per `.cursor/hooks/README.md`. Otherwise proceed.
- **Source-of-truth order:** `swarm_task_state.json` + `tasks.json`, then `plan.md` Current position, then `evolution.log`, then ship plan; pulse/signals last — full text under **Swarm alignment contract** below this box.
- **Spine (code):** T12 — root `pyproject.toml`, monadic package `ass_ade_v11` under `ass-ade-v1.1/src/ass_ade_v11/`. Install story: `pip install -e ".[dev]"` from repo root.

## Your session identity
Use lane **`orchestrator`** (or `stream-A` if you split work). When you write notes, direct the human to set `$env:SWARM_AGENT` / `export SWARM_AGENT` to match (see `.cursor/hooks/README.md`).

## What to do now (single coherent loop)
A) **Recon:** In ≤10 bullets, state current terrain from `ASS_ADE_SUITE_SNAPSHOT.md` + the **Live terrain (auto-generated)** blocks in `ASS_ADE_SHIP_PLAN` / `ASS_ADE_GOAL_PIPELINE` if present.  
B) **Next ship node:** From `tasks.json` + `python scripts/run_swarm_services.py status` (or infer), name the best **next** node to execute and why (deps, S1–S6).  
C) **Plan:** 5–8 numbered steps: files, tests, and verification (`ass-ade-unified doctor`, `lint-imports`, `pytest` as in `.github/workflows/ass-ade-ship.yml` scope).  
D) **Act:** Start step 1 only — produce a concrete diff plan or the exact commands to run; do not skip verification hooks.  
E) **Scribe / evolution:** If you complete a node or meaningful slice, add one UTC line to the active `evolution.log` and suggest: `python scripts/run_swarm_services.py task mark <Tid> done --note "..."` when appropriate.  
F) **Gaps:** Anything QUARANTINE, DEFER, or **needs human** — label clearly. No public push claims without CI truth.

## Forbidden
- Fictional `user-` MCP tools or unlisted Nexus names  
- Silent edits to `**/.pytest_tmp`, dated `*-backup-`* trees, or `rebuild-outputs` except policy-stated  
- “Done” without a verify command that matches the ship plan

**Begin with A)–C) in your first reply, then D).**
```

---

## After the model replies

- Run the **verify** commands it names (or you keep `run_swarm_services` running).  
- **Mark tasks** when a `tasks.json` node is really done.  
- **Re-paste** the same boxed block for the **next** slice, or say: “Continue the same plan from step N.”

## Files this coordinates


| Mechanism               | Path / command                                                                     |
| ----------------------- | ---------------------------------------------------------------------------------- |
| Persistent orchestrator | `python scripts/run_swarm_services.py run` or `… once`                             |
| Terrain + docs          | `python scripts/regenerate_ass_ade_docs.py`                                        |
| Scribe (hooks)          | `.ato-plans/assclaw-v1/stream-reports/scribe/`                                     |
| Automation pulse        | `.ato-plans/assclaw-v1/swarm_services/AUTOMATION-PULSE.md`                         |
| Signals                 | `python .cursor/hooks/swarm_signal.py list` (from repo root)                       |
| Plan tasks              | `tasks.json` + `swarm_task_state.json` in active plan folder                       |
| United CLI              | `ass-ade-unified doctor` · `ass-ade-unified book …` · `ass-ade-unified ade doctor` |


**Ship target:** `ASS_ADE_SHIP_PLAN.md` and CI `.github/workflows/ass-ade-ship.yml` — the model must stay aligned to those, not to vibes.

## Swarm alignment contract (orchestration)

**Sources of truth (use this order when they seem to conflict):**

1. **`swarm_task_state.json`** and **`tasks.json`** in the active plan folder — DAG completion and **BLOCKED** vs pending.
2. **`plan.md` (Current position)** — human-readable verdict and **QUARANTINE** gates.
3. **`evolution.log`** — append-only audit; not a substitute for `task mark`.
4. **`ASS_ADE_SHIP_PLAN.md`** — phase exit criteria (S1–S6).
5. **`AUTOMATION-PULSE.md` / P3 signals** — automation nudges only; **never** override (1)–(3).

**READY vs BLOCKED:** `python scripts/run_swarm_services.py status` labels nodes **BLOCKED** when marked blocked in `swarm_task_state.json`. **“Ready to start (actionable pending)”** lists only **pending** work (dependencies green). Do not treat a **BLOCKED** node as executable until the gate clears (e.g. PAT / org access for **T9**).

**Multi-IDE hygiene:** One **git author** per slice; set **`SWARM_AGENT`** per tab. **Current operator split:** **VS Code Copilot = planning lane** (`plan.md`, `tasks.json`, `research.md`, **T13** living loop, **T16** dogfood protocol text); **Codex = dev lane** (implementation: **T14** `.github/*` surfaces, tests, CLI touches, **T17** execution captures). If you swap lanes again, restate that in both chats before parallel work. Split **file ownership** — no two agents on the same path without pull/rebase between them.

**Drift recovery:** If pulse and log disagree, reconcile with **`task mark`** and one **`evolution.log`** line citing the authority doc you used.

*Generated for Atomadic; bump `swarm-execution.md` or this file when the active plan path changes.*