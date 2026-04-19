# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testtrustgate.py:63
# Component id: og.source.a3_og_features.test_exception_handling_sybil_sanitized
from __future__ import annotations

__version__ = "0.1.0"

def test_exception_handling_sybil_sanitized(self) -> None:
    """Exception in sybil_check should not leak raw exception to caller."""
    client = _mock_client()
    client.sybil_check.side_effect = ValueError("Invalid agent signature")
    result = trust_gate(client, "agent-bad-sig")
    sybil_step = next(s for s in result.steps if s.name == "sybil_check")
    assert sybil_step.detail == "step_failed"
    assert "Invalid" not in sybil_step.detail
    assert "signature" not in sybil_step.detail
