# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_test_scan_source_symbols_finds_functions.py:5
# Component id: at.source.ass_ade.test_scan_source_symbols_finds_functions
__version__ = "0.1.0"

def test_scan_source_symbols_finds_functions(tmp_path: Path) -> None:
    src = tmp_path / "module.py"
    src.write_text("def foo():\n    pass\n\nclass Bar:\n    pass\n", encoding="utf-8")

    symbols = scan_source_symbols(tmp_path)
    names = {s["name"] for s in symbols}

    assert "foo" in names
    assert "Bar" in names
