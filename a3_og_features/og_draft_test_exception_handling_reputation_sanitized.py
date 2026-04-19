# Extracted from C:/!ass-ade/tests/test_workflows.py:138
# Component id: og.source.ass_ade.test_exception_handling_reputation_sanitized
from __future__ import annotations

__version__ = "0.1.0"

def test_exception_handling_reputation_sanitized(self) -> None:
    """Exception in reputation_score should not leak raw exception to caller."""
    client = _mock_client()
    client.reputation_score.side_effect = NexusServerError("Internal server error: 500")
    result = trust_gate(client, "agent-server-err")
    rep_step = next(s for s in result.steps if s.name == "reputation_score")
    assert rep_step.detail == "step_failed"
    assert "Internal" not in rep_step.detail
    assert "500" not in rep_step.detail
