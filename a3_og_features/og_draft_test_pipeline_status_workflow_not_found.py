# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:500
# Component id: og.source.ass_ade.test_pipeline_status_workflow_not_found
from __future__ import annotations

__version__ = "0.1.0"

def test_pipeline_status_workflow_not_found(self, tmp_path: Path) -> None:
    """Pipeline status should handle missing workflow gracefully."""
    workflow_dir = tmp_path / ".ass-ade" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)

    with patch("pathlib.Path.cwd", return_value=tmp_path):
        result = runner.invoke(
            app,
            ["pipeline", "status", "nonexistent-workflow"],
        )

    # Should exit cleanly when workflow not found
    assert result.exit_code == 0 or "not found" in result.stdout.lower()
