# Extracted from C:/!ass-ade/tests/test_docs_engine.py:24
# Component id: mo.source.ass_ade.test_detect_languages_on_tmp
from __future__ import annotations

__version__ = "0.1.0"

def test_detect_languages_on_tmp(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text("pass", encoding="utf-8")
    (tmp_path / "utils.py").write_text("pass", encoding="utf-8")
    (tmp_path / "README.md").write_text("# hi", encoding="utf-8")

    result = detect_languages(tmp_path)

    assert result.get("py") == 2
    assert result.get("md") == 1
