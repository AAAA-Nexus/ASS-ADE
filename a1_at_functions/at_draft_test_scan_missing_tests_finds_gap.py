# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_scan_missing_tests_finds_gap.py:7
# Component id: at.source.a1_at_functions.test_scan_missing_tests_finds_gap
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
