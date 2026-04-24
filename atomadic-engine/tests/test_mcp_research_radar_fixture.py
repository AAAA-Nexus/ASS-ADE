"""Tier a1 — MCP manifest golden-path gate (research radar REFINE).

Local MCPAgentBench-style *smoke*: a fixed trio of tools must remain in
``mcp/server.json``; obvious distractor names must never appear as shipped tools.
Nexus public contract slice uses the same httpx.MockTransport pattern as
``test_nexus_client.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

import httpx

from ass_ade.mcp.server import MCPServer
from ass_ade.nexus.client import NexusClient

REPO_ROOT = Path(__file__).resolve().parents[1]
MCP_MANIFEST = REPO_ROOT / "mcp" / "server.json"


def _dispatch(server: MCPServer, request: dict[str, object]) -> object:
    return getattr(server, "_handle")(request)


def _initialize_mcp_server(server: MCPServer) -> None:
    init = _dispatch(
        server,
        {"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {}},
    )
    assert init is not None
    _dispatch(server, {"method": "notifications/initialized", "params": {}})

CANONICAL_TRIO = ("map_terrain", "read_file", "trust_gate")
DISTRACTORS = ("shadow_write_all", "delete_production_db", "exfil_env_secrets")


def _tool_names() -> set[str]:
    data = json.loads(MCP_MANIFEST.read_text(encoding="utf-8"))
    tools = data.get("tools")
    assert isinstance(tools, list), "mcp/server.json must list tools"
    return {str(t) for t in tools}


def test_mcp_server_json_contains_golden_tool_trio() -> None:
    tools = _tool_names()
    for name in CANONICAL_TRIO:
        assert name in tools, f"expected canonical MCP tool {name!r} in mcp/server.json"


def test_mcp_server_json_excludes_distractor_tool_names() -> None:
    tools = _tool_names()
    leaked = sorted(tools & set(DISTRACTORS))
    assert not leaked, f"distractor tool names must not ship: {leaked}"


def test_mcp_in_process_tools_list_contains_map_terrain(tmp_path: Path) -> None:
    server = MCPServer(str(tmp_path))
    _initialize_mcp_server(server)
    response = _dispatch(
        server,
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
    )
    assert response is not None
    tools = response["result"]["tools"]
    assert any(t["name"] == "map_terrain" for t in tools)


def test_mcp_in_process_map_terrain_tool_call_returns_proceed(tmp_path: Path) -> None:
    server = MCPServer(str(tmp_path))
    _initialize_mcp_server(server)
    response = _dispatch(
        server,
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "map_terrain",
                "arguments": {
                    "task_description": "Need an existing reader.",
                    "required_capabilities": {"tools": ["read_file"]},
                },
            },
        },
    )
    assert response is not None
    assert response["result"]["isError"] is False
    text = response["result"]["content"][0]["text"]
    assert '"verdict": "PROCEED"' in text


def test_nexus_public_contract_slice_still_parses() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        payloads = {
            "/health": {"status": "ok"},
            "/openapi.json": {"info": {"version": "0.5.1"}},
            "/.well-known/agent.json": {"name": "AAAA-Nexus", "skills": []},
            "/.well-known/mcp.json": {"name": "AAAA-Nexus", "tools": []},
        }
        return httpx.Response(200, json=payloads[request.url.path])

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        assert client.get_health().status == "ok"
        assert client.get_mcp_manifest().name == "AAAA-Nexus"
