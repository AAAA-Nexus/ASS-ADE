# Extracted from C:/!ass-ade/src/ass_ade/a2a/__init__.py:112
# Component id: mo.source.ass_ade.validationissue
from __future__ import annotations

__version__ = "0.1.0"

class ValidationIssue:
    """A single validation finding."""

    severity: str  # "error" | "warning" | "info"
    field: str
    message: str
