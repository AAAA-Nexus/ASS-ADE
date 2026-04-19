# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_hallucination_check.py:7
# Component id: at.source.a1_at_functions.test_hallucination_check
from __future__ import annotations

__version__ = "0.1.0"

def test_hallucination_check(self):
    gates = QualityGates(self._mock_client())
    result = gates.check_hallucination("The file has been fixed.")
    assert result is not None
    assert result["verdict"] == "safe"
