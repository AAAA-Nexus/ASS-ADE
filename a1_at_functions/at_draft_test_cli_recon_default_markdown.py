# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_cli_recon_default_markdown.py:7
# Component id: at.source.a1_at_functions.test_cli_recon_default_markdown
from __future__ import annotations

__version__ = "0.1.0"

def test_cli_recon_default_markdown(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    result = runner.invoke(app, ["recon", str(tmp_path)])
    assert result.exit_code == 0
    assert "RECON_REPORT" in result.output
