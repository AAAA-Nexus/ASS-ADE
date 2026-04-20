# Context pack: `!ass-ade-dev` fully functional (OOTB)

**Schema:** `atomadic.context-pack.v1`  
**Generated:** 2026-04-20T02:53:00Z  
**Pack dir:** `.ass-ade/context-packs/ass-ade-dev-fully-functional-20260420-0253/`  
**Verdict (pack readiness):** PASS

## Intent

Bring the **emitted consumer** tree `C:\!aaaa-nexus\!ass-ade-dev` to a **fully functional** baseline: clean virtualenv, `pip install -e .`, `import ass_ade.cli`, and `ass-ade --help` without `PYTHONPATH`, with declared dependencies matching what `ass_ade.cli` imports at load time. Keep canonical emitter in `C:\!aaaa-nexus\!ass-ade` as the long-term source of truth for default deps.

## Repo map (summary)

| Area | Role |
|------|------|
| `!ass-ade/.ass-ade/tier-map.json` | Monadic routing for `src/ass_ade/**` |
| `!ass-ade/src/ass_ade/engine/rebuild/package_emitter.py` | Emits runnable package: `_DEFAULT_PYPROJECT_DEPS`, wheel `packages`, tier `__init__.py` |
| `!ass-ade/src/ass_ade/engine/rebuild/orchestrator.py` | Rebuild orchestration; invokes emitter |
| `!ass-ade-dev/` | Phase-7 output: root `pyproject.toml`, vendored `ass_ade/`, tier dirs `a0_qk_constants` … `a4_sy_orchestration`, `.ass-ade/` mirror |
| `!ass-ade-dev/ass_ade/mcp/utils.py` | Imports `jsonschema` at module top (pulled in by `ass_ade.cli`) |

**Hot path for this task:** emitter defaults → root `pyproject.toml` in the consumer; import chain `cli` → `mcp.utils` → `jsonschema`.

## Local verification (evidence)

- **Failure mode (before fix):** fresh venv + `pip install -e .` → `ModuleNotFoundError: No module named 'jsonschema'` on `import ass_ade.cli` because root `pyproject.toml` omitted `jsonschema` while vendored `package_emitter._DEFAULT_PYPROJECT_DEPS` already listed it.
- **Pass (after fix):** same procedure succeeds; `ass-ade --help` prints Typer usage.

## Web research (merged)

- **Hatch / Hatchling:** Official build docs describe `[tool.hatch.build.targets.wheel]` and explicit `packages` for shipping specific directories—matches the consumer’s multi-package layout (`ass_ade` + tier packages). See [Hatch build configuration — Packages](https://hatch.pypa.io/latest/config/build/#packages).
- **Hop 1b — MCP / agents (external, DEFER):** arXiv benchmarks (e.g. [MCPAgentBench](https://arxiv.org/abs/2512.24565), [MCPToolBench++](https://arxiv.org/abs/2508.07575)) document stress cases for MCP tool use at scale. **Not reproduced locally**; cited for product context only (why MCP payload validation sits on the CLI import path).

## Tech docs (version-scoped)

- **PEP 660** editable installs: interoperability with Hatchling backends — [pip local installs](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs).
- **Hatch dev mode / wheel target** drives editable path resolution — [Hatch dev mode](https://hatch.pypa.io/latest/config/build/#dev-mode).

## Risks and gaps

1. **Drift:** Consumer root `pyproject.toml` can fall behind `_DEFAULT_PYPROJECT_DEPS` unless rebuild re-emits it after emitter edits.
2. **No tests in `!ass-ade-dev`:** Packaging can be green while behavior regressions go unnoticed until canonical `pytest` is run in `!ass-ade`.
3. **Publishing:** If you ship sdists, validate Hatch sdist `include`/`only-include` vs wheel-only `packages` (known footguns in multi-top-level layouts).

## Next edits (for the dev agent)

1. ~~Add `jsonschema>=4.23,<5` to `!ass-ade-dev/pyproject.toml`~~ **Done in this session.**
2. After any emitter dependency change in `!ass-ade`, **re-run rebuild** into `!ass-ade-dev` (or diff root `pyproject.toml` against `_DEFAULT_PYPROJECT_DEPS`).
3. Optional: extend `emit_runnable_package` / orchestrator to **copy a minimal smoke test** or document a one-liner in `AGENTS.md` for CI.

## Handoff

Attach **`context-pack.md`** (and optionally **`context-pack.json`**) to the coding task. For further monadic work in canonical sources, use **`/ass`** with `.ass-ade/tier-map.json` first.
