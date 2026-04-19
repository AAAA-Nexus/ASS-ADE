"""Base types for the ASS-ADE tool system."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel


class ToolResult(BaseModel):
    """Result of a tool execution."""

    output: str = ""
    error: str | None = None
    success: bool = True


@runtime_checkable
class Tool(Protocol):
    """Protocol for ASS-ADE tools."""

    @property
    def name(self) -> str: ...

    @property
    def description(self) -> str: ...

    @property
    def parameters(self) -> dict[str, Any]: ...

    def execute(self, **kwargs: Any) -> ToolResult: ...
