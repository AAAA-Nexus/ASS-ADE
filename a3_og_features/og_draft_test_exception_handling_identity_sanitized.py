# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testtrustgate.py:51
# Component id: og.source.a3_og_features.test_exception_handling_identity_sanitized
from __future__ import annotations

__version__ = "0.1.0"

def test_exception_handling_identity_sanitized(self) -> None:
    """Exception in identity_verify should not leak raw exception to caller."""
    client = _mock_client()
    client.identity_verify.side_effect = RuntimeError("Connection timeout to server")
    result = trust_gate(client, "agent-error")
    # Verify detail is generic, not raw exception
    identity_step = next(s for s in result.steps if s.name == "identity_verify")
    assert identity_step.detail == "step_failed"
    assert "Connection" not in identity_step.detail
    assert "timeout" not in identity_step.detail
    assert result.verdict == "DENY"
