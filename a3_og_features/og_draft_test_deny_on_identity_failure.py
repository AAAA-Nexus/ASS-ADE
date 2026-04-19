# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testtrustgate.py:15
# Component id: og.source.a3_og_features.test_deny_on_identity_failure
from __future__ import annotations

__version__ = "0.1.0"

def test_deny_on_identity_failure(self) -> None:
    client = _mock_client()
    client.identity_verify.return_value = IdentityVerification(decision="deny", actor="test")
    result = trust_gate(client, "agent-bad")
    assert result.verdict == "DENY"
