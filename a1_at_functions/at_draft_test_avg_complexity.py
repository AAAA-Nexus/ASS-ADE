# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_avg_complexity.py:7
# Component id: at.source.a1_at_functions.test_avg_complexity
from __future__ import annotations

__version__ = "0.1.0"

def test_avg_complexity(self):
    router = EpistemicRouter()
    router.route("Hi")
    router.route("Write code")
    avg = router.avg_complexity
    assert 0 <= avg <= 1.0
