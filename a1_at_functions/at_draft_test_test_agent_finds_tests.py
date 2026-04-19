# Extracted from C:/!ass-ade/tests/test_parallel_recon.py:267
# Component id: at.source.ass_ade.test_test_agent_finds_tests
from __future__ import annotations

__version__ = "0.1.0"

def test_test_agent_finds_tests(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _test_agent(tmp_path, files)

    assert result["test_files"] >= 1
    assert result["test_functions"] >= 2
    assert "pytest" in result["frameworks"]
    assert isinstance(result["coverage_ratio"], float)
