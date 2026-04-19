# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_contract_attestation_happy_path.py:7
# Component id: at.source.a1_at_functions.test_contract_attestation_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_contract_attestation_happy_path():
    """Test contract_attestation GET endpoint."""
    def handler(request):
        assert "/v1/contract/attestation/" in request.url.path
        return httpx.Response(200, json={"contract_id": "contract_123", "attestation": "certified"})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.contract_attestation(contract_id="contract_123")
        assert result is not None
