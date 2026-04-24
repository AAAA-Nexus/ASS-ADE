"""Tests for x402 payment module and CLI commands."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from ass_ade.cli import app
from ass_ade.config import AssAdeConfig, write_default_config
from ass_ade.nexus.x402 import (
    PaymentChallenge,
    PaymentResult,
    PaymentProof,
    X402ClientFlow,
    format_payment_consent,
    get_chain_config,
    build_payment_header,
    ATOMADIC_TREASURY,
    BASE_MAINNET_CHAIN_ID,
    BASE_SEPOLIA_CHAIN_ID,
)

runner = CliRunner()


def _hybrid_config(tmp_path: Path) -> Path:
    config_path = tmp_path / ".ass-ade" / "config.json"
    write_default_config(config_path, config=AssAdeConfig(profile="hybrid"), overwrite=True)
    return config_path


def _make_ctx_mgr(mock_instance: MagicMock) -> MagicMock:
    ctx = MagicMock()
    ctx.__enter__ = MagicMock(return_value=mock_instance)
    ctx.__exit__ = MagicMock(return_value=False)
    return ctx


# ---------------------------------------------------------------------------
# PaymentChallenge tests
# ---------------------------------------------------------------------------


class TestPaymentChallenge:
    def test_from_response_full(self) -> None:
        body = {
            "x402_version": "2.1",
            "chain_id": 8453,
            "token_address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            "amount_micro_usdc": 8000,
            "amount_usdc": "0.008000",
            "recipient": "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9",
            "nonce": "abc123",
            "expires": 9999999999,
            "endpoint": "/v1/trust/score",
        }
        c = PaymentChallenge.from_response(body)
        assert c.amount_micro_usdc == 8000
        assert c.amount_usdc == 0.008
        assert c.recipient == "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9"
        assert c.chain_id == 8453
        assert c.endpoint == "/v1/trust/score"
        assert not c.is_expired
        assert "$0.008000 USDC" in c.display_amount

    def test_from_response_minimal(self) -> None:
        with pytest.raises(ValueError, match="recipient"):
            PaymentChallenge.from_response({})

    def test_expired_challenge(self) -> None:
        c = PaymentChallenge.from_response(
            {
                "recipient": "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9",
                "amount_micro_usdc": 1,
                "expires": 1,
            }
        )
        assert c.is_expired


# ---------------------------------------------------------------------------
# PaymentProof tests (new)
# ---------------------------------------------------------------------------


class TestPaymentProof:
    def test_from_payment_result_success(self) -> None:
        """PaymentProof should parse from a successful PaymentResult."""
        result = PaymentResult(
            success=True,
            txid="0xabc123",
            signature_header="sig123;0x1234567890abcdef;0xabc123;8000",
            testnet=True,
        )
        proof = PaymentProof.from_payment_result(result)
        assert proof is not None
        assert proof.signature == "sig123"
        assert proof.wallet_address == "0x1234567890abcdef"
        assert proof.transaction_id == "0xabc123"
        assert proof.amount_micro_usdc == 8000

    def test_from_payment_result_failure(self) -> None:
        """PaymentProof should return None for failed PaymentResult."""
        result = PaymentResult(success=False, error="No wallet")
        proof = PaymentProof.from_payment_result(result)
        assert proof is None

    def test_to_header_value(self) -> None:
        """PaymentProof should format as HTTP header value."""
        proof = PaymentProof(
            signature="sig123",
            wallet_address="0x1234",
            transaction_id="0xabc",
            amount_micro_usdc=8000,
        )
        header = proof.to_header_value()
        assert header == "sig123;0x1234;0xabc;8000"

    def test_from_header_value(self) -> None:
        """PaymentProof should parse from HTTP header value."""
        header = "sig123;0x1234;0xabc;8000"
        proof = PaymentProof.from_header_value(header)
        assert proof is not None
        assert proof.signature == "sig123"
        assert proof.wallet_address == "0x1234"
        assert proof.transaction_id == "0xabc"
        assert proof.amount_micro_usdc == 8000

    def test_header_roundtrip(self) -> None:
        """PaymentProof should roundtrip through header format."""
        original = PaymentProof(
            signature="sig456",
            wallet_address="0xabcdef",
            transaction_id="0x9876",
            amount_micro_usdc=5000,
        )
        header = original.to_header_value()
        restored = PaymentProof.from_header_value(header)
        assert restored == original


# ---------------------------------------------------------------------------
# X402ClientFlow tests (new)
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Chain config tests
# ---------------------------------------------------------------------------


class TestChainConfig:
    def test_mainnet_by_default(self) -> None:
        with patch.dict("os.environ", {"ATOMADIC_X402_TESTNET": ""}, clear=False):
            config = get_chain_config()
        assert config["chain_id"] == BASE_MAINNET_CHAIN_ID
        assert config["testnet"] is False
        assert "mainnet" in config["network_name"].lower()

    def test_testnet_mode(self) -> None:
        with patch.dict("os.environ", {"ATOMADIC_X402_TESTNET": "1"}, clear=False):
            config = get_chain_config()
        assert config["chain_id"] == BASE_SEPOLIA_CHAIN_ID
        assert config["testnet"] is True
        assert "sepolia" in config["network_name"].lower()

    def test_custom_rpc(self) -> None:
        with patch.dict("os.environ", {"BASE_RPC_URL": "https://custom.rpc"}, clear=False):
            config = get_chain_config()
        assert config["rpc_url"] == "https://custom.rpc"


# ---------------------------------------------------------------------------
# Payment consent formatting
# ---------------------------------------------------------------------------


class TestPaymentConsent:
    def test_format_includes_amount(self) -> None:
        c = PaymentChallenge.from_response({
            "amount_usdc": "0.008000",
            "amount_micro_usdc": 8000,
            "recipient": ATOMADIC_TREASURY,
            "endpoint": "/v1/trust/score",
        })
        text = format_payment_consent(c)
        assert "$0.008000 USDC" in text
        assert "/v1/trust/score" in text
        assert ATOMADIC_TREASURY in text

    def test_testnet_label(self) -> None:
        c = PaymentChallenge.from_response(
            {
                "amount_micro_usdc": 1000,
                "amount_usdc": "0.001",
                "recipient": "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9",
            }
        )
        with patch.dict("os.environ", {"ATOMADIC_X402_TESTNET": "1"}, clear=False):
            text = format_payment_consent(c)
        assert "TESTNET" in text


# ---------------------------------------------------------------------------
# Payment result + header building
# ---------------------------------------------------------------------------


class TestPaymentResult:
    def test_build_header_success(self) -> None:
        r = PaymentResult(success=True, txid="abc123", signature_header="sig;pk;txid;8000")
        headers = build_payment_header(r)
        assert "PAYMENT-SIGNATURE" in headers
        assert headers["PAYMENT-SIGNATURE"] == "sig;pk;txid;8000"

    def test_build_header_failure(self) -> None:
        r = PaymentResult(success=False, error="no wallet")
        headers = build_payment_header(r)
        assert headers == {}


# ---------------------------------------------------------------------------
# End-to-end client flow tests (new)
# ---------------------------------------------------------------------------


class TestX402EndToEndFlow:
    """Test the full x402 payment flow from challenge to proof."""

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


# ---------------------------------------------------------------------------
# CLI wallet command
# ---------------------------------------------------------------------------


class TestWalletCommand:
    def test_wallet_shows_status(self, tmp_path: Path) -> None:
        result = runner.invoke(
            app, ["wallet", "--config", str(_hybrid_config(tmp_path))],
            env={"ATOMADIC_X402_TESTNET": "1", "ATOMADIC_WALLET_KEY": ""},
        )
        assert result.exit_code == 0
        assert "Testnet Mode" in result.stdout or "x402" in result.stdout

    def test_wallet_testnet_on(self, tmp_path: Path) -> None:
        result = runner.invoke(
            app, ["wallet", "--config", str(_hybrid_config(tmp_path))],
            env={"ATOMADIC_X402_TESTNET": "1"},
        )
        assert result.exit_code == 0


# ---------------------------------------------------------------------------
# CLI pay command
# ---------------------------------------------------------------------------


class TestPayCommand:
    def test_pay_no_payment_required(self, tmp_path: Path) -> None:
        """If endpoint returns 200, pay should show results without payment."""
        mock_nx = MagicMock()
        mock_nx._post_with_x402.return_value = {"trust_score": 0.95}
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["pay", "/v1/trust/score", "--config", str(_hybrid_config(tmp_path))],
            )
        assert result.exit_code == 0
        assert "No payment required" in result.stdout

    def test_pay_shows_challenge(self, tmp_path: Path) -> None:
        """If endpoint returns 402, pay should show the payment challenge."""
        mock_nx = MagicMock()
        challenge = PaymentChallenge.from_response({
            "amount_micro_usdc": 8000,
            "amount_usdc": "0.008000",
            "recipient": ATOMADIC_TREASURY,
            "endpoint": "/v1/trust/score",
            "chain_id": 84532,
        })
        mock_nx._post_with_x402.return_value = {
            "payment_required": True,
            "challenge": challenge,  # New: typed challenge in response
            "raw": {
                "amount_micro_usdc": 8000,
                "amount_usdc": "0.008000",
                "recipient": ATOMADIC_TREASURY,
                "endpoint": "/v1/trust/score",
                "chain_id": 84532,
            },
        }
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["pay", "/v1/trust/score", "--config", str(_hybrid_config(tmp_path))],
                input="n\n",  # Decline payment
            )
        assert "Payment Required" in result.stdout or "0.008000" in result.stdout
