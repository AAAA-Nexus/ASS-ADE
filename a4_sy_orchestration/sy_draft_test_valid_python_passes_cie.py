# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_gates.py:88
# Component id: sy.source.ass_ade.test_valid_python_passes_cie
__version__ = "0.1.0"

    def test_valid_python_passes_cie(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "ok.py"), "content": "def f(): return 1\n"}
        result = MagicMock(success=True, output="wrote 18 bytes")
        out = server._post_tool_hook("write_file", args, result)
        # Valid code → result unchanged
        assert out.success is True
