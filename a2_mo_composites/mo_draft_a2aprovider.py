# Extracted from C:/!ass-ade/src/ass_ade/a2a/__init__.py:64
# Component id: mo.source.ass_ade.a2aprovider
from __future__ import annotations

__version__ = "0.1.0"

class A2AProvider(BaseModel):
    """Organization or individual providing the agent."""

    organization: str = ""
    url: str = ""
