# ASS-ADE architecture (public tree)

## What this repository is

- **One Python distribution** (metadata in root [`pyproject.toml`](../pyproject.toml)): package name `ass-ade`.
- **Two import roots in one checkout:**
  - **`ass_ade_v11`** under [`ass-ade-v1.1/src/ass_ade_v11/`](../ass-ade-v1.1/src/ass_ade_v11/) for the monadic CNA spine.
  - **`ass_ade`** under [`atomadic-engine/src/ass_ade/`](../atomadic-engine/src/ass_ade/) for the restored Atomadic engine shell and legacy rebuild surface.
- **Primary CLI:** `ass-ade`, defined in `[project.scripts]` in `pyproject.toml`.
- **Alias:** `atomadic` resolves to the same merged CLI for operator muscle memory.

## Monadic tiers (import law)

Code is organized in **five tiers** (a0 → a4). Higher tiers may import lower tiers; the reverse is forbidden. CI enforces this with **import-linter**; contracts are declared in `pyproject.toml` under `[tool.importlinter]`.

| Tier | Package segment | Role (short) |
|------|-----------------|--------------|
| a0 | `ass_ade_v11.a0_qk_constants` | Constants / QK |
| a1 | `ass_ade_v11.a1_at_functions` | Pure functions |
| a2 | `ass_ade_v11.a2_mo_composites` | Stateful composites |
| a3 | `ass_ade_v11.a3_og_features` | Features |
| a4 | `ass_ade_v11.a4_sy_orchestration` | Orchestration, CLI entry |
| ade | `ass_ade_v11.ade` | Cross-IDE materializer, discover (stdlib-oriented) |

The **`ade`** subtree ships **materialize** and related operator tooling so consumers can mirror hooks and cross-IDE samples into a target workspace. See [`ASS_ADE_UNIFICATION.md`](ASS_ADE_UNIFICATION.md).

## Book pipeline

The phased **book** (recon through package) is the core assimilation spine. Operators typically use:

- `ass-ade doctor`
- `ass-ade rebuild ...`
- `ass-ade book rebuild ...`
- `ass-ade assimilate <primary> <out> [--also ...] [--policy ...]`

Golden behavior is covered in CI (`.github/workflows/ass-ade-ship.yml`).

## Restored Atomadic Engine

The broad `ass_ade` surface is vendored in [`atomadic-engine/`](../atomadic-engine/) so one editable install no longer depends on a sibling checkout or a machine-wide `C:\!atomadic` package. This subtree owns:

- `ass_ade.cli` - broad Typer shell flattened into `ass-ade` and aliased by `atomadic`
- `ass_ade.engine.rebuild` - legacy local rebuild engine and emitters
- `ass_ade.nexus` - typed AAAA-Nexus client, validation, sessions, x402 primitives
- `ass_ade.mcp` - local MCP server and remote MCP helpers
- `ass_ade.a2a`, `ass_ade.agent`, `ass_ade.tools`, `ass_ade.local` - A2A, agent loop, tools, docs/certify/lint/enhance surfaces

Long-term architecture still moves reusable rebuild emitters into `ass_ade_v11` tiers. Until then, `atomadic-engine` is the runtime compatibility surface, not a separate product.

## Tests and fixtures

- Spine tests: [`ass-ade-v1.1/tests/`](../ass-ade-v1.1/tests/)
- Engine tests: [`atomadic-engine/tests/`](../atomadic-engine/tests/)
- **dogfood** marker: long-running; excluded from default CI.
- **Synth-tests** manifest is checked in CI via `ass-ade book synth-tests --check`.

## Related reading

- [ONE_WORKING_PRODUCT.md](ONE_WORKING_PRODUCT.md) — current trunk decision and source roles.
- [ASS_ADE_UNIFICATION.md](ASS_ADE_UNIFICATION.md) — install modes and roadmap to one package name.
- [README — first run](PUBLIC_SHOWCASE_README.md#first-run)
