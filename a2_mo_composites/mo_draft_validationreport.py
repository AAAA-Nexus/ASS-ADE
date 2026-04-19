# Extracted from C:/!ass-ade/src/ass_ade/a2a/__init__.py:121
# Component id: mo.source.ass_ade.validationreport
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
