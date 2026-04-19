# Extracted from C:/!ass-ade/src/ass_ade/a2a/__init__.py:137
# Component id: at.source.ass_ade.validate_agent_card
from __future__ import annotations

__version__ = "0.1.0"

def validate_agent_card(data: dict[str, Any]) -> ValidationReport:
    """Validate a raw dict against the A2A agent card schema.

    Returns a ValidationReport with structured findings.
    """
    issues: list[ValidationIssue] = []

    # Required fields
    if "name" not in data or not data.get("name", "").strip():
        issues.append(ValidationIssue("error", "name", "Agent card must have a non-empty 'name' field"))

    # Parse into model
    try:
        card = A2AAgentCard.model_validate(data)
    except ValidationError as exc:
        issues.append(ValidationIssue("error", "_parse", f"Failed to parse agent card: {exc}"))
        return ValidationReport(valid=False, issues=issues)

    # Structural warnings
    if not card.description:
        issues.append(ValidationIssue("warning", "description", "Missing description — agents should describe themselves"))

    if not card.url:
        issues.append(ValidationIssue("warning", "url", "Missing url — no way to reach this agent"))
    elif card.url:
        parsed = urlparse(card.url)
        if parsed.scheme not in ("http", "https"):
            issues.append(ValidationIssue("error", "url", f"Invalid URL scheme: {parsed.scheme}"))

    if not card.version:
        issues.append(ValidationIssue("warning", "version", "Missing version — consider semver"))

    if not card.skills:
        issues.append(ValidationIssue("warning", "skills", "No skills advertised — agent has no discoverable capabilities"))

    for i, skill in enumerate(card.skills):
        if not skill.id:
            issues.append(ValidationIssue("error", f"skills[{i}].id", "Skill must have an id"))
        if not skill.name:
            issues.append(ValidationIssue("error", f"skills[{i}].name", "Skill must have a name"))

    if card.authentication and not card.authentication.schemes:
        issues.append(ValidationIssue("warning", "authentication.schemes", "Authentication declared but no schemes listed"))

    has_errors = any(i.severity == "error" for i in issues)
    return ValidationReport(valid=not has_errors, issues=issues, card=card)
