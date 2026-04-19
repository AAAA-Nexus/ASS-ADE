# Extracted from C:/!ass-ade/tests/test_routing.py:96
# Component id: at.source.ass_ade.test_history_tracking
from __future__ import annotations

__version__ = "0.1.0"

def test_history_tracking(self):
    router = EpistemicRouter()
    router.route("Hello")
    router.route("Write a complex algorithm with formal proof")
    assert len(router.history) == 2
