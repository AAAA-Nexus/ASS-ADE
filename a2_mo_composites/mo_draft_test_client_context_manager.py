# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:1300
# Component id: mo.source.ass_ade.test_client_context_manager
from __future__ import annotations

__version__ = "0.1.0"

def test_client_context_manager():
    """Test that client properly closes HTTP connections."""
    transport = httpx.MockTransport(lambda r: httpx.Response(200, json={"status": "ok"}))

    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.get_health()
        assert result is not None
