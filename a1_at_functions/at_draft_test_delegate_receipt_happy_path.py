# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_delegate_receipt_happy_path.py:7
# Component id: at.source.a1_at_functions.test_delegate_receipt_happy_path
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
