# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_parallel_recon.py:159
# Component id: at.source.ass_ade.test_scout_basic_counts
__version__ = "0.1.0"

def test_scout_basic_counts(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _scout_agent(tmp_path, files)

    assert result["total_files"] > 0
    assert result["total_size_kb"] > 0
    assert result["max_depth"] >= 1
    assert isinstance(result["top_level"], list)
    assert ".py" in result["by_extension"]
    assert result["source_files"] > 0
