# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_gates.py:107
# Component id: sy.source.ass_ade.test_owasp_eval_injection_blocked
__version__ = "0.1.0"

    def test_owasp_eval_injection_blocked(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "bad.py"), "content": "result = eval(user_input)\n"}
        out = server._post_tool_hook("write_file", args, MagicMock(success=True, output="ok"))
        assert out.success is False
        assert "CIE REJECTED" in (out.error or "")
        assert "A03_injection_eval" in (out.error or "")
