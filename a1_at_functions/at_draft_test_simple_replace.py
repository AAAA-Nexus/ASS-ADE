# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_simple_replace.py:7
# Component id: at.source.a1_at_functions.test_simple_replace
from __future__ import annotations

__version__ = "0.1.0"

def test_simple_replace(self, workspace: Path):
    tool = EditFileTool(str(workspace))
    r = tool.execute(path="hello.py", old_string="hello world", new_string="goodbye world")
    assert r.success
    assert (workspace / "hello.py").read_text() == "print('goodbye world')\n"
