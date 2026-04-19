# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/x402.py:199
# Component id: at.source.ass_ade.format_payment_consent
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
