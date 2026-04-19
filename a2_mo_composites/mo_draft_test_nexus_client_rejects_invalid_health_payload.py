# Extracted from C:/!ass-ade/tests/test_nexus_client.py:26
# Component id: mo.source.ass_ade.test_nexus_client_rejects_invalid_health_payload
from __future__ import annotations

__version__ = "0.1.0"

def test_nexus_client_rejects_invalid_health_payload() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json={"version": "0.5.1"}))

    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        with pytest.raises(Exception):
            client.get_health()
