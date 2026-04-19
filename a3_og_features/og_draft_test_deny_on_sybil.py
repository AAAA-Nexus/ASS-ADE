# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testtrustgate.py:21
# Component id: og.source.a3_og_features.test_deny_on_sybil
from __future__ import annotations

__version__ = "0.1.0"

def test_deny_on_sybil(self) -> None:
    client = _mock_client()
    client.sybil_check.return_value = SybilCheckResult(sybil_risk="high", score=0.9)
    result = trust_gate(client, "agent-sybil")
    assert result.verdict == "DENY"
