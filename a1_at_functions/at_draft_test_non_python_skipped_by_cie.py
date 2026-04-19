# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testciegateonwrite.py:33
# Component id: at.source.ass_ade.test_non_python_skipped_by_cie
__version__ = "0.1.0"

    def test_non_python_skipped_by_cie(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "readme.txt"), "content": "raw text with eval()"}
        result = MagicMock(success=True, output="ok")
        out = server._post_tool_hook("write_file", args, result)
        # Text files aren't AST-validated or OWASP-scanned → pass through
        assert out.success is True
