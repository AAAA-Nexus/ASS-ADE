# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_doc_agent_coverage.py:7
# Component id: at.source.a1_at_functions.test_doc_agent_coverage
from __future__ import annotations

__version__ = "0.1.0"

def test_doc_agent_coverage(tmp_path: Path) -> None:
    f = tmp_path / "module.py"
    f.write_text(
        'def good():\n    """Docs here."""\n    pass\n'
        "def bad():\n    pass\n",
        encoding="utf-8",
    )
    files = _iter_files(tmp_path)
    result = _doc_agent(tmp_path, files)
    assert result["doc_coverage"] == 0.5
    assert result["total_public_callables"] == 2
