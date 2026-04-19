# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:231
# Component id: qk.source.ass_ade.test_get_proof
__version__ = "0.1.0"

    def test_get_proof(self) -> None:
        """X402ClientFlow should extract PaymentProof from result."""
        flow = X402ClientFlow()
        result = PaymentResult(
            success=True,
            txid="0xabc",
            signature_header="sig;0x1234;0xabc;5000",
        )
        proof = flow.get_proof(result)
        assert proof is not None
        assert proof.wallet_address == "0x1234"
