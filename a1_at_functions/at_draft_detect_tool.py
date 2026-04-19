# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_detect_tool.py:7
# Component id: at.source.a1_at_functions.detect_tool
from __future__ import annotations

__version__ = "0.1.0"

def detect_tool(name: str) -> ToolStatus:
    if which(name) is None:
        return ToolStatus(name=name, available=False, error="not found")

    try:
        result = subprocess.run(
            [name, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return ToolStatus(name=name, available=False, error=str(exc))

    version_line = (result.stdout or result.stderr).strip().splitlines()
    if result.returncode != 0:
        error = version_line[0] if version_line else f"exit code {result.returncode}"
        return ToolStatus(name=name, available=False, error=error)

    version = version_line[0] if version_line else "available"
    return ToolStatus(name=name, available=True, version=version)
