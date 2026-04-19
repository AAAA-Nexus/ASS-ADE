# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_not_found.py:7
# Component id: at.source.a1_at_functions.test_not_found
from __future__ import annotations

__version__ = "0.1.0"

def test_not_found(self, workspace: Path):
    tool = EditFileTool(str(workspace))
    r = tool.execute(path="hello.py", old_string="NOPE", new_string="X")
    assert not r.success
    assert "not found" in (r.error or "").lower()
