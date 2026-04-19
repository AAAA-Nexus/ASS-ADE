# Extracted from C:/!ass-ade/tests/test_tools_builtin.py:95
# Component id: at.source.ass_ade.test_multiple_matches
from __future__ import annotations

__version__ = "0.1.0"

def test_multiple_matches(self, workspace: Path):
    (workspace / "dup.py").write_text("a\na\na\n", encoding="utf-8")
    tool = EditFileTool(str(workspace))
    r = tool.execute(path="dup.py", old_string="a", new_string="b")
    assert not r.success
    assert "3 locations" in (r.error or "")
