# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testqualitygates.py:38
# Component id: at.source.ass_ade.test_shield_tool_allowed
__version__ = "0.1.0"

    def test_shield_tool_allowed(self):
        gates = QualityGates(_mock_nexus())
        result = gates.shield_tool("read_file", {"path": "test.py"})
        assert result is not None
        assert result["blocked"] is False
