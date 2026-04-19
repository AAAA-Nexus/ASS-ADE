# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_cli_recon_out_flag.py:7
# Component id: at.source.a1_at_functions.test_cli_recon_out_flag
from __future__ import annotations

__version__ = "0.1.0"

def test_cli_recon_out_flag(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    out_file = tmp_path / "report.md"
    result = runner.invoke(app, ["recon", str(tmp_path), "--out", str(out_file)])
    assert result.exit_code == 0
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "RECON_REPORT" in content
