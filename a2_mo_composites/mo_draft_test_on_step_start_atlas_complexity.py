# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testengineorchestrator.py:19
# Component id: mo.source.ass_ade.test_on_step_start_atlas_complexity
__version__ = "0.1.0"

    def test_on_step_start_atlas_complexity(self) -> None:
        o = EngineOrchestrator({})
        result = o.on_step_start("a" * 2000)  # long = high complexity
        assert result["atlas_complexity"] > 1.0
