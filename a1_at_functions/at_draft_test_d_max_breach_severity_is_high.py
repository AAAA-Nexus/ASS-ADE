# Extracted from C:/!ass-ade/tests/test_phase1_integration.py:188
# Component id: at.source.ass_ade.test_d_max_breach_severity_is_high
from __future__ import annotations

__version__ = "0.1.0"

def test_d_max_breach_severity_is_high(self):
    from ass_ade.agent.bas import _SEVERITY
    assert _SEVERITY.get("d_max_breach") == "high"
