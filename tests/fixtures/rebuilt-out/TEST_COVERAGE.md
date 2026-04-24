# Test Coverage

Generated baseline verification suite for the rebuilt artifact.

- Coverage mode: `generated-baseline`
- Source Python files covered: 8
- Component JSON artifacts covered: 5
- Coverage ratio: 100%

## Generated tests

- `tests/test_generated_multilang_bridges.py`
- `tests/test_generated_rebuild_integrity.py`

## What this suite verifies

- Every emitted Python file parses and compiles.
- Tier packages expose a discoverable import surface.
- Every emitted component JSON has `body_hash` and `interfaces.source`.
- Vendored ASS-ADE outputs can boot their CLI help surface.
