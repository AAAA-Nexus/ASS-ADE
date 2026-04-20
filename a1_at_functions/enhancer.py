"""Local codebase enhancement scanner.

Scans for improvement opportunities without network calls. Returns
ranked findings that the CLI forwards to the Nexus API for deep
analysis and blueprint generation.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

DEFAULT_IGNORED_DIRS = {
    ".git", ".hg", ".svn", ".venv", "__pycache__", "node_modules",
    "target", ".pytest_cache", ".ruff_cache", "build", "dist",
    ".ass-ade",  # selfbuild artifact directories — not part of the live source
}
_MAX_SCAN_FILES = 500


def _walk_python_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.py"):
        if any(part in DEFAULT_IGNORED_DIRS or part == ".venv" for part in path.parts):
            continue
        files.append(path)
        if len(files) >= _MAX_SCAN_FILES:
            break
    return sorted(files)


def _read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []


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


def scan_long_functions(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    counter = 1
    for path in _walk_python_files(root):
        lines = _read_lines(path)
        func_start: int | None = None
        func_name = ""
        func_indent = 0
        line_count = 0

        def _flush(end_line: int) -> None:
            nonlocal func_start, func_name, func_indent, line_count, counter
            if func_start is not None and line_count > 50:
                rel = str(path.relative_to(root))
                findings.append({
                    "id": counter,
                    "category": "long_function",
                    "title": f"Long function: {func_name}",
                    "description": f"{func_name} spans ~{line_count} lines in {rel}.",
                    "file": rel,
                    "line": func_start + 1,
                    "impact": "medium",
                    "effort": "medium",
                })
                counter += 1
            func_start = None

        for i, raw in enumerate(lines):
            stripped = raw.lstrip()
            indent = len(raw) - len(stripped)
            is_def = stripped.startswith("def ") or stripped.startswith("async def ")
            is_class = stripped.startswith("class ")

            if func_start is not None:
                if (is_def or is_class) and indent <= func_indent:
                    _flush(i)
                elif stripped and not stripped.startswith("#"):
                    line_count += 1

            if is_def and func_start is None:
                _flush(i)
                func_start = i
                func_name = stripped.split("(")[0].replace("async def ", "").replace("def ", "").strip()
                func_indent = indent
                line_count = 0

            if len(findings) >= 8:
                break
        _flush(len(lines))
        if len(findings) >= 8:
            break
    return findings


def scan_missing_docs(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    counter = 1
    for path in _walk_python_files(root):
        lines = _read_lines(path)
        for i, line in enumerate(lines):
            stripped = line.lstrip()
            if not (stripped.startswith("def ") or stripped.startswith("class ")):
                continue
            name_part = stripped.split("(")[0].split(" ", 1)[-1].strip().rstrip(":")
            if name_part.startswith("_"):
                continue
            has_doc = False
            for j in range(i + 1, min(i + 4, len(lines))):
                next_stripped = lines[j].lstrip()
                if next_stripped.startswith('"""') or next_stripped.startswith("'''"):
                    has_doc = True
                    break
                if next_stripped and not next_stripped.startswith("#"):
                    break
            if not has_doc:
                rel = str(path.relative_to(root))
                findings.append({
                    "id": counter,
                    "category": "missing_docs",
                    "title": f"Missing docstring: {name_part}",
                    "description": f"{name_part} in {rel} has no docstring.",
                    "file": rel,
                    "line": i + 1,
                    "impact": "low",
                    "effort": "low",
                })
                counter += 1
                if len(findings) >= 8:
                    return findings
    return findings


