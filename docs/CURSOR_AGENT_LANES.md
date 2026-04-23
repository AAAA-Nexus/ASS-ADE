# Cursor Agent Lanes: ASS-ADE Single CLI Cleanup

Status: active handoff for small Cursor-model tasks.

Product rule: there is one operator CLI, `ass-ade`. `atomadic` may stay as an alias to the same CLI. Do not add or document `ass-ade-unified` or `ass-ade-v11` as user-facing commands.

Do not edit sibling product folders. Work only in `C:\!aaaa-nexus\!ass-ade`.

## Cursor + AAAA-Nexus Setup

Before any lane edits, use the existing Cursor workspace setup:

- Read `AGENTS.md`, `agents/_PROTOCOL.md`, `agents/NEXUS_SWARM_MCP.md`, and the lane prompt under `agents/25-28`.
- Use Cursor file/search/edit/terminal/diagnostics tools normally; keep diffs inside the lane's owned files.
- Use the configured MCP server `user-aaaa-nexus` when available. The operator has authorized the paid AAAA-Nexus key for this ASS-ADE cleanup.
- Do not print, reveal, or write API keys. Use configured MCP auth only.
- Run Nexus preflight before edits: `uep_preflight`, drift/trust checks via `uep_context` and `sys_trust_gate`, and Aegis injection/bounds checks where applicable.
- Run Nexus postflight before final: `hallucination_oracle` and `sys_trust_gate`; add `lineage_record` or `uep_trace_certify` when the lane changes release-facing docs or tests.
- If Cursor MCP returns an invocation contract, complete the required follow-up request as described in `agents/NEXUS_SWARM_MCP.md`; do not stop at the contract text.
- If the MCP server is unreachable, report `nexus_unreachable` with the exact failing tool and continue only with clearly local/read-only work.
- Use repo-side helpers when useful: `.github/agents/*.agent.md`, `.github/skills/ass-ade-ship-control/SKILL.md`, and `agents/build_swarm_registry.json`.

## Lane 1: Docs Command Sweep

Agent prompt: `agents/25-ass-ade-cli-doc-sweeper.prompt.md`

Owned files:

- `README.md`
- `docs/*.md`
- `ASS_ADE_MATRIX.md`
- `ASS_ADE_SHIP_PLAN.md`
- `ASS_ADE_GOAL_PIPELINE.md`

Tiny tasks:

1. Replace user-facing `ass-ade-unified ...` examples with `ass-ade ...`.
2. Replace user-facing `ass-ade-v11 rebuild ...` examples with `ass-ade book rebuild ...`.
3. Keep package names like `ass_ade_v11` and folder names like `ass-ade-v1.1/` unchanged.
4. Do not edit source code or tests.

Done when:

```text
rg -n "ass-ade-unified|ass-ade-v11 " README.md docs ASS_ADE_MATRIX.md ASS_ADE_SHIP_PLAN.md ASS_ADE_GOAL_PIPELINE.md
```

Only archive/history/vendor mentions remain, and each remaining mention explains why it is not a product CLI.

## Lane 2: Agent Prompt Sweep

Agent prompt: `agents/26-ass-ade-agent-prompt-sweeper.prompt.md`

Owned files:

- `AGENTS.md`
- `agents/*.md`
- `agents/*.prompt.md`
- `ass-ade-v1.1/src/ass_ade_v11/ade/cross_ide_bundled/*.md`
- `ass-ade-v1.1/src/ass_ade_v11/ade/SWARM-ONE-PROMPT.vendor.md`

Tiny tasks:

1. Replace operator examples with `ass-ade doctor`, `ass-ade ade ...`, `ass-ade book ...`, or `ass-ade assimilate ...`.
2. Keep internal package and source folder names unchanged.
3. Do not edit Python source except generated docs embedded as markdown.
4. Run the prompt alignment check.

Done when:

```text
python agents/check_swarm_prompt_alignment.py
rg -n "ass-ade-unified|ass-ade-v11 " AGENTS.md agents ass-ade-v1.1/src/ass_ade_v11/ade
```

Only clearly historical references remain.

## Lane 3: CLI Smoke Tests

Agent prompt: `agents/27-ass-ade-cli-smoke-tester.prompt.md`

Owned files:

- `ass-ade-v1.1/tests/test_unified_cli.py`
- `ass-ade-v1.1/tests/test_staging_handoff.py`
- `pyproject.toml` only if the test proves an entry point mismatch

Tiny tasks:

1. Assert `ass-ade` is the product CLI in tests and fixture snippets.
2. Add or keep tests for `rebuild`, `build` alias, `book rebuild`, `assimilate`, and `doctor`.
3. Do not refactor the CLI implementation.
4. Do not remove `atomadic`; it is the alias.

Done when:

```text
python -m pytest ass-ade-v1.1/tests/test_unified_cli.py ass-ade-v1.1/tests/test_staging_handoff.py -q
```

## Lane 4: Duplicate Install Audit

Agent prompt: `agents/28-ass-ade-env-dedupe-auditor.prompt.md`

Owned files:

- `docs/ONE_WORKING_PRODUCT.md`
- `docs/ASS_ADE_UNIFICATION.md`
- `docs/TROUBLESHOOTING.md` if it exists, otherwise create it

Tiny tasks:

1. Document how to detect stale editable installs that point at old `ass_ade` trees.
2. Include read-only commands: `python -m pip list`, `python -m pip show ass-ade`, `where ass-ade`, `python -c "import ass_ade; print(ass_ade.__file__)"`.
3. Say not to delete folders automatically.
4. Say the merged `ass-ade` wrapper forces the bundled engine for CLI commands, but raw Python imports can still be affected by old `.pth` files.

Done when:

```text
rg -n "C:\\\\!atomadic|\\.pth|pip show ass-ade|where ass-ade" docs/ONE_WORKING_PRODUCT.md docs/ASS_ADE_UNIFICATION.md docs/TROUBLESHOOTING.md
```

## Global Rules For All Lanes

- Do not edit `QUARANTINE_IP_LEAK_v20/`.
- Do not copy code from generated release folders.
- Do not uninstall packages or delete sibling folders.
- Keep changes small and file-owned.
- If a command fails, paste the command and the exact failure into your final note.
