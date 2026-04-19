# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testmcpprotocol.py:7
# Component id: sy.source.a4_sy_orchestration.testmcpprotocol
from __future__ import annotations

__version__ = "0.1.0"

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
