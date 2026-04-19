# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_build_recommendations.py:7
# Component id: at.source.a1_at_functions.build_recommendations
from __future__ import annotations

__version__ = "0.1.0"

def build_recommendations(audit: list[ProtocolAuditCheck], goal: str) -> list[str]:
    recommendations: list[str] = []

    if not any(check.name == "Protocol docs are public-safe" and check.passed for check in audit):
        recommendations.append(
            "Document the public-safe protocol cycle so contributors know what ASS-ADE may and may not inherit from private backend patterns."
        )

    if not any(check.name == "Standalone local value exists" and check.passed for check in audit):
        recommendations.append(
            "Add another local-only capability so the public repo keeps earning attention even without remote endpoints."
        )

    for check in audit:
        if check.name == "Local mode is the default" and not check.passed:
            recommendations.append("Reset profile to 'local' in config: ass-ade config set profile local")
        elif check.name == "Public shell scaffold present" and not check.passed:
            recommendations.append("Run 'ass-ade init' to create the required scaffold structure")
        elif check.name == "Remote contract boundary preserved" and not check.passed:
            recommendations.append("Remove any private backend references from public-facing modules")

    recommendations.append(f"Use the next enhancement cycle to target: {goal}")
    recommendations.append(
        "Prefer typed public contracts, degraded local fallbacks, and explicit remote opt-in over reproducing backend logic locally."
    )
    return recommendations
