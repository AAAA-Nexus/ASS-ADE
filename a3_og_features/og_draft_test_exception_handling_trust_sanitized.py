# Extracted from C:/!ass-ade/tests/test_workflows.py:128
# Component id: og.source.ass_ade.test_exception_handling_trust_sanitized
from __future__ import annotations

__version__ = "0.1.0"

def test_exception_handling_trust_sanitized(self) -> None:
    """Exception in trust_score should not leak raw exception to caller."""
    client = _mock_client()
    client.trust_score.side_effect = OSError("Network unreachable")
    result = trust_gate(client, "agent-net-fail")
    trust_step = next(s for s in result.steps if s.name == "trust_score")
    assert trust_step.detail == "step_failed"
    assert "Network" not in trust_step.detail
    assert "unreachable" not in trust_step.detail
