# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testqualitygatesconfig.py:11
# Component id: at.source.ass_ade.test_config_passed_through
__version__ = "0.1.0"

    def test_config_passed_through(self) -> None:
        mock_client = MagicMock()
        config = {"alphaverus": {"beam_width": 8}, "dgm_h": {"simulation_cycles": 20}}
        gates = QualityGates(mock_client, config=config)
        assert gates._v18_config == config
