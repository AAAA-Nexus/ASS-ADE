# Extracted from C:/!ass-ade/tests/test_parallel_recon.py:383
# Component id: at.source.ass_ade.test_cli_recon_default_markdown
from __future__ import annotations

__version__ = "0.1.0"

def test_cli_recon_default_markdown(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    result = runner.invoke(app, ["recon", str(tmp_path)])
    assert result.exit_code == 0
    assert "RECON_REPORT" in result.output
