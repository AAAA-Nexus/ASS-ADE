"""Tests for MCP server, streaming, and diff preview."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ass_ade.agent.loop import AgentLoop
from ass_ade.engine.types import (
    CompletionResponse,
    Message,
    ToolCallRequest,
)
from ass_ade.mcp.server import MCPServer
from ass_ade.tools.base import ToolResult
from ass_ade.tools.builtin import EditFileTool
from ass_ade.tools.registry import ToolRegistry


def _initialize_server(server: MCPServer) -> None:
    response = server._handle({
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {},
    })
    assert response is not None
    server._handle({"method": "notifications/initialized", "params": {}})

# ══════════════════════════════════════════════════════════════════════════════
# MCP Server
# ══════════════════════════════════════════════════════════════════════════════


class TestMCPServer:
    @pytest.fixture
    def server(self, tmp_path: Path) -> MCPServer:
        (tmp_path / "hello.py").write_text("print('hi')\n")
        return MCPServer(working_dir=str(tmp_path))

    def test_initialize(self, server: MCPServer):
        req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        resp = server._handle(req)
        assert resp is not None
        assert resp["id"] == 1
        result = resp["result"]
        assert result["protocolVersion"] == "2025-11-25"
        assert result["serverInfo"]["name"] == "ass-ade"
        assert "tools" in result["capabilities"]

    def test_tools_list(self, server: MCPServer):
        _initialize_server(server)
        req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        resp = server._handle(req)
        assert resp is not None
        tools = resp["result"]["tools"]
        names = {t["name"] for t in tools}
        assert "read_file" in names
        assert "write_file" in names
        assert "edit_file" in names
        assert "run_command" in names
        assert "list_directory" in names
        assert "search_files" in names
        assert "grep_search" in names
        assert "phase0_recon" in names
        assert "context_pack" in names
        assert "context_memory_store" in names
        assert "context_memory_query" in names
        assert "map_terrain" in names
        # Verify minimum expected tools; exact count may vary with additional tools
        assert len(tools) >= 19  # At least 8 builtin + 11 workflow/agent/A2A

    def test_tools_call_read_file(self, server: MCPServer):
        _initialize_server(server)
        req = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "read_file", "arguments": {"path": "hello.py"}},
        }
        resp = server._handle(req)
        assert resp is not None
        assert resp["result"]["isError"] is False
        content = resp["result"]["content"][0]["text"]
        assert "print('hi')" in content

    def test_tools_call_unknown(self, server: MCPServer):
        _initialize_server(server)
        req = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "nonexistent_tool", "arguments": {}},
        }
        resp = server._handle(req)
        assert resp is not None
        assert resp["result"]["isError"] is True
        assert "Unknown tool" in resp["result"]["content"][0]["text"]

    def test_unknown_method(self, server: MCPServer):
        _initialize_server(server)
        req = {"jsonrpc": "2.0", "id": 5, "method": "weird/method", "params": {}}
        resp = server._handle(req)
        assert resp is not None
        assert "error" in resp
        assert resp["error"]["code"] == -32601

    def test_ping(self, server: MCPServer):
        req = {"jsonrpc": "2.0", "id": 6, "method": "ping", "params": {}}
        resp = server._handle(req)
        assert resp is not None
        assert resp["result"] == {}

    def test_notification_no_response(self, server: MCPServer):
        req = {"method": "notifications/initialized", "params": {}}
        resp = server._handle(req)
        assert resp is None

    def test_tools_call_write_file(self, server: MCPServer, tmp_path: Path):
        _initialize_server(server)
        req = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {
                "name": "write_file",
                "arguments": {"path": "new.py", "content": "x = 1\n"},
            },
        }
        resp = server._handle(req)
        assert resp["result"]["isError"] is False
        assert (tmp_path / "new.py").read_text() == "x = 1\n"

    def test_tools_call_list_directory(self, server: MCPServer):
        _initialize_server(server)
        req = {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "tools/call",
            "params": {"name": "list_directory", "arguments": {}},
        }
        resp = server._handle(req)
        assert resp["result"]["isError"] is False
        assert "hello.py" in resp["result"]["content"][0]["text"]


# ══════════════════════════════════════════════════════════════════════════════
# Diff Preview
# ══════════════════════════════════════════════════════════════════════════════


class TestDiffPreview:
    def test_preview_returns_diff(self, tmp_path: Path):
        (tmp_path / "code.py").write_text("x = 1\ny = 2\nz = 3\n")
        tool = EditFileTool(str(tmp_path))
        result = tool.execute(
            path="code.py",
            old_string="y = 2",
            new_string="y = 42",
            preview=True,
        )
        assert result.success
        assert "---" in result.output  # unified diff header
        assert "-y = 2" in result.output
        assert "+y = 42" in result.output

    def test_preview_does_not_modify(self, tmp_path: Path):
        (tmp_path / "code.py").write_text("x = 1\ny = 2\nz = 3\n")
        tool = EditFileTool(str(tmp_path))
        tool.execute(
            path="code.py",
            old_string="y = 2",
            new_string="y = 42",
            preview=True,
        )
        # File should be unchanged
        assert (tmp_path / "code.py").read_text() == "x = 1\ny = 2\nz = 3\n"

    def test_apply_includes_diff(self, tmp_path: Path):
        (tmp_path / "code.py").write_text("x = 1\ny = 2\nz = 3\n")
        tool = EditFileTool(str(tmp_path))
        result = tool.execute(
            path="code.py",
            old_string="y = 2",
            new_string="y = 42",
            preview=False,
        )
        assert result.success
        assert "Applied edit" in result.output
        assert "-y = 2" in result.output
        assert "+y = 42" in result.output
        # File should be changed
        assert "y = 42" in (tmp_path / "code.py").read_text()


# ══════════════════════════════════════════════════════════════════════════════
# Streaming (step_stream)
# ══════════════════════════════════════════════════════════════════════════════


class _MockProvider:
    def __init__(self, responses):
        self._responses = list(responses)
        self._idx = 0

    def complete(self, request):
        idx = min(self._idx, len(self._responses) - 1)
        self._idx += 1
        return self._responses[idx]


class _EchoTool:
    @property
    def name(self):
        return "echo"

    @property
    def description(self):
        return "Echo input."

    @property
    def parameters(self):
        return {"type": "object", "properties": {"text": {"type": "string"}}}

    def execute(self, **kwargs):
        return ToolResult(output=f"echoed: {kwargs.get('text', '')}")


class TestStepStream:
    def test_simple_done_event(self, tmp_path):
        provider = _MockProvider([
            CompletionResponse(
                message=Message(role="assistant", content="Hello!"),
                finish_reason="stop",
            )
        ])
        loop = AgentLoop(
            provider=provider,
            registry=ToolRegistry(),
            working_dir=str(tmp_path),
        )
        events = list(loop.step_stream("Hi"))
        assert len(events) == 1
        assert events[0].kind == "done"
        assert events[0].text == "Hello!"

    def test_tool_call_events(self, tmp_path):
        provider = _MockProvider([
            CompletionResponse(
                message=Message(
                    role="assistant",
                    content="",
                    tool_calls=[
                        ToolCallRequest(id="c1", name="echo", arguments={"text": "x"})
                    ],
                ),
                finish_reason="tool_calls",
            ),
            CompletionResponse(
                message=Message(role="assistant", content="Done."),
                finish_reason="stop",
            ),
        ])
        registry = ToolRegistry()
        registry.register(_EchoTool())

        loop = AgentLoop(
            provider=provider,
            registry=registry,
            working_dir=str(tmp_path),
        )
        events = list(loop.step_stream("Echo x"))

        kinds = [e.kind for e in events]
        assert "tool_call" in kinds
        assert "tool_result" in kinds
        assert "done" in kinds

        tool_event = next(e for e in events if e.kind == "tool_call")
        assert tool_event.tool_name == "echo"

        result_event = next(e for e in events if e.kind == "tool_result")
        assert result_event.tool_result is not None
        assert result_event.tool_result.success

    def test_blocked_event(self, tmp_path):
        provider = _MockProvider([])
        mock_gates = MagicMock()
        mock_gates.scan_prompt.return_value = {"blocked": True}

        loop = AgentLoop(
            provider=provider,
            registry=ToolRegistry(),
            working_dir=str(tmp_path),
            quality_gates=mock_gates,
        )
        events = list(loop.step_stream("Bad input"))
        assert len(events) == 1
        assert events[0].kind == "blocked"

    def test_max_rounds_error_event(self, tmp_path):
        never_stop = CompletionResponse(
            message=Message(
                role="assistant",
                content="",
                tool_calls=[
                    ToolCallRequest(id="c1", name="echo", arguments={"text": "loop"})
                ],
            ),
            finish_reason="tool_calls",
        )
        provider = _MockProvider([never_stop] * 30)
        registry = ToolRegistry()
        registry.register(_EchoTool())

        loop = AgentLoop(
            provider=provider,
            registry=registry,
            working_dir=str(tmp_path),
        )
        events = list(loop.step_stream("Loop"))
        assert events[-1].kind == "error"
        assert "maximum" in events[-1].text.lower()
