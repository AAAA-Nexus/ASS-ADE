# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:245
# Component id: at.source.ass_ade.test_tier_agent_counts
__version__ = "0.1.0"

def test_tier_agent_counts(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _tier_agent(tmp_path, files)

    assert result["total_py_files"] > 0
    assert sum(result["tier_distribution"].values()) == result["total_py_files"]
    assert result["dominant_tier"] in ("qk", "at", "mo", "og", "sy")
