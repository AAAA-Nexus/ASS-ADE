# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_discovery_protocol_happy_path.py:7
# Component id: at.source.a1_at_functions.test_discovery_protocol_happy_path
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
