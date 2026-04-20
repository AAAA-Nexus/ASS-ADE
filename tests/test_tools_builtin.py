"""Tests for the ASS-ADE built-in tools."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from ass_ade.tools.builtin import (
    EditFileTool,
    GrepSearchTool,
    ListDirectoryTool,
    ReadFileTool,
    RunCommandTool,
    SearchFilesTool,
    WriteFileTool,
)
from ass_ade.tools.registry import default_registry


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    """Create a temporary workspace with sample files."""
    (tmp_path / "hello.py").write_text("print('hello world')\n", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "data.txt").write_text("line1\nline2\nline3\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Project\nSome docs.\n", encoding="utf-8")
    return tmp_path


# ── ReadFileTool ──────────────────────────────────────────────────────────────


class TestReadFile:
    def test_read_full(self, workspace: Path):
        tool = ReadFileTool(str(workspace))
        r = tool.execute(path="hello.py")
        assert r.success
        assert "hello world" in r.output

    def test_read_line_range(self, workspace: Path):
        tool = ReadFileTool(str(workspace))
        r = tool.execute(path="sub/data.txt", start_line=2, end_line=2)
        assert r.success
        assert r.output.strip() == "line2"

    def test_read_missing(self, workspace: Path):
        tool = ReadFileTool(str(workspace))
        r = tool.execute(path="nope.py")
        assert not r.success
        assert "not found" in (r.error or "").lower()


# ── WriteFileTool ─────────────────────────────────────────────────────────────


class TestWriteFile:
    def test_create_new(self, workspace: Path):
        tool = WriteFileTool(str(workspace))
        r = tool.execute(path="new.py", content="x = 1\n")
        assert r.success
        assert (workspace / "new.py").read_text() == "x = 1\n"

    def test_create_nested(self, workspace: Path):
        tool = WriteFileTool(str(workspace))
        r = tool.execute(path="a/b/c.py", content="pass\n")
        assert r.success
        assert (workspace / "a" / "b" / "c.py").exists()

    def test_reject_outside_cwd(self, workspace: Path):
        tool = WriteFileTool(str(workspace))
        # Try to escape up
        r = tool.execute(path="../escape.py", content="pwned")
        assert not r.success
        assert "outside" in (r.error or "").lower()


# ── EditFileTool ──────────────────────────────────────────────────────────────


class TestEditFile:
    def test_simple_replace(self, workspace: Path):
        tool = EditFileTool(str(workspace))
        r = tool.execute(path="hello.py", old_string="hello world", new_string="goodbye world")
        assert r.success
        assert (workspace / "hello.py").read_text() == "print('goodbye world')\n"

    def test_not_found(self, workspace: Path):
        tool = EditFileTool(str(workspace))
        r = tool.execute(path="hello.py", old_string="NOPE", new_string="X")
        assert not r.success
        assert "not found" in (r.error or "").lower()

    def test_multiple_matches(self, workspace: Path):
        (workspace / "dup.py").write_text("a\na\na\n", encoding="utf-8")
        tool = EditFileTool(str(workspace))
        r = tool.execute(path="dup.py", old_string="a", new_string="b")
        assert not r.success
        assert "3 locations" in (r.error or "")


# ── RunCommandTool ────────────────────────────────────────────────────────────


class TestRunCommand:
    def test_echo(self, workspace: Path):
        tool = RunCommandTool(str(workspace))
        r = tool.execute(command="python hello.py")
        assert r.success
        assert "hello world" in r.output

    def test_blocked_dangerous(self, workspace: Path):
        tool = RunCommandTool(str(workspace))
        r = tool.execute(command="rm -rf /")
        assert not r.success
        assert "blocked" in (r.error or "").lower()

    def test_timeout(self, workspace: Path):
        (workspace / "sleepy.py").write_text("import time\ntime.sleep(10)\n", encoding="utf-8")
        tool = RunCommandTool(str(workspace))
        r = tool.execute(command="python sleepy.py", timeout=1)
        assert not r.success
        assert "timed out" in (r.error or "").lower()


# ── ListDirectoryTool ─────────────────────────────────────────────────────────


class TestListDirectory:
    def test_list_root(self, workspace: Path):
        tool = ListDirectoryTool(str(workspace))
        r = tool.execute()
        assert r.success
        assert "hello.py" in r.output
        assert "sub/" in r.output

    def test_list_subdir(self, workspace: Path):
        tool = ListDirectoryTool(str(workspace))
        r = tool.execute(path="sub")
        assert r.success
        assert "data.txt" in r.output


# ── SearchFilesTool ───────────────────────────────────────────────────────────


class TestSearchFiles:
    def test_glob_py(self, workspace: Path):
        tool = SearchFilesTool(str(workspace))
        r = tool.execute(pattern="**/*.py")
        assert r.success
        assert "hello.py" in r.output

    def test_no_matches(self, workspace: Path):
        tool = SearchFilesTool(str(workspace))
        r = tool.execute(pattern="**/*.rs")
        assert "No matches" in r.output


# ── GrepSearchTool ────────────────────────────────────────────────────────────


class TestGrepSearch:
    def test_find_pattern(self, workspace: Path):
        tool = GrepSearchTool(str(workspace))
        r = tool.execute(pattern="hello")
        assert r.success
        assert "hello.py" in r.output

    def test_no_matches(self, workspace: Path):
        tool = GrepSearchTool(str(workspace))
        r = tool.execute(pattern="ZZZZZ_NOTHING")
        assert "No matches" in r.output

    def test_invalid_regex(self, workspace: Path):
        tool = GrepSearchTool(str(workspace))
        r = tool.execute(pattern="[invalid")
        assert not r.success
        assert "Invalid regex" in (r.error or "")


# ── ToolRegistry ──────────────────────────────────────────────────────────────


class TestRegistry:
    def test_default_registry_has_all_tools(self, workspace: Path):
        reg = default_registry(str(workspace))
        names = reg.list_tools()
        assert "read_file" in names
        assert "write_file" in names
        assert "edit_file" in names
        assert "run_command" in names
        assert "list_directory" in names
        assert "search_files" in names
        assert "grep_search" in names

    def test_execute_unknown(self, workspace: Path):
        reg = default_registry(str(workspace))
        r = reg.execute("no_such_tool")
        assert not r.success
        assert "Unknown tool" in (r.error or "")

    def test_schemas(self, workspace: Path):
        reg = default_registry(str(workspace))
        schemas = reg.schemas()
        assert len(schemas) == len(reg.list_tools())
        assert all(s.name for s in schemas)

    def test_loads_generated_tool_from_runtime_surface(self, workspace: Path):
        generated = workspace / "src" / "ass_ade" / "tools" / "generated"
        generated.mkdir(parents=True)
        (generated / "demo_generated.py").write_text(
            """\
