from __future__ import annotations

import subprocess
from dataclasses import dataclass
from shutil import which


@dataclass(frozen=True)
class ToolStatus:
    name: str
    available: bool
    version: str | None = None
    error: str | None = None


DEFAULT_TOOLS = ("python", "py", "git", "node", "npm", "cargo", "rustc", "uv")


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


def collect_tool_status(tools: tuple[str, ...] = DEFAULT_TOOLS) -> list[ToolStatus]:
    return [detect_tool(tool) for tool in tools]
