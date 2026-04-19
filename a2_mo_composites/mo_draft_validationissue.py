# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_validationissue.py:7
# Component id: mo.source.a2_mo_composites.validationissue
from __future__ import annotations

__version__ = "0.1.0"

class ValidationIssue:
    """A single validation finding."""

    severity: str  # "error" | "warning" | "info"
    field: str
    message: str
