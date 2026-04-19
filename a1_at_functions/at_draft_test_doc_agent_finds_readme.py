# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_doc_agent_finds_readme.py:7
# Component id: at.source.a1_at_functions.test_doc_agent_finds_readme
from __future__ import annotations

__version__ = "0.1.0"

def test_doc_agent_finds_readme(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _doc_agent(tmp_path, files)
    assert result["has_readme"] is True
