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

## More documentation

Optional depth for contributors and operators (the sections above stay the public showcase):

- **MAP = TERRAIN index:** `.ass-ade/terrain-index.v0.json`
- **Triple lane (expansion / evolution / promotion):** `docs/atomadic-triple-lane-handbook.md`
- **Release checklist:** `docs/RELEASE_CHECKLIST.md`
- **Nexus, trust surfaces, hosted MCP DEFER:** `docs/NEXUS_AND_TRUST_SURFACES.md`
- **Bounded Forge loop:** `docs/FORGE_NARROW_SLICE.md`

---

## Showcase: ASS-CLAW Merge-Rebuild Demo

ASS-ADE rebuilt three CLAW-ecosystem projects into a single certified monadic tree in a single command.

**Repos merged:**
| Repo | Stars | Notes |
|------|-------|-------|
| [OpenClaw](https://github.com/nicehash/OpenClaw) | 361 K ⭐ | Multi-platform 2D game engine, C++/Swift/Kotlin |
| ClawCode | — | Python-heavy, 6 circular import cycles, 214 KB monolith files |
| [Oh My Claude Code](https://github.com/nicehash/oh-my-claudecode) | 30 K ⭐ | TypeScript Claude Code config framework |

**Stats (2026-04-20):**

| Metric | Before | After |
|--------|--------|-------|
| Input files | 4,106 across 3 repos | — |
| Output components | — | **92,305** classified |
| Circular imports | 6 | **0** (dissolved by reconstruction) |
| Purity violations fixed | — | **8,257** |
| Audit pass rate | — | **100%** |
| Wall-clock time | — | **~24 min** |
| Certificate SHA-256 | — | `641257797f688d53...` |

**Tier distribution after merge:**

| Tier | Components |
|------|-----------|
| a0_qk_constants | 3,792 |
| a1_at_functions | 58,034 |
| a2_mo_composites | 11,571 |
| a3_og_features | 9,908 |
| a4_sy_orchestration | 8,272 |
| **Total** | **91,577** |

**Command used:**
```bash
ass-ade rebuild openclaw clawcode oh-my-claudecode \
  --output ASS-CLAW --yes --no-forge
```

### Reentrant Rebuild

The `feat/reentrant-rebuild-fix` branch enables **reentrant rebuilds** — you can now point ASS-ADE at its own output and rebuild it again. This unlocks infinite evolution loops: each pass can refine, re-classify, and re-certify the tree without manual intervention.

```bash
# Rebuild a previously rebuilt monadic tree (new capability)
ass-ade rebuild ./ASS-CLAW --output ./ASS-CLAW-v2

# Result: 729 source files → 2,399 components, 100% audit pass
```

Previously, the engine hard-skipped all tier-named directories
(`a0_qk_constants` through `a4_sy_orchestration`), making it impossible
to re-ingest a rebuilt tree. The fix makes tier-dir exclusion opt-in via
`ASS_ADE_SKIP_TIER_DIRS=1`.

---

## License

See `LICENSE`.
