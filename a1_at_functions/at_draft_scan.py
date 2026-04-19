# Extracted from C:/!ass-ade/tools/enhance_tool.py:10
# Component id: at.source.ass_ade.scan
from __future__ import annotations

__version__ = "0.1.0"

def scan(
    path: str,
    local_only: bool = False,
    min_severity: str = "info",
    timeout: int = 120,
) -> dict:
    """Scan a codebase for enhancement opportunities.

    Args:
        path: Absolute or relative path to the codebase.
        local_only: Skip AAAA-Nexus enrichment; use local analysis only.
        min_severity: Minimum severity level to report (info/low/medium/high/critical).
        timeout: Maximum seconds to wait for the command.

    Returns:
        dict with keys:
            ok (bool): True when exit_code == 0.
            exit_code (int): Raw process exit code.
            stdout (str): Captured standard output.
            stderr (str): Captured standard error.
            findings (list[dict] | None): Parsed findings list when ok=True.
    """
    cmd = [
        sys.executable, "-m", "ass_ade", "enhance", "scan", path,
        "--json",
        "--min-severity", min_severity,
    ]
    if local_only:
        cmd.append("--local-only")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "exit_code": 124,
            "stdout": "",
            "stderr": f"enhance scan timed out after {timeout}s",
            "findings": None,
        }
    except FileNotFoundError as exc:
        return {
            "ok": False,
            "exit_code": 127,
            "stdout": "",
            "stderr": str(exc),
            "findings": None,
        }

    findings = None
    if result.returncode == 0 and result.stdout.strip():
        try:
            parsed = json.loads(result.stdout)
            findings = parsed if isinstance(parsed, list) else parsed.get("findings")
        except json.JSONDecodeError:
            pass

    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "findings": findings,
    }
