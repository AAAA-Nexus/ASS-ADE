# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_routing.py:90
# Component id: at.source.ass_ade.test_route_without_nexus
__version__ = "0.1.0"

    def test_route_without_nexus(self):
        router = EpistemicRouter()
        decision = router.route("Hello world")
        assert isinstance(decision, RoutingDecision)
        assert decision.source == "local"
