# Nexus, x402, and trust surfaces (ASS-ADE)

**Epistemic label:** *Verified* items reference files and tests in this repo. *DEFER* items need sibling repos, secrets, or live URLs.

## Verified — code and tests

| Surface | Location | Notes |
|---------|----------|--------|
| Nexus HTTP client | `src/ass_ade/nexus/client.py` | Session, retries, API calls |
| x402 / payments composite | `src/ass_ade/nexus/x402.py` | Billing path composition |
| MCP `trust_gate` tool | `src/ass_ade/mcp/server.py` (`_call_trust_gate`) | Uses `_get_nexus_client()`; **local** profile raises / blocks remote trust unless configured |
| CLI doctor | `src/ass_ade/cli.py` | Local-by-default remote probe; see `CONTRIBUTING.md` |
| Tests (no live network) | `tests/test_mcp_extended.py` (`TestMCPTrustGate`), `tests/test_new_commands.py` | Mock `NexusClient` at boundaries |

## Environment variables (names only)

Configure via env / dotenv as documented in `AssAdeConfig` (see `src/ass_ade/config.py`). Do **not** commit real API keys. Typical names include Nexus base URL and API key variables referenced in `CONTRIBUTING.md` and tests (placeholder values only in tests).

## Rollback

1. Switch profile to **local** and remove or unset remote Nexus keys from the environment.
2. Restart the MCP host so `trust_gate` and other tools reload config.
3. If a bad deploy shipped, `git restore` the affected files and re-run `python scripts/atomadic_dev_harness.py --full`.

## Smoke (local, no billing)

```bash
python -m pip install -e ".[dev]"
python -m pytest tests/test_mcp_extended.py::TestMCPTrustGate -q
python -m pytest tests/test_new_commands.py -q
```

## DEFER — Hosted MCP parity (`tools/list` / `tools/call` against a Worker)

**Owner:** storefront + CI maintainers.

**Next action:** Implement smoke in sibling workspace `!aaaa-nexus-storefront` (relative to `!aaaa-nexus`) and wire secrets only in GitHub Actions — not in this repository’s plaintext docs. When a stable public base URL and auth flow exist, add the **Actions run URL** to the active ato-plan `research.md` and a path-only `growthNotes` line here.

Until then, treat **hosted MCP parity** as roadmap **aspirational** (`ass-ade-sovereign-ade` phase), not a shipped guarantee of this package alone.
