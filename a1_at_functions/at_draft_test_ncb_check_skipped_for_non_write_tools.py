# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_ncb_check_skipped_for_non_write_tools.py:7
# Component id: at.source.a1_at_functions.test_ncb_check_skipped_for_non_write_tools
from __future__ import annotations

__version__ = "0.1.0"

def test_ncb_check_skipped_for_non_write_tools(self, tmp_path):
    server = _make_server(tmp_path)
    server._ncb_mode = "block"
    # list_directory etc. should never be NCB-gated
    allow, _ = server._pre_tool_hook("list_directory", _mk_args(tmp_path))
    assert allow is True
