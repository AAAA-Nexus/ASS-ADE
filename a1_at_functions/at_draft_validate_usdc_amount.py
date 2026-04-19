# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_validate_usdc_amount.py:7
# Component id: at.source.a1_at_functions.validate_usdc_amount
from __future__ import annotations

__version__ = "0.1.0"

def validate_usdc_amount(value: float) -> float:
    """Positive, max 1,000,000 USDC."""
    if value <= 0:
        raise ValueError("USDC amount must be positive.")
    if value > MAX_USDC:
        raise ValueError(f"USDC amount exceeds maximum ({MAX_USDC:,.0f}).")
    return value
