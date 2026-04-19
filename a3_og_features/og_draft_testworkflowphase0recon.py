# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_testworkflowphase0recon.py:7
# Component id: og.source.a3_og_features.testworkflowphase0recon
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
