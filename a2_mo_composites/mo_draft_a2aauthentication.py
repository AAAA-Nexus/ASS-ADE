# Extracted from C:/!ass-ade/src/ass_ade/a2a/__init__.py:57
# Component id: mo.source.ass_ade.a2aauthentication
from __future__ import annotations

__version__ = "0.1.0"

class A2AAuthentication(BaseModel):
    """Authentication requirements for the agent."""

    schemes: list[str] = Field(default_factory=list)  # e.g. ["bearer", "x402"]
    credentials: str | None = None  # human-readable note
