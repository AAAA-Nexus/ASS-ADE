# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testepistemicrouter.py:46
# Component id: sy.source.ass_ade.test_route_with_nexus_exception_falls_back_local
__version__ = "0.1.0"

    def test_route_with_nexus_exception_falls_back_local(self):
        nexus = type("NexusBoom", (), {
            "routing_recommend": lambda self, **kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
        })()
        router = EpistemicRouter(nexus_client=nexus)
        decision = router.route("Write a function to parse JSON")
        assert decision.source == "local"
