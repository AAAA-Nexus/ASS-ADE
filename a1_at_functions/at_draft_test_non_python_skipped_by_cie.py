# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_non_python_skipped_by_cie.py:7
# Component id: at.source.a1_at_functions.test_non_python_skipped_by_cie
from __future__ import annotations

__version__ = "0.1.0"

def test_non_python_skipped_by_cie(self, tmp_path):
    server = _make_server(tmp_path)
    args = {"path": str(tmp_path / "readme.txt"), "content": "raw text with eval()"}
    result = MagicMock(success=True, output="ok")
    out = server._post_tool_hook("write_file", args, result)
    # Text files aren't AST-validated or OWASP-scanned → pass through
    assert out.success is True
