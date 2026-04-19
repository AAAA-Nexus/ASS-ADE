# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:211
# Component id: at.source.ass_ade.test_classify_tier_qk
__version__ = "0.1.0"

def test_classify_tier_qk(tmp_path: Path) -> None:
    f = tmp_path / "constants.py"
    f.write_text("MAX = 3\nTIMEOUT = 30\n", encoding="utf-8")
    assert _classify_tier(f) == "qk"
