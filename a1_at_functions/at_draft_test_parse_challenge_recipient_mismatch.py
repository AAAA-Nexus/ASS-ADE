# Extracted from C:/!ass-ade/tests/test_x402_flow.py:195
# Component id: at.source.ass_ade.test_parse_challenge_recipient_mismatch
from __future__ import annotations

__version__ = "0.1.0"

def test_parse_challenge_recipient_mismatch(self) -> None:
    """Recipient mismatches should be rejected before consent."""
    flow = X402ClientFlow()
    challenge = flow.parse_challenge({
        "recipient": "0x0000000000000000000000000000000000000001",
        "amount_micro_usdc": 1000,
        "expires": 9999999999,
    })
    assert challenge is None
    assert "treasury" in flow.last_error.lower()
