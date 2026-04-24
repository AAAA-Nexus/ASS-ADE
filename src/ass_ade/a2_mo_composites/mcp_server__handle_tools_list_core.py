"""Tier a2 — assimilated method 'MCPServer._handle_tools_list'

Assimilated from: server.py:834-854
"""

from __future__ import annotations


# --- assimilated symbol ---
def _handle_tools_list(self, req_id: Any, _params: dict[str, Any]) -> dict[str, Any]:
    # MCP 2025-11-25: support cursor-based pagination.
    # All our tools fit in one page, so nextCursor is always absent.
    # We accept but ignore any incoming cursor.
    tools: list[dict[str, Any]] = []

    # Built-in IDE tools from registry — include annotations
    for schema in self._registry.schemas():
        entry: dict[str, Any] = {
            "name": schema.name,
            "description": schema.description,
            "inputSchema": schema.parameters,
        }
        if schema.name in _BUILTIN_ANNOTATIONS:
            entry["annotations"] = _BUILTIN_ANNOTATIONS[schema.name]
        tools.append(entry)

    # Workflow, agent, and A2A tools (annotations already embedded)
    tools.extend(_WORKFLOW_TOOLS)

    return self._result(req_id, {"tools": tools})

