# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testcertifyoutput.py:14
# Component id: og.source.a3_og_features.test_hallucination_failure_blocks
from __future__ import annotations

__version__ = "0.1.0"

def test_hallucination_failure_blocks(self) -> None:
    client = _mock_client()
    client.hallucination_oracle.return_value = HallucinationResult(verdict="unsafe")
    result = certify_output(client, "Suspicious output that is unsafe.")
    assert result.passed is False
