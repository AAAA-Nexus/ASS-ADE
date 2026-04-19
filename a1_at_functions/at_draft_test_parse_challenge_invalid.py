# Extracted from C:/!ass-ade/tests/test_x402_flow.py:166
# Component id: at.source.ass_ade.test_parse_challenge_invalid
from __future__ import annotations

__version__ = "0.1.0"

def test_parse_challenge_invalid(self) -> None:
    """X402ClientFlow should set last_error on parse failure."""
    flow = X402ClientFlow()
    challenge = flow.parse_challenge({})  # Missing required fields
    assert challenge is None
    assert flow.last_error  # Error should be set
