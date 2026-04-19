# Extracted from C:/!ass-ade/src/ass_ade/tools/builtin.py:241
# Component id: mo.source.ass_ade.runcommandtool
from __future__ import annotations

__version__ = "0.1.0"

class RunCommandTool:
    """Execute a shell command in the working directory."""

    def __init__(self, working_dir: str = ".") -> None:
        self._cwd = Path(working_dir).resolve()

    @property
    def name(self) -> str:
        return "run_command"

    @property
    def description(self) -> str:
        return "Execute a shell command and return stdout/stderr. Use for running tests, builds, linters, etc."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command to execute."},
                "timeout": {"type": "integer", "description": "Timeout in seconds (default 30, max 120)."},
            },
            "required": ["command"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        command = kwargs["command"]
        timeout = min(int(kwargs.get("timeout", 30)), 120)

        try:
            parts = shlex.split(command)
        except ValueError as exc:
            return ToolResult(error=f"Invalid command syntax: {exc}", success=False)

        if not parts:
            return ToolResult(error="Empty command.", success=False)

        executable = parts[0].lower()
        # Strip path prefix so "C:\\Python\\python.exe" → "python.exe" → "python"
        executable_stem = re.split(r"[\\/]", executable)[-1]
        executable_stem = re.sub(r"\.(exe|cmd|bat)$", "", executable_stem)
        if executable_stem not in _ALLOWED_COMMANDS:
            return ToolResult(
                error=(
                    f"Command blocked: '{parts[0]}' is not in the allowed list. "
                    f"Allowed: {', '.join(sorted(_ALLOWED_COMMANDS))}"
                ),
                success=False,
            )

        try:
            result = subprocess.run(
                parts,
                shell=False,
                cwd=str(self._cwd),
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return ToolResult(error=f"Command timed out after {timeout}s.", success=False)
        except OSError as exc:
            return ToolResult(error=str(exc), success=False)

        output_parts: list[str] = []
        if result.stdout:
            output_parts.append(result.stdout)
        if result.stderr:
            output_parts.append(f"[stderr]\n{result.stderr}")

        output = "\n".join(output_parts) or "(no output)"
        if len(output) > _MAX_CMD_OUTPUT:
            output = output[:_MAX_CMD_OUTPUT] + "\n... [truncated at 50KB]"

        return ToolResult(
            output=f"[exit code: {result.returncode}]\n{output}",
            success=result.returncode == 0,
        )
