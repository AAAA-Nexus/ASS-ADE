# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_editplanexecutor.py:111
# Component id: at.source.ass_ade.preview
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
