"""Built-in tools for the ASS-ADE agentic IDE.

These tools give the agent full file-system and shell access within the
working directory, mirroring the capabilities of Claude Code, Cursor,
and similar agentic IDEs.

File mutations (write_file, edit_file) are automatically recorded in the
undo history, so each edit can be reverted via the undo_edit tool.
"""

from __future__ import annotations

import difflib
import os
import re
import shlex
import subprocess
from pathlib import Path
from typing import Any

from ass_ade.tools.base import ToolResult
from ass_ade.tools.history import FileHistory

_MAX_FILE_OUTPUT = 100_000
_MAX_CMD_OUTPUT = 50_000
_MAX_GLOB_RESULTS = 200
_MAX_GREP_MATCHES = 100
_MAX_DIR_ENTRIES = 500
_SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".tox", ".mypy_cache"}

# Allowlist for run_command — only these executables may be invoked.
_ALLOWED_COMMANDS = {
    "cargo", "git", "go", "make", "mypy", "node", "npm", "npx", "pip",
    "python", "python3", "py", "pytest", "ruff", "tsc", "uv", "yarn",
}


def _resolve(cwd: Path, path: str) -> Path:
    p = Path(path)
    if p.is_absolute():
        return p
    return (cwd / p).resolve()


# ══════════════════════════════════════════════════════════════════════════════
# read_file
# ══════════════════════════════════════════════════════════════════════════════


