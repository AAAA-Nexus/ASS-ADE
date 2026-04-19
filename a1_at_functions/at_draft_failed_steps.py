# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_pipelineresult.py:15
# Component id: at.source.ass_ade.failed_steps
__version__ = "0.1.0"

    def failed_steps(self) -> list[StepResult]:
        return [s for s in self.steps if s.status == StepStatus.FAILED]
