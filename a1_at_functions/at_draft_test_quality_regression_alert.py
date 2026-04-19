# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_quality_regression_alert.py:7
# Component id: at.source.a1_at_functions.test_quality_regression_alert
from __future__ import annotations

__version__ = "0.1.0"

def test_quality_regression_alert(self) -> None:
    b = BAS({})
    alerts = b.monitor_all({"score_delta": -0.5})
    kinds = {a.kind for a in alerts}
    assert "quality_regression" in kinds
