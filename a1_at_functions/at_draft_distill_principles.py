# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_distill_principles.py:7
# Component id: at.source.a1_at_functions.distill_principles
from __future__ import annotations

__version__ = "0.1.0"

def distill_principles(self, report: AuditReport | None = None) -> list[str]:
    default_principles = [
        "verify before acting",
        "prefer reuse over regeneration",
        "halt on capability gap",
    ]

    if report is None or not report.failures:
        self._principles = list(default_principles)
        return list(self._principles)

    # Count failures per group.
    group_counts: dict[str, int] = {}
    for f in report.failures:
        g = f.get("group", "unknown")
        group_counts[g] = group_counts.get(g, 0) + 1

    group_to_principle = {
        "foundational": "Always classify epistemic tier before acting",
        "operational": "Minimize tool round-trips and track token budget",
        "autonomous": "Consult persistent memory and capture traces for every cycle",
        "meta_cognition": "Certify output and check hallucination signals before delivery",
        "hyperagent": "Invoke MAP=TERRAIN, ATLAS, and LIFR engines for complex tasks",
    }

    # Threshold: a group contributes a principle when it has >= 2 failures
    # (or any failures if there are few overall).
    threshold = 2 if len(report.failures) > 5 else 1
    derived: list[str] = []
    for group, count in sorted(group_counts.items(), key=lambda kv: -kv[1]):
        if count >= threshold and group in group_to_principle:
            derived.append(group_to_principle[group])

    if not derived:
        derived = list(default_principles)

    # Cap at 5 principles total.
    merged: list[str] = []
    for p in derived + default_principles:
        if p not in merged:
            merged.append(p)
        if len(merged) >= 5:
            break

    self._principles = merged
    return list(self._principles)
