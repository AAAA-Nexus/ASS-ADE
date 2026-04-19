# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_vrf_gaming_happy_path.py:7
# Component id: at.source.a1_at_functions.test_vrf_gaming_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_vrf_gaming_happy_path(method_name, response_json):
    """Test VRF gaming methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "vrf_draw":
            result = client.vrf_draw(range_min=1, range_max=100, count=3)
        else:  # vrf_verify_draw
            result = client.vrf_verify_draw(draw_id="vrf_draw_123")
        assert result is not None
