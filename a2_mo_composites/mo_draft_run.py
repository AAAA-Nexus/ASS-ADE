# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_wisdomengine.py:231
# Component id: mo.source.a2_mo_composites.run
from __future__ import annotations

__version__ = "0.1.0"

def run(self, ctx: dict) -> dict:
    report = self.run_audit(ctx.get("cycle_state", {}))
    return {
        "passed": report.passed,
        "failed": report.failed,
        "score": report.score,
        "conviction": report.conviction,
        "failures": report.failures[:5],
        "warnings": list(report.warnings),
    }
