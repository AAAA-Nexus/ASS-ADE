# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_route_without_nexus.py:7
# Component id: at.source.a1_at_functions.test_route_without_nexus
from __future__ import annotations

__version__ = "0.1.0"

def test_route_without_nexus(self):
    router = EpistemicRouter()
    decision = router.route("Hello world")
    assert isinstance(decision, RoutingDecision)
    assert decision.source == "local"
