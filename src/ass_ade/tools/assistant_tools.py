"""MCP-registered assistant tools — harvest, tasks, insights."""

from __future__ import annotations

from typing import Any

from ass_ade.tools.base import Tool, ToolResult


class HarvestTool(Tool):
    """Crawl directories to extract insights, tasks, and research notes."""

    def __init__(self, working_dir: str = ".") -> None:
        self._working_dir = working_dir

    @property
    def name(self) -> str:
        return "harvest"

    @property
    def description(self) -> str:
        return (
            "Crawl one or more directories (or the working directory) and extract research insights, "
            "action items, and TODO tasks from .md, .txt, .py, and other text files. "
            "Persists results to the local knowledge base (~/.ass-ade/assistant/). "
            "Returns a summary of docs scanned, insights found, and tasks extracted."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "paths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Directories or files to harvest. Defaults to ['.'].",
                    "default": ["."],
                },
                "extensions": {
                    "type": "string",
                    "description": "Comma-separated extensions to scan (e.g. '.md,.txt,.py').",
                    "default": ".md,.txt,.rst,.py,.ts,.js",
                },
                "max_files": {
                    "type": "integer",
                    "description": "Maximum files to scan.",
                    "default": 500,
                },
                "dry_run": {
                    "type": "boolean",
                    "description": "If true, extract but do not persist to the knowledge base.",
                    "default": False,
                },
            },
            "required": [],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        from ass_ade.a3_og_features.harvest import harvest
        paths = kwargs.get("paths") or [self._working_dir]
        ext_str = kwargs.get("extensions", ".md,.txt,.rst,.py,.ts,.js")
        ext_tuple = tuple(
            e.strip() if e.strip().startswith(".") else f".{e.strip()}"
            for e in ext_str.split(",")
        )
        max_files = int(kwargs.get("max_files", 500))
        dry_run = bool(kwargs.get("dry_run", False))
        try:
            result = harvest(paths, extensions=ext_tuple, max_files=max_files, save=not dry_run)
            return ToolResult(output=result.summary_line(), success=True)
        except Exception as exc:
            return ToolResult(output="", error=str(exc), success=False)


class AssistantStatusTool(Tool):
    """Show personal assistant status: open tasks, insights count."""

    def __init__(self, working_dir: str = ".") -> None:
        pass

    @property
    def name(self) -> str:
        return "assistant_status"

    @property
    def description(self) -> str:
        return "Return a summary of the personal assistant knowledge base: open tasks, total insights, base directory."

    @property
    def parameters(self) -> dict[str, Any]:
        return {"type": "object", "properties": {}, "required": []}

    def execute(self, **kwargs: Any) -> ToolResult:
        from ass_ade.a2_mo_composites.personal_assistant import PersonalAssistant
        import json
        try:
            pa = PersonalAssistant()
            stat = pa.status()
            return ToolResult(output=json.dumps(stat, indent=2), success=True)
        except Exception as exc:
            return ToolResult(output="", error=str(exc), success=False)


class AssistantTasksTool(Tool):
    """List extracted tasks from the knowledge base."""

    def __init__(self, working_dir: str = ".") -> None:
        pass

    @property
    def name(self) -> str:
        return "assistant_tasks"

    @property
    def description(self) -> str:
        return (
            "Return a list of action items and TODOs extracted from your files. "
            "Filter by status: open, in_progress, or done."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["open", "in_progress", "done"],
                    "description": "Filter tasks by status.",
                    "default": "open",
                },
                "limit": {"type": "integer", "default": 20},
            },
            "required": [],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        from ass_ade.a0_qk_constants.assistant_types import TaskStatus
        from ass_ade.a2_mo_composites.personal_assistant import PersonalAssistant
        import json
        status_str = kwargs.get("status", "open")
        limit = int(kwargs.get("limit", 20))
        try:
            ts = TaskStatus(status_str)
        except ValueError:
            return ToolResult(output="", error=f"Unknown status: {status_str}", success=False)
        try:
            pa = PersonalAssistant()
            tasks = pa.list_tasks(ts)[:limit]
            return ToolResult(output=json.dumps(tasks, indent=2), success=True)
        except Exception as exc:
            return ToolResult(output="", error=str(exc), success=False)


class AssistantInsightsTool(Tool):
    """Return research insights from the knowledge base."""

    def __init__(self, working_dir: str = ".") -> None:
        pass

    @property
    def name(self) -> str:
        return "assistant_insights"

    @property
    def description(self) -> str:
        return (
            "Return extracted research insights (decisions, actions, ideas, risks, questions) "
            "from the local knowledge base. Filter by tag."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "tag": {
                    "type": "string",
                    "enum": ["decision", "action", "question", "idea", "risk", ""],
                    "description": "Filter by insight tag. Empty for all.",
                    "default": "",
                },
                "limit": {"type": "integer", "default": 20},
            },
            "required": [],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        from ass_ade.a2_mo_composites.personal_assistant import PersonalAssistant
        import json
        tag = kwargs.get("tag", "") or None
        limit = int(kwargs.get("limit", 20))
        try:
            pa = PersonalAssistant()
            insights = pa.list_insights(tag)[:limit]
            return ToolResult(output=json.dumps(insights, indent=2), success=True)
        except Exception as exc:
            return ToolResult(output="", error=str(exc), success=False)
