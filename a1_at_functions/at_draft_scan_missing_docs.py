# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/local/enhancer.py:131
# Component id: at.source.ass_ade.scan_missing_docs
__version__ = "0.1.0"

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
