# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:206
# Component id: at.source.ass_ade.test_can_pay_valid
__version__ = "0.1.0"

    def test_can_pay_valid(self) -> None:
        """X402ClientFlow should accept valid challenges."""
        flow = X402ClientFlow()
        with patch.dict("os.environ", {"ATOMADIC_X402_TESTNET": "1"}, clear=False):
            challenge = PaymentChallenge.from_response({
                "recipient": "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9",
                "amount_micro_usdc": 5000,
                "expires": 9999999999,
                "chain_id": BASE_SEPOLIA_CHAIN_ID,
                "endpoint": "/v1/trust/score",
            })
            assert flow.can_pay(challenge)
