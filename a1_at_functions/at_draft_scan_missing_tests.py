# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_scan_missing_tests.py:7
# Component id: at.source.a1_at_functions.scan_missing_tests
from __future__ import annotations

__version__ = "0.1.0"

def scan_missing_tests(root: Path) -> list[dict[str, Any]]:
    src_dir = root / "src"
    if not src_dir.exists():
        src_dir = root
    tests_dir = root / "tests"

    src_files = [p for p in _walk_python_files(src_dir) if not p.name.startswith("test_") and not p.name.endswith("_test.py")]

    test_files: set[str] = set()
    if tests_dir.exists():
        for p in _walk_python_files(tests_dir):
            name = p.stem.removeprefix("test_")
            if p.stem.endswith("_test"):
                name = p.stem[:-5]
            test_files.add(name)

    findings: list[dict[str, Any]] = []
    counter = 1
    for src_file in src_files:
        stem = src_file.stem
        if stem in ("__init__", "__main__"):
            continue
        if stem not in test_files:
            rel = str(src_file.relative_to(root))
            findings.append({
                "id": counter,
                "category": "missing_tests",
                "title": f"No tests for {src_file.name}",
                "description": f"{rel} has no corresponding test file under tests/.",
                "file": rel,
                "line": None,
                "impact": "high",
                "effort": "medium",
            })
            counter += 1
            if len(findings) >= 10:
                break
    return findings
