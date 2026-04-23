"""x402 Autonomous Payment Client for Base L2 (USDC).

Implements the client side of the x402 micro-settlement protocol:

1. Detect 402 Payment Required response
2. Parse payment challenge (amount, recipient, nonce, chain_id)
3. Display cost breakdown and get user consent
4. Sign and submit USDC transfer on Base (mainnet or Sepolia testnet)
5. Retry original request with payment proof header

Testnet mode:
    export ATOMADIC_X402_TESTNET=1
    export ATOMADIC_WALLET_KEY=<your-base-sepolia-private-key>

Mainnet mode:
    export ATOMADIC_WALLET_KEY=<your-base-mainnet-private-key>

Get testnet funds:
    - Base Sepolia ETH: https://www.alchemy.com/faucets/base-sepolia
    - Testnet USDC: mint from test contract or use faucet
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any


# Base chain IDs
BASE_MAINNET_CHAIN_ID = 8453
BASE_SEPOLIA_CHAIN_ID = 84532

# Base RPC endpoints
BASE_MAINNET_RPC = "https://mainnet.base.org"
BASE_SEPOLIA_RPC = "https://sepolia.base.org"

# USDC contract addresses
USDC_BASE_MAINNET = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
USDC_BASE_SEPOLIA = "0x036CbD53842c5426634e7929541eC2318f3dCF7e"

# Treasury (from wrangler.toml)
ATOMADIC_TREASURY = "0xCBd9e4c44958ee76E0F941106Ea960D476c48FD9"

# Payment safety limits
MAX_CHALLENGE_MICRO_USDC = 10_000_000  # $10 USDC ceiling
MAX_GAS_PRICE_GWEI = 500

@dataclass
class PaymentChallenge:
    """Parsed x402 payment challenge from a 402 response."""
    amount_micro_usdc: int
    amount_usdc: float
    recipient: str
    nonce: str
    expires: int
    chain_id: int
    token_address: str
    endpoint: str
    x402_version: str = "2.1"

    def validate(self) -> PaymentChallenge:
        """Validate the challenge before any user consent or payment attempt."""
        if self.amount_micro_usdc <= 0:
            raise ValueError("402 response missing required field: amount_micro_usdc")
        if self.amount_micro_usdc > MAX_CHALLENGE_MICRO_USDC:
            raise ValueError(
                f"402 response amount {self.amount_micro_usdc} outside valid range "
                f"(1-{MAX_CHALLENGE_MICRO_USDC})"
            )
        if not self.recipient.strip():
            raise ValueError("402 response missing required field: recipient")
        if self.recipient.strip().lower() != ATOMADIC_TREASURY.lower():
            raise ValueError("402 response recipient does not match expected treasury")
        return self

    @classmethod
    def from_response(cls, body: dict) -> PaymentChallenge:
        """Parse a 402 JSON response body into a PaymentChallenge."""
        recipient = body.get("recipient", "")
        amount_raw = body.get("amount_micro_usdc", 0)
        if not recipient:
            raise ValueError("402 response missing required field: recipient")
        try:
            amount = int(amount_raw)
        except (TypeError, ValueError):
            raise ValueError("402 response field amount_micro_usdc must be an integer") from None
        challenge = cls(
            amount_micro_usdc=amount,
            amount_usdc=float(body.get("amount_usdc", 0)),
            recipient=recipient,
            nonce=body.get("nonce", ""),
            expires=body.get("expires", 0),
            chain_id=body.get("chain_id", BASE_MAINNET_CHAIN_ID),
            token_address=body.get("token_address") or body.get("sdk_hints", {}).get("token_address", ""),
            endpoint=body.get("endpoint", ""),
            x402_version=body.get("x402_version", "2.1"),
        )
        return challenge.validate()

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires if self.expires else False

    @property
    def display_amount(self) -> str:
        if self.amount_usdc:
            return f"${self.amount_usdc:.6f} USDC"
        return f"{self.amount_micro_usdc} micro-USDC"


@dataclass
class PaymentResult:
    """Result of an x402 payment attempt."""
    success: bool
    txid: str = ""
    signature_header: str = ""
    error: str = ""
    testnet: bool = False


@dataclass
class PaymentProof:
    """Structured proof of x402 payment for request retry.

    The payment proof is encoded as an HTTP header: PAYMENT-SIGNATURE
    Format: <signature_hex>;<wallet_address>;<transaction_id>;<amount_micro_usdc>

    This structure formalizes the contract between client (who creates it)
    and server (who validates it).
    """
    signature: str  # hex-encoded transaction signature
    wallet_address: str  # sender's wallet address (checksummed)
    transaction_id: str  # blockchain transaction ID
    amount_micro_usdc: int  # USDC amount in micro units

    @classmethod
    def from_payment_result(cls, result: PaymentResult) -> PaymentProof | None:
        """Parse a PaymentProof from a successful PaymentResult."""
        if not result.success or not result.signature_header:
            return None
        try:
            parts = result.signature_header.split(";")
            if len(parts) != 4:
                return None
            sig, addr, txid, amount_str = parts
            return cls(
                signature=sig,
                wallet_address=addr,
                transaction_id=txid,
                amount_micro_usdc=int(amount_str),
            )
        except (ValueError, IndexError):
            return None

    def to_header_value(self) -> str:
        """Format as HTTP header value (PAYMENT-SIGNATURE)."""
        return f"{self.signature};{self.wallet_address};{self.transaction_id};{self.amount_micro_usdc}"

    @classmethod
    def from_header_value(cls, header_value: str) -> PaymentProof | None:
        """Parse from HTTP header value (PAYMENT-SIGNATURE)."""
        try:
            parts = header_value.split(";")
            if len(parts) != 4:
                return None
            sig, addr, txid, amount_str = parts
            return cls(
                signature=sig,
                wallet_address=addr,
                transaction_id=txid,
                amount_micro_usdc=int(amount_str),
            )
        except (ValueError, IndexError):
            return None


def is_testnet() -> bool:
    """Check if testnet mode is enabled."""
    return os.environ.get("ATOMADIC_X402_TESTNET", "").strip() in ("1", "true", "yes")


def get_chain_config() -> dict[str, Any]:
    """Get chain configuration based on testnet/mainnet mode."""
    testnet = is_testnet()
    return {
        "testnet": testnet,
        "chain_id": BASE_SEPOLIA_CHAIN_ID if testnet else BASE_MAINNET_CHAIN_ID,
        "rpc_url": os.environ.get(
            "BASE_RPC_URL",
            BASE_SEPOLIA_RPC if testnet else BASE_MAINNET_RPC,
        ),
        "usdc_address": USDC_BASE_SEPOLIA if testnet else USDC_BASE_MAINNET,
        "treasury": ATOMADIC_TREASURY,
        "network_name": "Base Sepolia (testnet)" if testnet else "Base (mainnet)",
    }


def format_payment_consent(challenge: PaymentChallenge) -> str:
    """Format a human-readable payment consent message."""
    config = get_chain_config()
    lines = [
        "x402 Payment Required",
        "=" * 40,
        f"  Endpoint:  {challenge.endpoint}",
        f"  Amount:    {challenge.display_amount}",
        f"  Network:   {config['network_name']}",
        f"  Recipient: {challenge.recipient}",
        f"  Token:     USDC ({config['usdc_address'][:10]}...)",
        f"  Chain ID:  {config['chain_id']}",
        "=" * 40,
    ]
    if config["testnet"]:
        lines.append("  MODE: TESTNET (no real funds)")
    return "\n".join(lines)


def submit_payment(challenge: PaymentChallenge) -> PaymentResult:
    """Submit a USDC payment on Base to fulfill an x402 challenge.

    Requires ATOMADIC_WALLET_KEY environment variable with the sender's
    private key (hex, without 0x prefix).

    For testnet: set ATOMADIC_X402_TESTNET=1

    Returns PaymentResult with txid and signature header on success.
    """
    wallet_key = os.environ.get("ATOMADIC_WALLET_KEY", "").strip()
    if not wallet_key:
        return PaymentResult(
            success=False,
            error="ATOMADIC_WALLET_KEY not set. Export your Base wallet private key.",
        )

    if challenge.is_expired:
        return PaymentResult(success=False, error="Payment challenge has expired.")

    if challenge.amount_micro_usdc <= 0 or challenge.amount_micro_usdc > MAX_CHALLENGE_MICRO_USDC:
        return PaymentResult(
            success=False,
            error=f"Payment aborted: amount {challenge.amount_micro_usdc} outside valid range (1\u2013{MAX_CHALLENGE_MICRO_USDC})",
        )

    config = get_chain_config()

    if challenge.chain_id and challenge.chain_id != config["chain_id"]:
        return PaymentResult(
            success=False,
            error=(
                f"Payment aborted: challenge chain_id {challenge.chain_id} "
                f"does not match active chain {config['chain_id']}"
            ),
        )

    if challenge.token_address:
        try:
            challenge_token = challenge.token_address.lower()
            expected_token = config["usdc_address"].lower()
        except AttributeError:
            return PaymentResult(success=False, error="Payment aborted: invalid token address in challenge")
        if challenge_token != expected_token:
            return PaymentResult(
                success=False,
                error=(
                    f"Payment aborted: challenge token {challenge.token_address} "
                    f"does not match expected USDC token {config['usdc_address']}"
                ),
            )

    try:
        from eth_account import Account
        from web3 import Web3
    except ImportError:
        return PaymentResult(
            success=False,
            error="web3 and eth-account packages required. Install: pip install web3 eth-account",
        )

    try:
        w3 = Web3(Web3.HTTPProvider(config["rpc_url"]))
        if not w3.is_connected():
            return PaymentResult(success=False, error=f"Cannot connect to {config['rpc_url']}")

        account = Account.from_key(wallet_key)

        # USDC ERC-20 transfer ABI
        usdc_abi = [
            {
                "name": "transfer",
                "type": "function",
                "inputs": [
                    {"name": "to", "type": "address"},
                    {"name": "amount", "type": "uint256"},
                ],
                "outputs": [{"name": "", "type": "bool"}],
            }
        ]

        usdc = w3.eth.contract(
            address=Web3.to_checksum_address(config["usdc_address"]),
            abi=usdc_abi,
        )

        # Build transfer transaction
        recipient = Web3.to_checksum_address(challenge.recipient)
        expected = Web3.to_checksum_address(ATOMADIC_TREASURY)
        if recipient != expected:
            return PaymentResult(
                success=False,
                error=f"Payment aborted: server proposed recipient {recipient} does not match expected treasury {expected}",
            )
        nonce = w3.eth.get_transaction_count(account.address)

        gas_price = w3.eth.gas_price
        max_gas_wei = MAX_GAS_PRICE_GWEI * 10**9
        if gas_price > max_gas_wei:
            return PaymentResult(
                success=False,
                error=f"Gas price {gas_price / 10**9:.1f} Gwei exceeds limit {MAX_GAS_PRICE_GWEI} Gwei. Retry when network is less congested.",
            )

        tx = usdc.functions.transfer(
            recipient, challenge.amount_micro_usdc
        ).build_transaction({
            "from": account.address,
            "nonce": nonce,
            "gas": 100_000,
            "gasPrice": gas_price,
            "chainId": config["chain_id"],
        })

        # Sign and send
        signed = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        txid = tx_hash.hex()

        # Build the payment proof header
        # Format: <sig_hex>;<wallet_addr>;<txid>;<amount_micro>
        sig_hex = signed.signature.hex()
        if sig_hex.startswith("0x"):
            sig_hex = sig_hex[2:]
        wallet_addr = account.address[2:]  # Remove 0x prefix — wallet address, not public key
        header = f"{sig_hex};{wallet_addr};{txid};{challenge.amount_micro_usdc}"

        return PaymentResult(
            success=True,
            txid=txid,
            signature_header=header,
            testnet=config["testnet"],
        )

    except (ValueError, TypeError, OSError, RuntimeError):
        import logging
        logging.getLogger(__name__).exception("Payment submission failed")
        return PaymentResult(success=False, error="Payment submission failed. Check logs for details.")


def build_payment_header(result: PaymentResult) -> dict[str, str]:
    """Build the HTTP headers to submit with the paid request retry.

    Uses PaymentProof to format the PAYMENT-SIGNATURE header consistently.
    Returns empty dict if payment was unsuccessful.
    """
    proof = PaymentProof.from_payment_result(result)
    if not proof:
        return {}
    return {"PAYMENT-SIGNATURE": proof.to_header_value()}


class X402ClientFlow:
    """Orchestrates the full client-side x402 payment flow.

    This helper encapsulates the complete flow from receiving a 402 challenge
    to submitting the paid request retry. It provides a reusable, typed path
    for applications that need to handle x402 payments programmatically.

    Usage::

        flow = X402ClientFlow()
        challenge = flow.parse_challenge(response_dict)
        if not flow.can_pay(challenge):
            raise ValueError(f"Cannot pay: {flow.last_error}")
        payment = flow.execute_payment(challenge)
        if payment.success:
            headers = flow.build_proof_headers(payment)
            # ... submit retry with headers
    """

    def __init__(self) -> None:
        self.last_error: str = ""

    def parse_challenge(self, response_dict: dict) -> PaymentChallenge | None:
        """Parse a 402 response dict into a PaymentChallenge.

        Returns None if parsing fails; check last_error for details.
        """
        try:
            return PaymentChallenge.from_response(response_dict)
        except ValueError as e:
            self.last_error = str(e)
            return None

    def can_pay(self, challenge: PaymentChallenge) -> bool:
        """Check if a challenge can be paid with current configuration.

        Returns False and sets last_error if the challenge cannot be fulfilled.
        """
        if challenge.is_expired:
            self.last_error = "Challenge has expired"
            return False

        if challenge.amount_micro_usdc <= 0 or challenge.amount_micro_usdc > MAX_CHALLENGE_MICRO_USDC:
            self.last_error = (
                f"Amount {challenge.amount_micro_usdc} outside valid range "
                f"(1–{MAX_CHALLENGE_MICRO_USDC})"
            )
            return False

        if challenge.recipient.strip().lower() != ATOMADIC_TREASURY.lower():
            self.last_error = "Recipient does not match expected treasury"
            return False

        config = get_chain_config()
        if challenge.chain_id and challenge.chain_id != config["chain_id"]:
            self.last_error = (
                f"Chain mismatch: challenge {challenge.chain_id} vs active {config['chain_id']}"
            )
            return False

        if challenge.token_address:
            try:
                if challenge.token_address.lower() != config["usdc_address"].lower():
                    self.last_error = (
                        f"Token mismatch: challenge {challenge.token_address} "
                        f"vs expected {config['usdc_address']}"
                    )
                    return False
            except AttributeError as exc:
                self.last_error = f"Invalid token address: {exc}"
                return False

        return True

    def execute_payment(self, challenge: PaymentChallenge) -> PaymentResult:
        """Submit payment for the challenge.

        Returns PaymentResult with success status and details.
        Calls the lower-level submit_payment() function.
        """
        return submit_payment(challenge)

    def build_proof_headers(self, payment: PaymentResult) -> dict[str, str]:
        """Build HTTP headers from a successful payment for request retry."""
        return build_payment_header(payment)

    def get_proof(self, payment: PaymentResult) -> PaymentProof | None:
        """Extract structured PaymentProof from a payment result."""
        return PaymentProof.from_payment_result(payment)
