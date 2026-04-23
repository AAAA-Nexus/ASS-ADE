# Atomadic Cursor Agent Instructions

Cursor Agent must follow the Atomadic global development suite for this workspace.

Authoritative local surfaces:

- **MAP = TERRAIN index:** `.ass-ade/terrain-index.v0.json` (canonical pointers to tier-map, MCP manifest, autonomous graphs, ASO, demos; extend these before adding parallel tooling)
- **Contributing + label CI:** `CONTRIBUTING.md` (`ass-ade-blueprint` / `ass-ade-feature` lanes); local preflight `python scripts/atomadic_dev_harness.py --quick`
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
