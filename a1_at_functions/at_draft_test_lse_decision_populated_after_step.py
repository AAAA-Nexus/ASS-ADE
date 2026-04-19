# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_phase1_integration.py:119
# Component id: at.source.ass_ade.test_lse_decision_populated_after_step
__version__ = "0.1.0"

    def test_lse_decision_populated_after_step(self):
        provider = _make_provider_returning_text("result")
        registry = ToolRegistry()
        lse = LSEEngine({})
        loop = AgentLoop(provider=provider, registry=registry, lse=lse)
        loop.step("simple question")
        assert loop.last_lse_decision is not None
        # Canonical tier names (catalog-aware); haiku/sonnet/opus are aliases
        assert loop.last_lse_decision.tier in {"fast", "balanced", "deep"}
