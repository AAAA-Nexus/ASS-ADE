# Context pack — multiplan wave2 pilot (2026-04-22)

## What landed

- **`run_command`:** blocks `python -c`, `node -e`/`--eval`, NUL and newline-injected commands by default; override **`ASS_ADE_ALLOW_INLINE_RUN_COMMAND=1`** for local debugging only.
- **Tests:** `tests/test_mcp_privileged_builtin_tools.py` + `tests/test_tools_builtin.py` updates.
- **Docs / terrain:** `.ass-ade/specs/trust-gate-mcp-envelope.spec.md`, `terrain-index.v0.json` checklist, `CONTRIBUTING.md`, `README.md`.
- **GitHub:** issue templates + PR template; `epiphany-cycle` uses `--durations=20`.

## Verification

`pytest tests/` → **1273 passed**; `python scripts/atomadic_dev_harness.py --quick` → **10 passed**.

## Verdict

**PASS**
