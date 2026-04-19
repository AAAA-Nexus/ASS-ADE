# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_pipelineresult.py:19
# Component id: at.source.ass_ade.summary
__version__ = "0.1.0"

    def summary(self) -> str:
        total = len(self.steps)
        passed = sum(1 for s in self.steps if s.status == StepStatus.PASSED)
        failed = sum(1 for s in self.steps if s.status == StepStatus.FAILED)
        skipped = sum(1 for s in self.steps if s.status == StepStatus.SKIPPED)
        verdict = "PASSED" if self.passed else "FAILED"
        return f"[{verdict}] {self.name}: {passed}/{total} passed, {failed} failed, {skipped} skipped ({self.duration_ms:.0f}ms)"
