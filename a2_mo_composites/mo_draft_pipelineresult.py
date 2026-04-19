# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_pipelineresult.py:5
# Component id: mo.source.ass_ade.pipelineresult
__version__ = "0.1.0"

class PipelineResult:
    """Result of an entire pipeline execution."""

    name: str
    steps: list[StepResult] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    passed: bool = False
    duration_ms: float = 0.0

    @property
    def failed_steps(self) -> list[StepResult]:
        return [s for s in self.steps if s.status == StepStatus.FAILED]

    @property
    def summary(self) -> str:
        total = len(self.steps)
        passed = sum(1 for s in self.steps if s.status == StepStatus.PASSED)
        failed = sum(1 for s in self.steps if s.status == StepStatus.FAILED)
        skipped = sum(1 for s in self.steps if s.status == StepStatus.SKIPPED)
        verdict = "PASSED" if self.passed else "FAILED"
        return f"[{verdict}] {self.name}: {passed}/{total} passed, {failed} failed, {skipped} skipped ({self.duration_ms:.0f}ms)"
