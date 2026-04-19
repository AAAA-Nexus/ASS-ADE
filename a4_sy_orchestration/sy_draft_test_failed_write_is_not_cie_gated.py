# Extracted from C:/!ass-ade/tests/test_mcp_gates.py:123
# Component id: sy.source.ass_ade.test_failed_write_is_not_cie_gated
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
