# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_preview_does_not_modify.py:7
# Component id: at.source.a1_at_functions.test_preview_does_not_modify
from __future__ import annotations

__version__ = "0.1.0"

def test_preview_does_not_modify(self, tmp_path: Path):
    (tmp_path / "code.py").write_text("x = 1\ny = 2\nz = 3\n")
    tool = EditFileTool(str(tmp_path))
    tool.execute(
        path="code.py",
        old_string="y = 2",
        new_string="y = 42",
        preview=True,
    )
    # File should be unchanged
    assert (tmp_path / "code.py").read_text() == "x = 1\ny = 2\nz = 3\n"
