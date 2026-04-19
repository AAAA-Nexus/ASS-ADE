# Extracted from C:/!ass-ade/src/ass_ade/agent/dgm_h.py:70
# Component id: at.source.ass_ade.validated
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
