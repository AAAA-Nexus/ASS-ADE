# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_consensus_result_happy_path.py:7
# Component id: at.source.a1_at_functions.test_consensus_result_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_consensus_result_happy_path():
    """Test consensus_result GET endpoint."""
    def handler(request):
        assert "/v1/consensus/session/" in request.url.path and "/result" in request.url.path
        return httpx.Response(200, json={"session_id": "session_123", "winning_output": "output", "confidence": 0.95})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.consensus_result(session_id="session_123")
        assert result is not None
