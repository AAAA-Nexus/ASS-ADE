# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tools_builtin.py:197
# Component id: at.source.ass_ade.test_execute_unknown
__version__ = "0.1.0"

    def test_execute_unknown(self, workspace: Path):
        reg = default_registry(str(workspace))
        r = reg.execute("no_such_tool")
        assert not r.success
        assert "Unknown tool" in (r.error or "")
