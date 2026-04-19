# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testciegateonwrite.py:5
# Component id: mo.source.ass_ade.testciegateonwrite
__version__ = "0.1.0"

class TestCIEGateOnWrite:
    def test_valid_python_passes_cie(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "ok.py"), "content": "def f(): return 1\n"}
        result = MagicMock(success=True, output="wrote 18 bytes")
        out = server._post_tool_hook("write_file", args, result)
        # Valid code → result unchanged
        assert out.success is True

    def test_syntax_error_blocked_by_cie(self, tmp_path):
        server = _make_server(tmp_path)
        target = tmp_path / "broken.py"
        # Pre-write so undo_edit has something to roll back (not strictly needed here)
        target.write_text("")
        args = {"path": str(target), "content": "def broken(:\n    pass\n"}
        original = MagicMock(success=True, output="wrote")
        out = server._post_tool_hook("write_file", args, original)
        assert out.success is False
        assert "CIE REJECTED" in (out.error or "")

    def test_owasp_eval_injection_blocked(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "bad.py"), "content": "result = eval(user_input)\n"}
        out = server._post_tool_hook("write_file", args, MagicMock(success=True, output="ok"))
        assert out.success is False
        assert "CIE REJECTED" in (out.error or "")
        assert "A03_injection_eval" in (out.error or "")

    def test_non_python_skipped_by_cie(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "readme.txt"), "content": "raw text with eval()"}
        result = MagicMock(success=True, output="ok")
        out = server._post_tool_hook("write_file", args, result)
        # Text files aren't AST-validated or OWASP-scanned → pass through
        assert out.success is True

    def test_failed_write_is_not_cie_gated(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "x.py"), "content": "def ok(): pass"}
        result = MagicMock(success=False, error="disk full")
        out = server._post_tool_hook("write_file", args, result)
        # Unchanged — CIE only runs on successful writes
        assert out.success is False
        assert out.error == "disk full"
