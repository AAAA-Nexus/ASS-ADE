# Extracted from C:/!ass-ade/tests/test_parallel_recon.py:290
# Component id: at.source.ass_ade.test_doc_agent_finds_readme
from __future__ import annotations

__version__ = "0.1.0"

def test_doc_agent_finds_readme(tmp_path: Path) -> None:
    _seed_full_repo(tmp_path)
    files = _iter_files(tmp_path)
    result = _doc_agent(tmp_path, files)
    assert result["has_readme"] is True
