# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_multiple_matches.py:7
# Component id: at.source.a1_at_functions.test_multiple_matches
from __future__ import annotations

__version__ = "0.1.0"

def test_multiple_matches(self, workspace: Path):
    (workspace / "dup.py").write_text("a\na\na\n", encoding="utf-8")
    tool = EditFileTool(str(workspace))
    r = tool.execute(path="dup.py", old_string="a", new_string="b")
    assert not r.success
    assert "3 locations" in (r.error or "")
