# Extracted from C:/!ass-ade/src/ass_ade/local/enhancer.py:294
# Component id: at.source.ass_ade.scan_todo_fixme
from __future__ import annotations

__version__ = "0.1.0"

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
