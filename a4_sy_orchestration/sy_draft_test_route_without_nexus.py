# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testepistemicrouter.py:6
# Component id: sy.source.ass_ade.test_route_without_nexus
__version__ = "0.1.0"

    def test_route_without_nexus(self):
        router = EpistemicRouter()
        decision = router.route("Hello world")
        assert isinstance(decision, RoutingDecision)
        assert decision.source == "local"