def scan_security_patterns(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    counter = 1
    patterns = [
        ("pickle.loads(", "Unsafe deserialization via pickle.loads"),  # nosec
        ("eval(", "Use of eval()"),  # nosec
        ("exec(", "Use of exec()"),  # nosec
    ]
    for path in _walk_python_files(root):
        is_test = (
            path.stem.startswith("test_")
            or path.stem.endswith("_test")
            or any(part in ("tests", "test") for part in path.parts)
        )
        if is_test:
            continue  # test files intentionally use unsafe patterns for validation
        lines = _read_lines(path)
        for i, line in enumerate(lines):
            if "# nosec" in line or "# noqa: S" in line:
                continue
            for pat, msg in patterns:
                if pat in line:
                    rel = str(path.relative_to(root))
                    findings.append({
                        "id": counter,
                        "category": "security",
                        "title": msg,
                        "description": f"{msg} at {rel}:{i + 1}.",
                        "file": rel,
                        "line": i + 1,
                        "impact": "high",
                        "effort": "low",
                    })
                    counter += 1
                    if len(findings) >= 10:
                        return findings
            if "subprocess.run(" in line or "subprocess.call(" in line:
                if "shell=True" in line:
                    rel = str(path.relative_to(root))
                    findings.append({
                        "id": counter,
                        "category": "security",
                        "title": "subprocess call with shell=True",
                        "description": f"subprocess call with shell=True at {rel}:{i + 1}.",
                        "file": rel,
                        "line": i + 1,
                        "impact": "high",
                        "effort": "low",
                    })
                    counter += 1
                    if len(findings) >= 10:
                        return findings
            if not is_test and line.lstrip().startswith("assert "):
                if "# nosec" not in line:
                    rel = str(path.relative_to(root))
                    findings.append({
                        "id": counter,
                        "category": "security",
                        "title": "Assertions used for control flow",
                        "description": f"assert used for control flow at {rel}:{i + 1}.",
                        "file": rel,
                        "line": i + 1,
                        "impact": "high",
                        "effort": "low",
                    })
                    counter += 1
                    if len(findings) >= 10:
                        return findings
    return findings


def scan_bare_except(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    counter = 1
    for path in _walk_python_files(root):
        lines = _read_lines(path)
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped == "except:":
                rel = str(path.relative_to(root))
                findings.append({
                    "id": counter,
                    "category": "bare_except",
                    "title": "Bare except clause",
                    "description": f"Bare except: in {rel}:{i + 1} catches all exceptions including SystemExit.",
                    "file": rel,
                    "line": i + 1,
                    "impact": "medium",
                    "effort": "low",
                })
                counter += 1
                if len(findings) >= 8:
                    return findings
    return findings


def scan_missing_type_hints(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    counter = 1
    for path in _walk_python_files(root):
        if "test" in path.stem or "test" in str(path.parent):
            continue
        lines = _read_lines(path)
        for i, line in enumerate(lines):
            stripped = line.lstrip()
            if not stripped.startswith("def "):
                continue
            name_part = stripped[4:].split("(")[0].strip()
            if name_part.startswith("_"):
                continue
            combined = line
            if i + 1 < len(lines):
                combined += lines[i + 1]
            if "->" not in combined:
                rel = str(path.relative_to(root))
                findings.append({
                    "id": counter,
                    "category": "missing_types",
                    "title": f"Missing return type hint: {name_part}",
                    "description": f"{name_part} in {rel} has no return type annotation.",
                    "file": rel,
                    "line": i + 1,
                    "impact": "low",
                    "effort": "low",
                })
                counter += 1
                if len(findings) >= 8:
                    return findings
    return findings


def scan_todo_fixme(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    counter = 1
    markers = ("# TODO", "# FIXME", "# HACK", "# XXX")
    for path in _walk_python_files(root):
        lines = _read_lines(path)
        for i, line in enumerate(lines):
            for marker in markers:
                if marker in line:
                    rel = str(path.relative_to(root))
                    findings.append({
                        "id": counter,
                        "category": "technical_debt",
                        "title": f"Technical debt marker: {marker.strip()}",
                        "description": line.strip(),
                        "file": rel,
                        "line": i + 1,
                        "impact": "low",
                        "effort": "medium",
                    })
                    counter += 1
                    if len(findings) >= 6:
                        return findings
                    break
    return findings


def rank_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    impact_order = {"high": 0, "medium": 1, "low": 2}
    effort_order = {"low": 0, "medium": 1, "high": 2}
    ranked = sorted(
        findings,
        key=lambda f: (impact_order.get(f.get("impact", "low"), 2), effort_order.get(f.get("effort", "medium"), 1)),
    )
    for i, finding in enumerate(ranked, start=1):
        finding["id"] = i
    return ranked


def build_enhancement_report(root: Path) -> dict[str, Any]:
    scanners = [
        scan_missing_tests,
        scan_long_functions,
        scan_missing_docs,
        scan_security_patterns,
        scan_bare_except,
        scan_missing_type_hints,
        scan_todo_fixme,
    ]
    all_findings: list[dict[str, Any]] = []
    for scanner in scanners:
        try:
            all_findings.extend(scanner(root))
        except Exception:
            pass

    ranked = rank_findings(all_findings)

    by_impact: dict[str, int] = {"high": 0, "medium": 0, "low": 0}
    by_category: dict[str, int] = {}
    for f in ranked:
        impact = f.get("impact", "low")
        by_impact[impact] = by_impact.get(impact, 0) + 1
        cat = f.get("category", "unknown")
        by_category[cat] = by_category.get(cat, 0) + 1

    scanned = len(_walk_python_files(root))

    return {
        "root": str(root.resolve()),
        "total_findings": len(ranked),
        "by_impact": by_impact,
        "by_category": by_category,
        "findings": ranked,
        "scanned_files": scanned,
    }
