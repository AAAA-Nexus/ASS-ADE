# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_data_convert_nonexistent_file.py:7
# Component id: at.source.a1_at_functions.test_data_convert_nonexistent_file
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
