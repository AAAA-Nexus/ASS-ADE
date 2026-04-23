# Copilot / Chat custom instructions (sample) — **copy** to `.github/copilot-instructions.md` or your org’s path

You are working in the **ASS-ADE (Atomadic)** monorepo. Obey these sources in order:

1. `AGENTS.md` at repo root
2. `ASS_ADE_SHIP_PLAN.md` and `ASS_ADE_GOAL_PIPELINE.md`
3. `agents/_PROTOCOL.md` and `agents/ASS_ADE_MONADIC_CODING.md` (CNA / monadic law)
4. `docs/ASS_ADE_UNIFICATION.md`

**MAP = TERRAIN:** do not ship stubs, fake “done” without tests, or undocumented `engine/*` drops. If blocked, list gaps and refuse.

**CLI (verify after edits):** from repo root with venv active — `ass-ade-unified doctor` · `pytest ass-ade-v1.1/tests` (or CI-equivalent) · `lint-imports` as configured.

**IDE:** this session may be VS Code (Copilot / Codex). Hooks under `.cursor/` are for Cursor; use the integrated terminal for `python .ade/persistent/run_swarm_services.py status` if `.ade` is materialized.
