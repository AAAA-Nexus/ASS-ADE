# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testpipelinerun.py:189
# Component id: og.source.a2_mo_composites.test_pipeline_history_lists_workflows
from __future__ import annotations

__version__ = "0.1.0"

def test_pipeline_history_lists_workflows(self, tmp_path: Path) -> None:
    """Pipeline history should list recent workflows."""
    workflow_dir = tmp_path / ".ass-ade" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)

    # Create several workflow files
    for i in range(3):
        workflow_data = {
            "name": f"test-workflow-{i}",
            "passed": i % 2 == 0,
            "duration_ms": 500 + i * 100,
        }
        workflow_file = workflow_dir / f"workflow-{i:03d}.json"
        workflow_file.write_text(json.dumps(workflow_data), encoding="utf-8")

    with patch("pathlib.Path.cwd", return_value=tmp_path):
        result = runner.invoke(
            app,
            ["pipeline", "history", "--limit", "5"],
        )

    # History should display a table with workflows
    assert result.exit_code == 0, f"History failed:\n{result.stdout}"
    # Should show table or list of workflows
    assert "test-workflow" in result.stdout or "History" in result.stdout or "Workflow" in result.stdout
