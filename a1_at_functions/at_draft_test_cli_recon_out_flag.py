# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:422
# Component id: at.source.ass_ade.test_cli_recon_out_flag
__version__ = "0.1.0"

def test_cli_recon_out_flag(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    out_file = tmp_path / "report.md"
    result = runner.invoke(app, ["recon", str(tmp_path), "--out", str(out_file)])
    assert result.exit_code == 0
    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "RECON_REPORT" in content
