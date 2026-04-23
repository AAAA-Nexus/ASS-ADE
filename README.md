# ASS-ADE

<pre>
    ___   _____ _____       ___   ____  ___
   /   | / ___// ___/      /   | / __ \/ __/
  / /| | \__ \ \__ \______/ /| |/ / / / /_
 / ___ |___/ /___/ /_____/ ___ / /_/ / __/
/_/  |_/____//____/     /_/  |_|\____/_/
</pre>

[![CI](https://github.com/AAAA-Nexus/ASS-ADE/actions/workflows/ass-ade-ship.yml/badge.svg)](https://github.com/AAAA-Nexus/ASS-ADE/actions/workflows/ass-ade-ship.yml)
[![Version](https://img.shields.io/badge/version-1.1.0a1-blue)](pyproject.toml)
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

## Project Map

| Surface | Purpose |
|-----|---------|
| [`ASS_ADE_SHIP_PLAN.md`](ASS_ADE_SHIP_PLAN.md) | Exit criteria and phased ship plan |
| [`docs/ASS_ADE_UNIFICATION.md`](docs/ASS_ADE_UNIFICATION.md) | Single-spine packaging and migration story |
| [`AGENTS.md`](AGENTS.md) | Operator map, ADE hooks, and agent protocol surfaces |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Repo hygiene, validation expectations, and contribution norms |
| [`SECURITY.md`](SECURITY.md) | Responsible disclosure path for security reports |

## CI And Quality Gates

The public ship workflow runs import-law checks, `pytest -m "not dogfood"`, synth-tests validation, and a golden assimilate pass with artifacts. The goal is a public tree that reflects the real release surface, not a demo-only snapshot.

## Community And Security

Use the GitHub issue forms for reproducible bugs and feature proposals. Keep vulnerability details out of public issues and follow [`SECURITY.md`](SECURITY.md) for disclosure.

## License

See [`LICENSE`](LICENSE). This repository is proprietary unless a specific sub-surface states otherwise.
