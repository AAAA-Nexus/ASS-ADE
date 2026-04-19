# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/local/enhancer.py:259
# Component id: at.source.ass_ade.scan_missing_type_hints
__version__ = "0.1.0"

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
