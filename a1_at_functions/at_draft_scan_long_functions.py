# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_scan_long_functions.py:7
# Component id: at.source.a1_at_functions.scan_long_functions
from __future__ import annotations

__version__ = "0.1.0"

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
