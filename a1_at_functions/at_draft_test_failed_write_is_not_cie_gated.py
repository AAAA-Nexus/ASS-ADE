# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_failed_write_is_not_cie_gated.py:7
# Component id: at.source.a1_at_functions.test_failed_write_is_not_cie_gated
from __future__ import annotations

__version__ = "0.1.0"

def test_failed_write_is_not_cie_gated(self, tmp_path):
    server = _make_server(tmp_path)
    args = {"path": str(tmp_path / "x.py"), "content": "def ok(): pass"}
    result = MagicMock(success=False, error="disk full")
    out = server._post_tool_hook("write_file", args, result)
    # Unchanged — CIE only runs on successful writes
    assert out.success is False
    assert out.error == "disk full"
