# Extracted from C:/!ass-ade/tests/test_engine_integration.py:185
# Component id: mo.source.ass_ade.test_monitor_all_fires_multiple_alerts
from __future__ import annotations

__version__ = "0.1.0"

def test_monitor_all_fires_multiple_alerts(self) -> None:
    b = BAS({})
    alerts = b.monitor_all({
        "synergy": 0.9,
        "novelty": 0.9,
        "trust_score": 0.1,
        "budget_pct": 0.95,
        "gvu_delta": 0.0,
    })
    kinds = {a.kind for a in alerts}
    assert "emergent_synergy" in kinds
    assert "trust_violation" in kinds
    assert "budget_exhaustion" in kinds
