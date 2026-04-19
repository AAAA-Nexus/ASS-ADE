# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:180
# Component id: mo.source.ass_ade.test_ratchetgate_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_ratchetgate_happy_path(method_name, path, response_json):
    """Test RatchetGate methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "ratchet_register":
            result = client.ratchet_register(agent_id=324)
        elif method_name == "ratchet_advance":
            result = client.ratchet_advance(session_id="ratchet_abc123")
        elif method_name == "ratchet_probe":
            result = client.ratchet_probe(session_ids=["ratchet_abc123"])
        assert result is not None
