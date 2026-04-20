from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from ass_ade.cli import app
from ass_ade.context_memory import (
    VECTOR_DIMENSIONS,
    build_context_packet,
    query_vector_memory,
    store_vector_memory,
    vector_embed,
)
from ass_ade.mcp.server import MCPServer
from ass_ade.recon import phase0_recon

runner = CliRunner()


def _initialize_server(server: MCPServer) -> None:
    response = server._handle({
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {},
    })
    assert response is not None
    server._handle({"method": "notifications/initialized", "params": {}})


def _seed_repo(root: Path) -> None:
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "README.md").write_text("# demo\n", encoding="utf-8")
    (root / "src" / "mcp_server.py").write_text(
        "def list_tools():\n    return []\n",
        encoding="utf-8",
    )
    (root / "tests" / "test_mcp_server.py").write_text(
        "def test_tools():\n    assert True\n",
        encoding="utf-8",
    )


def test_phase0_recon_requires_latest_docs_for_technical_task(tmp_path: Path) -> None:
    _seed_repo(tmp_path)

    result = phase0_recon(
        task_description="Add an MCP tool schema",
        working_dir=tmp_path,
    )

    assert result.verdict == "RECON_REQUIRED"
    assert result.research_targets[0].suggested_url is not None
    assert "modelcontextprotocol.io" in result.research_targets[0].suggested_url
    assert "src/mcp_server.py" in result.codebase.relevant_files


def test_phase0_recon_ready_when_sources_are_attached(tmp_path: Path) -> None:
    _seed_repo(tmp_path)

    result = phase0_recon(
        task_description="Add an MCP tool schema",
        working_dir=tmp_path,
        provided_sources=["https://modelcontextprotocol.io/specification/2025-11-25/server/tools"],
    )

    assert result.verdict == "READY_FOR_PHASE_1"
    assert result.provided_sources


def test_context_packet_includes_file_hashes(tmp_path: Path) -> None:
    _seed_repo(tmp_path)

    packet = build_context_packet(
        task_description="Add an MCP tool schema",
        working_dir=tmp_path,
        file_paths=["src/mcp_server.py"],
        source_urls=["https://modelcontextprotocol.io/specification/2025-11-25/server/tools"],
    )

    assert packet.recon_verdict == "READY_FOR_PHASE_1"
    assert packet.files[0].path == "src/mcp_server.py"
    assert len(packet.files[0].sha256) == 64


def test_vector_memory_store_and_query(tmp_path: Path) -> None:
    vector = vector_embed("trusted rag context")
    assert len(vector) == VECTOR_DIMENSIONS

    stored = store_vector_memory(
        text="trusted rag context for mcp tools",
        namespace="demo",
        metadata={"source": "unit"},
        working_dir=tmp_path,
    )
    result = query_vector_memory(
        query="mcp trusted context",
        namespace="demo",
        working_dir=tmp_path,
    )

    assert stored.id == result.matches[0].id
    assert result.matches[0].metadata["source"] == "unit"


def test_mcp_phase0_recon_tool_requires_sources(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    server = MCPServer(str(tmp_path))
    _initialize_server(server)

    response = server._handle({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "phase0_recon",
            "arguments": {"task_description": "Add an MCP tool schema"},
        },
    })

    assert response is not None
    assert response["result"]["isError"] is True
    payload = json.loads(response["result"]["content"][0]["text"])
    assert payload["verdict"] == "RECON_REQUIRED"


def test_mcp_context_memory_roundtrip(tmp_path: Path) -> None:
    server = MCPServer(str(tmp_path))
    _initialize_server(server)
    store_response = server._handle({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "context_memory_store",
            "arguments": {"text": "phase zero recon context", "namespace": "demo"},
        },
    })
    query_response = server._handle({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "context_memory_query",
            "arguments": {"query": "recon", "namespace": "demo"},
        },
    })

    assert store_response is not None
    assert store_response["result"]["isError"] is False
    assert query_response is not None
    payload = json.loads(query_response["result"]["content"][0]["text"])
    assert len(payload["matches"]) == 1


def test_cli_phase0_recon_json(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    result = runner.invoke(
        app,
        [
            "workflow",
            "phase0-recon",
            "Add an MCP tool schema",
            "--path",
            str(tmp_path),
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert '"verdict": "RECON_REQUIRED"' in result.stdout


def test_cli_context_store_query_json(tmp_path: Path) -> None:
    stored = runner.invoke(
        app,
        [
            "context",
            "store",
            "trusted docs packet",
            "--namespace",
            "demo",
            "--path",
            str(tmp_path),
            "--json",
        ],
    )
    queried = runner.invoke(
        app,
        [
            "context",
            "query",
            "trusted docs",
            "--namespace",
            "demo",
            "--path",
            str(tmp_path),
            "--json",
        ],
    )

    assert stored.exit_code == 0
    assert queried.exit_code == 0
    assert '"matches"' in queried.stdout
