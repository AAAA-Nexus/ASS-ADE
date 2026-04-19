# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testpipelinerun.py:175
# Component id: og.source.a2_mo_composites.test_pipeline_status_workflow_not_found
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
