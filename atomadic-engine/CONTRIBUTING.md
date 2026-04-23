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
