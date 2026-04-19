# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_starterkit.py:7
# Component id: mo.source.a2_mo_composites.starterkit
from __future__ import annotations

__version__ = "0.1.0"

class StarterKit(NexusModel):
    """/v1/dev/starter — DEV-601"""
    project_name: str | None = None
    files: dict | None = None
    x402_wired: bool | None = None
