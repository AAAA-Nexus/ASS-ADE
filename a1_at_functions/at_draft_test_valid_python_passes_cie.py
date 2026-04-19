# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_valid_python_passes_cie.py:7
# Component id: at.source.a1_at_functions.test_valid_python_passes_cie
from __future__ import annotations

__version__ = "0.1.0"

def test_valid_python_passes_cie(self, tmp_path):
    server = _make_server(tmp_path)
    args = {"path": str(tmp_path / "ok.py"), "content": "def f(): return 1\n"}
    result = MagicMock(success=True, output="wrote 18 bytes")
    out = server._post_tool_hook("write_file", args, result)
    # Valid code → result unchanged
    assert out.success is True
