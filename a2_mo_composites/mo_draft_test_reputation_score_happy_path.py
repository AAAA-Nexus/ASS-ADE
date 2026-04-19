# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:394
# Component id: mo.source.ass_ade.test_reputation_score_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_reputation_score_happy_path():
    """Test reputation_score GET endpoint."""
    def handler(request):
        assert "/v1/reputation/score/" in request.url.path
        return httpx.Response(200, json={"agent_id": "agent_1", "tier": "gold", "fee_multiplier": 0.8})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.reputation_score(agent_id="agent_1")
        assert result is not None
