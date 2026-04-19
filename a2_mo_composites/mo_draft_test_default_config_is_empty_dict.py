# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_engine_integration.py:390
# Component id: mo.source.ass_ade.test_default_config_is_empty_dict
__version__ = "0.1.0"

    def test_default_config_is_empty_dict(self) -> None:
        mock_client = MagicMock()
        gates = QualityGates(mock_client)
        assert gates._v18_config == {}
