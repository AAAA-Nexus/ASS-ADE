# Extracted from C:/!ass-ade/tools/design_tool.py:10
# Component id: at.source.ass_ade.design
from __future__ import annotations

__version__ = "0.1.0"

def design(
    path: str,
    feature: str,
    output: str | None = None,
    local_only: bool = False,
    fmt: str = "json",
    timeout: int = 120,
) -> dict:
    """Generate an AAAA-SPEC-004 blueprint for a feature or codebase.

    Args:
        path: Absolute or relative path to the codebase to analyse.
        feature: Natural language description of the feature to design.
        output: Write the blueprint to this file path instead of stdout.
        local_only: Skip AAAA-Nexus enrichment; use local analysis only.
        fmt: Output format - "json" (default) or "markdown".
        timeout: Maximum seconds to wait for the command.

    Returns:
        dict with keys:
            ok (bool): True when exit_code == 0.
            exit_code (int): Raw process exit code.
            stdout (str): Captured standard output (blueprint JSON when ok=True).
            stderr (str): Captured standard error.
            blueprint (dict | None): Parsed blueprint dict when ok=True and fmt="json".
    """
    cmd = [sys.executable, "-m", "ass_ade", "design", path, "--feature", feature]
    if output:
        cmd.extend(["--output", output])
    if local_only:
        cmd.append("--local-only")
    if fmt != "json":
        cmd.extend(["--format", fmt])

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
            "stderr": f"design timed out after {timeout}s",
            "blueprint": None,
        }
    except FileNotFoundError as exc:
        return {
            "ok": False,
            "exit_code": 127,
            "stdout": "",
            "stderr": str(exc),
            "blueprint": None,
        }

    blueprint = None
    if result.returncode == 0 and fmt == "json" and result.stdout.strip():
        try:
            blueprint = json.loads(result.stdout)
        except json.JSONDecodeError:
            pass

    return {
        "ok": result.returncode == 0,
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "blueprint": blueprint,
    }
