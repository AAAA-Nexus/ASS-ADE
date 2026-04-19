# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_certify_output_verify_happy_path.py:7
# Component id: at.source.a1_at_functions.test_certify_output_verify_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_certify_output_verify_happy_path():
    """Test certify_output_verify GET endpoint."""
    def handler(request):
        assert "/v1/certify/output/" in request.url.path and "/verify" in request.url.path
        return httpx.Response(200, json={"certificate_id": "cert_123", "verified": True})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.certify_output_verify(certificate_id="cert_123")
        assert result is not None
