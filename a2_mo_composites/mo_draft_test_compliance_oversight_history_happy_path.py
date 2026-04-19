# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:930
# Component id: mo.source.ass_ade.test_compliance_oversight_history_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_compliance_oversight_history_happy_path():
    """Test compliance_oversight_history GET endpoint (returns raw dict)."""
    def handler(request):
        return httpx.Response(200, json={"history": [{"reviewer": "rev1", "decision": "approved"}]})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.compliance_oversight_history(system_id="system_1")
        assert isinstance(result, dict)
