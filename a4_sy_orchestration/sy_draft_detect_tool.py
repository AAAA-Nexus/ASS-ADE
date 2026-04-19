# Extracted from C:/!ass-ade/src/ass_ade/system.py:19
# Component id: sy.source.ass_ade.detect_tool
from __future__ import annotations

__version__ = "0.1.0"

def detect_tool(name: str) -> ToolStatus:
    executable = which(name)
    if executable is None:
        return ToolStatus(name=name, available=False, error="not found")

    try:
        result = subprocess.run(
            [executable, "--version"],
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
