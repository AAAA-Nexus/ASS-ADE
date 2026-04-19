# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:327
# Component id: at.source.ass_ade.test_full_flow_parse_and_validate
__version__ = "0.1.0"

    def test_full_flow_parse_and_validate(self) -> None:
        """Full flow: parse challenge → validate → build proof."""
        flow = X402ClientFlow()

        # Step 1: Server returns 402 with challenge
        response_body = {
            "x402_version": "2.1",
            "chain_id": BASE_SEPOLIA_CHAIN_ID,
            "token_address": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
            "amount_micro_usdc": 5000,
            "amount_usdc": "0.005000",
            "recipient": "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9",
            "nonce": "test_nonce",
            "expires": 9999999999,
            "endpoint": "/v1/trust/score",
        }

        # Step 2: Client parses challenge
        challenge = flow.parse_challenge(response_body)
        assert challenge is not None
        assert challenge.amount_micro_usdc == 5000
        assert challenge.endpoint == "/v1/trust/score"

        # Step 3: Client checks if it can pay
        with patch.dict("os.environ", {"ATOMADIC_X402_TESTNET": "1"}, clear=False):
            assert flow.can_pay(challenge)

        # Step 4: Simulate successful payment (normally would submit to blockchain)
        payment = PaymentResult(
            success=True,
            txid="0x1234567890abcdef",
            signature_header="abcd;0xWalletAddress;0x1234567890abcdef;5000",
            testnet=True,
        )

        # Step 5: Extract proof and build headers
        proof = flow.get_proof(payment)
        assert proof is not None
        assert proof.transaction_id == "0x1234567890abcdef"
        assert proof.amount_micro_usdc == 5000

        # Step 6: Build headers for retry
        headers = flow.build_proof_headers(payment)
        assert headers["PAYMENT-SIGNATURE"] == "abcd;0xWalletAddress;0x1234567890abcdef;5000"
