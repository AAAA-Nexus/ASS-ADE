# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_cli_recon_missing_path.py:7
# Component id: at.source.a1_at_functions.test_cli_recon_missing_path
from __future__ import annotations

__version__ = "0.1.0"

def test_cli_recon_missing_path(tmp_path: Path) -> None:
    nonexistent = tmp_path / "does_not_exist"
    result = runner.invoke(app, ["recon", str(nonexistent)])
    assert result.exit_code != 0
