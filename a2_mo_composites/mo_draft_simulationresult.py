# Extracted from C:/!ass-ade/src/ass_ade/agent/dgm_h.py:49
# Component id: mo.source.ass_ade.simulationresult
from __future__ import annotations

__version__ = "0.1.0"

class SimulationResult:
    """Real DGM-H simulation result with per-cycle telemetry."""

    patch_id: str
    cycles: int
    improvement: float
    weighted_before: float
    weighted_after: float
    noise_sigma: float
    constitutional_violation: bool
    per_cycle_metrics: list[dict[str, Any]] = field(default_factory=list)
    violations: list[str] = field(default_factory=list)
    artifact_path: str | None = None
    threshold: float = _VALIDATION_THRESHOLD

    # ── Back-compat aliases for existing gates code ──────────────────────────
    @property
    def delta(self) -> float:
        return self.improvement

    @property
    def validated(self) -> bool:
        # Require: no violations, improvement >= threshold AND > 2σ of noise.
        return (
            not self.constitutional_violation
            and not self.violations
            and self.improvement >= self.threshold
            and self.improvement > (2.0 * self.noise_sigma)
        )
