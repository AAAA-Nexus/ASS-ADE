# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:92
# Component id: mo.source.ass_ade.test_discovery_protocol_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_discovery_protocol_happy_path(method_name, path, response_json, expected_key):
    """Test discovery & protocol methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        method = getattr(client, method_name)
        result = method()
        assert hasattr(result, expected_key), f"{method_name} missing {expected_key}"
