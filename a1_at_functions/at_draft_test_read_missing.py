# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testreadfile.py:18
# Component id: at.source.ass_ade.test_read_missing
__version__ = "0.1.0"

    def test_read_missing(self, workspace: Path):
        tool = ReadFileTool(str(workspace))
        r = tool.execute(path="nope.py")
        assert not r.success
        assert "not found" in (r.error or "").lower()
