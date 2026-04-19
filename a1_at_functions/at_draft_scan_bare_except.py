# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/local/enhancer.py:234
# Component id: at.source.ass_ade.scan_bare_except
__version__ = "0.1.0"

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
