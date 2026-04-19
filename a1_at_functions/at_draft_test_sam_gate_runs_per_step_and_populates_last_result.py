# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testsaminagentloop.py:6
# Component id: at.source.ass_ade.test_sam_gate_runs_per_step_and_populates_last_result
__version__ = "0.1.0"

    def test_sam_gate_runs_per_step_and_populates_last_result(self):
        nexus = _make_nexus_mock()
        gates = QualityGates(nexus, config={})
        provider = _make_provider_returning_text("hello")
        registry = ToolRegistry()

        loop = AgentLoop(
            provider=provider,
            registry=registry,
            quality_gates=gates,
        )

        with patch("ass_ade.context_memory.vector_embed", return_value=[0.1, 0.2, 0.3]):
            loop.step("What is 1+1?")

        assert loop.last_sam_result is not None
        assert "trs" in loop.last_sam_result
        assert "composite" in loop.last_sam_result
