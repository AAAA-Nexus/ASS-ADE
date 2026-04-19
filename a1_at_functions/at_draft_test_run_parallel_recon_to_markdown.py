# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:349
# Component id: at.source.ass_ade.test_run_parallel_recon_to_markdown
__version__ = "0.1.0"

def test_run_parallel_recon_to_markdown(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    report = run_parallel_recon(tmp_path)
    md = report.to_markdown()
    assert "# RECON_REPORT" in md
    assert "## Scout" in md
    assert "## Dependencies" in md
    assert "## Tier Distribution" in md
    assert "## Tests" in md
    assert "## Documentation" in md
