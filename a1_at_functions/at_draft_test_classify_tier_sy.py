# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:234
# Component id: at.source.ass_ade.test_classify_tier_sy
__version__ = "0.1.0"

def test_classify_tier_sy(tmp_path: Path) -> None:
    f = tmp_path / "app.py"
    f.write_text(
        "import os\nimport sys\nimport json\n"
        "def main(): pass\n"
        "if __name__ == '__main__':\n    main()\n",
        encoding="utf-8",
    )
    assert _classify_tier(f) == "sy"
