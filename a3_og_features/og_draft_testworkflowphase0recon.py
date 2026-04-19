# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:602
# Component id: og.source.ass_ade.testworkflowphase0recon
from __future__ import annotations

__version__ = "0.1.0"

class TestWorkflowPhase0Recon:
    """Test `workflow phase0-recon` command — repo reconnaissance."""

    def test_workflow_phase0_recon_ready(self, tmp_path: Path) -> None:
        """Phase 0 recon should identify relevant files and sources."""
        (tmp_path / "README.md").write_text("# My Project", encoding="utf-8")
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "main.py").write_text("def main(): pass", encoding="utf-8")

        result = runner.invoke(
            app,
            ["workflow", "phase0-recon", "Add async support", "--path", str(tmp_path)],
        )

        assert result.exit_code == 0
