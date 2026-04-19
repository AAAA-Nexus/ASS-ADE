# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:474
# Component id: og.source.ass_ade.test_pipeline_status_workflow_found
from __future__ import annotations

__version__ = "0.1.0"

def test_pipeline_status_workflow_found(self, tmp_path: Path) -> None:
    """Pipeline status should display workflow status when file exists."""
    # Create a workflows directory with a sample workflow file
    workflow_dir = tmp_path / ".ass-ade" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)

    workflow_data = {
        "name": "trust-gate-agent-001",
        "passed": True,
        "duration_ms": 1234.5,
        "summary": "Trust gate: ALLOW verdict"
    }
    workflow_file = workflow_dir / "trust-gate-20250417-120000.json"
    workflow_file.write_text(json.dumps(workflow_data), encoding="utf-8")

    # Mock the working directory to use tmp_path
    with patch("pathlib.Path.cwd", return_value=tmp_path):
        result = runner.invoke(
            app,
            ["pipeline", "status", "trust-gate-20250417-120000.json"],
        )

    # Status command should succeed and output JSON
    assert result.exit_code == 0, f"Status failed:\n{result.stdout}"
    assert "trust-gate-agent-001" in result.stdout
