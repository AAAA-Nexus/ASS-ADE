# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_alert_severity_mapping.py:7
# Component id: at.source.a1_at_functions.test_alert_severity_mapping
from __future__ import annotations

__version__ = "0.1.0"

def test_alert_severity_mapping(self) -> None:
    b = BAS({})
    high_kinds = ["emergent_synergy", "gvu_jump", "trust_violation", "budget_exhaustion"]
    for kind in high_kinds:
        a = Alert(kind=kind, severity="", payload={}, ts="")
        b_alert = b.alert(kind, {})
        assert b_alert.severity == "high", f"{kind} should be high severity"
