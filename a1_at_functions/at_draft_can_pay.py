# Extracted from C:/!ass-ade/src/ass_ade/nexus/x402.py:403
# Component id: at.source.ass_ade.can_pay
from __future__ import annotations

__version__ = "0.1.0"

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
