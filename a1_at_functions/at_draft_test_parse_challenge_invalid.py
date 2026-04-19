# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testx402clientflow.py:24
# Component id: at.source.a2_mo_composites.test_parse_challenge_invalid
from __future__ import annotations

__version__ = "0.1.0"

def test_parse_challenge_invalid(self) -> None:
    """X402ClientFlow should set last_error on parse failure."""
    flow = X402ClientFlow()
    challenge = flow.parse_challenge({})  # Missing required fields
    assert challenge is None
    assert flow.last_error  # Error should be set
