# Extracted from C:/!ass-ade/tests/test_engine_integration.py:231
# Component id: mo.source.ass_ade.test_flush_alerts_drains_buffer
from __future__ import annotations

__version__ = "0.1.0"

def test_flush_alerts_drains_buffer(self) -> None:
    b = BAS({})
    b.monitor_all({"synergy": 0.9, "trust_score": 0.1})
    flushed = b.flush_alerts()
    assert len(flushed) >= 1
    # second flush is empty
    assert b.flush_alerts() == []
