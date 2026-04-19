# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testx402clientflow.py:53
# Component id: at.source.a2_mo_composites.test_parse_challenge_recipient_mismatch
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
