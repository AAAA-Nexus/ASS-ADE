# Extracted from C:/!ass-ade/tests/test_docs_engine.py:103
# Component id: mo.source.ass_ade.test_scan_source_symbols_skips_venv
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_source_symbols_skips_venv(tmp_path: Path) -> None:
    venv_py = tmp_path / ".venv" / "lib"
    venv_py.mkdir(parents=True)
    (venv_py / "hidden.py").write_text("def secret(): pass\n", encoding="utf-8")

    symbols = scan_source_symbols(tmp_path)
    names = {s["name"] for s in symbols}

    assert "secret" not in names
