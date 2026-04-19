# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_a2askill.py:7
# Component id: mo.source.a2_mo_composites.a2askill
from __future__ import annotations

__version__ = "0.1.0"

class A2ASkill(BaseModel):
    """A single skill advertised by an agent."""

    id: str
    name: str
    description: str = ""
    tags: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
