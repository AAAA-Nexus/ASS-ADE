# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_handle_x402_empty_body.py:7
# Component id: at.source.a1_at_functions.test_handle_x402_empty_body
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
