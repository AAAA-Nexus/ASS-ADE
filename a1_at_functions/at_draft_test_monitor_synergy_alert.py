# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_monitor_synergy_alert.py:7
# Component id: at.source.a1_at_functions.test_monitor_synergy_alert
from __future__ import annotations

__version__ = "0.1.0"

def test_monitor_synergy_alert(self) -> None:
    b = BAS({"synergy": {"threshold": 0.5}})
    a = b.monitor({"synergy": 0.8, "novelty": 0.0, "gvu_delta": 0.0})
    assert a is not None
    assert a.kind == "emergent_synergy"
    assert a.severity == "high"
