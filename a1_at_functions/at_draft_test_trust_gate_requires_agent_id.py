# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_trust_gate_requires_agent_id.py:7
# Component id: at.source.a1_at_functions.test_trust_gate_requires_agent_id
from __future__ import annotations

__version__ = "0.1.0"

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
