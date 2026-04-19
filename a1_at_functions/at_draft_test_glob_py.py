# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testsearchfiles.py:6
# Component id: at.source.ass_ade.test_glob_py
__version__ = "0.1.0"

    def test_glob_py(self, workspace: Path):
        tool = SearchFilesTool(str(workspace))
        r = tool.execute(pattern="**/*.py")
        assert r.success
        assert "hello.py" in r.output
