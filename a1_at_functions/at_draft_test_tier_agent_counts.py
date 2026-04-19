# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_tier_agent_counts.py:7
# Component id: at.source.a1_at_functions.test_tier_agent_counts
from __future__ import annotations

__version__ = "0.1.0"

def test_tier_agent_counts(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _tier_agent(tmp_path, files)

    assert result["total_py_files"] > 0
    assert sum(result["tier_distribution"].values()) == result["total_py_files"]
    assert result["dominant_tier"] in ("qk", "at", "mo", "og", "sy")
