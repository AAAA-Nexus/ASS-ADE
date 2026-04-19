# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:1310
# Component id: mo.source.ass_ade.test_client_manual_close
from __future__ import annotations

__version__ = "0.1.0"

def test_client_manual_close():
    """Test manual client close."""
    transport = httpx.MockTransport(lambda r: httpx.Response(200, json={"status": "ok"}))
    client = NexusClient(base_url="https://atomadic.tech", transport=transport)
    result = client.get_health()
    assert result is not None
    client.close()
