# Extracted from C:/!ass-ade/src/ass_ade/tools/plan.py:195
# Component id: at.source.ass_ade.preview
from __future__ import annotations

__version__ = "0.1.0"

def preview(self, plan: EditPlan) -> str:
    """Return a combined diff of all edits in the plan."""
    if not plan.validated:
        errs = self.validate(plan)
        if errs:
            return "Validation errors:\n" + "\n".join(f"  ✗ {e}" for e in errs)
    return "\n\n".join(
        f"--- {e.description} ---\n{e.diff}" for e in plan.edits if e.diff
    )
