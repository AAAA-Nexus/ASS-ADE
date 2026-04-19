# Extracted from C:/!ass-ade/tests/test_enhancer.py:58
# Component id: at.source.ass_ade.test_scan_long_functions_detects
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_long_functions_detects(tmp_path: Path) -> None:
    body_lines = "\n".join(f"    x_{i} = {i}" for i in range(60))
    content = f"def big_function():\n{body_lines}\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_long_functions(tmp_path)

    assert len(findings) >= 1
    assert findings[0]["category"] == "long_function"
