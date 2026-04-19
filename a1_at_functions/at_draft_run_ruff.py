# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a1_at_functions/at_draft_run_ruff.py:5
# Component id: at.source.ass_ade.run_ruff
__version__ = "0.1.0"

def run_ruff(root: Path, fix: bool = False) -> dict[str, Any]:
    if not shutil.which("ruff"):
        return {"linter": "ruff", "ok": None, "error": "ruff not found"}

    cmd = [
        "ruff", "check", str(root), "--output-format", "json",
        "--exclude", ".pytest_tmp",
    ]
    if fix:
        cmd.append("--fix")

    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60,
            encoding="utf-8", errors="replace",
        )
        # Use stdout only for JSON — stderr is ruff's error/status channel.
        raw = proc.stdout or ""
        if not raw.strip():
            # ruff produced no JSON output; treat as environment error, not a lint failure
            err = proc.stderr.strip() or "ruff produced no output"
            return {
                "linter": "ruff", "ok": None, "error": err,
                "findings": [], "error_count": 0, "warning_count": 0,
            }
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return {
                "linter": "ruff", "ok": None, "raw": raw, "error": "failed to parse output",
                "findings": [], "error_count": 0, "warning_count": 0,
            }

        findings: list[dict[str, Any]] = []
        error_count = 0
        warning_count = 0

        for item in data:
            code: str = item.get("code") or ""
            location = item.get("location") or {}
            finding = {
                "file": item.get("filename", ""),
                "row": location.get("row", 0),
                "col": location.get("column", 0),
                "code": code,
                "message": item.get("message", ""),
            }
            findings.append(finding)
            # E/F codes are errors; W codes are warnings
            if code.startswith("W"):
                warning_count += 1
            else:
                error_count += 1

        return {
            "linter": "ruff",
            "ok": len(findings) == 0,
            "error_count": error_count,
            "warning_count": warning_count,
            "findings": findings,
            "raw": raw,
        }
    except subprocess.TimeoutExpired:
        return {"linter": "ruff", "ok": None, "error": "timed out"}
    except Exception as exc:
        return {"linter": "ruff", "ok": None, "error": str(exc)}
