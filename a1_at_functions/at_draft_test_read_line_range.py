# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testreadfile.py:12
# Component id: at.source.ass_ade.test_read_line_range
__version__ = "0.1.0"

    def test_read_line_range(self, workspace: Path):
        tool = ReadFileTool(str(workspace))
        r = tool.execute(path="sub/data.txt", start_line=2, end_line=2)
        assert r.success
        assert r.output.strip() == "line2"
