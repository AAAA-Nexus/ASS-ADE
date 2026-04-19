# Contributing

## Philosophy

ASS-ADE follows the 5-tier monadic composition law. Every contribution must respect
the tier boundaries — a component at tier N may only depend on tiers below N.

## Tiers at a glance

| Folder | Tier | Rule |
|--------|------|------|
| `a0_qk_constants/` | qk | No imports from this repo. Pure constants/axioms only. |
| `a1_at_functions/` | at | May import qk. Pure functions, no I/O. |
| `a2_mo_composites/` | mo | May import at + qk. May hold state. |
| `a3_og_features/` | og | May import mo and below. I/O permitted. |
| `a4_sy_orchestration/` | sy | Top-level only. Wires og into pipelines. |

## Workflow

1. Write a blueprint first: `ass-ade design "My feature" --output ./blueprints`
2. Rebuild to materialize: `ass-ade rebuild . --output ./output`
3. Lint: `ass-ade lint ./output`
4. Certify: `ass-ade certify ./output`

## Code style

- Python 3.11+
- Ruff for linting and formatting (`ruff check . && ruff format .`)
- Pydantic models for all data structures
- Type hints required on all public APIs

## Tests

```bash
python -m pytest tests/ -q
```

All tests must pass before a PR is accepted.

## IP boundary

This is the public-safe shell of the Atomadic ecosystem. Do NOT add:
- Private prompt or orchestration internals
- Internal-only proof identifiers
- Hidden routing or pricing heuristics
- Private roadmap markers

## Rebuild baseline

This folder was built from `C:\!ass-ade` · rebuild `20260418_220755` · 2026-04-19.
