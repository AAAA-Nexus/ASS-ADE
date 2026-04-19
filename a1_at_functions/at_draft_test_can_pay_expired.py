# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:173
# Component id: at.source.ass_ade.test_can_pay_expired
__version__ = "0.1.0"

    def test_can_pay_expired(self) -> None:
        """X402ClientFlow should reject expired challenges."""
        flow = X402ClientFlow()
        challenge = PaymentChallenge.from_response({
            "recipient": ATOMADIC_TREASURY,
            "amount_micro_usdc": 1000,
            "expires": 1,  # Already expired
        })
        assert not flow.can_pay(challenge)
        assert "expired" in flow.last_error.lower()
