# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_subscriber_exception_does_not_propagate.py:7
# Component id: at.source.a1_at_functions.test_subscriber_exception_does_not_propagate
from __future__ import annotations

__version__ = "0.1.0"

def test_subscriber_exception_does_not_propagate(self) -> None:
    b = BAS({})
    b.subscribe(lambda a: (_ for _ in ()).throw(RuntimeError("boom")))
    # Should not raise
    b.monitor_all({"synergy": 0.9})
