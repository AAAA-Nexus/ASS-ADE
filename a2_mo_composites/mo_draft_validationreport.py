# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_validationreport.py:7
# Component id: mo.source.a2_mo_composites.validationreport
from __future__ import annotations

__version__ = "0.1.0"

class ValidationReport:
    """Result of validating an agent card."""

    valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    card: A2AAgentCard | None = None

    @property
    def errors(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[ValidationIssue]:
        return [i for i in self.issues if i.severity == "warning"]
