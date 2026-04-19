# Extracted from C:/!ass-ade/tests/test_docs_engine.py:35
# Component id: mo.source.ass_ade.test_detect_languages_ignores_venv
from __future__ import annotations

__version__ = "0.1.0"

def test_detect_languages_ignores_venv(tmp_path: Path) -> None:
    venv = tmp_path / ".venv" / "lib"
    venv.mkdir(parents=True)
    (venv / "something.py").write_text("pass", encoding="utf-8")
    # Also add a real py file so the dict is non-empty in a different ext
    (tmp_path / "real.txt").write_text("x", encoding="utf-8")

    result = detect_languages(tmp_path)

    assert "py" not in result, ".venv .py files should be excluded"
