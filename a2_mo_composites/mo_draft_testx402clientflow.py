# Extracted from C:/!ass-ade/tests/test_x402_flow.py:149
# Component id: mo.source.ass_ade.testx402clientflow
from __future__ import annotations

__version__ = "0.1.0"

class TestX402ClientFlow:
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

    def test_parse_challenge_invalid(self) -> None:
        """X402ClientFlow should set last_error on parse failure."""
        flow = X402ClientFlow()
        challenge = flow.parse_challenge({})  # Missing required fields
        assert challenge is None
        assert flow.last_error  # Error should be set

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

    def test_parse_challenge_amount_too_large(self) -> None:
        """Oversized challenges should be rejected during parsing."""
        flow = X402ClientFlow()
        challenge = flow.parse_challenge({
            "recipient": "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9",
            "amount_micro_usdc": 100_000_000_000,
            "expires": 9999999999,
        })
        assert challenge is None
        assert "range" in flow.last_error.lower()

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
