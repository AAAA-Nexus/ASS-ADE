# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_format_payment_consent.py:7
# Component id: at.source.a1_at_functions.format_payment_consent
from __future__ import annotations

__version__ = "0.1.0"

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
