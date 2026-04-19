# Extracted from C:/!ass-ade/src/ass_ade/map_terrain.py:1171
# Component id: mo.source.ass_ade.inventionstub
from __future__ import annotations

__version__ = "0.1.0"

class InventionStub(BaseModel):
    """A generated implementation packet for a missing capability."""

    capability_name: str
    stub_path: str
    spec_summary: str
    verification_criteria: list[str] = Field(default_factory=list)
