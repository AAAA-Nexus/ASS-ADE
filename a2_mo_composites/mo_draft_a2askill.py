# Extracted from C:/!ass-ade/src/ass_ade/a2a/__init__.py:47
# Component id: mo.source.ass_ade.a2askill
from __future__ import annotations

__version__ = "0.1.0"

class A2ASkill(BaseModel):
    """A single skill advertised by an agent."""

    id: str
    name: str
    description: str = ""
    tags: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
