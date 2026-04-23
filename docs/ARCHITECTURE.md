# ASS-ADE architecture (public tree)

## What this repository is

- **One Python distribution** (metadata in root [`pyproject.toml`](../pyproject.toml)): package name `ass-ade-v1-1`, import root **`ass_ade_v11`**.
- **Sources** live under [`ass-ade-v1.1/src/ass_ade_v11/`](../ass-ade-v1.1/src/ass_ade_v11/).
- **Primary CLI:** `ass-ade-unified` (and `ass-ade-v11` alias), defined in `[project.scripts]` in `pyproject.toml`.

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

- `ass-ade-unified doctor`
- `ass-ade-unified book rebuild …`
- `ass-ade-unified assimilate <primary> <out> [--also …] [--policy …]`

Golden behavior is covered in CI (`.github/workflows/ass-ade-ship.yml`).

## Tests and fixtures

- Tests: [`ass-ade-v1.1/tests/`](../ass-ade-v1.1/tests/)
- **dogfood** marker: long-running; excluded from default CI.
- **Synth-tests** manifest is checked in CI via `ass-ade-v11 synth-tests --check`.

## Related reading

- [ASS_ADE_UNIFICATION.md](ASS_ADE_UNIFICATION.md) — install modes and roadmap to one package name.
- [README — first run](PUBLIC_SHOWCASE_README.md#first-run)
