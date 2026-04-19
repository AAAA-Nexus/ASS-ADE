# Extracted from C:/!ass-ade/tests/test_search_x402.py:155
# Component id: at.source.ass_ade.test_handle_x402_empty_body
from __future__ import annotations

__version__ = "0.1.0"

def test_handle_x402_empty_body(self) -> None:
    """handle_x402 should handle empty or malformed 402 body."""
    client = self._make_client()
    mock_response = httpx.Response(402, text="Payment Required")
    result = client.handle_x402(mock_response)
    assert result["payment_required"] is True
    assert result["amount_usdc"] == 0
    assert result["network"] == "base"
    client.close()
