# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testengineorchestratorphase15.py:33
# Component id: mo.source.ass_ade.test_check_conviction_gate_non_destructive_tool
__version__ = "0.1.0"

    def test_check_conviction_gate_non_destructive_tool(self):
        orch = self._make()
        # Non-destructive tool: read_file should NOT be blocked
        blocked = orch.check_conviction_gate("read_file", {})
        assert blocked is False
