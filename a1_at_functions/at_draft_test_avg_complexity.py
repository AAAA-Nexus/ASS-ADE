# Extracted from C:/!ass-ade/tests/test_routing.py:102
# Component id: at.source.ass_ade.test_avg_complexity
from __future__ import annotations

__version__ = "0.1.0"

def test_avg_complexity(self):
    router = EpistemicRouter()
    router.route("Hi")
    router.route("Write code")
    avg = router.avg_complexity
    assert 0 <= avg <= 1.0
