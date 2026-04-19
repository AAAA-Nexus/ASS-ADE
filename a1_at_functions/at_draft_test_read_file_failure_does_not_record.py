# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_read_file_failure_does_not_record.py:7
# Component id: at.source.a1_at_functions.test_read_file_failure_does_not_record
from __future__ import annotations

__version__ = "0.1.0"

def test_read_file_failure_does_not_record(self, tmp_path):
    target = tmp_path / "missing.py"
    server = _make_server(tmp_path)
    result = MagicMock(success=False, error="not found")
    server._post_tool_hook("read_file", _mk_args(target), result)
    assert server.tca.ncb_contract(target) is False
