# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_tools_builtin.py:147
# Component id: mo.source.ass_ade.testsearchfiles
__version__ = "0.1.0"

class TestSearchFiles:
    def test_glob_py(self, workspace: Path):
        tool = SearchFilesTool(str(workspace))
        r = tool.execute(pattern="**/*.py")
        assert r.success
        assert "hello.py" in r.output

    def test_no_matches(self, workspace: Path):
        tool = SearchFilesTool(str(workspace))
        r = tool.execute(pattern="**/*.rs")
        assert "No matches" in r.output