class ReadFileTool:
    """Read file contents, optionally a specific line range."""

    def __init__(self, working_dir: str = ".") -> None:
        self._cwd = Path(working_dir).resolve()

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Read the contents of a file. Use start_line/end_line for partial reads (1-based, inclusive)."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path relative to the working directory."},
                "start_line": {"type": "integer", "description": "First line to read (1-based). Omit for full file."},
                "end_line": {"type": "integer", "description": "Last line to read (1-based, inclusive)."},
            },
            "required": ["path"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        path = _resolve(self._cwd, kwargs["path"])
        try:
            path.relative_to(self._cwd)
        except ValueError:
            return ToolResult(error="Cannot read files outside the working directory.", success=False)
        if not path.is_file():
            return ToolResult(error=f"File not found: {kwargs['path']}", success=False)

        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines(keepends=True)

        start = kwargs.get("start_line")
        end = kwargs.get("end_line")
        if start is not None:
            start = max(1, int(start)) - 1
            end = int(end) if end else len(lines)
            lines = lines[start:end]

        content = "".join(lines)
        if len(content) > _MAX_FILE_OUTPUT:
            content = content[:_MAX_FILE_OUTPUT] + "\n... [truncated at 100KB]"
        return ToolResult(output=content)


# ══════════════════════════════════════════════════════════════════════════════
# write_file
# ══════════════════════════════════════════════════════════════════════════════


class WriteFileTool:
    """Create a new file or overwrite an existing file."""

    def __init__(self, working_dir: str = ".", history: FileHistory | None = None) -> None:
        self._cwd = Path(working_dir).resolve()
        self._history = history

    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "Create a new file or overwrite an existing file with the given content."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path relative to the working directory."},
                "content": {"type": "string", "description": "Full content to write."},
            },
            "required": ["path", "content"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        path = _resolve(self._cwd, kwargs["path"])
        content = kwargs["content"]

        try:
            path.relative_to(self._cwd)
        except ValueError:
            return ToolResult(error="Cannot write outside the working directory.", success=False)

        # Record undo snapshot if file exists
        if path.is_file() and self._history:
            rel = str(path.relative_to(self._cwd))
            self._history.record(rel, path.read_text(encoding="utf-8"))

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return ToolResult(output=f"Wrote {len(content)} bytes to {kwargs['path']}")


# ══════════════════════════════════════════════════════════════════════════════
# edit_file
# ══════════════════════════════════════════════════════════════════════════════


class EditFileTool:
    """Search-and-replace edit in a file.

    The ``old_string`` must match exactly one location in the file.
    """

    def __init__(self, working_dir: str = ".", history: FileHistory | None = None) -> None:
        self._cwd = Path(working_dir).resolve()
        self._history = history

    @property
    def name(self) -> str:
        return "edit_file"

    @property
    def description(self) -> str:
        return (
            "Edit a file by replacing exact text. The old_string must match exactly "
            "one location. Include enough context (3+ surrounding lines) to be unique."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path relative to the working directory."},
                "old_string": {"type": "string", "description": "Exact text to find (must appear exactly once)."},
                "new_string": {"type": "string", "description": "Replacement text."},
                "preview": {"type": "boolean", "description": "If true, return diff without applying. Default: false."},
            },
            "required": ["path", "old_string", "new_string"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        path = _resolve(self._cwd, kwargs["path"])
        try:
            path.relative_to(self._cwd)
        except ValueError:
            return ToolResult(error="Cannot edit files outside the working directory.", success=False)
        if not path.is_file():
            return ToolResult(error=f"File not found: {kwargs['path']}", success=False)

        old_string = kwargs["old_string"]
        new_string = kwargs["new_string"]
        preview = kwargs.get("preview", False)

        text = path.read_text(encoding="utf-8")
        count = text.count(old_string)

        if count == 0:
            return ToolResult(error="old_string not found in file.", success=False)
        if count > 1:
            return ToolResult(
                error=f"old_string matches {count} locations. Add more context to be unique.",
                success=False,
            )

        new_text = text.replace(old_string, new_string, 1)

        # Generate unified diff
        diff = difflib.unified_diff(
            text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f"a/{kwargs['path']}",
            tofile=f"b/{kwargs['path']}",
        )
        diff_str = "".join(diff)

        if preview:
            return ToolResult(output=diff_str or "(no changes)")

        # Record undo snapshot before mutation
        if self._history:
            rel = str(path.relative_to(self._cwd))
            self._history.record(rel, text)

        path.write_text(new_text, encoding="utf-8")
        return ToolResult(output=f"Applied edit to {kwargs['path']}\n\n{diff_str}")


# ══════════════════════════════════════════════════════════════════════════════
# run_command
# ══════════════════════════════════════════════════════════════════════════════


class RunCommandTool:
    """Execute a shell command in the working directory."""

    def __init__(self, working_dir: str = ".") -> None:
        self._cwd = Path(working_dir).resolve()

    @property
    def name(self) -> str:
        return "run_command"

    @property
    def description(self) -> str:
        return (
            "Execute a shell command and return stdout/stderr. Only a fixed allowlist "
            "of executables is permitted; shell metacharacters are not interpreted "
            "(shell=False). Inline interpreters are blocked by default (python -c, "
            "node -e) — use script files in the workspace. Override for local debugging "
            "only: ASS_ADE_ALLOW_INLINE_RUN_COMMAND=1."
        )

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

        if "\x00" in command or "\n" in command or "\r" in command:
            # NUL breaks argument parsing; embedded newlines are almost never legitimate
            # single-line IDE commands and are a common injection shape.
            return ToolResult(
                error="Command blocked: NUL or multiline shell command is not allowed.",
                success=False,
            )

        if os.environ.get("ASS_ADE_ALLOW_INLINE_RUN_COMMAND") != "1":
            if executable_stem in {"python", "python3", "py"} and "-c" in parts:
                return ToolResult(
                    error=(
                        "Command blocked: inline `python -c` is disabled for MCP "
                        "`run_command` (arbitrary code execution). Add a .py file in the "
                        "workspace and run `python thatfile.py`, or set "
                        "ASS_ADE_ALLOW_INLINE_RUN_COMMAND=1 for local debugging only."
                    ),
                    success=False,
                )
            if executable_stem == "node" and ("-e" in parts or "--eval" in parts):
                return ToolResult(
                    error=(
                        "Command blocked: `node -e` / `--eval` is disabled for MCP "
                        "`run_command`. Use a workspace script file, or set "
                        "ASS_ADE_ALLOW_INLINE_RUN_COMMAND=1 for local debugging only."
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


# ══════════════════════════════════════════════════════════════════════════════
# list_directory
# ══════════════════════════════════════════════════════════════════════════════


class ListDirectoryTool:
    """List files and directories."""

    def __init__(self, working_dir: str = ".") -> None:
        self._cwd = Path(working_dir).resolve()

    @property
    def name(self) -> str:
        return "list_directory"

    @property
    def description(self) -> str:
        return "List files and directories. Entries ending with / are directories."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory path (default: working directory).",
                },
            },
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        path = _resolve(self._cwd, kwargs.get("path", "."))
        try:
            path.relative_to(self._cwd)
        except ValueError:
            return ToolResult(error="Cannot list directories outside the working directory.", success=False)
        if not path.is_dir():
            return ToolResult(error=f"Not a directory: {kwargs.get('path', '.')}", success=False)

        entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        lines: list[str] = []
        for entry in entries[:_MAX_DIR_ENTRIES]:
            suffix = "/" if entry.is_dir() else ""
            lines.append(f"{entry.name}{suffix}")

        if len(entries) > _MAX_DIR_ENTRIES:
            lines.append(f"... and {len(entries) - _MAX_DIR_ENTRIES} more entries")

        return ToolResult(output="\n".join(lines))


# ══════════════════════════════════════════════════════════════════════════════
# search_files
# ══════════════════════════════════════════════════════════════════════════════


class SearchFilesTool:
    """Find files matching a glob pattern."""

    def __init__(self, working_dir: str = ".") -> None:
        self._cwd = Path(working_dir).resolve()

    @property
    def name(self) -> str:
        return "search_files"

    @property
    def description(self) -> str:
        return "Find files matching a glob pattern (e.g., '**/*.py', 'src/**/*.ts')."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Glob pattern to match files."},
            },
            "required": ["pattern"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        pattern = kwargs["pattern"]
        matches = sorted(self._cwd.glob(pattern))

        filtered = [
            m
            for m in matches
            if m.is_file()
            and not any(p in _SKIP_DIRS for p in m.relative_to(self._cwd).parts)
        ]

        if not filtered:
            return ToolResult(output="No matches found.")

        lines = [str(m.relative_to(self._cwd)) for m in filtered[:_MAX_GLOB_RESULTS]]
        if len(filtered) > _MAX_GLOB_RESULTS:
            lines.append(f"... and {len(filtered) - _MAX_GLOB_RESULTS} more matches")

        return ToolResult(output="\n".join(lines))


# ══════════════════════════════════════════════════════════════════════════════
# grep_search
# ══════════════════════════════════════════════════════════════════════════════


class GrepSearchTool:
    """Search file contents by regex pattern."""

    def __init__(self, working_dir: str = ".") -> None:
        self._cwd = Path(working_dir).resolve()

    @property
    def name(self) -> str:
        return "grep_search"

    @property
    def description(self) -> str:
        return "Search file contents for a regex pattern. Returns matching lines with file:line: prefix."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Regex pattern (case-insensitive)."},
                "include": {
                    "type": "string",
                    "description": "Glob to filter files (e.g., '**/*.py'). Default: all files.",
                },
            },
            "required": ["pattern"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        pattern_str = kwargs["pattern"]
        include = kwargs.get("include", "**/*")

        try:
            pattern = re.compile(pattern_str, re.IGNORECASE)
        except re.error as exc:
            return ToolResult(error=f"Invalid regex: {exc}", success=False)

        results: list[str] = []
        for filepath in sorted(self._cwd.glob(include)):
            if not filepath.is_file():
                continue
            parts = filepath.relative_to(self._cwd).parts
            if any(p in _SKIP_DIRS for p in parts):
                continue

            try:
                text = filepath.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue

            rel = str(filepath.relative_to(self._cwd))
            for i, line in enumerate(text.splitlines(), 1):
                if pattern.search(line):
                    results.append(f"{rel}:{i}: {line.rstrip()}")
                    if len(results) >= _MAX_GREP_MATCHES:
                        results.append("... [truncated at 100 matches]")
                        return ToolResult(output="\n".join(results))

        if not results:
            return ToolResult(output="No matches found.")
        return ToolResult(output="\n".join(results))


# ══════════════════════════════════════════════════════════════════════════════
# undo_edit
# ══════════════════════════════════════════════════════════════════════════════


class UndoEditTool:
    """Undo the last edit to a file, restoring its previous content."""

    def __init__(self, working_dir: str = ".", history: FileHistory | None = None) -> None:
        self._cwd = Path(working_dir).resolve()
        self._history = history

    @property
    def name(self) -> str:
        return "undo_edit"

    @property
    def description(self) -> str:
        return (
            "Undo the last write_file or edit_file operation on a file, "
            "restoring it to its previous content. Supports multiple undo steps."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path (relative to working directory) to undo.",
                },
            },
            "required": ["path"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        if self._history is None:
            return ToolResult(error="Undo history not available.", success=False)

        path_str = kwargs["path"]
        # Normalize to relative path
        resolved = _resolve(self._cwd, path_str)
        try:
            rel = str(resolved.relative_to(self._cwd))
        except ValueError:
            rel = path_str

        depth = self._history.depth(rel)
        if depth == 0:
            return ToolResult(error=f"No undo history for {path_str}", success=False)

        snap = self._history.undo(rel)
        if snap is None:
            return ToolResult(error=f"Failed to undo {path_str}", success=False)

        remaining = self._history.depth(rel)
        return ToolResult(
            output=f"Restored {path_str} to snapshot #{snap.sequence} ({remaining} undo steps remaining)"
        )
