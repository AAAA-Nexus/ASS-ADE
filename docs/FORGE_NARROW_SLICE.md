# Recursive Forge — narrow slice (one-repo, bounded)

This document defines a **minimal** Forge-style loop that fits inside `!ass-ade` without claiming full DGM-H or sovereign ADE completion.

## Preconditions (verified)

- Monadic law: `.ass-ade/tier-map.json` + `pytest tests/test_monadic_purity.py`
- MCP contract: `mcp/server.json` + `pytest tests/test_mcp_manifest_parity.py`
- Privileged tools: `.ass-ade/specs/trust-gate-mcp-envelope.spec.md` + `tests/test_mcp_privileged_builtin_tools.py`

## Bounded loop (repeat at most once per PR unless CI is green)

1. **Propose:** Open or update an ato-plan / issue with a single scoped goal.
2. **Apply:** Land code + tests in one PR; extend `tier-map.json` before merge if new modules appear.
3. **Verify:**  
   `python scripts/atomadic_dev_harness.py --quick`  
   then `python -m pytest tests/ -q --tb=line` for release candidates.
4. **Record:** Append a **path-only** line to `.ass-ade/ass-ade-suite-roadmap.json` `growthNotes` (no marketing adjectives).

## Audit trail

Optional append-only log (repo-local, not secrets):

- `.ass-ade/final-form-audit.log` — one ISO-8601 UTC line per merge that self-identifies as following this slice.

## Out of scope

- Multi-repo Recursive Forge without separate plans per repo.
- Prompt changes without `@prompt-master-auditor` review (see Atomadic workflow skills).
