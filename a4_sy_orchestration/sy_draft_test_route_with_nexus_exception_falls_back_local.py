# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_testepistemicrouter.py:48
# Component id: sy.source.a4_sy_orchestration.test_route_with_nexus_exception_falls_back_local
from __future__ import annotations

__version__ = "0.1.0"

def test_route_with_nexus_exception_falls_back_local(self):
    nexus = type("NexusBoom", (), {
        "routing_recommend": lambda self, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
    })()
    router = EpistemicRouter(nexus_client=nexus)
    decision = router.route("Write a function to parse JSON")
    assert decision.source == "local"
