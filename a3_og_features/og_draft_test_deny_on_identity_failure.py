# Extracted from C:/!ass-ade/tests/test_workflows.py:70
# Component id: og.source.ass_ade.test_deny_on_identity_failure
from __future__ import annotations

__version__ = "0.1.0"

def test_deny_on_identity_failure(self) -> None:
    client = _mock_client()
    client.identity_verify.return_value = IdentityVerification(decision="deny", actor="test")
    result = trust_gate(client, "agent-bad")
    assert result.verdict == "DENY"
