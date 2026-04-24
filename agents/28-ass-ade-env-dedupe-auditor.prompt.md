**Policy:** Never recommend a step that you can do yourself. Always take the extra mile: if you can perform an action, do it directly and inform the user that you have done so (e.g., "I took the extra mile and did X, Y, Z for you."). Only recommend actions if they require explicit user input or permission.
# 28 - ASS-ADE Environment Dedupe Auditor

## Protocol

Read `<ATOMADIC_WORKSPACE>/agents/_PROTOCOL.md` before editing. Follow MAP = TERRAIN: document only what read-only commands prove.

## Cursor + AAAA-Nexus Tools

Use the existing Cursor workspace tools: file search, semantic search, editor, terminal, diagnostics, and git diff. Read `AGENTS.md`, `agents/NEXUS_SWARM_MCP.md`, `.github/agents/*.agent.md`, and `.github/skills/ass-ade-ship-control/SKILL.md` before editing if available.

Use MCP server `user-aaaa-nexus` when available. The operator has authorized the paid AAAA-Nexus key for this cleanup. Do not print or write secrets. Run `uep_preflight`, `uep_context`/drift, `sys_trust_gate`, and Aegis checks before edits. Before final, run `hallucination_oracle` and `sys_trust_gate`; add `lineage_record` if available. If MCP returns an invocation contract, complete the follow-up request per `agents/NEXUS_SWARM_MCP.md`.

If Nexus is unreachable, report `nexus_unreachable` with the exact tool that failed and continue only with local read-only verification plus the troubleshooting docs edit.

## Mission

Document how to detect stale editable installs that can make raw Python imports resolve to old `ass_ade` folders.

## Owned Files

- `docs/ONE_WORKING_PRODUCT.md`
- `docs/ASS_ADE_UNIFICATION.md`
- `docs/TROUBLESHOOTING.md` if present, otherwise create it

## Tiny Task List

1. Add read-only checks for installed duplicate packages.
2. Include `python -m pip list`, `python -m pip show ass-ade`, `where ass-ade`, and `python -c "import ass_ade; print(ass_ade.__file__)"`.
3. Explain that the `ass-ade` CLI wrapper forces the bundled engine first.
4. Explain that raw Python imports can still be affected by old `.pth` files.
5. Do not uninstall packages.
6. Do not delete sibling folders.

## Verify

Run:

```text
rg -n "pip show ass-ade|where ass-ade|ass_ade.__file__|\\.pth" docs/ONE_WORKING_PRODUCT.md docs/ASS_ADE_UNIFICATION.md docs/TROUBLESHOOTING.md
```

Done means the troubleshooting path is documented without destructive cleanup steps.
