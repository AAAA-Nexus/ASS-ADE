# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testengineorchestratorphase15.py:45
# Component id: mo.source.ass_ade.test_engine_report_includes_new_engines_after_init
__version__ = "0.1.0"

    def test_engine_report_includes_new_engines_after_init(self):
        orch = self._make()
        # Touch the new engines to init them
        _ = orch.lse
        _ = orch.tca
        _ = orch.cie
        _ = orch.lora_flywheel
        rep = orch.engine_report()
        assert "lse" in rep
        assert "tca" in rep
        assert "cie" in rep
        assert "lora_flywheel" in rep
