# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testerrorhandling.py:5
# Component id: mo.source.ass_ade.testerrorhandling
__version__ = "0.1.0"

class TestErrorHandling:
    """Test graceful error handling for edge cases."""

    def test_data_convert_nonexistent_file(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Data convert should error if input file doesn't exist."""
        result = runner.invoke(
            app,
            ["data", "convert", str(tmp_path / "nonexistent.json"), "yaml", "--config", str(hybrid_config)],
        )
        
        # Should fail because file doesn't exist
        assert result.exit_code != 0

    def test_compliance_check_invalid_json(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Compliance check should error if payload is invalid JSON."""
        bad_json = tmp_path / "bad.json"
        bad_json.write_text("{ invalid json }", encoding="utf-8")
        
        result = runner.invoke(
            app,
            ["compliance", "check", str(bad_json), "--config", str(hybrid_config)],
        )
        
        assert result.exit_code != 0
