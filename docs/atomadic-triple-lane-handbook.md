# Atomadic triple lane — expansion, evolution, promotion (ASS-ADE)

**Epistemic status:** *Verified* statements point at repo paths and tests. *Aspirational* items are roadmap phases until smoke artifacts and CI URLs exist.

This handbook operationalizes the **expansion / evolution / promotion** framing for contributors and agents. It does **not** add MCP tools by itself — follow the procedures below when you do.

## Expansion (technical terrain)

**Verified anchors**

- **MAP = TERRAIN index:** `.ass-ade/terrain-index.v0.json`
- **Monadic law:** `.ass-ade/tier-map.json` (no upward imports between `a0`–`a4`)
- **Public MCP contract:** `mcp/server.json` must match code; run `pytest tests/test_mcp_manifest_parity.py` and `tests/test_mcp_extended.py` when the manifest changes.
- **Privileged built-ins:** `.ass-ade/specs/trust-gate-mcp-envelope.spec.md` and `tests/test_mcp_privileged_builtin_tools.py`

**Procedure (when adding a capability)**

1. Classify modules in `tier-map.json` before merge.
2. If adding MCP tools: extend `mcp/server.json` and the in-process registry in lockstep; extend parity tests in the same PR.
3. Extend `.ass-ade/autonomous/mcp-hooks-compatibility.v0.json` when hooks or workflows change (include rollback notes).

## Evolution (governance)

**Verified**

- **Roadmap + radar:** `.ass-ade/ass-ade-suite-roadmap.json` (`growthNotes`, `researchRadar.nextReviewBy`, refinement evidence paths).
- **Evolution context gate:** `python scripts/check_evolution_context.py --roadmap .ass-ade/ass-ade-suite-roadmap.json` (also runs in CI on guarded paths).

**Aspirational**

- Full DGM-H / Recursive Forge governance packets — only when a human requests them and harness artifacts exist (see roadmap phase `ass-ade-sovereign-ade`).

Append `.ato-plans/.../evolution.log` (plan folders) when scope shifts; append roadmap `growthNotes` only with **paths or command outcomes**, not prose-only claims.

## Promotion (credibility)

**Verified**

- **Contributor path:** `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`
- **Local preflight:** `python scripts/atomadic_dev_harness.py --quick`
- **Demos index:** `docs/demos/README.md`

**Aspirational**

- Marketplace / registry listings — **DEFER** until a public server URL, auth story, and billing alignment are documented (see roadmap hosted MCP parity).

## Nexus and payments

**Verified:** Doctor behavior and tests are described in `CONTRIBUTING.md` (local default, `--remote`, env-key cases; `tests/test_cli.py`).

**Aspirational / quarantine:** Live x402 spend and hosted MCP parity require explicit env, keys, and CI evidence — do not document fake endpoints.

## DEFER — CI run URLs

Paste GitHub Actions run URLs into your active **ato-plan** `research.md` after the first successful run on the default branch. **Owner:** maintainer with repository push access.
