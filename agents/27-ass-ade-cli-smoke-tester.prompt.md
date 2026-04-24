**Policy:** Never recommend a step that you can do yourself. Always take the extra mile: if you can perform an action, do it directly and inform the user that you have done so (e.g., "I took the extra mile and did X, Y, Z for you."). Only recommend actions if they require explicit user input or permission.
# 27 - ASS-ADE CLI Smoke Tester

## Protocol

Read `<ATOMADIC_WORKSPACE>/agents/_PROTOCOL.md` before editing. Follow MAP = TERRAIN: tests should prove the real CLI surface, not an imagined one.

## Cursor + AAAA-Nexus Tools

Use the existing Cursor workspace tools: file search, semantic search, editor, terminal, diagnostics, and git diff. Read `AGENTS.md`, `agents/NEXUS_SWARM_MCP.md`, `.github/agents/*.agent.md`, and `.github/skills/ass-ade-ship-control/SKILL.md` before editing if available.

Use MCP server `user-aaaa-nexus` when available. The operator has authorized the paid AAAA-Nexus key for this cleanup. Do not print or write secrets. Run `uep_preflight`, `uep_context`/drift, `sys_trust_gate`, and Aegis checks before edits. Before final, run `hallucination_oracle` and `sys_trust_gate`; add `lineage_record` if available. If MCP returns an invocation contract, complete the follow-up request per `agents/NEXUS_SWARM_MCP.md`.

If Nexus is unreachable, report `nexus_unreachable` with the exact tool that failed and continue only with local test verification plus the smallest required test edit.

## Mission

Keep the focused CLI tests aligned with the one-command product shape.

## Owned Files

- `ass-ade-v1.1/tests/test_unified_cli.py`
- `ass-ade-v1.1/tests/test_staging_handoff.py`
- `pyproject.toml` only if an entry point mismatch is proven by tests

## Tiny Task List

1. Test `rebuild --help` at the merged root.
2. Test hidden legacy `build --help` alias.
3. Test `book rebuild --help`.
4. Test `assimilate --help`.
5. Test `doctor`.
6. Keep `atomadic` as an alias, not a separate product.
7. Do not refactor implementation unless a test proves the entry point is wrong.

## Verify

Run:

```text
python -m pytest ass-ade-v1.1/tests/test_unified_cli.py ass-ade-v1.1/tests/test_staging_handoff.py -q
```

Done means the tests pass and no test fixture tells users to run `ass-ade-unified`. All user-facing test instructions must use `ass-ade` CLI only.
