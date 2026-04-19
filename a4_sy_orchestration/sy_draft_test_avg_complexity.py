# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testepistemicrouter.py:18
# Component id: sy.source.ass_ade.test_avg_complexity
__version__ = "0.1.0"

    def test_avg_complexity(self):
        router = EpistemicRouter()
        router.route("Hi")
        router.route("Write code")
        avg = router.avg_complexity
        assert 0 <= avg <= 1.0
