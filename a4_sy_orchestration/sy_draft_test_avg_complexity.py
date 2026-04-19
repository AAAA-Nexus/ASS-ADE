# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testepistemicrouter.py:20
# Component id: sy.source.a4_sy_orchestration.test_avg_complexity
from __future__ import annotations

__version__ = "0.1.0"

def test_avg_complexity(self):
    router = EpistemicRouter()
    router.route("Hi")
    router.route("Write code")
    avg = router.avg_complexity
    assert 0 <= avg <= 1.0
