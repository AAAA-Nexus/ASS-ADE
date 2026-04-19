# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/local/enhancer.py:169
# Component id: at.source.ass_ade.scan_security_patterns
__version__ = "0.1.0"

def scan_security_patterns(root: Path) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    counter = 1
    patterns = [
        ("pickle.loads(", "Unsafe deserialization via pickle.loads"),
        ("eval(", "Use of eval()"),
        ("exec(", "Use of exec()"),
    ]
    for path in _walk_python_files(root):
        is_test = "test" in path.stem or "test" in str(path.parent)
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
