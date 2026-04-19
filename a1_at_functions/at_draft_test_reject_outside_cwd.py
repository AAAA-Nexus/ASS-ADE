# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testwritefile.py:18
# Component id: at.source.ass_ade.test_reject_outside_cwd
__version__ = "0.1.0"

    def test_reject_outside_cwd(self, workspace: Path):
        tool = WriteFileTool(str(workspace))
        # Try to escape up
        r = tool.execute(path="../escape.py", content="pwned")
        assert not r.success
        assert "outside" in (r.error or "").lower()
