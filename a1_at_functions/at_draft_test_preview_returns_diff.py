# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testdiffpreview.py:6
# Component id: at.source.ass_ade.test_preview_returns_diff
__version__ = "0.1.0"

    def test_preview_returns_diff(self, tmp_path: Path):
        (tmp_path / "code.py").write_text("x = 1\ny = 2\nz = 3\n")
        tool = EditFileTool(str(tmp_path))
        result = tool.execute(
            path="code.py",
            old_string="y = 2",
            new_string="y = 42",
            preview=True,
        )
        assert result.success
        assert "---" in result.output  # unified diff header
        assert "-y = 2" in result.output
        assert "+y = 42" in result.output
