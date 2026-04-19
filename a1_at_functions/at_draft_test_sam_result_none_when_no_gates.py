# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase1_integration.py:105
# Component id: at.source.ass_ade.test_sam_result_none_when_no_gates
__version__ = "0.1.0"

    def test_sam_result_none_when_no_gates(self):
        provider = _make_provider_returning_text("hello")
        registry = ToolRegistry()
        loop = AgentLoop(provider=provider, registry=registry)
        loop.step("What is 2+2?")
        assert loop.last_sam_result is None
