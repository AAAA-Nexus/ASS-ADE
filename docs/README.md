# ASS-ADE documentation

This folder is the **technical documentation hub** for the public ASS-ADE tree. Start with the [showcase README](PUBLIC_SHOWCASE_README.md) (copied to repository root `README.md` on GitHub), then use the index below for depth.

## Reading order

| Order | Document | What you get |
|------|----------|--------------|
| 0 | [ONE_WORKING_PRODUCT.md](ONE_WORKING_PRODUCT.md) | **Current trunk decision**: what is product, donor, quarantine, or archive |
| 1 | [ASS_ADE_FEATURE_INVENTORY.md](ASS_ADE_FEATURE_INVENTORY.md) | **Deep feature x location map** for the single trunk |
| 2 | [PUBLIC_SHOWCASE_README.md](PUBLIC_SHOWCASE_README.md) | Install, first commands, CI, links |
| 3 | [ASS_ADE_UNIFICATION.md](ASS_ADE_UNIFICATION.md) | Single-product packaging story, `ass-ade`, materialize |
| 4 | [ARCHITECTURE.md](ARCHITECTURE.md) | Package layout, monadic tiers, restored engine |
| 5 | [ASS_ADE_SHIP_PLAN.md](../ASS_ADE_SHIP_PLAN.md) | Phased roadmap, exit criteria S1–S6 |
| 6 | [ASS_ADE_GOAL_PIPELINE.md](../ASS_ADE_GOAL_PIPELINE.md) | HAVE / GAP / IMPLEMENT checklist |
| 7 | [ASS_ADE_SPINE_RFC.md](ASS_ADE_SPINE_RFC.md) | Roles across trees (full workspace vs this repo) |
| 8 | [ASS_ADE_FORGE_CLI.md](ASS_ADE_FORGE_CLI.md) | Forge / dispatcher sketch |
| 9 | [EMITTER_PARITY.md](EMITTER_PARITY.md) | Emitter parity notes |
| 10 | [ATOMADIC_SWARM_SURFACE_AUDIT.md](ATOMADIC_SWARM_SURFACE_AUDIT.md) | IDE / hooks / agents surface audit |
| 11 | [CURSOR_AGENT_LANES.md](CURSOR_AGENT_LANES.md) | Four tiny Cursor-safe cleanup lanes |
| 12 | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Stale editable install checks |

## Specifications and schemas

| Path | Purpose |
|------|---------|
| [`ass-ade-v1.1/.ass-ade/specs/`](../ass-ade-v1.1/.ass-ade/specs/) | JSON Schemas for assimilate policy and plan artifacts |
| [`atomadic-engine/.ass-ade/tier-map.json`](../atomadic-engine/.ass-ade/tier-map.json) | Legacy engine tier map and ratchet baseline |

## Operator surfaces (repository root)

| File | Purpose |
|------|---------|
| [`AGENTS.md`](../AGENTS.md) | Agent protocol, hooks, operator map |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | Hygiene, validation, how to contribute |
| [`SECURITY.md`](../SECURITY.md) | Disclosure |
| [`ASS_ADE_MATRIX.md`](../ASS_ADE_MATRIX.md) | Capability matrix |
| [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md) | Duplicate install and environment troubleshooting |

## ADE strict harness (repo root)

The [`ADE/`](../ADE/) directory holds the duplicated **ADE** prompt stack and `harness/` gates used by CI (`ass-ade-ship` workflow).

## Public vs full workspace

Some older documents mention sibling trees (`ass-ade-v1`, `ass-ade`, `!atomadic-uep`) from the private Atomadic umbrella. The current product trunk is this checkout: `ass-ade-v1.1/` plus `atomadic-engine/`, wired by the root `pyproject.toml`. See [ONE_WORKING_PRODUCT.md](ONE_WORKING_PRODUCT.md) before editing any sibling folder.
