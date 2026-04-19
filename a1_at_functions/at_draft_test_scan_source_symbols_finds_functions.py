# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_scan_source_symbols_finds_functions.py:7
# Component id: at.source.a1_at_functions.test_scan_source_symbols_finds_functions
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_source_symbols_finds_functions(tmp_path: Path) -> None:
    src = tmp_path / "module.py"
    src.write_text("def foo():\n    pass\n\nclass Bar:\n    pass\n", encoding="utf-8")

    symbols = scan_source_symbols(tmp_path)
    names = {s["name"] for s in symbols}

    assert "foo" in names
    assert "Bar" in names
