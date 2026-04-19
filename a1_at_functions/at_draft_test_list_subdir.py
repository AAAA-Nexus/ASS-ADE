# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testlistdirectory.py:13
# Component id: at.source.ass_ade.test_list_subdir
__version__ = "0.1.0"

    def test_list_subdir(self, workspace: Path):
        tool = ListDirectoryTool(str(workspace))
        r = tool.execute(path="sub")
        assert r.success
        assert "data.txt" in r.output
