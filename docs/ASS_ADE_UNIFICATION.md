# ASS-ADE — single product (CNA / monadic) unification

> **Public `ASS-ADE` repository:** You have **`ass-ade-v1.1/`** and the unified CLI from the repo root. Sibling distributions (`ass-ade-v1`, legacy `ass-ade`) and `.ato-plans/` paths mentioned below apply to the **private umbrella** used to build releases, not to every public clone.

## Goal

One **shippable** ASS-ADE: **one import namespace** (eventually `ass_ade`), **one distribution**, **one primary CLI**, with **a0→a4 monadic layout**, **CNA ids**, and **import-linter** law — while retaining **every** capability that today lives across:

- [`ass-ade-v1`](../ass-ade-v1) — full Typer studio, `engine/rebuild`, Nexus families, interactive Atomadic, etc.
- [`ass-ade-v1.1`](../ass-ade-v1.1) — phased `pipeline_book` (0–7), tier purity, certify, synth-tests.
- [`ass-ade`](../ass-ade) — Click line, x402-heavy dependencies, genesis layout under `.ass-ade/`.

## One install from repo root (2026-04-22)

The **private Atomadic monorepo** now vendors the `atomadic` engine beside the spine:

- **`ass-ade-v1.1/src/ass_ade_v11/`** — monadic pipeline, `assimilate`, `book`, `ade materialize`, …
- **`atomadic-engine/src/ass_ade/`** — Click **`atomadic`** CLI (`build` / `extend` / `reclaim` / `forge`), sovereign + binder stack, engine tests under **`atomadic-engine/tests/`**

From **`C:\!atomadic`** (or your public staging checkout after sync):

```text
pip install -e ".[dev]"
ass-ade-unified doctor          # should report ass_ade OK
atomadic --help                 # direct Click entry (same as legacy ass-ade tree)
ass-ade-unified atomadic build --help   # shim: forwards argv to the Click group
ass-ade-unified assimilate PRIMARY OUT  # multi-root → monadic emit (policy when --also in CI)
ass-ade-unified book rebuild …
```

Optional: **`ass-ade-unified studio …`** still appears only if a **legacy** Typer `ass_ade.cli.app` exists (older v1 checkout). The shipped engine uses **Click**; prefer **`atomadic`** or **`ass-ade-unified atomadic`**.

**Assimilate** still wraps `run_book_until` with `extra_source_roots` (same engine as `book rebuild --also`, default `--stop-after package`). With `--also`, CI (or `ASS_ADE_ASSIMILATE_REQUIRE_POLICY=1`) requires **`--policy`** YAML per `.ass-ade/specs/assimilate-policy.schema.json`. Every run emits **`ASSIMILATE_PLAN`**; use **`--plan-out`** for a sidecar file.

This is a **physical merge of sources** into one distribution (`pyproject` at repo root); long-term rename `ass_ade_v11` → `ass_ade` remains a separate major release per the target architecture section below.

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

`ass-ade-unified ade doctor` — shows whether a monorepo is discoverable and
whether the current directory already has **`.ade/LAYOUT.json`**.

## Target architecture (physical merge)

Phased, low-regret order:

1. **Lock law** — keep `import-linter` contracts as the gate; all new code only in `a0…a4` (or the chosen single package’s tiers).
2. **Relocate engines** — move `ass_ade.engine.rebuild` responsibilities into `ass_ade_v11` tiers (a2 composites + a3 features + a4 orchestration shims) behind stable CNA ids; keep thin **compat re-exports** in v1 only as long as needed.
3. **Collapse CLIs** — one Typer root: pipeline subcommands stay; v1 commands migrate under names that match user mental model (`chat`, `nexus`, …) without a permanent `studio` prefix once namespaces merge.
4. **Single `pyproject`** — one `[project]` name (likely `ass-ade`), one version line, optional extras for x402 / dev; retire duplicate `pyproject.toml` trees or mark them read-only archives.
5. **Retire `ass_ade_v11` name** — rename package to `ass_ade` in a major release when imports and tier-map are updated everywhere (big bang; plan branch).

## What “done” means

- One checkout, one `pip install`, **`import ass_ade`** only.
- `ass-ade-unified` (or renamed `atomadic` / `ass-ade`) exposes **both** pipeline and studio commands **without** a nested `studio` group.
- [`ASS_ADE_MATRIX.md`](../ASS_ADE_MATRIX.md) collapses to a **single row** for the product.

## References

- [`ASS_ADE_SHIP_PLAN.md`](../ASS_ADE_SHIP_PLAN.md) — phased ship roadmap (S1–S6 exit criteria)  
- [`ASS_ADE_GOAL_PIPELINE.md`](../ASS_ADE_GOAL_PIPELINE.md) — HAVE / GAP / IMPLEMENT checklist  
- [`pyproject.toml`](../pyproject.toml) — distribution metadata, scripts, import-linter contracts  
- [`ass-ade-v1.1/.ass-ade/specs/`](../ass-ade-v1.1/.ass-ade/specs/) — `assimilate-policy` + `assimilate-plan` JSON Schemas  
- [`docs/README.md`](README.md) — full documentation index  
- [`docs/ASS_ADE_SPINE_RFC.md`](ASS_ADE_SPINE_RFC.md) — terrain roles (full workspace vs public tree)  
- [`ASS_ADE_MATRIX.md`](../ASS_ADE_MATRIX.md) — capability split  
- [`docs/ASS_ADE_FORGE_CLI.md`](ASS_ADE_FORGE_CLI.md) — dispatcher sketch for inventory / plan / rebuild  

_Private Atomadic workspace only:_ packaging ADR and ship-loop drafts under `.ato-plans/active/ass-ade-ship-nexus-github-20260422/` (not shipped on public GitHub).
