---
name: Feature request
about: Propose an enhancement aligned with monadic law and MCP contracts
labels: "type: enhancement"
---

## Problem

What capability is missing or painful today?

## Proposal

Describe the change at a high level.

## Terrain impact (checklist)

- [ ] **Tier:** new modules will be listed in `.ass-ade/tier-map.json` (no upward imports).
- [ ] **MCP:** if new tools, extend `mcp/server.json` + run `tests/test_mcp_manifest_parity.py`.
- [ ] **Hooks / swarm:** if Cursor hooks or autonomous graphs change, update `.ass-ade/autonomous/mcp-hooks-compatibility.v0.json` (rollback notes).
- [ ] **Tests:** new behavior covered by `pytest` (name the intended test module).

## Non-goals

What this change will explicitly not do.
