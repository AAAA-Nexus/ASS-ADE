# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testpipelinerun.py:213
# Component id: at.source.ass_ade.test_pipeline_history_empty
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
