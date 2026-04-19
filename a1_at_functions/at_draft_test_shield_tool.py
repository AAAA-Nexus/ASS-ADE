# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_agent.py:122
# Component id: at.source.ass_ade.test_shield_tool
__version__ = "0.1.0"

    def test_shield_tool(self):
        gates = QualityGates(self._mock_client())
        result = gates.shield_tool("read_file", {"path": "main.py"})
        assert result is not None
        assert not result["blocked"]
