# ASS-ADE documentation

This folder is the **technical documentation hub** for the public ASS-ADE tree. Start with the [showcase README](PUBLIC_SHOWCASE_README.md) (copied to repository root `README.md` on GitHub), then use the index below for depth.

## Reading order

| Order | Document | What you get |
|------|----------|--------------|
| 1 | [PUBLIC_SHOWCASE_README.md](PUBLIC_SHOWCASE_README.md) | Install, first commands, CI, links |
| 2 | [ASS_ADE_UNIFICATION.md](ASS_ADE_UNIFICATION.md) | Single-spine packaging story, `ass-ade-unified`, materialize |
| 3 | [ARCHITECTURE.md](ARCHITECTURE.md) | Package layout, monadic tiers, where code lives |
| 4 | [ASS_ADE_SHIP_PLAN.md](../ASS_ADE_SHIP_PLAN.md) | Phased roadmap, exit criteria S1–S6 |
| 5 | [ASS_ADE_GOAL_PIPELINE.md](../ASS_ADE_GOAL_PIPELINE.md) | HAVE / GAP / IMPLEMENT checklist |
| 6 | [ASS_ADE_SPINE_RFC.md](ASS_ADE_SPINE_RFC.md) | Roles across trees (full workspace vs this repo) |
| 7 | [ASS_ADE_FORGE_CLI.md](ASS_ADE_FORGE_CLI.md) | Forge / dispatcher sketch |
| 8 | [EMITTER_PARITY.md](EMITTER_PARITY.md) | Emitter parity notes |
| 9 | [ATOMADIC_SWARM_SURFACE_AUDIT.md](ATOMADIC_SWARM_SURFACE_AUDIT.md) | IDE / hooks / agents surface audit |

## Specifications and schemas

| Path | Purpose |
|------|---------|
| [`ass-ade-v1.1/.ass-ade/specs/`](../ass-ade-v1.1/.ass-ade/specs/) | JSON Schemas for assimilate policy and plan artifacts |

## Operator surfaces (repository root)

| File | Purpose |
|------|---------|
| [`AGENTS.md`](../AGENTS.md) | Agent protocol, hooks, operator map |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | Hygiene, validation, how to contribute |
| [`SECURITY.md`](../SECURITY.md) | Disclosure |
| [`ASS_ADE_MATRIX.md`](../ASS_ADE_MATRIX.md) | Capability matrix |

## ADE strict harness (repo root)

The [`ADE/`](../ADE/) directory holds the duplicated **ADE** prompt stack and `harness/` gates used by CI (`ass-ade-ship` workflow).

## Public vs full workspace

Some documents mention sibling trees (`ass-ade-v1`, `ass-ade`, `!atomadic-uep`) that exist in a **private Atomadic umbrella** but **are not shipped** in this public repository. This repo ships the **monadic spine** under `ass-ade-v1.1/` and root `pyproject.toml`. See the callout at the top of [ASS_ADE_SPINE_RFC.md](ASS_ADE_SPINE_RFC.md).
