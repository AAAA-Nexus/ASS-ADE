# Contributing to ASS-ADE

## CI label lanes (optional)

Pull requests that only need a **fast MCP + monadic + demos gate** (not the full `tests/` suite on every push) can add one of:

- **`ass-ade-blueprint`** — blueprint / design-heavy changes.
- **`ass-ade-feature`** — feature implementation slices.

When either label is present, workflow **`pr-labeled-ass-ade-smoke`** runs `check_evolution_context.py` (with PR git range) plus a narrow pytest set. Remove the label or push commits without the label to skip that job on the next run.

## Local harness (no MCP)

From the repo root with dev extras installed:

```bash
python scripts/atomadic_dev_harness.py --quick
python scripts/atomadic_dev_harness.py --full
python scripts/atomadic_dev_harness.py --evolution-only
```

## Monadic law

See `.ass-ade/tier-map.json` and `AGENTS.md` — no upward imports between tiers; extend existing packages (MAP = TERRAIN) before adding parallel registries.

## Canonical terrain index

The extension map (MCP manifest, autonomous JSON, context-pack gate, demos) lives in `.ass-ade/terrain-index.v0.json` — extend that index before adding parallel “source of truth” files.

## Local pytest on Windows

Occasionally pytest prints a benign `PermissionError` while cleaning `pytest-of-*` temp dirs on Windows; the process **exit code** should still be **0** when tests passed. For slow-test signal locally, use `pytest tests/ --durations=20` (CI: `epiphany-cycle` and `perf-durations.yml`).

## MCP `run_command` safety

Built-in `run_command` uses an executable allowlist, `shell=False`, and **blocks** `python -c` / `node -e` by default (use workspace script files). Local override **only** for debugging: `ASS_ADE_ALLOW_INLINE_RUN_COMMAND=1`.

## Nexus / doctor (billing and probes)

`ass-ade doctor` stays **local-by-default** (no automatic remote Nexus probe). Explicit `--remote`, hybrid profile behavior, and env-key cases are covered in `tests/test_cli.py` (`test_doctor_*`).
