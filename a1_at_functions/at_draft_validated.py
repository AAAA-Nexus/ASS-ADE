# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_validated.py:7
# Component id: at.source.a1_at_functions.validated
from __future__ import annotations

__version__ = "0.1.0"

def validated(self) -> bool:
    # Require: no violations, improvement >= threshold AND > 2σ of noise.
    return (
        not self.constitutional_violation
        and not self.violations
        and self.improvement >= self.threshold
        and self.improvement > (2.0 * self.noise_sigma)
    )
