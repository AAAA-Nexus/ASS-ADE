# Extracted from C:/!ass-ade/src/ass_ade/a2a/__init__.py:133
# Component id: at.source.ass_ade.warnings
from __future__ import annotations

__version__ = "0.1.0"

def warnings(self) -> list[ValidationIssue]:
    return [i for i in self.issues if i.severity == "warning"]
