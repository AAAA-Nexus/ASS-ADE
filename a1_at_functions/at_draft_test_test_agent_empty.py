# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_test_agent_empty.py:7
# Component id: at.source.a1_at_functions.test_test_agent_empty
from __future__ import annotations

__version__ = "0.1.0"

def test_test_agent_empty(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text("def run(): pass\n", encoding="utf-8")
    files = _iter_files(tmp_path)
    result = _test_agent(tmp_path, files)
    assert result["test_files"] == 0
    assert result["test_functions"] == 0
    assert result["coverage_ratio"] == 0.0
