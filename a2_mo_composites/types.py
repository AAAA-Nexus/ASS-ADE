"""Core type system for the ASS-ADE multi-model engine."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ToolCallRequest(BaseModel):
    """A tool invocation requested by a model."""

    id: str
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class Message(BaseModel):
    """A single message in a conversation."""

    role: str  # "system" | "user" | "assistant" | "tool"
    content: str = ""
    tool_calls: list[ToolCallRequest] = Field(default_factory=list)
    tool_call_id: str | None = None
    name: str | None = None


class ToolSchema(BaseModel):
    """Describes a tool the model may invoke."""

    name: str
    description: str
    parameters: dict[str, Any]


class CompletionRequest(BaseModel):
    """Model completion request."""

    messages: list[Message]
    tools: list[ToolSchema] = Field(default_factory=list)
    temperature: float = 0.0
    max_tokens: int = 4096
    model: str | None = None


class CompletionResponse(BaseModel):
    """Model completion response."""

    message: Message
    model: str | None = None
    finish_reason: str | None = None  # "stop" | "tool_calls" | "length"
    usage: dict[str, int] | None = None
