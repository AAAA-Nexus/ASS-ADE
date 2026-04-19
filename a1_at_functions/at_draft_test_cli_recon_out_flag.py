# Extracted from C:/!ass-ade/tests/test_parallel_recon.py:422
# Component id: at.source.ass_ade.test_cli_recon_out_flag
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
