"""Prompt artifact tools for ASS-ADE."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ass_ade.prompt_toolkit import (
    prompt_diff,
    prompt_hash,
    prompt_propose,
    prompt_section,
    prompt_validate,
)
from ass_ade.tools.base import ToolResult


class _PromptToolBase:
    def __init__(self, working_dir: str = ".") -> None:
        self._cwd = Path(working_dir).resolve()

    def _json(self, payload: Any) -> ToolResult:
        if hasattr(payload, "model_dump"):
            payload = payload.model_dump()
        return ToolResult(output=json.dumps(payload, indent=2))


class PromptHashTool(_PromptToolBase):
    @property
    def name(self) -> str:
        return "prompt_hash"

    @property
    def description(self) -> str:
        return "Return SHA-256 metadata for an explicit prompt file or prompt text."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt_path": {"type": "string", "description": "Repo-relative prompt file."},
                "prompt_text": {"type": "string", "description": "Inline prompt text."},
            },
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        return self._json(prompt_hash(working_dir=self._cwd, **kwargs))


class PromptValidateTool(_PromptToolBase):
    @property
    def name(self) -> str:
        return "prompt_validate"

    @property
    def description(self) -> str:
        return "Validate an explicit prompt artifact against a JSON hash manifest."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "manifest_path": {"type": "string", "description": "Repo-relative JSON manifest."},
                "prompt_path": {"type": "string", "description": "Repo-relative prompt file."},
                "prompt_text": {"type": "string", "description": "Inline prompt text."},
                "prompt_name": {"type": "string", "description": "Optional manifest prompt entry name."},
            },
            "required": ["manifest_path"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        return self._json(prompt_validate(working_dir=self._cwd, **kwargs))


class PromptSectionTool(_PromptToolBase):
    @property
    def name(self) -> str:
        return "prompt_section"

    @property
    def description(self) -> str:
        return "Extract a Markdown heading or XML tag section from an explicit prompt artifact."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "section": {"type": "string", "description": "Section title or XML tag name."},
                "prompt_path": {"type": "string", "description": "Repo-relative prompt file."},
                "prompt_text": {"type": "string", "description": "Inline prompt text."},
            },
            "required": ["section"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        return self._json(prompt_section(working_dir=self._cwd, **kwargs))


class PromptDiffTool(_PromptToolBase):
    @property
    def name(self) -> str:
        return "prompt_diff"

    @property
    def description(self) -> str:
        return "Compare an explicit prompt artifact to a baseline and return a redacted diff."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "baseline_path": {"type": "string", "description": "Repo-relative baseline file."},
                "prompt_path": {"type": "string", "description": "Repo-relative current prompt file."},
                "prompt_text": {"type": "string", "description": "Inline current prompt text."},
                "redacted": {"type": "boolean", "description": "Redact secrets in diff."},
                "max_lines": {"type": "integer", "description": "Maximum diff lines to return."},
            },
            "required": ["baseline_path"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        return self._json(prompt_diff(working_dir=self._cwd, **kwargs))


class PromptProposeTool(_PromptToolBase):
    @property
    def name(self) -> str:
        return "prompt_propose"

    @property
    def description(self) -> str:
        return "Create a prompt self-improvement proposal for an explicit prompt artifact."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "objective": {"type": "string", "description": "Improvement objective."},
                "prompt_path": {"type": "string", "description": "Repo-relative prompt file."},
                "prompt_text": {"type": "string", "description": "Inline prompt text."},
            },
            "required": ["objective"],
        }

    def execute(self, **kwargs: Any) -> ToolResult:
        return self._json(prompt_propose(working_dir=self._cwd, **kwargs))
