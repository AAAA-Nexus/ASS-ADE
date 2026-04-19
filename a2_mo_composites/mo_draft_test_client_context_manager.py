# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_test_client_context_manager.py:7
# Component id: mo.source.a2_mo_composites.test_client_context_manager
from __future__ import annotations

__version__ = "0.1.0"

def test_client_context_manager():
    """Test that client properly closes HTTP connections."""
    transport = httpx.MockTransport(lambda r: httpx.Response(200, json={"status": "ok"}))

    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.get_health()
        assert result is not None
