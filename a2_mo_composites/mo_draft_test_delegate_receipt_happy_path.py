# Extracted from C:/!ass-ade/tests/test_nexus_client_comprehensive.py:283
# Component id: mo.source.ass_ade.test_delegate_receipt_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_delegate_receipt_happy_path():
    """Test delegate_receipt GET endpoint."""
    def handler(request):
        assert "/v1/delegate/receipt/" in request.url.path
        return httpx.Response(200, json={"receipt_id": "receipt_123", "signature": "sig_xyz"})

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        result = client.delegate_receipt(receipt_id="receipt_123")
        assert result is not None
