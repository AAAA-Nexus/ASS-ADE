# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_preview_returns_diff.py:7
# Component id: at.source.a1_at_functions.test_preview_returns_diff
from __future__ import annotations

__version__ = "0.1.0"

def test_preview_returns_diff(self, tmp_path: Path):
    (tmp_path / "code.py").write_text("x = 1\ny = 2\nz = 3\n")
    tool = EditFileTool(str(tmp_path))
    result = tool.execute(
        path="code.py",
        old_string="y = 2",
        new_string="y = 42",
        preview=True,
    )
    assert result.success
    assert "---" in result.output  # unified diff header
    assert "-y = 2" in result.output
    assert "+y = 42" in result.output
