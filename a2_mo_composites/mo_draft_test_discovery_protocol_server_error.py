# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:108
# Component id: mo.source.ass_ade.test_discovery_protocol_server_error
from __future__ import annotations

__version__ = "0.1.0"

def test_discovery_protocol_server_error(method_name):
    """Test discovery methods handle 500 errors."""
    transport = httpx.MockTransport(lambda r: httpx.Response(500, json={"error": "Internal Server Error"}))
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        with pytest.raises(Exception):  # raise_for_status
            getattr(client, method_name)()
