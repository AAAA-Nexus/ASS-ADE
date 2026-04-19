# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testx402clientflow.py:8
# Component id: at.source.a2_mo_composites.test_parse_challenge_valid
from __future__ import annotations

__version__ = "0.1.0"

def test_parse_challenge_valid(self) -> None:
    """X402ClientFlow should parse a valid challenge response."""
    flow = X402ClientFlow()
    body = {
        "amount_micro_usdc": 5000,
        "amount_usdc": 0.005,
        "recipient": ATOMADIC_TREASURY,
        "nonce": "abc",
        "expires": 9999999999,
        "chain_id": BASE_MAINNET_CHAIN_ID,
        "endpoint": "/v1/trust/score",
    }
    challenge = flow.parse_challenge(body)
    assert challenge is not None
    assert challenge.amount_micro_usdc == 5000
