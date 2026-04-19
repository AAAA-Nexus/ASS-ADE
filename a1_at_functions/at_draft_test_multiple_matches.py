# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testeditfile.py:18
# Component id: at.source.ass_ade.test_multiple_matches
__version__ = "0.1.0"

    def test_multiple_matches(self, workspace: Path):
        (workspace / "dup.py").write_text("a\na\na\n", encoding="utf-8")
        tool = EditFileTool(str(workspace))
        r = tool.execute(path="dup.py", old_string="a", new_string="b")
        assert not r.success
        assert "3 locations" in (r.error or "")
