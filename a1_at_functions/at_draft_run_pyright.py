# Extracted from C:/!ass-ade/src/ass_ade/local/linter.py:152
# Component id: at.source.ass_ade.run_pyright
from __future__ import annotations

__version__ = "0.1.0"

def run_pyright(root: Path) -> dict[str, Any]:
    if not shutil.which("pyright"):
        return {"linter": "pyright", "ok": None, "error": "pyright not found"}

    cmd = ["pyright", "--outputjson", str(root)]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120, encoding="utf-8", errors="replace")
        raw = proc.stdout or proc.stderr or ""
        try:
            data = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError:
            return {"linter": "pyright", "ok": False, "raw": raw, "error": "failed to parse output"}

        general_diag = data.get("generalDiagnostics") or []
        findings: list[dict[str, Any]] = []
        error_count = 0
        warning_count = 0

        for item in general_diag:
            severity = item.get("severity", "error")
            finding = {
                "file": item.get("file", ""),
                "row": (item.get("range") or {}).get("start", {}).get("line", 0),
                "col": (item.get("range") or {}).get("start", {}).get("character", 0),
                "code": item.get("rule", ""),
                "message": item.get("message", ""),
            }
            findings.append(finding)
            if severity == "warning":
                warning_count += 1
            elif severity == "error":
                error_count += 1

        summary = data.get("summary") or {}
        ok = summary.get("errorCount", error_count) == 0

        return {
            "linter": "pyright",
            "ok": ok,
            "error_count": error_count,
            "warning_count": warning_count,
            "findings": findings,
            "raw": raw,
        }
    except subprocess.TimeoutExpired:
        return {"linter": "pyright", "ok": None, "error": "timed out"}
    except Exception as exc:
        return {"linter": "pyright", "ok": None, "error": str(exc)}
