"""MCP catalog: mcp/server.json must list only tools the server can actually expose."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def server_json_tools() -> set[str]:
    path = _REPO / "mcp" / "server.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    tools = data.get("tools")
    assert isinstance(tools, list) and tools
    return {str(t) for t in tools}


def test_server_json_tool_ids_are_subset_of_runtime_surfaces(server_json_tools: set[str]) -> None:
    """Every name in ``mcp/server.json`` appears in the builtin registry or workflow table."""
    from ass_ade.mcp.server import _WORKFLOW_TOOLS
    from ass_ade.tools.registry import default_registry

    workflow = {str(t["name"]) for t in _WORKFLOW_TOOLS if isinstance(t, dict) and t.get("name")}
    reg = default_registry(str(_REPO))
    available = set(reg.list_tools()) | workflow
    stray = sorted(server_json_tools - available)
    assert not stray, f"mcp/server.json lists unknown tools: {stray}"
