# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tools_builtin.py:129
# Component id: mo.source.ass_ade.testlistdirectory
__version__ = "0.1.0"

class TestListDirectory:
    def test_list_root(self, workspace: Path):
        tool = ListDirectoryTool(str(workspace))
        r = tool.execute()
        assert r.success
        assert "hello.py" in r.output
        assert "sub/" in r.output

    def test_list_subdir(self, workspace: Path):
        tool = ListDirectoryTool(str(workspace))
        r = tool.execute(path="sub")
        assert r.success
        assert "data.txt" in r.output
