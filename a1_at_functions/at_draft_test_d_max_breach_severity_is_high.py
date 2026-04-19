# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_d_max_breach_severity_is_high.py:7
# Component id: at.source.a1_at_functions.test_d_max_breach_severity_is_high
from __future__ import annotations

__version__ = "0.1.0"

def test_d_max_breach_severity_is_high(self):
    from ass_ade.agent.bas import _SEVERITY
    assert _SEVERITY.get("d_max_breach") == "high"
