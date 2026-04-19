# Extracted from C:/!ass-ade/src/ass_ade/agent/dgm_h.py:246
# Component id: at.source.ass_ade.simulate
from __future__ import annotations

__version__ = "0.1.0"

def simulate(self, patch: Any, cycles: int | None = None) -> SimulationResult:
    """Real DGM-H simulation. Accepts Patch or dict (spec-compliant)."""
    p = _coerce_patch(patch)
    n = cycles if cycles is not None else self._sim_cycles

    # Sovereign invariant check first; early halt on violation.
    violations = self._check_violations(p)
    constitutional = bool(violations)

    # Deterministic seeds so the same patch id reproduces.
    seed_before = int(hashlib.sha256((p.id + "|before").encode()).hexdigest()[:8], 16)
    seed_after = int(hashlib.sha256((p.id + "|after").encode()).hexdigest()[:8], 16)

    before = self._run_one(p, suffix="", seed=seed_before, cycles=n)
    suffix = _patch_prompt_suffix(p)
    after = self._run_one(p, suffix=suffix, seed=seed_after, cycles=n)

    weighted_before = before["weighted"]
    weighted_after = after["weighted"]
    denom = abs(weighted_before) if abs(weighted_before) > 1e-9 else 1e-9
    improvement = (weighted_after - weighted_before) / denom

    noise_sigma = max(before["noise_sigma"], after["noise_sigma"], 1e-6)
    # Require improvement to exceed both threshold and 2σ of noise.
    meaningful = improvement >= self._threshold and improvement > (2.0 * noise_sigma)
    if not meaningful and not suffix:
        # Opaque patch: no prompt-level change → treat as no improvement.
        improvement = min(improvement, 0.0)

    per_cycle_metrics: list[dict[str, Any]] = [
        {"phase": "before", **{k: v for k, v in before.items() if k != "per_task"}},
        {"phase": "after", **{k: v for k, v in after.items() if k != "per_task"}},
    ]

    result = SimulationResult(
        patch_id=p.id,
        cycles=n,
        improvement=improvement,
        weighted_before=weighted_before,
        weighted_after=weighted_after,
        noise_sigma=noise_sigma,
        constitutional_violation=constitutional,
        per_cycle_metrics=per_cycle_metrics,
        violations=violations,
        threshold=self._threshold,
    )

    # Persist artifact.
    try:
        self._state_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%f")
        artifact = self._state_dir / f"{ts}_{p.id}.json"
        artifact.write_text(
            json.dumps(asdict(result), indent=2, default=str),
            encoding="utf-8",
        )
        result.artifact_path = str(artifact)
    except OSError:
        # Never fail the sim due to disk issues.
        pass
    return result
