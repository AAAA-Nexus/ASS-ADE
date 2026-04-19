# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testqualitygates.py:44
# Component id: at.source.ass_ade.test_shield_tool_blocked
__version__ = "0.1.0"

    def test_shield_tool_blocked(self):
        gates = QualityGates(_mock_nexus(shield_blocked=True))
        result = gates.shield_tool("run_command", {"command": "rm -rf /"})
        assert result is not None
        assert result["blocked"] is True
