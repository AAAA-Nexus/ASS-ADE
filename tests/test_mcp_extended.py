"""Tests for MCP server — extended workflow, agent, and A2A tools."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from ass_ade.config import AssAdeConfig
from ass_ade.mcp.server import _WORKFLOW_TOOLS, MCPServer


def _initialize_server(server: MCPServer) -> None:
    response = server._handle({
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {},
    })
    assert response is not None
    server._handle({"method": "notifications/initialized", "params": {}})

# ── Tool listing ─────────────────────────────────────────────────────────────


class TestMCPToolListing:
    def test_tools_list_includes_builtin_and_extended(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {},
        })
        assert response is not None
        tools = response["result"]["tools"]
        names = {t["name"] for t in tools}

        # Built-in tools
        assert "read_file" in names
        assert "write_file" in names

        # Extended workflow tools
        assert "phase0_recon" in names
        assert "epiphany_breakthrough_cycle" in names
        assert "context_pack" in names
        assert "context_memory_store" in names
        assert "context_memory_query" in names
        assert "map_terrain" in names
        assert "trust_gate" in names
        assert "certify_output" in names
        assert "safe_execute" in names
        assert "ask_agent" in names
        assert "a2a_validate" in names
        assert "a2a_negotiate" in names

    def test_extended_tools_have_schemas(self) -> None:
        for tool in _WORKFLOW_TOOLS:
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool
            assert tool["inputSchema"]["type"] == "object"
            assert "required" in tool["inputSchema"]


# ── Workflow routing ─────────────────────────────────────────────────────────


class TestEpiphanyBreakthroughCycleTool:
    def test_epiphany_breakthrough_cycle_without_recon(self, tmp_path) -> None:
        server = MCPServer(str(tmp_path))
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "epiphany_breakthrough_cycle",
                "arguments": {
                    "task_description": "Write README install section for the CLI",
                    "run_phase0": False,
                    "observations": ["Users miss the hybrid profile step"],
                },
            },
        })
        assert response is not None
        assert response["result"]["isError"] is False
        payload = json.loads(response["result"]["content"][0]["text"])
        assert payload["schema_version"] == "ass-ade.epiphany-breakthrough-cycle.v1"
        assert payload["track"] == "documentation"
        assert payload["epiphanies"]


class TestMCPWorkflowRouting:
    def test_builtin_tool_still_works(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "list_directory", "arguments": {"path": "."}},
        })
        assert response is not None
        assert "isError" in response["result"]

    def test_unknown_tool_returns_error(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "nonexistent_tool", "arguments": {}},
        })
        assert response is not None
        assert response["result"]["isError"]


# ── A2A validate via MCP ─────────────────────────────────────────────────────


_FAKE_ADDR_INFO = [(None, None, None, None, ("93.184.216.34", None))]


class TestMCPA2AValidate:
    def test_a2a_validate_success(self) -> None:
        card_data = {"name": "Test", "description": "d", "url": "https://test.com", "version": "1.0"}
        mock_response = MagicMock()
        mock_response.json.return_value = card_data

        server = MCPServer(".")
        _initialize_server(server)
        with patch("ass_ade.a2a.socket.getaddrinfo", return_value=_FAKE_ADDR_INFO), \
             patch("ass_ade.a2a.httpx.get", return_value=mock_response):
            response = server._handle({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "a2a_validate", "arguments": {"url": "https://test.com"}},
            })

        assert response is not None
        result_data = json.loads(response["result"]["content"][0]["text"])
        assert result_data["valid"] is True

    def test_a2a_validate_missing_url(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "a2a_validate", "arguments": {"url": ""}},
        })
        assert response is not None
        assert response["error"]["code"] == -32602


# ── A2A negotiate via MCP ────────────────────────────────────────────────────


class TestMCPA2ANegotiate:
    def test_a2a_negotiate_invalid_remote(self) -> None:
        import httpx as _httpx

        server = MCPServer(".")
        _initialize_server(server)
        with patch("ass_ade.a2a.httpx.get", side_effect=_httpx.ConnectError("refused")):
            response = server._handle({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "a2a_negotiate", "arguments": {"remote_url": "https://bad.com"}},
            })

        assert response is not None
        assert response["result"]["isError"]


# ── Trust gate via MCP (local profile blocks) ────────────────────────────────


class TestMCPTrustGate:
    def test_trust_gate_requires_agent_id(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "trust_gate", "arguments": {"agent_id": ""}},
        })
        assert response is not None
        assert response["error"]["code"] == -32602

    def test_trust_gate_local_profile_blocked(self) -> None:

        server = MCPServer(".")
        _initialize_server(server)
        # Mock load_config to return local profile
        with patch("ass_ade.mcp.server.MCPServer._get_nexus_client", side_effect=RuntimeError("local")):
            response = server._handle({
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "trust_gate", "arguments": {"agent_id": "test-agent"}},
            })
        assert response is not None
        assert response["result"]["isError"]

    def test_get_nexus_client_uses_configured_api_key(self) -> None:
        server = MCPServer(".")
        cfg = AssAdeConfig(
            profile="hybrid",
            nexus_base_url="https://atomadic.tech",
            request_timeout_s=12.0,
            nexus_api_key="test-secret",
        )

        with (
            patch("ass_ade.config.load_config", return_value=cfg),
            patch("ass_ade.nexus.client.NexusClient") as client_cls,
        ):
            client = server._get_nexus_client()

        assert client is client_cls.return_value
        client_cls.assert_called_once_with(
            base_url="https://atomadic.tech",
            timeout=12.0,
            api_key="test-secret",
        )


# ── Initialize / ping ────────────────────────────────────────────────────────


class TestMCPProtocol:
    def test_initialize(self) -> None:
        server = MCPServer(".")
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {},
        })
        assert response is not None
        assert response["result"]["protocolVersion"] == "2025-11-25"
        assert response["result"]["serverInfo"]["version"] == "1.0.0"

    def test_ping(self) -> None:
        server = MCPServer(".")
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "ping",
            "params": {},
        })
        assert response is not None
        assert response["result"] == {}

    def test_initialize_declares_logging_capability(self) -> None:
        server = MCPServer(".")
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2025-11-25"},
        })
        assert response is not None
        caps = response["result"]["capabilities"]
        assert "logging" in caps
        assert "tools" in caps

    def test_initialize_ignores_older_client_version(self) -> None:
        """Server always responds with its own version regardless of client request."""
        server = MCPServer(".")
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2024-11-05"},
        })
        assert response is not None
        assert response["result"]["protocolVersion"] == "2025-11-25"


# ── MCP 2025-11-25 features ───────────────────────────────────────────────────


class TestMCP202511Features:
    def test_tool_annotations_present_on_workflow_tools(self) -> None:
        for tool in _WORKFLOW_TOOLS:
            assert "annotations" in tool, f"{tool['name']} missing annotations"
            ann = tool["annotations"]
            assert "readOnlyHint" in ann
            assert "destructiveHint" in ann
            assert "idempotentHint" in ann
            assert "openWorldHint" in ann

    def test_tools_list_includes_annotations_for_builtin_tools(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {},
        })
        assert response is not None
        tools = {t["name"]: t for t in response["result"]["tools"]}

        for name in ("read_file", "write_file", "edit_file", "run_command",
                     "list_directory", "search_files", "grep_search"):
            assert "annotations" in tools[name], f"{name} missing annotations"

    def test_read_file_is_readonly(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {},
        })
        tools = {t["name"]: t for t in response["result"]["tools"]}
        assert tools["read_file"]["annotations"]["readOnlyHint"] is True
        assert tools["read_file"]["annotations"]["destructiveHint"] is False

    def test_write_file_is_destructive(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {},
        })
        tools = {t["name"]: t for t in response["result"]["tools"]}
        assert tools["write_file"]["annotations"]["destructiveHint"] is True
        assert tools["write_file"]["annotations"]["readOnlyHint"] is False

    def test_run_command_is_open_world(self) -> None:
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {},
        })
        tools = {t["name"]: t for t in response["result"]["tools"]}
        assert tools["run_command"]["annotations"]["openWorldHint"] is True

    def test_tools_list_accepts_cursor_param(self) -> None:
        """Cursor is accepted; all tools returned in single page with no nextCursor."""
        server = MCPServer(".")
        _initialize_server(server)
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {"cursor": "some-cursor"},
        })
        assert response is not None
        assert "tools" in response["result"]
        assert "nextCursor" not in response["result"]

    def test_notifications_cancelled_suppresses_no_response(self) -> None:
        """notifications/cancelled has no id — server returns None."""
        server = MCPServer(".")
        response = server._handle({
            "method": "notifications/cancelled",
            "params": {"requestId": 42, "reason": "user cancel"},
        })
        assert response is None

    def test_cancelled_request_returns_error(self) -> None:
        """If a request ID is cancelled before dispatch, tools/call returns -32800."""
        server = MCPServer(".")
        _initialize_server(server)
        # Simulate the client sending a cancel notification first
        server._handle({
            "method": "notifications/cancelled",
            "params": {"requestId": 99},
        })
        # Now the request with that ID arrives
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 99,
            "method": "tools/call",
            "params": {"name": "read_file", "arguments": {"path": "."}},
        })
        assert response is not None
        assert "error" in response
        assert response["error"]["code"] == -32800

    def test_progress_token_extracted_from_meta(self, tmp_path) -> None:
        """_meta.progressToken is accepted in tools/call params without error."""
        # Create the server rooted at tmp_path so the file is within working dir.
        server = MCPServer(str(tmp_path))
        _initialize_server(server)
        # read_file is a builtin tool; it runs synchronously without progress,
        # but the server must accept the _meta field without error.
        test_file = tmp_path / "meta_test.txt"
        test_file.write_text("hello")
        response = server._handle({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "read_file",
                "arguments": {"path": "meta_test.txt"},
                "_meta": {"progressToken": "tok-1"},
            },
        })
        assert response is not None
        assert response["result"]["isError"] is False
