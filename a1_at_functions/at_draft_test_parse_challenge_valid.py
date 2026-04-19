# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:150
# Component id: at.source.ass_ade.test_parse_challenge_valid
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