from __future__ import annotations

from typing import Any

from ass_ade.tools.base import ToolResult


class DemoGeneratedTool:
    def __init__(self, working_dir: str = ".") -> None:
        self.working_dir = working_dir

    @property
    def name(self) -> str:
        return "demo_generated"

    @property
    def description(self) -> str:
        return "Generated tool loaded at runtime."

    @property
    def parameters(self) -> dict[str, Any]:
        return {"type": "object", "properties": {}}

    def execute(self, **kwargs: Any) -> ToolResult:
        return ToolResult(output=f"generated:{self.working_dir}")
""",
            encoding="utf-8",
        )

        reg = default_registry(str(workspace))
        result = reg.execute("demo_generated")

        assert "demo_generated" in reg.list_tools()
        assert result.success
        assert f"generated:{workspace}" in result.output

    def test_loads_asset_memory_tool_from_nested_working_dir(self, workspace: Path):
        generated = workspace / "src" / "ass_ade" / "tools" / "generated"
        generated.mkdir(parents=True)
        tool_path = generated / "asset_memory_tool.py"
        tool_path.write_text(
            """\
from __future__ import annotations

from typing import Any

from ass_ade.tools.base import ToolResult


class AssetMemoryTool:
    @property
    def name(self) -> str:
        return "asset_memory_tool"

    @property
    def description(self) -> str:
        return "Tool advertised through .ass-ade asset memory."

    @property
    def parameters(self) -> dict[str, Any]:
        return {"type": "object", "properties": {}}

    def execute(self, **kwargs: Any) -> ToolResult:
        return ToolResult(output="asset-memory-loaded")
""",
            encoding="utf-8",
        )
        ass_ade = workspace / ".ass-ade"
        ass_ade.mkdir()
        (ass_ade / "assets.json").write_text(
            json.dumps(
                {
                    "assets": [
                        {
                            "type": "tools",
                            "name": "asset_memory_tool",
                            "path": "src/ass_ade/tools/generated/asset_memory_tool.py",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        nested = workspace / "a4_sy_orchestration" / "nested"
        nested.mkdir(parents=True)

        reg = default_registry(str(nested))
        result = reg.execute("asset_memory_tool")

        assert "asset_memory_tool" in reg.list_tools()
        assert result.success
        assert result.output == "asset-memory-loaded"
