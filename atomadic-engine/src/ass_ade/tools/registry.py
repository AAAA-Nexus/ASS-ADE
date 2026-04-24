"""Tool registry — discovers and manages tools."""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
from typing import Any

from ass_ade.engine.types import ToolSchema
from ass_ade.tools.base import Tool, ToolResult


class ToolRegistry:
    """Registry of available tools."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[str]:
        return sorted(self._tools)

    def schemas(self) -> list[ToolSchema]:
        return [
            ToolSchema(
                name=t.name,
                description=t.description,
                parameters=t.parameters,
            )
            for t in self._tools.values()
        ]

    def execute(self, name: str, **kwargs: Any) -> ToolResult:
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(output="", error=f"Unknown tool: {name}", success=False)
        try:
            return tool.execute(**kwargs)
        except (
            AttributeError,
            LookupError,
            OSError,
            RuntimeError,
            TypeError,
            ValueError,
        ) as exc:
            return ToolResult(output="", error=str(exc), success=False)


_ROOT_SURFACE_DIRS = (
    "agents",
    "skills",
    "hooks",
    "tools",
    "mcp",
    "prompts",
    "instructions",
    "harnesses",
    "blueprints",
    "docs",
)

_ROOT_MONADIC_DIRS = (
    "qk",
    "at",
    "mo",
    "og",
    "sy",
    "a0_qk_constants",
    "a1_at_functions",
    "a2_mo_composites",
    "a3_og_features",
    "a4_sy_orchestration",
)


def _root_score(candidate: Path) -> int:
    score = 0
    if (candidate / ".git").exists():
        score += 5
    if (candidate / "pyproject.toml").exists():
        score += 4
    if (candidate / "src" / "ass_ade").is_dir():
        score += 4
    if (candidate / ".ass-ade").is_dir():
        score += 3
    score += sum(1 for name in _ROOT_SURFACE_DIRS if (candidate / name).is_dir())
    score += sum(1 for name in _ROOT_MONADIC_DIRS if (candidate / name).is_dir())
    return score


def _repo_root_from_working_dir(working_dir: str | Path) -> Path:
    cwd = Path(working_dir).resolve()
    best = cwd
    best_score = _root_score(cwd)
    for candidate in (cwd, *cwd.parents):
        score = _root_score(candidate)
        if score > best_score:
            best = candidate
            best_score = score
    return best


def _load_json_file(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _normalize_capability_type(value: Any) -> str:
    normalized = str(value or "").strip().lower().replace("-", "_")
    aliases = {
        "tool": "tools",
        "tools": "tools",
        "local_tool": "tools",
        "generated_tool": "tools",
    }
    return aliases.get(normalized, normalized)


def _resolve_repo_path(raw_path: Any, *, root: Path, cwd: Path) -> Path | None:
    if not isinstance(raw_path, str) or not raw_path.strip():
        return None
    path = Path(raw_path)
    if path.is_absolute():
        return path.resolve()
    root_candidate = (root / path).resolve()
    if root_candidate.exists():
        return root_candidate
    cwd_candidate = (cwd / path).resolve()
    if cwd_candidate.exists():
        return cwd_candidate
    return root_candidate


def _iter_asset_tool_paths(root: Path, cwd: Path) -> list[Path]:
    paths: list[Path] = []
    data = _load_json_file(root / ".ass-ade" / "assets.json")
    records: Any = []
    if isinstance(data, dict):
        records = data.get("assets", [])
    elif isinstance(data, list):
        records = data
    if not isinstance(records, list):
        return paths

    for record in records:
        if not isinstance(record, dict):
            continue
        if str(record.get("status", "active")).lower() in {"retired", "rejected"}:
            continue
        cap_type = _normalize_capability_type(
            record.get("type_key")
            or record.get("type")
            or record.get("kind")
            or record.get("category")
        )
        if cap_type != "tools":
            continue
        path = _resolve_repo_path(
            record.get("path") or record.get("repo_asset_path"),
            root=root,
            cwd=cwd,
        )
        if path is not None and path.suffix == ".py":
            paths.append(path)
    return paths


def _iter_manifest_tool_paths(root: Path, cwd: Path) -> list[Path]:
    generated_root = root / ".ass-ade" / "capability-development" / "generated"
    if not generated_root.is_dir():
        return []

    paths: list[Path] = []
    for manifest_path in sorted(generated_root.glob("*/manifest.json")):
        data = _load_json_file(manifest_path)
        if not isinstance(data, dict):
            continue
        capability = data.get("capability", {})
        cap_type = ""
        if isinstance(capability, dict):
            cap_type = _normalize_capability_type(
                capability.get("type_key")
                or capability.get("type")
                or capability.get("kind")
            )
        if cap_type and cap_type != "tools":
            continue
        path = _resolve_repo_path(data.get("repo_asset_path"), root=root, cwd=cwd)
        if path is not None and path.suffix == ".py":
            paths.append(path)
    return paths


def _generated_tool_paths(working_dir: str) -> list[Path]:
    cwd = Path(working_dir).resolve()
    root = _repo_root_from_working_dir(cwd)
    generated_dirs = [
        cwd / "src" / "ass_ade" / "tools" / "generated",
        root / "src" / "ass_ade" / "tools" / "generated",
        root / "tools" / "generated",
        root / ".ass-ade" / "tools" / "generated",
    ]

    paths: list[Path] = []
    for directory in generated_dirs:
        if directory.is_dir():
            paths.extend(path for path in sorted(directory.glob("*.py")))
    paths.extend(_iter_asset_tool_paths(root, cwd))
    paths.extend(_iter_manifest_tool_paths(root, cwd))

    unique: dict[str, Path] = {}
    for path in paths:
        if path.name == "__init__.py":
            continue
        try:
            resolved = path.resolve()
        except OSError:
            continue
        if resolved.is_file():
            unique[str(resolved).lower()] = resolved
    return sorted(unique.values(), key=lambda item: item.as_posix().lower())


def _module_name_for_path(path: Path) -> str:
    digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:12]
    return f"ass_ade_generated_tool_{path.stem}_{digest}"


def _instantiate_tool(candidate: type[Any], working_dir: str) -> Tool | None:
    for args, kwargs in (
        ((), {"working_dir": working_dir}),
        ((working_dir,), {}),
        ((), {}),
    ):
        try:
            tool = candidate(*args, **kwargs)
        except (AttributeError, OSError, RuntimeError, TypeError, ValueError):
            continue
        if isinstance(tool, Tool):
            return tool
    return None


def _register_generated_tools(registry: ToolRegistry, working_dir: str) -> None:
    for path in _generated_tool_paths(working_dir):
        try:
            spec = importlib.util.spec_from_file_location(
                _module_name_for_path(path), path
            )
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception:
            continue
        for _, candidate in inspect.getmembers(module, inspect.isclass):
            if candidate.__module__ != module.__name__:
                continue
            if not candidate.__name__.lower().endswith("tool"):
                continue
            tool = _instantiate_tool(candidate, working_dir)
            if tool is None:
                continue
            registry.register(tool)
            break


def default_registry(working_dir: str | None = None) -> ToolRegistry:
    """Create a registry pre-loaded with all built-in tools."""
    from ass_ade.tools.builtin import (
        EditFileTool,
        GrepSearchTool,
        ListDirectoryTool,
        ReadFileTool,
        RunCommandTool,
        SearchFilesTool,
        UndoEditTool,
        WriteFileTool,
    )
    from ass_ade.tools.history import FileHistory
    from ass_ade.tools.prompt import (
        PromptDiffTool,
        PromptHashTool,
        PromptProposeTool,
        PromptSectionTool,
        PromptValidateTool,
    )

    cwd = working_dir or "."

    # Initialize file history for undo support
    history = FileHistory(cwd)

    registry = ToolRegistry()
    registry.register(ReadFileTool(cwd))
    registry.register(WriteFileTool(cwd, history=history))
    registry.register(EditFileTool(cwd, history=history))
    registry.register(RunCommandTool(cwd))
    registry.register(ListDirectoryTool(cwd))
    registry.register(SearchFilesTool(cwd))
    registry.register(GrepSearchTool(cwd))
    registry.register(UndoEditTool(cwd, history=history))
    registry.register(PromptHashTool(cwd))
    registry.register(PromptValidateTool(cwd))
    registry.register(PromptSectionTool(cwd))
    registry.register(PromptDiffTool(cwd))
    registry.register(PromptProposeTool(cwd))
    _register_generated_tools(registry, cwd)
    return registry
