# Extracted from C:/!ass-ade/tests/test_routing.py:90
# Component id: at.source.ass_ade.test_route_without_nexus
from __future__ import annotations

__version__ = "0.1.0"

def test_route_without_nexus(self):
    router = EpistemicRouter()
    decision = router.route("Hello world")
    assert isinstance(decision, RoutingDecision)
    assert decision.source == "local"
