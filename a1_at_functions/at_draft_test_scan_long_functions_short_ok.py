# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_scan_long_functions_short_ok.py:7
# Component id: at.source.a1_at_functions.test_scan_long_functions_short_ok
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_long_functions_short_ok(tmp_path: Path) -> None:
    body_lines = "\n".join(f"    x_{i} = {i}" for i in range(10))
    content = f"def small_function():\n{body_lines}\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_long_functions(tmp_path)

    assert len(findings) == 0
