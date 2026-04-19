# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_mev_shield_happy_path.py:7
# Component id: at.source.a1_at_functions.test_mev_shield_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_mev_shield_happy_path(method_name, response_json):
    """Test MEV Shield methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "mev_protect":
            result = client.mev_protect(tx_bundle=["tx1", "tx2"])
        else:  # mev_status
            result = client.mev_status(bundle_id="bundle_123")
        assert result is not None
