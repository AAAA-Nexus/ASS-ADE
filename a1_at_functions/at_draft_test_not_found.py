# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testeditfile.py:12
# Component id: at.source.ass_ade.test_not_found
__version__ = "0.1.0"

    def test_not_found(self, workspace: Path):
        tool = EditFileTool(str(workspace))
        r = tool.execute(path="hello.py", old_string="NOPE", new_string="X")
        assert not r.success
        assert "not found" in (r.error or "").lower()
