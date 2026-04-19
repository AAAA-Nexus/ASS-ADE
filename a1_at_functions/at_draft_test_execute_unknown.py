# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_execute_unknown.py:7
# Component id: at.source.a1_at_functions.test_execute_unknown
from __future__ import annotations

__version__ = "0.1.0"

def test_execute_unknown(self, workspace: Path):
    reg = default_registry(str(workspace))
    r = reg.execute("no_such_tool")
    assert not r.success
    assert "Unknown tool" in (r.error or "")
