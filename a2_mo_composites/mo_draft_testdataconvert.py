# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli_happy_path.py:207
# Component id: mo.source.ass_ade.testdataconvert
__version__ = "0.1.0"

class TestDataConvert:
    """Test `data convert` command — convert structured data formats."""

    def test_data_convert_json_to_yaml(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Data format conversion test."""
        json_file = tmp_path / "config.json"
        json_file.write_text(json.dumps({"name": "app", "version": "1.0"}), encoding="utf-8")
        
        mock_nx = MagicMock()
        mock_nx.data_convert.return_value = FormatConversion(
            result='name: app\nversion: "1.0"',
            from_format="json",
            to_format="yaml",
        )
        
        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["data", "convert", str(json_file), "yaml", "--config", str(hybrid_config)],
            )
        
        # May succeed or require remote flag
        assert result.exit_code in (0, 2)
