# ASS-ADE — single product (CNA / monadic) unification

## Goal

One **shippable** ASS-ADE: **one import namespace** (eventually `ass_ade`), **one distribution**, **one primary CLI**, with **a0→a4 monadic layout**, **CNA ids**, and **import-linter** law — while retaining **every** capability that today lives across:

- [`ass-ade-v1`](../ass-ade-v1) — full Typer studio, `engine/rebuild`, Nexus families, interactive Atomadic, etc.
- [`ass-ade-v1.1`](../ass-ade-v1.1) — phased `pipeline_book` (0–7), tier purity, certify, synth-tests.
- [`ass-ade`](../ass-ade) — Click line, x402-heavy dependencies, genesis layout under `.ass-ade/`.

## Tonight’s bridge (operator reality)

Until code is physically merged into one `src/` tree:

1. Install the **monadic spine** from the **repository root** (T12): `pip install -e ".[dev]"` (metadata in root `pyproject.toml`; sources under `ass-ade-v1.1/src/`). **Contributors** need the **`[dev]`** extra for pytest, import-linter, PyYAML, and jsonschema (policy/plan validation and tests). A bare `pip install -e .` installs the CLI only; `--also` under CI or `ASS_ADE_ASSIMILATE_REQUIRE_POLICY=1` still requires `--policy` when validation deps are missing.
2. Install the **v1 studio** in the **same** venv: `pip install -e ./ass-ade-v1`
3. Run the **united** entrypoint:

```text
ass-ade-unified doctor
# One command: primary MAP + optional sibling roots → monadic emit (through book phases)
ass-ade-unified assimilate C:\path\to\primary C:\path\to\out --also C:\path\to\orphan-a --also C:\path\to\orphan-b
# In CI (or ASS_ADE_ASSIMILATE_REQUIRE_POLICY=1), add: --policy path\to\assimilate-policy.yaml (see .ass-ade/specs/)
ass-ade-unified book rebuild …
ass-ade-unified studio chat …
```

- **`assimilate`** — wraps `run_book_until` with `extra_source_roots` (same engine as `book rebuild --also`, default `--stop-after package`). With `--also`, CI (or `ASS_ADE_ASSIMILATE_REQUIRE_POLICY=1`) requires `--policy` YAML per `.ass-ade/specs/assimilate-policy.schema.json`. Every run emits **`ASSIMILATE_PLAN`** (validated JSON) on the book object; use **`--plan-out`** for a sidecar file (CI uploads it).
- **`book`** — same commands as `ass-ade-v11` (CNA/monadic pipeline).
- **`studio`** — appears only when `import ass_ade` works; it is the full v1 `ass_ade.cli` Typer app.

This satisfies “one product **experience**” without pretending the **source** merge is already done.

**CI:** GitHub Actions workflow `.github/workflows/ass-ade-ship.yml` runs lint-imports, `pytest ass-ade-v1.1/tests -m "not dogfood"`, synth-tests, and a **single-root** golden assimilate (no `--policy` in that job). **Org push** to `aaaa-nexus/ass-ade` remains **human-gated** (plan quarantine T9).

**IP / publish path:** build and test under **`C:\!atomadic`** (private). **Do not** push that workspace to public GitHub. Stage the scrubbed, shippable tree under **`C:\!aaaa-nexus`**, then push **from that** checkout only.

## ADE / Atomadic operator stack (shipped in the wheel)

The monadic package includes **`ass_ade_v11.ade`**: a **stdlib-only** materializer
that copies the same **swarm + hooks + automation** the Atomadic workspace uses
into a target project as **`<workspace>/.ade/`** (and optionally
**`<workspace>/.cursor/hooks`**) so the **prompt → product** path is
reproducible for every consumer.

- **CLI:** `ass-ade-unified ade materialize [WORKSPACE] [--source MONOREPO]`
	(default workspace: `.`). The source tree must contain **`agents/INDEX.md`**
	(set **`ATOMADIC_WORKSPACE`** to your clone, or use **`--source`**) — PyPI-only
	installs do not include the monorepo; the wheel carries the `ade` code, and
	**file copies** are taken from a checkout you point at.
- **Contents of `.ade/`** (indicative): `cursor-hooks/` (Swarm bus + scribe),
	`persistent/` (long-running `run_swarm_services` + `swarm_services/`), `scripts/`
	(terrain `regenerate_ass_ade_docs.py`, `sync_build_swarm_to_cursor.py` where present),
	`ade-harness/` (ADE `ade_hook_gate` + verify), `agents-core/` (INDEX, protocol, Nexus, monadic, ATO),
	**`cross-ide/`** (Cursor vs **VS Code** — **Copilot**, **OpenAI Codex**, **MCP** samples, Copilot-instructions sample, optional tasks).
- **VS Code:** `materialize` can **merge** Copilot + Python **extension recommendations** into **`.vscode/extensions.json`**. Configure **MCP** (e.g. from `cross-ide/vscode-mcp.example.json` into **`.vscode/mcp.json`**) and use **Agent** + **Plan** in Chat; follow **`cross-ide/CODEX-BUILD-CYCLE.md`**. Use **`--no-vscode`** to skip the extensions merge.
- **Hooks invariants:** `swarm_signal.py` is written so **`_REPO_ROOT`** resolves
	when the script lives in **`<repo>/.cursor/hooks/`**; use **`ass-ade-unified ade materialize`**
	with **`--no-cursor`** for a staging copy only, or the default to install into
	**`.cursor/hooks`**.
