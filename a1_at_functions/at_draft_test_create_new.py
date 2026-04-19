# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tools_builtin.py:59
# Component id: at.source.ass_ade.test_create_new
__version__ = "0.1.0"

    def test_create_new(self, workspace: Path):
        tool = WriteFileTool(str(workspace))
        r = tool.execute(path="new.py", content="x = 1\n")
        assert r.success
        assert (workspace / "new.py").read_text() == "x = 1\n"
