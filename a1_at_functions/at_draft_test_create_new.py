# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_create_new.py:7
# Component id: at.source.a1_at_functions.test_create_new
from __future__ import annotations

__version__ = "0.1.0"

def test_create_new(self, workspace: Path):
    tool = WriteFileTool(str(workspace))
    r = tool.execute(path="new.py", content="x = 1\n")
    assert r.success
    assert (workspace / "new.py").read_text() == "x = 1\n"
