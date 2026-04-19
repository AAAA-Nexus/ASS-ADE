# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_inventionstub.py:7
# Component id: mo.source.a2_mo_composites.inventionstub
from __future__ import annotations

__version__ = "0.1.0"

class InventionStub(BaseModel):
    """A generated placeholder module for a missing capability."""
    capability_name: str
    stub_path: str
    spec_summary: str
    verification_criteria: list[str] = Field(default_factory=list)
