# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_write_after_read_is_allowed_in_block_mode.py:7
# Component id: at.source.a1_at_functions.test_write_after_read_is_allowed_in_block_mode
from __future__ import annotations

__version__ = "0.1.0"

def test_write_after_read_is_allowed_in_block_mode(self, tmp_path):
    target = tmp_path / "existing.py"
    target.write_text("y = 2\n")
    server = _make_server(tmp_path)
    server._ncb_mode = "block"
    # Record a read
    server._post_tool_hook("read_file", _mk_args(target), MagicMock(success=True, output="y = 2\n"))
    allow, reason = server._pre_tool_hook("write_file", _mk_args(target))
    assert allow is True
