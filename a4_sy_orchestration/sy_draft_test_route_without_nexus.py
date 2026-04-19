# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testepistemicrouter.py:8
# Component id: sy.source.a4_sy_orchestration.test_route_without_nexus
from __future__ import annotations

__version__ = "0.1.0"

def test_route_without_nexus(self):
    router = EpistemicRouter()
    decision = router.route("Hello world")
    assert isinstance(decision, RoutingDecision)
    assert decision.source == "local"
