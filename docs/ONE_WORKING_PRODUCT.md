# One Working Product Plan

Status: active consolidation plan for `C:\!aaaa-nexus\!ass-ade`.

## Decision

The product trunk is this checkout:

- `C:\!aaaa-nexus\!ass-ade`

The trunk now contains both runtime lines in one install:

- `ass-ade-v1.1/src/ass_ade_v11/` - monadic CNA spine, `book`, `assimilate`, policy and plan artifacts, ADE materializer.
- `atomadic-engine/src/ass_ade/` - restored Atomadic engine shell, broad Typer CLI, local rebuild engine, Nexus client, MCP, A2A, agent loop, docs/certify/lint/enhance surfaces.

Everything outside this trunk is a donor, archive, or quarantine input. Do not edit another ASS-ADE folder as the product unless this document is changed first.

## Source Roles

| Path | Role | Use |
|------|------|-----|
| `!ass-ade/` | product trunk | Build, test, document, and ship from here. |
| `!ass-ade/ass-ade-v1.1/` | monadic spine | New CNA/pipeline work goes here. |
| `!ass-ade/atomadic-engine/` | restored engine | Legacy `ass_ade` CLI, rebuild, Nexus, MCP, A2A, agent and local tooling. |
| `ass-ade-fix/` | clean donor | Already copied into `atomadic-engine`; use for diff/reference only. |
| `QUARANTINE_IP_LEAK_v20/` | quarantine donor | Compare rebuild emitters only after IP/scrub review. |
| `ass-ade-final-release*`, `assimilated_ade/` | generated artifacts | Evidence only. Not source of truth until imports/tests pass. |
| `ASS-CLAW*`, `ass-claw-repos/` | separate product inputs | Do not merge automatically into ASS-ADE core. |
| `!ass-ade-control/`, `!ass-ade-cursor-dev-*` | audit/staging records | Useful inventory and merge history; not runtime source. |

## Commands

From `C:\!aaaa-nexus\!ass-ade`:

```text
pip install -e ".[dev]"
ass-ade --help
ass-ade doctor
ass-ade rebuild --help
ass-ade book rebuild --help
ass-ade assimilate PRIMARY OUT --also SIBLING --policy POLICY.yaml
atomadic --help
```

`ass-ade doctor` must show `ass_ade` resolving from:

```text
C:\!aaaa-nexus\!ass-ade\atomadic-engine\src\ass_ade
```

If it resolves from `C:\!atomadic` or another sibling, the environment is leaking an external install and the test is not trustworthy.

Read-only duplicate install checks:

```text
where ass-ade
python -m pip list | findstr /I "ass atomadic"
python -m pip show ass-ade
python -c "import ass_ade; print(ass_ade.__file__)"
```

The `ass-ade` CLI wrapper forces the bundled engine for CLI commands. Raw Python imports can still be affected by old editable `.pth` files; capture the paths before uninstalling or deleting anything. See [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md).

## Current Product Surface

| Surface | Package | Entrypoint |
|---------|---------|------------|
| Unified operator CLI | `ass_ade_v11` + `ass_ade` | `ass-ade` |
| Book phases 0-7 | `ass_ade_v11` | `ass-ade book ...` |
| Multi-root assimilate | `ass_ade_v11` | `ass-ade assimilate ...` |
| ADE materializer | `ass_ade_v11.ade` | `ass-ade ade ...` |
| Atomadic shell | `ass_ade` | `ass-ade ...` / `atomadic ...` |
| Legacy rebuild engine | `ass_ade.engine.rebuild` | `ass-ade rebuild ...` |
| Nexus/MCP/A2A/agent shell | `ass_ade` | `ass-ade nexus/mcp/a2a/agent ...` |

## Next Consolidation Work

1. Keep `atomadic-engine` green as a vendored engine subtree; do not copy new code from generated tier folders.
2. Port high-value `ass_ade.engine.rebuild` emitters into `ass_ade_v11` using `docs/EMITTER_PARITY.md`.
3. Add a checked multi-root golden fixture that exercises `ass_ade_v11` plus `atomadic-engine` with a policy file.
4. Resolve package-name strategy: keep `ass_ade_v11` as spine for this release, then plan the later major rename to `ass_ade`.
5. Treat quarantine code as evidence until a scrubbed diff is reviewed and tests prove the gain.

## Definition Of Done

- One checkout installs with `pip install -e ".[dev]"`.
- `ass-ade doctor` reports both packages from this checkout.
- `pytest ass-ade-v1.1/tests -m "not dogfood"` passes.
- `pytest atomadic-engine/tests` has a known, shrinking failure list or passes.
- Docs, matrix, and ship plan name `!ass-ade` as the only product trunk.
