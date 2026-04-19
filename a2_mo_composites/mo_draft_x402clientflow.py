# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_x402clientflow.py:7
# Component id: mo.source.a2_mo_composites.x402clientflow
from __future__ import annotations

__version__ = "0.1.0"

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
