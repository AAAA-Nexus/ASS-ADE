# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testqualitygatesconfig.py:6
# Component id: at.source.ass_ade.test_default_config_is_empty_dict
__version__ = "0.1.0"

    def test_default_config_is_empty_dict(self) -> None:
        mock_client = MagicMock()
        gates = QualityGates(mock_client)
        assert gates._v18_config == {}
