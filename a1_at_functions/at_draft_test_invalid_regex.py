# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:175
# Component id: at.source.ass_ade.test_invalid_regex
from __future__ import annotations

__version__ = "0.1.0"

def test_invalid_regex(self, workspace: Path):
    tool = GrepSearchTool(str(workspace))
    r = tool.execute(pattern="[invalid")
    assert not r.success
    assert "Invalid regex" in (r.error or "")
