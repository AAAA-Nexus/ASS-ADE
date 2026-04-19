# Extracted from C:/!ass-ade/tests/test_docs_engine.py:92
# Component id: mo.source.ass_ade.test_scan_source_symbols_finds_functions
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_source_symbols_finds_functions(tmp_path: Path) -> None:
    src = tmp_path / "module.py"
    src.write_text("def foo():\n    pass\n\nclass Bar:\n    pass\n", encoding="utf-8")

    symbols = scan_source_symbols(tmp_path)
    names = {s["name"] for s in symbols}

    assert "foo" in names
    assert "Bar" in names
