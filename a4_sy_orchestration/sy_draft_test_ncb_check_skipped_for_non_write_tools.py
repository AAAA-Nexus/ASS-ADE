# Extracted from C:/!ass-ade/tests/test_mcp_gates.py:74
# Component id: sy.source.ass_ade.test_ncb_check_skipped_for_non_write_tools
from __future__ import annotations

__version__ = "0.1.0"

def test_ncb_check_skipped_for_non_write_tools(self, tmp_path):
    server = _make_server(tmp_path)
    server._ncb_mode = "block"
    # list_directory etc. should never be NCB-gated
    allow, _ = server._pre_tool_hook("list_directory", _mk_args(tmp_path))
    assert allow is True
