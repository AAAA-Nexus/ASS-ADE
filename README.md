# ASS-ADE — Autonomous Sovereign System: Atomadic Development Environment

A monadic, tier-composed Python framework for building and operating Atomadic AI agents, MCP servers, A2A pipelines, and autonomous orchestration harnesses.

---

## Install

```bash
pip install -e ".[dev]"
```

Requires Python ≥ 3.11.

## Quickstart

```bash
# Verify the install
ass-ade --help

# Run the fast preflight gate
python scripts/atomadic_dev_harness.py --quick

# Run the full suite
python scripts/atomadic_dev_harness.py --full
```

## Run tests

```bash
pytest                      # 366 test functions across 65 files
pytest tests/test_cli.py    # single module
```

## Architecture — 5-Tier Monadic Law

Every source file belongs to exactly one tier. Tiers compose **upward only** — never downward or sideways.

| Tier | Directory | What lives here | Allowed imports |
|------|-----------|-----------------|-----------------|
| a0 | `a0_qk_constants/` | Constants, enums, TypedDicts, config dataclasses. Zero logic. | Nothing |
| a1 | `a1_at_functions/` | Pure stateless functions — validators, parsers, formatters | a0 only |
| a2 | `a2_mo_composites/` | Stateful classes, clients, registries, repositories | a0, a1 |
| a3 | `a3_og_features/` | Feature modules combining composites into capabilities | a0–a2 |
| a4 | `a4_sy_orchestration/` | CLI commands, entry points, top-level orchestrators | a0–a3 |

The canonical tier classification lives in `.ass-ade/tier-map.json`. Always read it before creating new files.

## Key subsystems

| Path | Purpose |
|------|---------|
| `src/ass_ade/cli.py` | Typer CLI entry point (`ass-ade`) |
| `src/ass_ade/mcp/` | MCP server integration |
| `src/ass_ade/a2a/` | Agent-to-Agent protocol handlers |
| `src/ass_ade/aso/` | Autonomous Sovereign Orchestration |
| `src/ass_ade/agent/` | Agent runtime and lifecycle |
| `src/ass_ade/engine/` | Core execution engine |
| `a3_og_features/` | Assembled feature pipelines |
| `a4_sy_orchestration/` | CLI commands and top-level runners |
| `benchmarks/` | Performance benchmarks |
| `harnesses/` | Integration test harnesses |
| `scripts/atomadic_dev_harness.py` | Local preflight / CI gate |

## Contributing

See `CONTRIBUTING.md` for CI label lanes (`ass-ade-blueprint`, `ass-ade-feature`) and local preflight instructions.

The monadic law is enforced: no upward imports between tiers. Before adding new logic, run `ass-ade map-terrain` to confirm the capability does not already exist.

## License

See `LICENSE`.
