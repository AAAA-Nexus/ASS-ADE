# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_scan_source_symbols_skips_venv.py:7
# Component id: at.source.a1_at_functions.test_scan_source_symbols_skips_venv
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_source_symbols_skips_venv(tmp_path: Path) -> None:
    venv_py = tmp_path / ".venv" / "lib"
    venv_py.mkdir(parents=True)
    (venv_py / "hidden.py").write_text("def secret(): pass\n", encoding="utf-8")

    symbols = scan_source_symbols(tmp_path)
    names = {s["name"] for s in symbols}

    assert "secret" not in names
