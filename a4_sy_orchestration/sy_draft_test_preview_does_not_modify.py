# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_server_streaming.py:169
# Component id: sy.source.ass_ade.test_preview_does_not_modify
__version__ = "0.1.0"

    def test_preview_does_not_modify(self, tmp_path: Path):
        (tmp_path / "code.py").write_text("x = 1\ny = 2\nz = 3\n")
        tool = EditFileTool(str(tmp_path))
        tool.execute(
            path="code.py",
            old_string="y = 2",
            new_string="y = 42",
            preview=True,
        )
        # File should be unchanged
        assert (tmp_path / "code.py").read_text() == "x = 1\ny = 2\nz = 3\n"
