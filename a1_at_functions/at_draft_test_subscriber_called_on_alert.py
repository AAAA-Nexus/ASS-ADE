# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_subscriber_called_on_alert.py:7
# Component id: at.source.a1_at_functions.test_subscriber_called_on_alert
from __future__ import annotations

__version__ = "0.1.0"

def test_subscriber_called_on_alert(self) -> None:
    b = BAS({})
    received: list[Alert] = []
    b.subscribe(lambda a: received.append(a))
    b.monitor_all({"synergy": 0.9})
    assert len(received) >= 1
    assert received[0].kind == "emergent_synergy"
