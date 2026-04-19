# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/validation.py:106
# Component id: at.source.ass_ade.validate_usdc_amount
__version__ = "0.1.0"

def validate_usdc_amount(value: float) -> float:
    """Positive, max 1,000,000 USDC."""
    if value <= 0:
        raise ValueError("USDC amount must be positive.")
    if value > MAX_USDC:
        raise ValueError(f"USDC amount exceeds maximum ({MAX_USDC:,.0f}).")
    return value
