# Extracted from C:/!ass-ade/tests/test_engine_integration.py:259
# Component id: mo.source.ass_ade.test_alert_severity_mapping
from __future__ import annotations

__version__ = "0.1.0"

def test_alert_severity_mapping(self) -> None:
    b = BAS({})
    high_kinds = ["emergent_synergy", "gvu_jump", "trust_violation", "budget_exhaustion"]
    for kind in high_kinds:
        a = Alert(kind=kind, severity="", payload={}, ts="")
        b_alert = b.alert(kind, {})
        assert b_alert.severity == "high", f"{kind} should be high severity"
