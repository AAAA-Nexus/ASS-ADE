# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_pipeline_history_empty.py:7
# Component id: at.source.a1_at_functions.test_pipeline_history_empty
from __future__ import annotations

__version__ = "0.1.0"

def test_pipeline_history_empty(self, tmp_path: Path) -> None:
    """Pipeline history should handle missing workflows directory gracefully."""
    with patch("pathlib.Path.cwd", return_value=tmp_path):
        result = runner.invoke(
            app,
            ["pipeline", "history"],
        )

    # Should exit cleanly with appropriate message
    assert result.exit_code == 0
    assert "history" in result.stdout.lower() or "found" in result.stdout.lower()
