# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_owasp_eval_injection_blocked.py:7
# Component id: at.source.a1_at_functions.test_owasp_eval_injection_blocked
from __future__ import annotations

__version__ = "0.1.0"

def test_owasp_eval_injection_blocked(self, tmp_path):
    server = _make_server(tmp_path)
    args = {"path": str(tmp_path / "bad.py"), "content": "result = eval(user_input)\n"}
    out = server._post_tool_hook("write_file", args, MagicMock(success=True, output="ok"))
    assert out.success is False
    assert "CIE REJECTED" in (out.error or "")
    assert "A03_injection_eval" in (out.error or "")
