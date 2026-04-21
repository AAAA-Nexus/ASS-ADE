# Proof-ready spec — Trust gate + MCP tool envelope (ASS-ADE)

**Epistemic label:** *requirements traceable to code and tests — not a Lean proof.*

## Scope

This document bounds the **trust_gate** MCP workflow tool and the **built-in privileged tools** (`write_file`, `edit_file`, `run_command`) so implementers and reviewers share one envelope.

## Actors and surfaces

| Symbol (informal) | Code anchor | Role |
|-------------------|-------------|------|
| Host | Cursor / Claude / other MCP client | Obtains user consent before `tools/call` |
| Server | `ass_ade.mcp.server.MCPServer` | JSON-RPC, cancellation, progress, routing |
| Registry | `ass_ade.tools.registry` | Built-in IDE tools (`run_command`, …) |
| TCA / CIE | `ass_ade.agent.tca`, `ass_ade.agent.cie` | NCB freshness, post-write validation for edits |

## Requirements

### R1 — Workspace confinement (file tools)

For `read_file`, `write_file`, `edit_file`, resolved paths **must** satisfy `path.resolve().relative_to(cwd.resolve())` or the tool returns a structured error (no partial write).

**Evidence tests:** `tests/test_tools_builtin.py` (`test_reject_outside_cwd`), `tests/test_mcp_privileged_builtin_tools.py` (`test_read_rejects_parent_escape`, `test_write_rejects_absolute_outside`).

### R2 — `run_command` allowlist and no shell

Arguments **must** be parsed with `shlex.split` and executed with `shell=False`. The first token’s executable stem **must** belong to `_ALLOWED_COMMANDS` in `ass_ade.tools.builtin`.

**Evidence tests:** `tests/test_tools_builtin.py` (`test_blocked_dangerous`), `tests/test_mcp_privileged_builtin_tools.py`.

### R3 — Inline interpreter block (default)

When `ASS_ADE_ALLOW_INLINE_RUN_COMMAND` is unset or not `1`, `run_command` **must** reject:

- `python` / `python3` / `py` invocations containing the `-c` argument token.
- `node` invocations containing `-e` or `--eval`.

**Evidence tests:** `tests/test_mcp_privileged_builtin_tools.py` (`test_run_command_blocks_python_inline_c_by_default`, `test_run_command_blocks_node_eval`, `test_mcp_run_command_blocks_inline_via_json_rpc`); override path: `test_run_command_allows_python_c_when_env_override`.

### R4 — NCB + CIE hooks (writes)

For `write_file` / `edit_file`, `MCPServer._pre_tool_hook` and `_post_tool_hook` apply NCB and CIE policies as implemented (warn vs block mode for NCB).

**Evidence:** `src/ass_ade/mcp/server.py` (`_pre_tool_hook`, `_post_tool_hook`); not formally verified here.

### R5 — MCP annotations

Built-in tools expose MCP 2025-11-25 **annotations** including `openWorldHint: true` for `run_command`.

**Evidence test:** `tests/test_mcp_extended.py` (`test_run_command_is_open_world`).

## Out of scope (explicit)

- Formal proof of CIE soundness or completeness.
- Guarantees about third-party executables once allowlisted (e.g. `pip install` targets).

## Revision discipline

Bump this document’s `revision` footer when R1–R5 change materially.

**Revision:** 1 — 2026-04-22 — aligned with `tests/test_mcp_privileged_builtin_tools.py` landing.
