# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testwritefile.py:12
# Component id: at.source.ass_ade.test_create_nested
__version__ = "0.1.0"

    def test_create_nested(self, workspace: Path):
        tool = WriteFileTool(str(workspace))
        r = tool.execute(path="a/b/c.py", content="pass\n")
        assert r.success
        assert (workspace / "a" / "b" / "c.py").exists()
