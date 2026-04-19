# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a4_sy_orchestration/sy_draft_testciegateonwrite.py:25
# Component id: at.source.ass_ade.test_owasp_eval_injection_blocked
__version__ = "0.1.0"

    def test_owasp_eval_injection_blocked(self, tmp_path):
        server = _make_server(tmp_path)
        args = {"path": str(tmp_path / "bad.py"), "content": "result = eval(user_input)\n"}
        out = server._post_tool_hook("write_file", args, MagicMock(success=True, output="ok"))
        assert out.success is False
        assert "CIE REJECTED" in (out.error or "")
        assert "A03_injection_eval" in (out.error or "")
