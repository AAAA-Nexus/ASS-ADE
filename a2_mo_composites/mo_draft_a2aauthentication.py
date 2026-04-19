# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_a2aauthentication.py:7
# Component id: mo.source.a2_mo_composites.a2aauthentication
from __future__ import annotations

__version__ = "0.1.0"

class A2AAuthentication(BaseModel):
    """Authentication requirements for the agent."""

    schemes: list[str] = Field(default_factory=list)  # e.g. ["bearer", "x402"]
    credentials: str | None = None  # human-readable note
