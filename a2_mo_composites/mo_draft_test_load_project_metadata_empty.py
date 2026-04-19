# Extracted from C:/!ass-ade/tests/test_docs_engine.py:79
# Component id: mo.source.ass_ade.test_load_project_metadata_empty
from __future__ import annotations

__version__ = "0.1.0"

def test_load_project_metadata_empty(tmp_path: Path) -> None:
    meta = load_project_metadata(tmp_path)

    assert isinstance(meta, dict)
    # Should return a dict with None values, not raise
    assert "name" in meta
