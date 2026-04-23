# ASS-ADE

<pre>
    ___   _____ _____       ___   ____  ___
   /   | / ___// ___/      /   | / __ \/ __/
  / /| | \__ \ \__ \______/ /| |/ / / / /_
 / ___ |___/ /___/ /_____/ ___ / /_/ / __/
/_/  |_/____//____/     /_/  |_|\____/_/
</pre>

[![CI](https://github.com/AAAA-Nexus/ASS-ADE/actions/workflows/ass-ade-ship.yml/badge.svg)](https://github.com/AAAA-Nexus/ASS-ADE/actions/workflows/ass-ade-ship.yml)
[![Version](https://img.shields.io/badge/version-1.1.0a3-blue)](pyproject.toml)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](pyproject.toml)
[![License](https://img.shields.io/badge/license-Proprietary-orange)](LICENSE)

**ASS-ADE** is the Autonomous Sovereign System: Atomadic Development Environment. This public repository ships the **monadic CNA spine** for turning messy Python estates into a policy-audited, testable package through one operator surface: **`ass-ade-unified`**.

The release tree is intentionally scrubbed for public consumption. Host-specific development layout, secrets, and private workspace scaffolding are kept out of this repository.

## What Ships Here

- **Unified CLI:** `ass-ade-unified` for doctoring, phased book runs, and release-facing operator flows.
- **Multi-root assimilation:** `assimilate` can take a primary source root plus sibling roots and emit a single monadic output.
- **Phased rebuild spine:** book phases 0-7, import-law enforcement, synth-tests, and golden fixtures.
- **Agent-ready ADE surfaces:** the repo carries the monadic ASS-ADE spine plus optional IDE / MCP materializer surfaces used by the broader Atomadic stack.

## Install

**Requirements:** Python **3.12+** and git.

```bash
git clone https://github.com/AAAA-Nexus/ASS-ADE.git
cd ASS-ADE
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate
pip install -e ".[dev]"
```

`[dev]` installs the validation and test stack used by the public release path: **pytest**, **import-linter**, **PyYAML**, and **jsonschema**. If you only need the CLI, `pip install -e .` is enough.

**Optional local LoRA extras:** `pip install -e ".[lora]"`.

## First Run

```bash
ass-ade-unified doctor
ass-ade-unified book rebuild --help
ass-ade-unified assimilate path/to/primary path/to/out --also path/to/sibling
```

The golden CI fixture lives in [`.github/workflows/ass-ade-ship.yml`](.github/workflows/ass-ade-ship.yml) and exercises `assimilate` on `ass-ade-v1.1/tests/fixtures/minimal_pkg`, emitting JSON and plan artifacts.

Multi-root assimilate with `--also` may require `--policy` when `ASS_ADE_ASSIMILATE_REQUIRE_POLICY=1` or under CI; see [`ass-ade-v1.1/.ass-ade/specs/`](ass-ade-v1.1/.ass-ade/specs/) and [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md).

## Documentation

**Start here:** [`docs/README.md`](docs/README.md) — full index (reading order, specs, operator files).

| Topic | Document |
|--------|-----------|
| Architecture (tiers, package layout) | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) |
| Packaging + `ass-ade-unified` | [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) |
| Phased roadmap + S1–S6 | [`ASS_ADE_SHIP_PLAN.md`](ASS_ADE_SHIP_PLAN.md) |
| HAVE / GAP checklist | [`ASS_ADE_GOAL_PIPELINE.md`](ASS_ADE_GOAL_PIPELINE.md) |
| Spine / workspace roles | [`docs/ASS_ADE_SPINE_RFC.md`](docs/ASS_ADE_SPINE_RFC.md) |
| Capability matrix | [`ASS_ADE_MATRIX.md`](ASS_ADE_MATRIX.md) |
| IDE / hooks audit | [`docs/ATOMADIC_SWARM_SURFACE_AUDIT.md`](docs/ATOMADIC_SWARM_SURFACE_AUDIT.md) |
| Forge CLI sketch | [`docs/ASS_ADE_FORGE_CLI.md`](docs/ASS_ADE_FORGE_CLI.md) |
| Emitter parity | [`docs/EMITTER_PARITY.md`](docs/EMITTER_PARITY.md) |

## CLI essentials

| Command | Use |
|---------|-----|
| `ass-ade-unified doctor` | Environment and monorepo discovery |
| `ass-ade-unified book rebuild --help` | Phased book / pipeline |
| `ass-ade-unified assimilate …` | Primary + optional `--also` roots → monadic emit |
| `ass-ade-v11 synth-tests --check --repo ass-ade-v1.1` | Manifest vs sources (also run in CI) |
| `lint-imports` | Monadic layer contract (after `[dev]` install) |

Use `ass-ade-unified --help` and subcommand `--help` for the full surface.

## Repository layout

| Path | Role |
|------|------|
| [`pyproject.toml`](pyproject.toml) | Distribution + `ass-ade-unified` / `ass-ade-v11` entry points |
| [`ass-ade-v1.1/src/ass_ade_v11/`](ass-ade-v1.1/src/ass_ade_v11/) | Library source (a0–a4 + `ade`) |
| [`ass-ade-v1.1/tests/`](ass-ade-v1.1/tests/) | Pytest suite (`-m "not dogfood"` in CI) |
| [`ADE/`](ADE/) | ADE harness + strict prompt stack (CI gate) |
| [`agents/`](agents/) | Pipeline prompts; alignment checked in CI |
| [`.github/workflows/ass-ade-ship.yml`](.github/workflows/ass-ade-ship.yml) | Public ship workflow |

## Project map (quick)

| Surface | Purpose |
|---------|---------|
| [`AGENTS.md`](AGENTS.md) | Operator map, hooks, agent protocol |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Hygiene, validation, contribution norms |
| [`SECURITY.md`](SECURITY.md) | Responsible disclosure |

## CI And Quality Gates

The public ship workflow runs import-law checks, `pytest -m "not dogfood"`, synth-tests validation, and a golden assimilate pass with artifacts. The goal is a public tree that reflects the real release surface, not a demo-only snapshot.

## Community And Security

Use the GitHub issue forms for reproducible bugs and feature proposals. Keep vulnerability details out of public issues and follow [`SECURITY.md`](SECURITY.md) for disclosure.

## License

See [`LICENSE`](LICENSE). This repository is proprietary unless a specific sub-surface states otherwise.
