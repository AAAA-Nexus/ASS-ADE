# Extracted from C:/!ass-ade/tests/test_enhancer.py:38
# Component id: at.source.ass_ade.test_scan_missing_tests_no_gap
from __future__ import annotations

__version__ = "0.1.0"

def test_scan_missing_tests_no_gap(tmp_path: Path) -> None:
    src_pkg = tmp_path / "src" / "mypackage"
    src_pkg.mkdir(parents=True)
    (src_pkg / "utils.py").write_text("def helper(): pass\n", encoding="utf-8")
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    (tests_dir / "test_utils.py").write_text("def test_helper(): pass\n", encoding="utf-8")

    findings = scan_missing_tests(tmp_path)

    # utils.py now has a corresponding test_utils.py — should not be flagged
    flagged_files = [f["file"] for f in findings]
    assert not any("utils" in fp for fp in flagged_files)
