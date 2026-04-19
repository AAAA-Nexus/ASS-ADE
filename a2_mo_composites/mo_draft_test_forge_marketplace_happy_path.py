# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:1241
# Component id: mo.source.ass_ade.test_forge_marketplace_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_forge_marketplace_happy_path(method_name, response_json):
    """Test Forge Marketplace methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "forge_leaderboard":
            result = client.forge_leaderboard()
        elif method_name == "forge_verify":
            result = client.forge_verify(agent_id="agent_1")
        elif method_name == "forge_quarantine":
            result = client.forge_quarantine(model_id="model_1", reason="security_risk")
        elif method_name == "forge_delta_submit":
            result = client.forge_delta_submit(agent_id="agent_1", delta={"improvement": "faster"})
        else:  # forge_badge
            result = client.forge_badge(badge_id="badge_123")
        assert result is not None
