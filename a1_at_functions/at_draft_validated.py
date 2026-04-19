# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_simulationresult.py:26
# Component id: at.source.ass_ade.validated
__version__ = "0.1.0"

    def validated(self) -> bool:
        # Require: no violations, improvement >= threshold AND > 2σ of noise.
        return (
            not self.constitutional_violation
            and not self.violations
            and self.improvement >= self.threshold
            and self.improvement > (2.0 * self.noise_sigma)
        )
