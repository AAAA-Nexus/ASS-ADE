# Extracted from C:/!ass-ade/tests/test_x402_flow.py:68
# Component id: at.source.ass_ade.test_from_response_minimal
from __future__ import annotations

__version__ = "0.1.0"

def test_from_response_minimal(self) -> None:
    with pytest.raises(ValueError, match="recipient"):
        PaymentChallenge.from_response({})
