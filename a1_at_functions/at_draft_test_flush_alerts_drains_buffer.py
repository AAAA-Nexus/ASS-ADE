# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_flush_alerts_drains_buffer.py:7
# Component id: at.source.a1_at_functions.test_flush_alerts_drains_buffer
from __future__ import annotations

__version__ = "0.1.0"

def test_flush_alerts_drains_buffer(self) -> None:
    b = BAS({})
    b.monitor_all({"synergy": 0.9, "trust_score": 0.1})
    flushed = b.flush_alerts()
    assert len(flushed) >= 1
    # second flush is empty
    assert b.flush_alerts() == []
