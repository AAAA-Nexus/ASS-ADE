# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:219
# Component id: qk.source.ass_ade.test_build_proof_headers
__version__ = "0.1.0"

    def test_build_proof_headers(self) -> None:
        """X402ClientFlow should build proof headers from payment result."""
        flow = X402ClientFlow()
        result = PaymentResult(
            success=True,
            txid="0xabc",
            signature_header="sig;0x1234;0xabc;5000",
        )
        headers = flow.build_proof_headers(result)
        assert "PAYMENT-SIGNATURE" in headers
        assert headers["PAYMENT-SIGNATURE"] == "sig;0x1234;0xabc;5000"
