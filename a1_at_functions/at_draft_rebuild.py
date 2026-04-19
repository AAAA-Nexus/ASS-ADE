# Extracted from C:/!ass-ade/tools/rebuild_tool.py:10
# Component id: at.source.ass_ade.rebuild
from __future__ import annotations

__version__ = "0.1.0"

def rebuild(
    path: str,
    local_only: bool = False,
    blueprint: str | None = None,
    output: str | None = None,
    dry_run: bool = False,
    timeout: int = 300,
) -> dict:
    """Rebuild a codebase into a tier-partitioned structure.

    Args:
        path: Absolute or relative path to the source codebase.
        local_only: Skip AAAA-Nexus enrichment; use local analysis only.
        blueprint: Path to an AAAA-SPEC-004 blueprint JSON file.
        output: Write output to this directory instead of auto-naming.
        dry_run: Show what would be moved without writing any files.
        timeout: Maximum seconds to wait for the command.

    Returns:
        dict with keys:
            ok (bool): True when exit_code == 0.
            exit_code (int): Raw process exit code.
            stdout (str): Captured standard output.
            stderr (str): Captured standard error.
    """
    cmd = [sys.executable, "-m", "ass_ade", "rebuild", path]
    if local_only:
        cmd.append("--only-path")
    if blueprint:
        cmd.extend(["--blueprint", blueprint])
    if output:
        cmd.extend(["--output", output])
    if dry_run:
        cmd.append("--dry-run")

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
            "stderr": f"rebuild timed out after {timeout}s",
        }
    except FileNotFoundError as exc:
        return {
            "ok": False,
            "exit_code": 127,
            "stdout": "",
            "stderr": str(exc),
        }

    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
