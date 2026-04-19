# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:372
# Component id: at.source.ass_ade.test_full_flow_payment_failure
__version__ = "0.1.0"

    def test_full_flow_payment_failure(self) -> None:
        """Full flow: challenge → failure to pay."""
        flow = X402ClientFlow()

        response_body = {
            "amount_micro_usdc": 5000,
            "amount_usdc": "0.005",
            "recipient": ATOMADIC_TREASURY,
            "expires": 1,  # Already expired
        }

        challenge = flow.parse_challenge(response_body)
        assert challenge is not None

        # Client should not proceed due to expiry
        assert not flow.can_pay(challenge)
        assert "expired" in flow.last_error.lower()
