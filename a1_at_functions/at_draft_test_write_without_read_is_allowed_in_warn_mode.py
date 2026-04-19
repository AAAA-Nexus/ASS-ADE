# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_write_without_read_is_allowed_in_warn_mode.py:7
# Component id: at.source.a1_at_functions.test_write_without_read_is_allowed_in_warn_mode
from __future__ import annotations

__version__ = "0.1.0"

def test_write_without_read_is_allowed_in_warn_mode(self, tmp_path):
    server = _make_server(tmp_path)
    # Default mode is "warn" → returns (True, "")
    allow, reason = server._pre_tool_hook("write_file", _mk_args(tmp_path / "new.py"))
    assert allow is True
