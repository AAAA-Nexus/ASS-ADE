# Extracted from C:/!ass-ade/tests/test_x402_flow.py:184
# Component id: at.source.ass_ade.test_parse_challenge_amount_too_large
from __future__ import annotations

__version__ = "0.1.0"

def test_parse_challenge_amount_too_large(self) -> None:
    """Oversized challenges should be rejected during parsing."""
    flow = X402ClientFlow()
    challenge = flow.parse_challenge({
        "recipient": "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9",
        "amount_micro_usdc": 100_000_000_000,
        "expires": 9999999999,
    })
    assert challenge is None
    assert "range" in flow.last_error.lower()
