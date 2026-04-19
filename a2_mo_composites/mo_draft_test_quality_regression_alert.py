# Extracted from C:/!ass-ade/tests/test_engine_integration.py:205
# Component id: mo.source.ass_ade.test_quality_regression_alert
from __future__ import annotations

__version__ = "0.1.0"

def test_quality_regression_alert(self) -> None:
    b = BAS({})
    alerts = b.monitor_all({"score_delta": -0.5})
    kinds = {a.kind for a in alerts}
    assert "quality_regression" in kinds
