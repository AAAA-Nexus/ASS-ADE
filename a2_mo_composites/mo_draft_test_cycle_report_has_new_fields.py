# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testengineorchestratorphase15.py:66
# Component id: mo.source.ass_ade.test_cycle_report_has_new_fields
__version__ = "0.1.0"

    def test_cycle_report_has_new_fields(self):
        from ass_ade.agent.orchestrator import CycleReport
        report = CycleReport(alerts=[])
        assert hasattr(report, "wisdom_ema")
        assert hasattr(report, "tca_stale_files")
        assert hasattr(report, "cie_passes")
        assert hasattr(report, "lora_pending")
        assert hasattr(report, "autopoietic_triggered")
