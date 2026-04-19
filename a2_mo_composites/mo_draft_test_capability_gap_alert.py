# Extracted from C:/!ass-ade/tests/test_engine_integration.py:199
# Component id: mo.source.ass_ade.test_capability_gap_alert
from __future__ import annotations

__version__ = "0.1.0"

def test_capability_gap_alert(self) -> None:
    b = BAS({})
    alerts = b.monitor_all({"missing_capabilities": ["llm", "search"]})
    kinds = {a.kind for a in alerts}
    assert "capability_gap" in kinds
