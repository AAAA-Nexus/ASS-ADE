"""Regression tests for privileged MCP built-ins (path + run_command hardening)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ass_ade.mcp.server import MCPServer
from ass_ade.tools.builtin import ReadFileTool, RunCommandTool, WriteFileTool


def _init(server: MCPServer) -> None:
    server._handle({"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {}})
    server._handle({"method": "notifications/initialized", "params": {}})


def test_run_command_blocks_python_inline_c_by_default(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ASS_ADE_ALLOW_INLINE_RUN_COMMAND", raising=False)
    tool = RunCommandTool(str(tmp_path))
    r = tool.execute(command='python -c "print(1)"')
    assert not r.success
    assert "inline" in (r.error or "").lower() or "disabled" in (r.error or "").lower()


def test_run_command_allows_python_c_when_env_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ASS_ADE_ALLOW_INLINE_RUN_COMMAND", "1")
    tool = RunCommandTool(str(tmp_path))
    r = tool.execute(command='python -c "print(99)"')
    assert r.success
    assert "99" in r.output


def test_run_command_blocks_multiline(tmp_path: Path) -> None:
    tool = RunCommandTool(str(tmp_path))
    r = tool.execute(command="python\nhello.py")
    assert not r.success
    assert "multiline" in (r.error or "").lower() or "nul" in (r.error or "").lower()


def test_run_command_blocks_node_eval(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ASS_ADE_ALLOW_INLINE_RUN_COMMAND", raising=False)
    tool = RunCommandTool(str(tmp_path))
    r = tool.execute(command='node -e "console.log(1)"')
    assert not r.success
    assert "node" in (r.error or "").lower() or "blocked" in (r.error or "").lower()


def test_read_rejects_parent_escape(tmp_path: Path) -> None:
    (tmp_path / "secret.txt").write_text("x", encoding="utf-8")
    sub = tmp_path / "w"
    sub.mkdir()
    tool = ReadFileTool(str(sub))
    r = tool.execute(path="../secret.txt")
    assert not r.success
    assert "outside" in (r.error or "").lower()


def test_write_rejects_absolute_outside(tmp_path: Path) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    target = outside / "x.txt"
    inner = tmp_path / "inner"
    inner.mkdir()
    tool = WriteFileTool(str(inner))
    r = tool.execute(path=str(target), content="no")
    assert not r.success


def test_mcp_run_command_blocks_inline_via_json_rpc(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("ASS_ADE_ALLOW_INLINE_RUN_COMMAND", raising=False)
    (tmp_path / "ok.py").write_text("print('ok')\n", encoding="utf-8")
    server = MCPServer(str(tmp_path))
    _init(server)
    resp = server._handle({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "run_command", "arguments": {"command": 'python -c "print(1)"'}},
    })
    assert resp is not None
    body = resp["result"]["content"][0]["text"]
    assert resp["result"]["isError"] is True
    assert "inline" in body.lower() or "disabled" in body.lower()
