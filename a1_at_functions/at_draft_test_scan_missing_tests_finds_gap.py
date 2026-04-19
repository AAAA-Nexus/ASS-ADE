# Extracted from C:/!ass-ade/tests/test_enhancer.py:26
# Component id: at.source.ass_ade.test_scan_missing_tests_finds_gap
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_missing_tests_finds_gap(tmp_path: Path) -> None:
    src_pkg = tmp_path / "src" / "mypackage"
    src_pkg.mkdir(parents=True)
    (src_pkg / "utils.py").write_text("def helper(): pass\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()

    findings = scan_missing_tests(tmp_path)

    assert len(findings) >= 1
    assert any("utils" in f["file"] for f in findings)
