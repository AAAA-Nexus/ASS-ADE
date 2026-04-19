# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_syntax_error_blocked_by_cie.py:7
# Component id: at.source.a1_at_functions.test_syntax_error_blocked_by_cie
from __future__ import annotations

__version__ = "0.1.0"

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
