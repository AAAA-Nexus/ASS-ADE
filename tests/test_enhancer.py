from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from ass_ade.local.enhancer import (
    apply_enhancement,
    build_enhancement_report,
    rank_findings,
    scan_bare_except,
    scan_long_functions,
    scan_missing_docs,
    scan_missing_tests,
    scan_security_patterns,
    scan_todo_fixme,
    scan_missing_type_hints,
)


# ---------------------------------------------------------------------------
# scan_missing_tests
# ---------------------------------------------------------------------------


def test_scan_missing_tests_finds_gap(tmp_path: Path) -> None:
    src_pkg = tmp_path / "src" / "mypackage"
    src_pkg.mkdir(parents=True)
    (src_pkg / "utils.py").write_text("def helper(): pass\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()

    findings = scan_missing_tests(tmp_path)

    assert len(findings) >= 1
    assert any("utils" in f["file"] for f in findings)


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


# ---------------------------------------------------------------------------
# scan_long_functions
# ---------------------------------------------------------------------------


def test_scan_long_functions_detects(tmp_path: Path) -> None:
    body_lines = "\n".join(f"    x_{i} = {i}" for i in range(60))
    content = f"def big_function():\n{body_lines}\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_long_functions(tmp_path)

    assert len(findings) >= 1
    assert findings[0]["category"] == "long_function"


def test_scan_long_functions_short_ok(tmp_path: Path) -> None:
    body_lines = "\n".join(f"    x_{i} = {i}" for i in range(10))
    content = f"def small_function():\n{body_lines}\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_long_functions(tmp_path)

    assert len(findings) == 0


# ---------------------------------------------------------------------------
# scan_missing_docs
# ---------------------------------------------------------------------------


def test_scan_missing_docs_detects(tmp_path: Path) -> None:
    content = "def public_function():\n    return 42\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_missing_docs(tmp_path)

    assert len(findings) >= 1
    assert any(f["category"] == "missing_docs" for f in findings)


def test_scan_missing_docs_private_ok(tmp_path: Path) -> None:
    content = "def _private():\n    return 42\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_missing_docs(tmp_path)

    # Private functions must not be flagged
    assert not any("_private" in f.get("title", "") for f in findings)


# ---------------------------------------------------------------------------
# scan_security_patterns
# ---------------------------------------------------------------------------


def test_scan_security_patterns_pickle(tmp_path: Path) -> None:
    content = "import pickle\nresult = pickle.loads(data)\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_security_patterns(tmp_path)

    assert any(f["category"] == "security" for f in findings)
    assert any("pickle" in f["title"].lower() for f in findings)


def test_scan_security_patterns_eval(tmp_path: Path) -> None:
    content = "output = eval(user_input)\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_security_patterns(tmp_path)

    assert any(f["category"] == "security" for f in findings)
    assert any("eval" in f["title"].lower() for f in findings)


# ---------------------------------------------------------------------------
# scan_bare_except
# ---------------------------------------------------------------------------


def test_scan_bare_except_detects(tmp_path: Path) -> None:
    content = "try:\n    risky()\nexcept:\n    pass\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_bare_except(tmp_path)

    assert len(findings) >= 1
    assert findings[0]["category"] == "bare_except"


def test_scan_bare_except_typed_ok(tmp_path: Path) -> None:
    content = "try:\n    risky()\nexcept ValueError:\n    pass\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_bare_except(tmp_path)

    assert len(findings) == 0


# ---------------------------------------------------------------------------
# scan_todo_fixme
# ---------------------------------------------------------------------------


def test_scan_todo_fixme_detects(tmp_path: Path) -> None:
    content = "def do_work():\n    pass  # TODO: fix this later\n"
    (tmp_path / "module.py").write_text(content, encoding="utf-8")

    findings = scan_todo_fixme(tmp_path)

    assert len(findings) >= 1
    assert any(f["category"] == "technical_debt" for f in findings)


# ---------------------------------------------------------------------------
# rank_findings
# ---------------------------------------------------------------------------


def test_rank_findings_order() -> None:
    findings: list[dict[str, Any]] = [
        {"id": 1, "impact": "low", "effort": "low", "category": "a"},
        {"id": 2, "impact": "high", "effort": "medium", "category": "b"},
        {"id": 3, "impact": "medium", "effort": "low", "category": "c"},
    ]

    ranked = rank_findings(findings)

    assert ranked[0]["impact"] == "high"


def test_rank_findings_reassigns_ids() -> None:
    findings: list[dict[str, Any]] = [
        {"id": 10, "impact": "low", "effort": "low", "category": "a"},
        {"id": 5, "impact": "medium", "effort": "low", "category": "b"},
        {"id": 7, "impact": "high", "effort": "low", "category": "c"},
    ]

    ranked = rank_findings(findings)

    ids = [f["id"] for f in ranked]
    assert ids == [1, 2, 3]


# ---------------------------------------------------------------------------
# build_enhancement_report
# ---------------------------------------------------------------------------


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


def test_build_enhancement_report_no_crash_empty_dir(tmp_path: Path) -> None:
    report = build_enhancement_report(tmp_path)

    assert isinstance(report, dict)
    assert "total_findings" in report


# ---------------------------------------------------------------------------
# apply_enhancement
# ---------------------------------------------------------------------------


def test_apply_enhancement_fixes_bare_except(tmp_path: Path) -> None:
    src = tmp_path / "module.py"
    src.write_text("try:\n    pass\nexcept:\n    pass\n", encoding="utf-8")
    finding = {"category": "bare_except", "file": "module.py", "line": 3}

    result = apply_enhancement(tmp_path, finding)

    assert result is True
    assert "except Exception:" in src.read_text(encoding="utf-8")


def test_apply_enhancement_bare_except_wrong_line_returns_false(tmp_path: Path) -> None:
    src = tmp_path / "module.py"
    src.write_text("try:\n    pass\nexcept:\n    pass\n", encoding="utf-8")
    finding = {"category": "bare_except", "file": "module.py", "line": 99}

    result = apply_enhancement(tmp_path, finding)

    assert result is False


def test_apply_enhancement_adds_docstring(tmp_path: Path) -> None:
    src = tmp_path / "module.py"
    src.write_text("def run():\n    return 1\n", encoding="utf-8")
    finding = {"category": "missing_docs", "file": "module.py", "line": 1}

    result = apply_enhancement(tmp_path, finding)

    assert result is True
    text = src.read_text(encoding="utf-8")
    assert '"""' in text


def test_apply_enhancement_skips_already_documented(tmp_path: Path) -> None:
    src = tmp_path / "module.py"
    src.write_text('def run():\n    """Already documented."""\n    return 1\n', encoding="utf-8")
    original = src.read_text(encoding="utf-8")
    finding = {"category": "missing_docs", "file": "module.py", "line": 1}

    result = apply_enhancement(tmp_path, finding)

    assert result is False
    assert src.read_text(encoding="utf-8") == original


def test_apply_enhancement_generates_test_stub(tmp_path: Path) -> None:
    (tmp_path / "src" / "mypkg").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    src_rel = "src/mypkg/widget.py"
    (tmp_path / src_rel).write_text("def do(): pass\n", encoding="utf-8")
    finding = {"category": "missing_tests", "file": src_rel}

    result = apply_enhancement(tmp_path, finding)

    assert result is True
    stub = tmp_path / "tests" / "test_widget.py"
    assert stub.exists()
    assert "importable" in stub.read_text(encoding="utf-8")


def test_apply_enhancement_unknown_category_returns_false(tmp_path: Path) -> None:
    src = tmp_path / "module.py"
    src.write_text("x = 1\n", encoding="utf-8")
    finding = {"category": "long_function", "file": "module.py", "line": 1}

    result = apply_enhancement(tmp_path, finding)

    assert result is False


def test_apply_enhancement_missing_file_returns_false(tmp_path: Path) -> None:
    finding = {"category": "bare_except", "file": "nonexistent.py", "line": 1}

    result = apply_enhancement(tmp_path, finding)

    assert result is False
