# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:89
# Component id: at.source.ass_ade.test_not_found
from __future__ import annotations

__version__ = "0.1.0"

def test_not_found(self, workspace: Path):
    tool = EditFileTool(str(workspace))
    r = tool.execute(path="hello.py", old_string="NOPE", new_string="X")
    assert not r.success
    assert "not found" in (r.error or "").lower()
