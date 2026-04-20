# Atomadic Cursor Agent Instructions

Cursor Agent must follow the Atomadic global development suite for this workspace.

Authoritative local surfaces:

- **MAP = TERRAIN index:** `.ass-ade/terrain-index.v0.json` (canonical pointers to tier-map, MCP manifest, autonomous graphs, ASO, demos; extend these before adding parallel tooling)
- **Contributing + label CI:** `CONTRIBUTING.md` (`ass-ade-blueprint` / `ass-ade-feature` lanes); local preflight `python scripts/atomadic_dev_harness.py --quick`
- **README showcase policy:** keep `README.md` focused on install, quickstart, architecture, and key subsystems; park ops and governance links in a tail `## More documentation` instead of long `## Contributing` blocks. Agent context: `.omc/skills/readme-showcase-vs-ops-docs-expertise.md`
- **Trust and promotion anchors:** `docs/atomadic-triple-lane-handbook.md`, `docs/RELEASE_CHECKLIST.md`, `.ass-ade/specs/trust-gate-mcp-envelope.spec.md`, plus tests `tests/test_mcp_privileged_builtin_tools.py`, `tests/test_docs_promotion_layout.py`, `tests/test_final_form_nexus_docs.py`; set `ASS_ADE_ALLOW_INLINE_RUN_COMMAND` when exercising privileged `run_command` inline paths
- **Last full-suite signal:** `pytest tests/` 1281 passed (~77s on Windows); `atomadic_dev_harness.py --quick` 10 passed; pytest may print a benign temp-dir `PermissionError` on atexit while still exiting 0
- User subagents: `C:/Users/atoma/.cursor/agents`
- Cursor suite manifest: `C:/Users/atoma/.cursor/atomadic/cursor-suite-manifest.json`
- Project rules: `C:\!aaaa-nexus\!ass-ade\.cursor\rules`
- AAAA-Nexus MCP: `aaaa-nexus` in `C:/Users/atoma/.cursor/mcp.json`
- Environment fallback: `C:/!ass-ade/.env`

Use the 15 Atomadic roles only unless the user explicitly asks otherwise:
`recon-swarm-orchestrator`, `monadic-enforcer`, `python-specialist-pure`,
`python-specialist-stateful`, `evolutionary-manager`,
`ass-ade-nexus-enforcer`, `formal-validator-proofbridge`,
`code-reviewer-multiagent`, `security-redteam`, `github-manager`,
`marketing-community`, `devops-puppeteer`, `documentation-synthesizer`,
`tool-discovery-mcpzero`, and `prompt-master-auditor`.

For code changes, check `.ass-ade/tier-map.json` when present and obey the
Monadic Development Standard. Never import upward between a0-a4 tiers.

## Recent landings

- 2026-04-22: Archived ato-pilot waves under `.ato-plans/completed/` (`ass-ade-expansion-evolution-promotion-20260422-1515`, `ass-ade-multiplan-wave2-20260422-1715`, `ass-ade-atomadic-final-form-20260419-1800`); final-form track closed T6/T8/T9 with T7 hosted MCP deferred to sibling `!aaaa-nexus-storefront`, `tasks.json` T9 dependsOn `[T6,T8]`, and supporting assets `docs/NEXUS_AND_TRUST_SURFACES.md`, `docs/FORGE_NARROW_SLICE.md`, `.ass-ade/final-form-audit.log`.
