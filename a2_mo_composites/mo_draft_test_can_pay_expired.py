# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testx402clientflow.py:29
# Component id: mo.source.ass_ade.test_can_pay_expired
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
