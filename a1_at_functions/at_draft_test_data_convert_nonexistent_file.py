# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:717
# Component id: at.source.ass_ade.test_data_convert_nonexistent_file
from __future__ import annotations

__version__ = "0.1.0"

def test_data_convert_nonexistent_file(self, tmp_path: Path, hybrid_config: Path) -> None:
    """Data convert should error if input file doesn't exist."""
    result = runner.invoke(
        app,
        ["data", "convert", str(tmp_path / "nonexistent.json"), "yaml", "--config", str(hybrid_config)],
    )

    # Should fail because file doesn't exist
    assert result.exit_code != 0
