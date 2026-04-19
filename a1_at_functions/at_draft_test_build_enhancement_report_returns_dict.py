# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_enhancer.py:203
# Component id: at.source.ass_ade.test_build_enhancement_report_returns_dict
__version__ = "0.1.0"

def test_build_enhancement_report_returns_dict(tmp_path: Path) -> None:
    pkg = tmp_path / "src" / "mypkg"
    pkg.mkdir(parents=True)
    (pkg / "core.py").write_text("def run():\n    pass  # TODO: implement\n", encoding="utf-8")
    (pkg / "utils.py").write_text("def helper():\n    return 1\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()

    report = build_enhancement_report(tmp_path)

    assert isinstance(report, dict)
    for key in ("root", "total_findings", "by_impact", "by_category", "findings", "scanned_files"):
        assert key in report, f"missing key: {key}"
