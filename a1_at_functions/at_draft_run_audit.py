# Extracted from C:/!ass-ade/src/ass_ade/agent/wisdom.py:89
# Component id: at.source.ass_ade.run_audit
from __future__ import annotations

__version__ = "0.1.0"

def run_audit(self, cycle_state: dict) -> AuditReport:
    self._audits += 1
    passed = 0
    failed = 0
    per_group: dict[str, dict] = {}
    failures: list[dict] = []
    warnings: list[str] = []

    for q in AUDIT_QUESTIONS:
        ok = self._answer(q, cycle_state)
        g = per_group.setdefault(q["group"], {"passed": 0, "failed": 0})
        if ok:
            passed += 1
            g["passed"] += 1
        else:
            failed += 1
            g["failed"] += 1
            failures.append({"id": q["id"], "group": q["group"], "text": q["text"]})

    total = passed + failed
    score = passed / total if total else 0.0
    # Update conviction EMA.
    self._conviction = 0.5 * self._conviction + 0.5 * score

    # Low-conviction warning after the first audit.
    if score < 0.3 and self._audits > 1:
        warnings.append("low_conviction")

    return AuditReport(
        total=total,
        passed=passed,
        failed=failed,
        score=score,
        conviction=self._conviction,
        per_group=per_group,
        failures=failures,
        warnings=warnings,
        principles=list(self._principles),
    )
