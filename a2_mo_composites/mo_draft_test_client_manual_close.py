# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_test_client_manual_close.py:7
# Component id: mo.source.a2_mo_composites.test_client_manual_close
from __future__ import annotations

__version__ = "0.1.0"

def test_client_manual_close():
    """Test manual client close."""
    transport = httpx.MockTransport(lambda r: httpx.Response(200, json={"status": "ok"}))
    client = NexusClient(base_url="https://atomadic.tech", transport=transport)
    result = client.get_health()
    assert result is not None
    client.close()
